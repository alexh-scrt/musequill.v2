import re
from typing import Iterable, List, Optional
from pydantic import ValidationError

from musequill.services.backend.writers.chapter_planning_model import GenericPlan
from .plan_validation_results import (
    ValidationIssue,
    ValidationResult
)
from .plan_baseline import PlanBaselines   

# Reuse your GenericPlan model
# from yourmodule import GenericPlan

def _make_refined_prompt(
    plan: Optional[GenericPlan],
    baselines: PlanBaselines,
    issues: List[ValidationIssue]
) -> str:
    """Build a terse, enforceable prompt that only addresses what failed."""
    hard_rules = []
    soft_rules = []

    # Identity locks
    if baselines.title:
        hard_rules.append(f'project.title MUST equal "{baselines.title}".')
    if baselines.author:
        hard_rules.append(f'project.author MUST equal "{baselines.author}".')

    if baselines.allowed_genres:
        hard_rules.append(f'project.genre MUST be one of: {sorted(baselines.allowed_genres)}.')
    if baselines.disallowed_genres:
        hard_rules.append(f'Disallowed genres: {sorted(baselines.disallowed_genres)}.')

    if baselines.required_entities:
        hard_rules.append(f'Must include required entities: {sorted(baselines.required_entities)} (as character keys or clearly in text).')

    if baselines.forbidden_terms:
        hard_rules.append(f'Forbidden terms: {sorted(baselines.forbidden_terms)} (must not appear anywhere).')

    for path, expected in baselines.require_empty_fields.items():
        hard_rules.append(f'Field {".".join(path)} MUST equal {expected}.')

    # Convert issues into plain directives
    for iss in issues:
        if iss.code.startswith("structure.chapters.min"):
            hard_rules.append(f"chapter_outline MUST contain at least {baselines.min_chapters} chapters with non-empty titles and descriptions.")
        if iss.code.startswith("structure.characters.min"):
            hard_rules.append(f"characters MUST contain at least {baselines.min_characters} entries with description and goals.")
        if iss.code == "structure.beats.min":
            soft_rules.append(f"Provide at least {baselines.min_beats} hero_journey_beats with meaningful descriptions.")
        if iss.code == "completeness.ch_titles.low_var":
            soft_rules.append("Chapter titles should be distinctive; avoid repeating generic phrasing.")
        if iss.code == "style.chapter.desc.short":
            soft_rules.append("Expand chapter descriptions to 2–4 sentences with concrete stakes and obstacles.")
        if iss.code == "style.logline.too_long":
            soft_rules.append(f"Constrain logline to <= {baselines.max_logline_chars} characters without losing specificity.")
        if iss.code == "completeness.themes.empty":
            soft_rules.append("Provide at least 2–3 concise themes.")
        if iss.code == "completeness.setting.bias" and baselines.preferred_setting_keywords:
            soft_rules.append(f"Surface preferred setting cues: {sorted(baselines.preferred_setting_keywords)}.")
        if iss.code == "completeness.themes.bias" and baselines.preferred_theme_keywords:
            soft_rules.append(f"Reflect preferred thematic cues: {sorted(baselines.preferred_theme_keywords)}.")
        if iss.code == "consistency.required_empty":
            hard_rules.append("Correct fields to required empty arrays/values exactly as specified.")
        if iss.code == "consistency.entity.missing":
            hard_rules.append("Add missing required entities as character entries or reference them meaningfully in text.")
        if iss.code.startswith("consistency.genre."):
            hard_rules.append("Adjust project.genre to meet the genre constraints above.")
        if iss.code.startswith("consistency.title") or iss.code.startswith("consistency.author"):
            hard_rules.append("Correct project identity fields exactly.")

    # Final prompt (LLM-facing)
    return (
        "You are a senior story planner.\n\n"
        "TASK: Produce exactly one valid JSON object that conforms to the GenericPlan schema and the rules below.\n\n"
        "HARD RULES (must pass):\n- " + "\n- ".join(hard_rules) + "\n\n"
        "QUALITY GUIDANCE (improves score):\n- " + ("\n- ".join(soft_rules) if soft_rules else "Keep descriptions specific and concrete.") + "\n\n"
        "OUTPUT:\n- One valid JSON object (no prose, no code fences).\n- Preserve existing useful content when possible; correct only what violates the rules.\n"
    )


