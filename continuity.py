# continuity.py
from __future__ import annotations
import glob, os, re
from typing import List, Tuple, Dict, Any

from musequill.services.backend.model import BookModelType

QA_RE = re.compile(r"```qa(.*?)```", re.S)

def _extract_qa(text: str) -> str:
    m = QA_RE.search(text)
    return (m.group(1).strip() if m else "").strip()

def _load_previous_chapters(manuscript_dir: str, upto_chapter_num: int) -> List[Tuple[int, str]]:
    files = sorted(glob.glob(os.path.join(manuscript_dir, "Chapter_*.md")))
    out = []
    for path in files:
        try:
            num = int(os.path.basename(path).split("_")[1].split(".")[0])
        except Exception:
            continue
        if num < upto_chapter_num:
            with open(path, "r", encoding="utf-8") as f:
                out.append((num, f.read()))
    return sorted(out, key=lambda x: x[0])

def _build_summary_prompt(book_model: BookModelType,
                          prior_summaries_bullets: str,
                          chapter_snippets: List[Tuple[int, str]],
                          max_words: int) -> str:
    # Use last 1–3 full chapters for rich context + any QA “progress” notes
    recent = chapter_snippets[-3:] if chapter_snippets else []
    recent_blocks = []
    for num, txt in recent:
        qa = _extract_qa(txt)
        recent_blocks.append(f"### Chapter {num}\n"
                             f"- Key progress (from qa):\n{qa if qa else '(no qa)'}\n"
                             f"- Snippet (first ~400 chars):\n{txt[:400]}")

    pov_type = book_model.pov.type
    return f"""Summarize the story so far for continuity.

# Canon (for guardrails; do not invent beyond this)
- Structure: {book_model.structure.type}
- POV: {pov_type} (keep summary objective; no character inner thoughts)
- Audience: {book_model.audience.type} {book_model.audience.age}

# Prior continuity (carry forward, compress if needed)
{prior_summaries_bullets}

# Recent chapters
{chr(10).join(recent_blocks)}

# Output (strict; <= {max_words} words):
Write concise bullets covering only facts established on-page:
- Current protagonist goal and constraints (timers, promises, obligations)
- Irreversible changes (gains/losses, revealed info, changed relationships)
- Active allies/antagonists and their status
- Inventory/boons/skills/rules that matter
- Unresolved hooks/foreshadowing to pay off
- Locations reached + next clear destination if any
- Tone/motifs in play (1–2 items)
Do not critique or speculate. No inner monologue. End with: 'Next immediate objective: …'"""

def make_story_to_date_summary(llm_fn,
                               book_model: BookModelType,
                               manuscript_dir: str,
                               upto_chapter_num: int,
                               max_words: int = 250,
                               prior_summary_path: str | None = None) -> str:
    """
    Returns a compact continuity summary up to (but not including) chapter `upto_chapter_num`.
    If nothing has been written yet (ch 1), returns an empty string.
    """
    prev = _load_previous_chapters(manuscript_dir, upto_chapter_num)
    if not prev:
        return ""  # chapter 1: nothing to summarize yet

    # Load last saved summary (optional) to build a hierarchical, rolling summary
    prior_summaries_bullets = ""
    if prior_summary_path and os.path.exists(prior_summary_path):
        with open(prior_summary_path, "r", encoding="utf-8") as f:
            prior_summaries_bullets = f.read().strip()

    prompt = _build_summary_prompt(book_model, prior_summaries_bullets, prev, max_words)
    summary = llm_fn(prompt, temperature=0.2, top_p=0.9, top_k=40)

    # Keep it around for the next call if you like
    if prior_summary_path:
        os.makedirs(os.path.dirname(prior_summary_path), exist_ok=True)
        with open(prior_summary_path, "w", encoding="utf-8") as f:
            f.write(summary.strip())

    return summary.strip()

def get_prev_chapter_text(manuscript_dir: str, chapter_num: int) -> str | None:
    """Fetch the full text of the immediately preceding chapter, if any."""
    prev_path = os.path.join(manuscript_dir, f"Chapter_{chapter_num-1:02d}.md")
    if os.path.exists(prev_path):
        with open(prev_path, "r", encoding="utf-8") as f:
            return f.read()
    return None
