# chapter_critic.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union
import re
import math

# --- Import your own types (adjust paths as needed) ---
# from musequill.services.backend.model.book import BookModelType
# from your_models import GenericPlan, GenericChapterBrief
# If your "chapter plan" type is named differently (e.g., GenericChapterPlan), swap it below.

from musequill.services.backend.model import BookModelType
from . import GenericPlan, GenericChapterBrief
from musequill.services.backend.llm import LLMService
from musequill.services.backend.utils import extract_json_from_response
# ---- Public dataclasses for consumers ----

@dataclass
class CritiqueAxisScore:
    axis: str
    score: float  # 0–1
    rationale: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "axis": self.axis,
            "score": self.score,
            "rationale": self.rationale
        }

@dataclass
class CritiqueFindings:
    overall_score: float  # 0–1
    axes: List[CritiqueAxisScore]
    red_flags: List[str]
    suggestions: List[str]
    inline_change_notes: List[str]  # concrete, localized suggestions
    keep_as_is: bool                 # if True, no revision needed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": self.overall_score,
            "axes": [axis.to_dict() for axis in self.axes],
            "red_flags": self.red_flags,
            "suggestions": self.suggestions,
            "inline_change_notes": self.inline_change_notes,
            "keep_as_is": self.keep_as_is
        }

@dataclass
class CritiqueArtifacts:
    """What we feed the critic alongside the chapter text."""
    previous_chapter: Optional[str]
    story_so_far_summary: str
    book_model_md: str               # e.g., BookModelType.to_markdown()
    chapter_brief_summary: str       # a compact string derived from GenericChapterBrief
    book_plan_summary: str           # compact string derived from GenericPlan

@dataclass
class CritiqueResult:
    pass_index: int
    findings: CritiqueFindings
    revised_text: str
    revision_prompt_used: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pass_index": self.pass_index,
            "findings": self.findings.to_dict(),
            "revised_text": self.revised_text,
            "revision_prompt_used": self.revision_prompt_used
        }

# ---- Utility: small local QC checks (fast & deterministic) ----

def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))

def _line_dupes(text: str, min_len: int = 25) -> List[str]:
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    seen, dups = {}, []
    for ln in lines:
        if len(ln) < min_len: 
            continue
        seen[ln] = seen.get(ln, 0) + 1
        if seen[ln] == 2:
            dups.append(ln)
    return dups

def _contains_banned(text: str, banned: List[str]) -> List[str]:
    hits = []
    lower = text.lower()
    for n in banned or []:
        if n and n.strip() and n.lower() in lower:
            hits.append(n)
    return hits

def _length_delta_ok(text: str, target: Optional[int], tolerance: float = 0.25) -> Tuple[bool, str]:
    if not target or target <= 0:
        return True, "No target length provided."
    wc = _word_count(text)
    lo, hi = int(target * (1 - tolerance)), int(target * (1 + tolerance))
    if lo <= wc <= hi:
        return True, f"Word count {wc} within [{lo}, {hi}]."
    return False, f"Word count {wc} outside [{lo}, {hi}] for target {target}."

# ---- Prompt builders ----

def _build_critic_prompt(
    current_chapter: str,
    artifacts: CritiqueArtifacts,
    banned_ngrams: List[str],
    target_words: Optional[int],
) -> str:
    # Focused, instruction-first prompt. The critic must return JSON-like blocks we can parse easily.
    return f"""You are a senior fiction editor and literary critic. Provide a candid, high-signal critique and actionable revision plan.

Context to honor (priority order):
1) Book model (canon rules): 
{artifacts.book_model_md}

2) Chapter brief (must-hit constraints & beats):
{artifacts.chapter_brief_summary}

3) Book plan (structure & global expectations):
{artifacts.book_plan_summary}

4) Story-so-far (continuity):
{artifacts.story_so_far_summary}

5) Previous chapter (local continuity; optional):
{artifacts.previous_chapter or "N/A"}

Chapter draft to critique:
<CHAPTER_DRAFT_START>
{current_chapter}
<CHAPTER_DRAFT_END>

Banned n-grams (must not appear): {banned_ngrams or []}
Target words (soft): {target_words if target_words else "N/A"}

Scoring axes (0–1, decimals allowed):
- Voice & POV adherence
- Continuity & Canon Consistency
- Character Integrity & Motivations
- Pacing & Scene Economy
- Conflict, Stakes & Turning Points
- Show-vs-Tell & Sensory Grounding
- Dialogue Credibility & Subtext
- Setting & Research Fidelity
- Safety & Content Compliance
- Language Quality (clarity, clichés, repetitions)

Return a JSON block with fields:
- "overall_score": float
- "axes": [{{"axis": str, "score": float, "rationale": str}}, ...]
- "red_flags": [str]  # blocking issues that require rewrite
- "suggestions": [str]  # prioritized improvement bullets (global)
- "inline_change_notes": [str]  # concrete localized edits with page/paragraph hints if possible
- "keep_as_is": bool  # True if no revision needed

Only return the JSON, nothing else.
"""

