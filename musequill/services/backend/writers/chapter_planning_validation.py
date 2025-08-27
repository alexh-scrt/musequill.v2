# validators/chapter_plan_validator.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import json, re
from pydantic import ValidationError

# Import your models/utilities
from musequill.services.backend.model.chapter_planning import HighLevelChapterPlan
from musequill.services.backend.model.book import BookModelType
from musequill.services.backend.utils.payloads import extract_json_from_response

@dataclass
class ValidationPolicy:
    """
    Generic, artifact-aware policy that can be tuned per project.
    """
    # Hard equals derived from BookModelType by default
    enforce_title_author: bool = True

    # Content leakage guard (project-agnostic)
    banned_substrings_ci: List[str] = field(default_factory=list)

    # Genre/World rules (auto-inferred from BookModelType, but can override)
    require_no_magic_for_realistic: bool = True
    require_no_mythic_for_realistic: bool = True

    # Two-hander heuristic (auto-detected from Structure, but can override)
    enforce_two_hander_presence: bool = True

    # POV guardrails (if the model specifies third-person limited alternating)
    enforce_pov_rules: bool = True

    # Soft checks (warnings, not hard fails)
    soft_checks: bool = True

    # Extra required mentions (e.g., setting anchors like "New York")
    required_mentions_ci: List[str] = field(default_factory=list)


def _ci_re(words: List[str]) -> Optional[re.Pattern]:
    words = [w for w in (words or []) if w and w.strip()]
    if not words:
        return None
    escaped = [re.escape(w) for w in words]
    return re.compile("|".join(escaped), re.I)


