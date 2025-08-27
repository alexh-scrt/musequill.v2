# prompting.py
from __future__ import annotations
from typing import Dict, Any, List, Optional
from musequill.services.backend.model import BookModelType
from musequill.services.backend.writers import GenericBookPlan
from musequill.services.backend.writers.chapter_planning_model import GenericPlan
from musequill.services.backend.writers.book_planning_model import GenericBookPlan
from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.utils import coerce_to_model
from musequill.services.backend.writers.research_model import RefinedResearch

DEFAULT_BANNED_NGRAMS = [
    # put project-specific offenders here; you can pass your own list per call
    "the sun cast dappled shadows",
    "trees grew taller and closer together",
    "a new trail revealed itself",
    "voice low and mysterious",
    "the forest is full of surprises",
    "we must be careful",
]

def _act_stakes_ladder(act: str) -> str:
    if act == "I":
        return ("Raise curiosity → introduce concrete risk → end with a "
                "changed situation (new obligation, lost item, time limit).")
    if act == "II":
        return ("Escalate costs and consequences; at least one plan fails; "
                "protagonist chooses a harder path; visible tradeoffs.")
    return ("Climax resolves central problem via protagonist’s decision/action; "
            "aftermath shows concrete change vs. Chapter 1 baseline.")

def _agency_rules(pov_type: str) -> List[str]:
    base = [
        "At least one pivotal turn is caused by the protagonist’s choice.",
        "Show problem→attempt→result cycles; include at least one failed attempt.",
        "Minimize external rescue; helpers can assist but not solve the core step."
    ]
    if pov_type == "third_person_objective":
        base.append("No inner monologue; externalize intention via dialogue and action.")
    return base

def build_chapter_prompt(
    book_model: BookModelType,
    canon_summary: str,
    research_refs: RefinedResearch,
    brief: GenericChapterBrief,
    story_so_far_summary: str,
    prev_chapter_text: str | None = None,
    banned_ngrams: List[str] | None = None,
) -> str:
    banned = banned_ngrams or DEFAULT_BANNED_NGRAMS
    bm = book_model
    
    # Prioritize brief parameters over book_model
    m = brief.meta
    c = brief.constraints
    
    # Use brief constraints as primary source, fall back to book_model if needed
    pov_type = c.pov.type if c.pov else (bm.pov.type if bm.pov else '')
    tone = c.tone if hasattr(c, 'tone') and c.tone else (bm.tone if hasattr(bm, 'tone') else '')
    pace = c.pace if hasattr(c, 'pace') and c.pace else (bm.pace if hasattr(bm, 'pace') else '')

    research_lines:List[str] = []
    for k, vals in research_refs.categories.items():
        research_topic: str = f'\n* {k.upper()}:'
        for v in vals:
            research_topic += f'\n\t- {v}'
        research_lines.append(research_topic)

    scenes_lines = []
    for s in brief.scenes:
        chars = ", ".join(s.characters_on_stage)
        scenes_lines.append(
            f"- Scene {s.scene}: {s.location} ({s.time}) | On-stage: {chars}\n"
            f"  Objective: {s.objective} | Conflict: {s.conflict} | Escalation: {s.escalation}\n"
            f"  Exit on: {s.exit_on} | POV rule: {s.objective_pov_notes or ''}"
        )

    banned_bullets = "\n".join([f"- {p}" for p in banned])
    dialogue_cues = "\n".join([f"- {d}" for d in brief.dialogue_cues])
    allow_show = "\n".join([f"- {d}" for d in (brief.style_checks.allow_show_dont_tell_examples if brief.style_checks else [])])
    forbid_terms = ", ".join(brief.style_checks.forbid_inner_monologue_terms if brief.style_checks else [])

    stakes = _act_stakes_ladder(m.act)
    agency = "\n".join([f"- {rule}" for rule in _agency_rules(pov_type)])

    bootstrap: str = ""
    if prev_chapter_text is None:
        # Prioritize brief bootstrap info over book_model
        bootstrap_text = (getattr(m, 'bootstrap', None) or 
                         (bm.book.bootstrap if bm.book else ''))
        if bootstrap_text:
            bootstrap = f"- How the story begins: {bootstrap_text}"

    return f"""You are a professional novelist writing to a locked canon.

# Canon (locked; do not contradict)
## Book Model (selected highlights)
- Title: {m.book_title if hasattr(m, 'book_title') and m.book_title else bm.book.title}
- Author: {m.author if hasattr(m, 'author') and m.author else bm.book.author}
- Genre/Audience: {bm.genre.primary.type if bm.genre and bm.genre.primary else ''} | {bm.audience.type if bm.audience else ''} {bm.audience.age if bm.audience else ''}
- Structure: {bm.structure.type if bm.structure else ''} — {bm.plot.type if bm.plot else ''}
- POV: {pov_type} (rule: {c.pov.rule if c.pov else (bm.pov.type if bm.pov else 'N/A')})
- Tone/Pace: {tone} / {pace}

## Canonical Summary (source of truth)
{canon_summary}

# Continuity Inputs (use for consistency; do not restate at length)
- Story so far (summary): {story_so_far_summary.strip()}
- Previous chapter (for tone/continuity, do not repeat content): { (prev_chapter_text or '').strip()[:2000] }

# Research Materials (facts and flavor you may draw from)
{research_lines}

# Current Chapter Brief (authoritative for this chapter)
- Act: {m.act} | Chapter {m.chapter_number}: {m.chapter_title} | Target words: ~{brief.meta.target_words}

- Narrative beats: {", ".join(brief.narrative_beats)}
- Setups to seed: {", ".join(brief.setups)}
- Payoffs to deliver/advance: {", ".join(brief.payoffs)}
- Foreshadowing: {", ".join(brief.foreshadowing)}
- Motifs: {", ".join(brief.motifs)}
- Scenes (plan):
{chr(10).join(scenes_lines)}

# Craft Requirements (enforced)
- **Progress Rule**: This chapter must advance the overall story state in at least one irreversible way (new obligation, gained/lost item, deadline, promise, revealed location, changed relationship).
- **Agency Rule**:\n{agency}
- **Stakes Ladder (by act)**: {stakes}
- **Objective POV guardrail**: do NOT use inner-thought terms ({forbid_terms}). Convey interiority via action, dialogue, or sensory detail only.
- **Dialogue**: Make it character-specific and purposeful; avoid repeating warnings or generic sayings.
- **Style for readability**: Prefer sentences 8–18 words on average; vary cadence; trim filter verbs (saw, felt, heard) unless essential.
- **Avoid Repetition**: Do not reuse the following phrases/stock lines; replace with fresh language:\n{banned_bullets}
- **Title**: Generate a unique, concrete chapter title (no reused titles).

# Output Format (strict)
1) A single Markdown chapter:
   - H1 with the final unique title.
   - 2–5 clearly separated scene blocks (use `###` headings per scene).
   - Length: target {int(m.target_words*0.9)}–{int(m.target_words*1.1)} words.
2) After the chapter, include a brief QA block in fenced code labeled `qa` with:
   - One sentence explaining the **irreversible progress**.
   - The protagonist **decision that changed the outcome**.
   - Any **new/retired motifs or promises**.

Write the chapter now, honoring all constraints. Do not include an outline or meta commentary outside the final `qa` block."""