def _build_revision_prompt(
    current_chapter: str,
    findings: CritiqueFindings,
    artifacts: CritiqueArtifacts,
    banned_ngrams: List[str],
    target_words: Optional[int],
) -> str:
    # Ask for a revised chapter that addresses the concrete issues.
    return f"""You are a novel line-editor. Revise the chapter to address the following critique findings.

Findings (JSON):
overall_score={findings.overall_score}
axes={[{"axis": a.axis, "score": a.score} for a in findings.axes]}
red_flags={findings.red_flags}
suggestions={findings.suggestions}
inline_change_notes={findings.inline_change_notes}

Non-negotiables:
- Obey canon and constraints.
- Avoid banned n-grams: {banned_ngrams or []}.
- Preserve continuity with story-so-far and previous chapter.
- Prefer "show" over "tell"; keep POV guardrails intact.
- Keep a coherent, cinematic scene flow with clear conflict and beats.

Target words (soft): {target_words if target_words else "N/A"}.
If you must deviate, do so for quality and cohesion; do not pad.

Context (do not repeat back, just use):
[Book model]:
{artifacts.book_model_md}

[Chapter brief]:
{artifacts.chapter_brief_summary}

[Book plan]:
{artifacts.book_plan_summary}

[Story so far]:
{artifacts.story_so_far_summary}

[Chapter to revise]:
{current_chapter}

[Previous chapter]:
{artifacts.previous_chapter or "N/A"}

Return:
1) The fully revised chapter (Markdown allowed).
2) A short list "changes_made" with bullet points of notable edits.
3) Do not add anything else

Format strictly as:

<REVISED_CHAPTER_START>
...revised chapter...
<REVISED_CHAPTER_END>

<CHANGES_MADE_START>
- change 1
- change 2
<CHANGES_MADE_END>
"""

# ---- JSON extraction helpers (robust-ish without external deps) ----


def _extract_revised(text: str) -> Tuple[str, List[str]]:
    chap = ""
    changes: List[str] = []
    
    # Strip input and handle cases where there might be leading/trailing content
    text = text.strip()
    
    # More robust patterns that handle variations in spacing, line breaks, and surrounding content
    # Case-insensitive and flexible whitespace handling with optional leading/trailing content
    chapter_patterns = [
        # Exact match patterns
        r"<REVISED_CHAPTER_START>\s*\n?([\s\S]*?)\n?\s*<REVISED_CHAPTER_END>",
        r"< *REVISED_CHAPTER_START *>\s*\n?([\s\S]*?)\n?\s*< *REVISED_CHAPTER_END *>",
        r"<\s*REVISED_CHAPTER_START\s*>\s*\n?([\s\S]*?)\n?\s*<\s*REVISED_CHAPTER_END\s*>",
        # Patterns that ignore leading/trailing content
        r".*?<REVISED_CHAPTER_START>\s*\n?([\s\S]*?)\n?\s*<REVISED_CHAPTER_END>.*",
        r".*?< *REVISED_CHAPTER_START *>\s*\n?([\s\S]*?)\n?\s*< *REVISED_CHAPTER_END *>.*",
        r".*?<\s*REVISED_CHAPTER_START\s*>\s*\n?([\s\S]*?)\n?\s*<\s*REVISED_CHAPTER_END\s*>.*",
    ]
    
    changes_patterns = [
        # Exact match patterns
        r"<CHANGES_MADE_START>\s*\n?([\s\S]*?)\n?\s*<CHANGES_MADE_END>",
        r"< *CHANGES_MADE_START *>\s*\n?([\s\S]*?)\n?\s*< *CHANGES_MADE_END *>",
        r"<\s*CHANGES_MADE_START\s*>\s*\n?([\s\S]*?)\n?\s*<\s*CHANGES_MADE_END\s*>",
        # Patterns that ignore leading/trailing content
        r".*?<CHANGES_MADE_START>\s*\n?([\s\S]*?)\n?\s*<CHANGES_MADE_END>.*",
        r".*?< *CHANGES_MADE_START *>\s*\n?([\s\S]*?)\n?\s*< *CHANGES_MADE_END *>.*",
        r".*?<\s*CHANGES_MADE_START\s*>\s*\n?([\s\S]*?)\n?\s*<\s*CHANGES_MADE_END\s*>.*",
    ]
    
    # Try each chapter pattern until one matches
    for pattern in chapter_patterns:
        m1 = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m1:
            chap = m1.group(1).strip()
            break
    
    # Try each changes pattern until one matches  
    for pattern in changes_patterns:
        m2 = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m2:
            raw_changes = m2.group(1).strip()
            # Handle various bullet point formats: -, *, •, or just plain lines
            changes = []
            for line in raw_changes.splitlines():
                line = line.strip()
                if line:
                    # Remove common bullet point markers
                    line = re.sub(r'^[-*•]\s*', '', line).strip()
                    if line:
                        changes.append(line)
            break
    
    return chap, changes