def validate_output_generic(
    response_text: str,
    book: BookModelType,
    policy: Optional[ValidationPolicy] = None,
    raw_artifacts: Optional[Dict[str, Any]] = None,  # optionally pass dna/summary/research if you want cross-checks later
) -> Dict[str, Any]:
    """
    Validates an LLM response against the schema and artifact-derived domain rules.

    Returns a dict with:
      - is_valid, parsed_successfully, validation_passed
      - hard_errors (list), soft_warnings (list)
      - stats (counts)
      - repaired_prompt (string)  # one-shot repair instruction if invalid
    """
    policy = policy or ValidationPolicy()
    hard_errors: List[str] = []
    soft_warnings: List[str] = []

    # 1) Parse JSON
    try:
        response_json = extract_json_from_response(response_text)
    except json.JSONDecodeError as e:
        return {
            "is_valid": False,
            "parsed_successfully": False,
            "validation_passed": False,
            "hard_errors": [f"JSON parsing failed: {str(e)}"],
            "soft_warnings": [],
            "stats": {},
            "repaired_prompt": _make_repair_prompt(None, f"JSON parsing failed: {str(e)}")
        }

    # 2) Schema validation
    try:
        plan = HighLevelChapterPlan(**response_json)
    except ValidationError as e:
        return {
            "is_valid": False,
            "parsed_successfully": True,
            "validation_passed": False,
            "hard_errors": [f"Schema validation failed: {str(e)}"],
            "soft_warnings": [],
            "stats": {},
            "repaired_prompt": _make_repair_prompt(response_json, f"Schema validation failed: {str(e)}")
        }

    # Convenience copies
    raw_str = json.dumps(response_json, ensure_ascii=False)
    title = getattr(plan.project, "title", "")
    author = getattr(plan.project, "author", "")

    # 3) Artifact-derived hard checks
    if policy.enforce_title_author:
        if title != book.book.title:
            hard_errors.append(f"project.title must equal '{book.book.title}'")
        if author != book.book.author:
            hard_errors.append(f"project.author must equal '{book.book.author}'")

    # 4) Genre/world realism constraints
    # Infer "realistic" if genre primary/sub does NOT include fantasy/sf/speculative terms
    primary = (book.genre.primary.type or "").lower()
    sub_genre = getattr(book.genre, "sub", None)
    sub = (sub_genre.type or "").lower() if sub_genre else ""
    fantasy_keywords = [
        "fantasy", "sci-fi", "science fiction", "speculative", 
        "paranormal", "urban fantasy", "magical"
    ]
    is_realistic = not any(g in f"{primary} {sub}" for g in fantasy_keywords)

    if is_realistic and policy.require_no_magic_for_realistic:
        magic_rules = getattr(plan.world_bible, 'soft_magic_rules', [])
        if magic_rules != []:
            hard_errors.append(
                "world_bible.soft_magic_rules must be [] for realistic genres"
            )

    if is_realistic and policy.require_no_mythic_for_realistic:
        mythic_figs = getattr(plan.characters, 'mythic_figures', [])
        if mythic_figs not in ([], None):
            hard_errors.append(
                "characters.mythic_figures must be [] for realistic genres"
            )

    # 5) Two-hander enforcement if structure says so
    # If BookModelType has structure.type like "Two-Hander (Dual Arc)"
    structure = (book.structure.type or "").lower()
    is_two_hander = "two" in structure and "hand" in structure
    if policy.enforce_two_hander_presence and is_two_hander:
        # Expect two leads. Schema has one 'protagonist'; 
        # put the other in meadow_cast with role co-protagonist.
        leads = []
        # Try to parse leads from book.characters.protagonists
        try:
            protagonists = getattr(book.characters, "protagonists", [])
            leads = [x for x in protagonists 
                    if isinstance(x, str) and x.strip()]
        except (AttributeError, TypeError):
            pass

        # Fallback: attempt from book model prose (optional)
        # else you can skip if not reliable

        if leads and len(leads) >= 2:
            # Basic presence checks in output
            out_names_ci = raw_str.lower()
            missing = [nm for nm in leads if nm.lower() not in out_names_ci]
            if missing:
                missing_names = ", ".join(missing)
                hard_errors.append(
                    f"Missing expected co-lead names in output: {missing_names}"
                )
        else:
            # At least ensure protagonist + one co-protagonist mention exists
            # Look for "co-protagonist" role in meadow_cast
            meadow_cast = getattr(plan.characters, 'meadow_cast', []) or []
            has_co = any(
                (getattr(mc, 'role', '') or "").lower().find("co-protagonist") >= 0
                for mc in meadow_cast
                if mc and hasattr(mc, 'role')
            )
            if not has_co:
                soft_warnings.append(
                    "Two-hander structure detected but no co-protagonist "
                    "role found in meadow_cast"
                )

    # 6) POV guardrails
    project_pov = getattr(plan.project, 'pov', {})
    if isinstance(project_pov, dict):
        pov_text = " ".join([f"{k}:{v}" for k, v in project_pov.items()])
    else:
        pov_text = str(project_pov)
    
    wants_alt_third = ("third" in pov_text.lower() and 
                      "limited" in pov_text.lower())
    if policy.enforce_pov_rules and wants_alt_third:
        # Expect guardrails mention like "one close POV per chapter"
        guardrails = getattr(plan.style_guide, 'objective_pov_guardrails', []) or []
        guard = " ".join(guardrails).lower()
        pov_keywords = [
            "no head-hopping", "one close pov", "one pov per chapter", 
            "scene transitions on pov change"
        ]
        if not any(kw in guard for kw in pov_keywords):
            soft_warnings.append(
                "POV is third-person limited but objective_pov_guardrails "
                "do not include no head-hopping guidance"
            )

    # 7) Banned substrings (generic leakage firewall)
    if policy.banned_substrings_ci:
        banned_re = _ci_re(policy.banned_substrings_ci)
        if banned_re and banned_re.search(raw_str):
            hard_errors.append("Banned substrings present (content leakage)")

    # 8) Required mentions (anchors, e.g., city or institutions)
    if policy.required_mentions_ci:
        req_re = _ci_re(policy.required_mentions_ci)
        if req_re and not req_re.search(raw_str):
            soft_warnings.append(f"Required mentions not found: {policy.required_mentions_ci}")

    # 9) Stats
    stats = {
        "chapter_count": len(plan.chapter_outline),
        "hero_journey_beats": len(plan.hero_journey_beats),
        "themes_count": len(plan.themes),
        "research_items": len(plan.research_checklist),
    }

    # 10) Final result
    ok = len(hard_errors) == 0
    return {
        "is_valid": ok,
        "parsed_successfully": True,
        "validation_passed": ok,
        "hard_errors": hard_errors,
        "soft_warnings": soft_warnings,
        "stats": stats,
        "repaired_prompt": None if ok else _make_repair_prompt(response_json, "; ".join(hard_errors))
    }


def _make_repair_prompt(previous_json: Optional[Dict[str, Any]], error_msg: str) -> str:
    pj = json.dumps(previous_json, ensure_ascii=False) if previous_json is not None else ""
    return (
        "Repair the prior JSON to satisfy all schema and artifact-derived rules. "
        "Do not change project.title or project.author if already correct. "
        "If the genre is realistic, world_bible.soft_magic_rules must be [] "
        "and characters.mythic_figures must be []. "
        "If the structure indicates a two-hander, include both leads "
        "(co-protagonist in meadow_cast if needed). "
        "Output only corrected JSON.\n\n"
        f"Validation errors:\n{error_msg}\n\n"
        f"Previous JSON:\n{pj}"
    )