def _contains_any(text: str, needles: Iterable[str]) -> bool:
    t = text.lower()
    return any(n.lower() in t for n in needles if n)

def _collect_text(plan: GenericPlan) -> str:
    parts = [plan.logline or ""]
    parts.extend(plan.themes or [])
    parts.append(plan.project.genre or "")
    parts.append(plan.project.sub_genre or "" if plan.project.sub_genre else "")
    parts.append(plan.world_bible.setting or "")
    parts.append(plan.world_bible.time_period or "" if plan.world_bible.time_period else "")
    parts.append(plan.world_bible.technology or "" if plan.world_bible.technology else "")
    for c_name, c in (plan.characters or {}).items():
        parts.append(c_name)
        parts.append(c.description or "")
        parts.extend(c.goals or [])
    for b in (plan.hero_journey_beats or []):
        parts.append(b.beat)
        parts.append(b.description)
    for ch in (plan.chapter_outline or []):
        parts.append(ch.title)
        parts.append(ch.description)
    return "\n".join(parts)

def validate_plan_against_baselines(
    plan_json: dict,
    baselines: PlanBaselines,
) -> ValidationResult:
    issues: List[ValidationIssue] = []

    # 1) Schema / structural validity via Pydantic
    try:
        plan = GenericPlan.model_validate(plan_json)
    except ValidationError as ve:
        for e in ve.errors():
            issues.append(ValidationIssue(
                severity="error",
                code="schema.invalid",
                message=f"{e.get('loc')} -> {e.get('msg')}"
            ))
        return ValidationResult(
            is_valid=False, score=0.0, issues=issues, regenerate=True,
            refined_prompt=_make_refined_prompt(None, baselines, issues)
        )

    # ---------- SCORING ACCUMULATORS ----------
    score = 1.0
    WEIGHTS = {
        "structure": 0.35,
        "consistency": 0.30,
        "completeness": 0.20,
        "style": 0.15,
    }

    # 2) Structure checks (beyond Pydantic)
    # chapters unique handled by your model; we add some basic thresholds
    if len(plan.characters) < baselines.min_characters:
        issues.append(ValidationIssue("error","structure.characters.min",
            f"characters has {len(plan.characters)} but requires at least {baselines.min_characters}."))
    if len(plan.chapter_outline) < baselines.min_chapters:
        issues.append(ValidationIssue("error","structure.chapters.min",
            f"chapter_outline has {len(plan.chapter_outline)} but requires at least {baselines.min_chapters}."))
    if baselines.max_chapters and len(plan.chapter_outline) > baselines.max_chapters:
        issues.append(ValidationIssue("warn","structure.chapters.max",
            f"chapter_outline has {len(plan.chapter_outline)} which exceeds preferred maximum {baselines.max_chapters}."))
    if len(plan.hero_journey_beats) < baselines.min_beats:
        issues.append(ValidationIssue("warn","structure.beats.min",
            f"hero_journey_beats has {len(plan.hero_journey_beats)} but {baselines.min_beats}+ is preferred."))

    # 3) Consistency checks vs baselines (identity, genre, entities, forbidden)
    if baselines.title and plan.project.title.strip() != baselines.title.strip():
        issues.append(ValidationIssue("error","consistency.title",
            f'project.title "{plan.project.title}" must equal "{baselines.title}".'))
    if baselines.author and plan.project.author.strip() != baselines.author.strip():
        issues.append(ValidationIssue("error","consistency.author",
            f'project.author "{plan.project.author}" must equal "{baselines.author}".'))

    if baselines.allowed_genres and plan.project.genre not in baselines.allowed_genres:
        issues.append(ValidationIssue("error","consistency.genre.allowed",
            f'project.genre "{plan.project.genre}" not in allowed_genres {sorted(baselines.allowed_genres)}.'))
    if baselines.disallowed_genres and plan.project.genre in baselines.disallowed_genres:
        issues.append(ValidationIssue("error","consistency.genre.disallowed",
            f'project.genre "{plan.project.genre}" is disallowed.'))

    all_text = _collect_text(plan)
    # Required entities: must appear either as a character key or in text
    for ent in baselines.required_entities:
        in_chars = ent in plan.characters
        in_text = ent.lower() in all_text.lower()
        if not (in_chars or in_text):
            issues.append(ValidationIssue("error","consistency.entity.missing",
                f'Required entity "{ent}" not found in characters or text.'))

    # Forbidden terms
    if baselines.forbidden_terms and _contains_any(all_text, baselines.forbidden_terms):
        bad = [t for t in baselines.forbidden_terms if t.lower() in all_text.lower()]
        issues.append(ValidationIssue("error","consistency.forbidden.terms",
            f"Forbidden terms present: {sorted(set(bad))}."))

    # Required empty fields (path -> []), if you later add such fields
    for path, required_value in baselines.require_empty_fields.items():
        val = plan_json
        for k in path:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                val = None
                break
        if val != required_value:
            issues.append(ValidationIssue("error","consistency.required_empty",
                f'Field {".".join(path)} must equal {required_value}, got {val}.'))

    # 4) Completeness & specificity
    if len(plan.themes) == 0:
        issues.append(ValidationIssue("warn","completeness.themes.empty","themes is empty."))

    # Mild heuristic: chapter titles should be unique and >= 60% unique
    titles = [c.title.strip().lower() for c in plan.chapter_outline]
    unique_ratio = len(set(titles)) / max(1, len(titles))
    if unique_ratio < 0.6:
        issues.append(ValidationIssue("warn","completeness.ch_titles.low_var",
            f"Only {unique_ratio:.0%} of chapter titles are unique; increase variety."))

    # Preferred signals
    if baselines.preferred_theme_keywords and not _contains_any(" ".join(plan.themes), baselines.preferred_theme_keywords):
        issues.append(ValidationIssue("warn","completeness.themes.bias",
            f"themes lacks preferred keywords {sorted(baselines.preferred_theme_keywords)}."))

    if baselines.preferred_setting_keywords and not _contains_any(all_text, baselines.preferred_setting_keywords):
        issues.append(ValidationIssue("warn","completeness.setting.bias",
            f"text lacks preferred setting keywords {sorted(baselines.preferred_setting_keywords)}."))

    # 5) Style/Hygiene
    if plan.logline and len(plan.logline) > baselines.max_logline_chars:
        issues.append(ValidationIssue("warn","style.logline.too_long",
            f"logline exceeds {baselines.max_logline_chars} chars; tighten."))

    # Penalize very short descriptions (weak specificity)
    short_desc_ch = sum(1 for c in plan.chapter_outline if len(c.description) < 40)
    if short_desc_ch > 0:
        issues.append(ValidationIssue("warn","style.chapter.desc.short",
            f"{short_desc_ch} chapter descriptions are very short; add specificity."))

    # ---------- Compute score and decision ----------
    def subtract(weight_key: str, fraction: float):
        nonlocal score
        score -= WEIGHTS[weight_key] * fraction
        score = max(0.0, min(1.0, score))

    # Structure
    if any(i.severity=="error" and i.code.startswith("structure.") for i in issues):
        subtract("structure", 1.0)
    else:
        # partial deductions for warns
        warns = sum(1 for i in issues if i.code.startswith("structure.") and i.severity=="warn")
        if warns:
            subtract("structure", min(1.0, 0.25*warns))

    # Consistency
    if any(i.severity=="error" and i.code.startswith("consistency.") for i in issues):
        subtract("consistency", 1.0)
    else:
        warns = sum(1 for i in issues if i.code.startswith("consistency.") and i.severity=="warn")
        if warns:
            subtract("consistency", min(1.0, 0.25*warns))

    # Completeness
    warns = sum(1 for i in issues if i.code.startswith("completeness."))
    if warns:
        subtract("completeness", min(1.0, 0.2*warns))

    # Style
    warns = sum(1 for i in issues if i.code.startswith("style."))
    if warns:
        subtract("style", min(1.0, 0.2*warns))

    # Validity + regenerate policy
    hard_errors = any(i.severity=="error" for i in issues)
    is_valid = not hard_errors
    regenerate = hard_errors or score < 0.72  # tunable quality bar

    refined = _make_refined_prompt(plan, baselines, issues) if regenerate else None

    return ValidationResult(
        is_valid=is_valid,
        score=round(score, 3),
        issues=issues,
        regenerate=regenerate,
        refined_prompt=refined
    )