# ---- Acceptance policy ----

@dataclass
class AcceptancePolicy:
    min_overall_score: float = 0.78
    min_axis_score: float = 0.7
    allow_red_flags: bool = False  # any red flag forces revision

    def accept(self, findings: CritiqueFindings) -> Tuple[bool, List[str]]:
        reasons = []
        if findings.overall_score < self.min_overall_score:
            reasons.append(f"overall_score {findings.overall_score:.2f} < {self.min_overall_score:.2f}")
        for a in findings.axes:
            if a.score < self.min_axis_score:
                reasons.append(f"{a.axis} {a.score:.2f} < {self.min_axis_score:.2f}")
        if not self.allow_red_flags and findings.red_flags:
            reasons.append(f"red flags present: {findings.red_flags[:3]}{'...' if len(findings.red_flags)>3 else ''}")
        return (len(reasons) == 0), reasons

# ---- Main API ----

class ChapterCritic:
    """
    Runs up to N critique→revision passes with an LLM.
    """

    def __init__(self, llm: LLMService, acceptance: Optional[AcceptancePolicy] = None):
        self.llm = llm
        self.acceptance = acceptance or AcceptancePolicy()

    async def critique_once(
        self,
        *,
        current_chapter: str,
        previous_chapter: Optional[str],
        story_so_far_summary: str,
        book_model: BookModelType,
        chapter_plan: GenericChapterBrief,   # swap to your chapter-plan type if different
        book_plan: GenericPlan,
        banned_ngrams: Optional[List[str]] = None,
        target_words: Optional[int] = None,
        decode_overrides: Optional[Dict[str, Any]] = None,
    ) -> CritiqueResult:
        """Single critique pass + optional rewrite (depending on acceptance)."""

        # Prepare artifacts
        artifacts = CritiqueArtifacts(
            previous_chapter=previous_chapter,
            story_so_far_summary=story_so_far_summary,
            book_model_md=getattr(book_model, "to_markdown", lambda: str(book_model))(),
            chapter_brief_summary=_summarize_chapter_brief(chapter_plan),
            book_plan_summary=_summarize_book_plan(book_plan),
        )

        # Quick local checks (non-blocking; turned into red flags if necessary)
        local_red_flags = []
        ok_len, msg_len = _length_delta_ok(current_chapter, getattr(chapter_plan.meta, "target_words", target_words))
        if not ok_len:
            local_red_flags.append(msg_len)

        dupes = _line_dupes(current_chapter)
        if dupes:
            local_red_flags.append(f"Detected repeated lines: {min(len(dupes),5)} samples (e.g., “{dupes[0][:80]}…”)")

        banned_hits = _contains_banned(current_chapter, banned_ngrams or [])
        if banned_hits:
            local_red_flags.append(f"Banned n-grams present: {banned_hits[:5]}")

        # Ask LLM to critique
        critic_prompt = _build_critic_prompt(
            current_chapter=current_chapter,
            artifacts=artifacts,
            banned_ngrams=banned_ngrams or [],
            target_words=getattr(chapter_plan.meta, "target_words", target_words),
        )

        decode_opts = {
            "temperature": 0.3,     # analysis is best at low temperature
            "top_p": 0.9,
            "max_tokens": 3000,
            **(decode_overrides or {})
        }
        await self.llm.update_default_parameters(**decode_opts)
        resp = await self.llm.generate(critic_prompt)
        data = extract_json_from_response(resp["response"])

        # Build findings
        axes = [
            CritiqueAxisScore(
                axis=ax.get("axis", "unknown"),
                score=float(ax.get("score", 0)),
                rationale=ax.get("rationale", "").strip() or "No rationale provided."
            )
            for ax in data.get("axes", [])
        ]
        findings = CritiqueFindings(
            overall_score=float(data.get("overall_score", 0)),
            axes=axes,
            red_flags=(data.get("red_flags") or []) + local_red_flags,
            suggestions=data.get("suggestions") or [],
            inline_change_notes=data.get("inline_change_notes") or [],
            keep_as_is=bool(data.get("keep_as_is", False))
        )

        # Accept or revise?
        accepted, _ = self.acceptance.accept(findings)
        if findings.keep_as_is and not findings.red_flags:
            accepted = True

        revised_text = current_chapter
        revision_prompt_used = None

        if not accepted:
            revision_prompt = _build_revision_prompt(
                current_chapter=current_chapter,
                findings=findings,
                artifacts=artifacts,
                banned_ngrams=banned_ngrams or [],
                target_words=getattr(chapter_plan.meta, "target_words", target_words),
            )
            revision_decode = {
                "temperature": 0.85,  # creative but controlled line-edit
                "top_p": 0.9,
                "max_tokens": 8000
            }
            await self.llm.update_default_parameters(**revision_decode)
            rev = await self.llm.generate(revision_prompt)
            revised_text, _ = _extract_revised(rev["response"])
            revision_prompt_used = revision_prompt

            # If the model somehow failed to return revised content, fall back
            if not revised_text.strip():
                revised_text = current_chapter

        return CritiqueResult(
            pass_index=0,
            findings=findings,
            revised_text=revised_text,
            revision_prompt_used=revision_prompt_used
        )

    async def improve_up_to(
        self,
        *,
        current_chapter: str,
        previous_chapter: Optional[str],
        story_so_far_summary: str,
        book_model: BookModelType,
        chapter_plan: GenericChapterBrief,
        book_plan: GenericPlan,
        banned_ngrams: Optional[List[str]] = None,
        target_words: Optional[int] = None,
        max_passes: int = 3,
    ) -> Tuple[str, List[CritiqueResult]]:
        """
        Run up to `max_passes` critique→revision passes.
        Returns (final_chapter, all_pass_results).
        """
        text = current_chapter
        results: List[CritiqueResult] = []

        for p in range(max_passes):
            res = await self.critique_once(
                current_chapter=text,
                previous_chapter=previous_chapter,
                story_so_far_summary=story_so_far_summary,
                book_model=book_model,
                chapter_plan=chapter_plan,
                book_plan=book_plan,
                banned_ngrams=banned_ngrams,
                target_words=target_words,
            )
            res.pass_index = p
            results.append(res)

            accepted, _ = self.acceptance.accept(res.findings)
            if accepted or res.findings.keep_as_is:
                return res.revised_text, results

            # Otherwise, iterate with the revised text
            text = res.revised_text

        # If we exit the loop, return the best (last) version with full trace
        return text, results

# ---- Summarizers for artifacts (compact strings for prompts) ----

def _summarize_chapter_brief(chb: GenericChapterBrief) -> str:
    """
    Build a compact one-pager string from GenericChapterBrief.
    Adjust attribute accesses to your actual model structure.
    """
    try:
        meta = chb.meta
        constraints = chb.constraints
        beats = getattr(chb, "chapter_specific_beats", []) or getattr(chb, "narrative_beats", [])
        tp = getattr(chb, "act_turning_points", [])
        return (
            f"Chapter {getattr(meta, 'chapter_number', '?')}: {getattr(meta, 'chapter_title', '')}\n"
            f"Act: {getattr(meta, 'act', '')} • Target words: {getattr(meta, 'target_words', '')}\n"
            f"POV: {getattr(constraints, 'pov', {}).get('type','')}\n"
            f"Tone: {getattr(constraints, 'tone','')} • Pace: {getattr(constraints, 'pace','')}\n"
            f"Beats: {', '.join(beats[:8])}\n"
            f"Act turning points: {', '.join(tp[:4])}"
        )
    except Exception:
        return str(chb)

def _summarize_book_plan(bp: GenericPlan) -> str:
    """
    Very compact summary built from GenericPlan.
    """
    try:
        proj = bp.project
        hl = (
            f"Title: {proj.title} | Author: {proj.author} | Genre: {proj.genre} | "
            f"Sub: {getattr(proj, 'sub_genre', '')} | Length: {getattr(proj, 'length','')}\n"
            f"Logline: {bp.logline}\n"
            f"Themes: {', '.join(bp.themes[:6])}\n"
            f"Pacing targets: {getattr(bp.pacing_targets, 'word_count', '')} / "
            f"{getattr(bp.pacing_targets, 'chapter_length', '')}\n"
            f"World: {getattr(bp.world_bible, 'setting', '')} ({getattr(bp.world_bible, 'time_period', '')})"
        )
        return hl
    except Exception:
        return str(bp)
