# chapter_writer.py
# A generic, canon-locked chapter writer for any book/genre.
# Expects chapter briefs like the one you posted.
from __future__ import annotations
from typing import Dict, Any, List, Callable, Tuple
import re, textwrap
from typing import Any, Dict, List, Optional, Tuple, Callable
import os, re, math, textwrap, unicodedata
from datetime import datetime

from continuity import make_story_to_date_summary, get_prev_chapter_text
from musequill.services.backend.llm.ollama_client import (
    create_llm_service,
    LLMService
)

from musequill.services.backend.model import BookModelType
from musequill.services.backend.writers import GenericBookPlan
from musequill.services.backend.writers.chapter_planning_model import GenericPlan
from musequill.services.backend.writers.book_planning_model import GenericBookPlan
from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.utils import coerce_to_model
from musequill.services.backend.writers.research_model import RefinedResearch

LLMFn = Callable[[str], str]  # Your LLM: def complete(prompt: str) -> str

banned_ngrams = [
                "the sun cast dappled shadows",
                "trees grew taller and closer together",
                "a new trail revealed itself",
                "voice low and mysterious",
                "the forest is full of surprises",
                "we must be careful",
            ]

# ---------- Public API ----------
# chapter_writer.py

def count_ngrams(text: str, n: int = 3) -> Dict[str, int]:
    words = re.findall(r"[A-Za-z']+", text.lower())
    grams = [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]
    freq = {}
    for g in grams:
        freq[g] = freq.get(g, 0) + 1
    return freq

def find_banned(text: str, banned: List[str]) -> List[str]:
    low = text.lower()
    return [p for p in banned if p.lower() in low]

def extract_qa(text: str) -> Tuple[str, str]:
    m = re.search(r"```qa(.*?)```", text, flags=re.S)
    qa = m.group(0) if m else ""
    clean = text.replace(qa, "").strip()
    return clean, (m.group(1).strip() if m else "")

def needs_revision(chapter_text: str, banned_phrases: List[str], target_words: int) -> List[str]:
    issues = []
    word_count = len(re.findall(r"\b\w+\b", chapter_text))
    if not (0.75*target_words <= word_count <= 1.25*target_words):
        issues.append(f"length off target ({word_count} vs {target_words}).")
    dupes = [g for g,c in count_ngrams(chapter_text, 4).items() if c>=3]
    if dupes:
        issues.append(f"repetitive 4-grams ({len(dupes)}) found.")
    banned_hit = find_banned(chapter_text, banned_phrases)
    if banned_hit:
        issues.append(f"banned phrases used: {', '.join(banned_hit)}.")
    if chapter_text.count("# ") != 1:
        issues.append("missing or multiple H1 titles.")
    if "###" not in chapter_text:
        issues.append("no scene headings (###).")
    return issues

def revision_prompt(original: str, issues: List[str], brief: GenericChapterBrief, banned: List[str]) -> str:
    bullets = "\n".join([f"- {i}" for i in issues])
    banned_bullets = "\n".join([f"- {p}" for p in banned])
    return f"""Revise the chapter below to fix the listed issues without changing canon or POV constraints.
Fixes required:
{bullets}

Avoid these phrases entirely:
{banned_bullets}

Keep structure (H1 title; `###` scene headings). Keep length within ±10% of target {brief.meta.target_words} words.

=== BEGIN CHAPTER ===
{original}
=== END CHAPTER ===
Return only the revised chapter and the `qa` block.
"""

def adjust_llm_parameters_for_issues(issues: List[str], base_params: Dict[str, Any], attempt: int) -> Dict[str, Any]:
    """Adjust LLM parameters based on the types of issues encountered."""
    params = base_params.copy()
    
    # Determine issue types
    has_length_issues = any("length" in issue for issue in issues)
    has_repetition_issues = any("repetitive" in issue or "4-grams" in issue for issue in issues)
    has_banned_phrases = any("banned phrases" in issue for issue in issues)
    has_structure_issues = any("title" in issue or "scene headings" in issue for issue in issues)
    
    # Adjust parameters based on attempt number and issue types
    if attempt == 1:
        # Second attempt: moderate adjustments
        if has_repetition_issues:
            params["repeat_penalty"] = min(1.25, params.get("repeat_penalty", 1.1) + 0.1)
            params["frequency_penalty"] = min(0.4, params.get("frequency_penalty", 0.2) + 0.1)
            params["presence_penalty"] = min(0.4, params.get("presence_penalty", 0.2) + 0.1)
        
        if has_length_issues:
            params["temperature"] = max(0.7, params.get("temperature", 0.9) - 0.1)
            params["top_p"] = max(0.8, params.get("top_p", 0.9) - 0.05)
        
        if has_banned_phrases:
            params["temperature"] = max(0.6, params.get("temperature", 0.9) - 0.2)
            params["top_k"] = max(40, params.get("top_k", 60) - 10)
    
    elif attempt == 2:
        # Third attempt: aggressive adjustments
        if has_repetition_issues:
            params["repeat_penalty"] = 1.3
            params["frequency_penalty"] = 0.5
            params["presence_penalty"] = 0.5
            params["repeat_last_n"] = min(256, params.get("repeat_last_n", 128) * 2)
        
        if has_length_issues or has_structure_issues:
            params["temperature"] = 0.6
            params["top_p"] = 0.75
            params["top_k"] = 30
        
        if has_banned_phrases:
            params["temperature"] = 0.5
            params["top_k"] = 25
            params["min_p"] = 0.1
    
    return params


async def write_chapter_with_qc(
    llm: LLMService,
    book_model: BookModelType,
    canon_summary: str,
    research_refs: RefinedResearch,
    brief: GenericChapterBrief,
    story_so_far_summary: str,
    prev_chapter_text: str | None,
    banned_ngrams: List[str],
    decode_overrides: Dict[str, Any] | None = None,
    max_retries: int = 3,
) -> Dict[str, str]:
    from prompting import build_chapter_prompt

    prompt = build_chapter_prompt(
        book_model, canon_summary, research_refs, brief,
        story_so_far_summary, prev_chapter_text, banned_ngrams
    )

    # Base parameters for initial attempt
    base_decode_opts = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 60,
        "repeat_penalty": 1.1,
        "repeat_last_n": 128,
        "min_p": 0.05,
        "max_tokens": 15000,
        "presence_penalty": 0.2,
        "frequency_penalty": 0.2,
        **(decode_overrides or {})
    }

    text, qa = "", ""
    all_attempts_issues = []
    
    for attempt in range(max_retries):
        # Adjust parameters based on previous issues (if any)
        if attempt == 0:
            decode_opts = base_decode_opts.copy()
        else:
            previous_issues = all_attempts_issues[-1] if all_attempts_issues else []
            decode_opts = adjust_llm_parameters_for_issues(previous_issues, base_decode_opts, attempt)
        
        await llm.update_default_parameters(**decode_opts)
        
        if attempt == 0:
            # Initial generation
            draft = await llm.generate(prompt)
            text, qa = extract_qa(draft['response'])
        else:
            # Revision attempts
            revision_prompt_text = revision_prompt(text, all_attempts_issues[-1], brief, banned_ngrams)
            fix = await llm.generate(revision_prompt_text)
            text, qa = extract_qa(fix['response'])
        
        # Check for issues
        issues = needs_revision(text, banned_ngrams, brief.meta.target_words)
        all_attempts_issues.append(issues)
        
        if not issues:
            # Success! No issues found
            return {
                "chapter_md": text,
                "qa": qa,
                "notes": f"OK (resolved after {attempt + 1} attempt{'s' if attempt > 0 else ''})"
            }
    
    # All attempts exhausted - return final result with remaining issues
    final_issues = all_attempts_issues[-1] if all_attempts_issues else []
    return {
        "chapter_md": text,
        "qa": qa,
        "notes": f"Issues remaining after {max_retries} attempts: " + "; ".join(final_issues) if final_issues else f"Completed after {max_retries} attempts"
    }

from .chapter_critic import (
    ChapterCritic,
    AcceptancePolicy,
    CritiqueResult
)
from .chapter_brief_model import GenericChapterBrief

async def adaptive_chapter_critique(
    *,
    llm: LLMService,
    book_model: BookModelType,
    book_plan: GenericBookPlan,
    brief: GenericChapterBrief,
    story_so_far_summary: str,
    chapter_text: str,
    prev_chapter_text: str | None,
    banned_ngrams: List[str],
) -> Dict[str, Any]:
    critic = ChapterCritic(
        llm, 
        acceptance=AcceptancePolicy(
            min_overall_score=0.80,   # tighten/loosen as you wish
            min_axis_score=0.72,
            allow_red_flags=False
        )
    )

    final_text, critique_results = await critic.improve_up_to(
        current_chapter=chapter_text,                           # from your draft/rewrite
        previous_chapter=prev_chapter_text,
        story_so_far_summary=story_so_far_summary,
        book_model=book_model,
        chapter_plan=brief,                             # your GenericChapterBrief
        book_plan=book_plan,                    # your GenericPlan
        banned_ngrams=banned_ngrams,
        target_words=brief.meta.target_words,
        max_passes=3
    )

    return {
        "chapter_md": final_text,
        "critique_results": [r.to_dict() for r in critique_results]
    }


async def write_all_chapters_with_qc(
    *,
    book_model: BookModelType,
    book_plan: GenericBookPlan,
    chapter_briefs: List[GenericChapterBrief],
    book_summary: str,
    research_corpus: RefinedResearch,
    llm: LLMService,
    out_dir: str = "manuscript",
) -> List[Dict[str, Any]]:
    """
    Iterate over briefs in order, carrying forward rolling recaps/continuity.
    """
    # Extract from the GenericBookPlan structure
    # Note: book_model is passed as a parameter, use that instead
    # book_summary is passed as a parameter, use that instead

    os.makedirs(out_dir, exist_ok=True)
    results: List[Dict[str, Any]] = []

    story_so_far:str = ""
    prev_chapter:str|None = None

    manuscript_dir = os.path.join(out_dir, "manuscript")

    for brief in sorted(chapter_briefs, key=lambda b: b.meta.chapter_number):
        chapter_num = int(brief.meta.chapter_number)
        res = await write_chapter_with_qc(
            llm=llm,
            book_model=book_model,
            canon_summary=book_summary,
            research_refs=research_corpus,
            brief=brief,
            story_so_far_summary=story_so_far,   # <— THIS is story_to_date_summary
            prev_chapter_text=prev_chapter,
            banned_ngrams= banned_ngrams,
            max_retries=3,
        )

        res = await adaptive_chapter_critique(
            llm=llm,
            book_model=book_model,
            book_plan=book_plan,
            brief=brief,
            story_so_far_summary=story_so_far,
            chapter_text=res['chapter_md'],
            prev_chapter_text=prev_chapter,
            banned_ngrams=banned_ngrams
        )


        results.append(res)

        story_so_far = make_story_to_date_summary(
            llm_fn=llm,
            book_model=book_model,
            manuscript_dir=manuscript_dir,
            upto_chapter_num=chapter_num,
            max_words=500,  # keep compact
            prior_summary_path="summaries/story_so_far.md",
        )

        prev_chapter = res['chapter_md']
        save_markdown_chapter(res['chapter_md'], brief, out_dir)

    return results



# ---------- Context Pack ----------

def build_context_pack(
    *,
    book_model: BookModelType,
    book_summary: str,
    constraints: Dict[str, Any],
    research_corpus: Dict[str, Any],
    chapter_brief: GenericChapterBrief,
    prior_chapter_text: Optional[str],
    prior_chapter_summary: Optional[str],
    cumulative_summary: Optional[str],
) -> Dict[str, Any]:

    # trim noisy fields from book_model for prompt economy
    model_compact = {
        "book": {
            "title": dget(book_model, "book.title", "Untitled"),
            "author": dget(book_model, "book.author", "Unknown Author"),
            "type": dget(book_model, "book.type"),
            "length": dget(book_model, "book.length"),
            "language": dget(book_model, "book.language"),
        },
        "structure": book_model.get("structure"),
        "audience": book_model.get("audience"),
        "genre": book_model.get("genre"),
        "tone": book_model.get("tone") or constraints.get("tone"),
        "pov": book_model.get("pov") or constraints.get("pov"),
        "plot": book_model.get("plot"),
        "style": book_model.get("style"),
        "world": book_model.get("world"),
    }

    # research_pack = select_research_for_prompt(research_corpus, chapter_brief, max_items=6)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "book_model": model_compact,
        "book_summary": book_summary.strip(),
        "constraints": {
            "pov": constraints.get("pov"),
            "tone": constraints.get("tone"),
            "pace": constraints.get("pace"),
            "safety": getattr(chapter_brief.constraints, 'safety', None),
        },
        "chapter_brief": chapter_brief,
        "rolling": {
            "prior_chapter_summary": prior_chapter_summary or "",
            "cumulative_summary": cumulative_summary or "",
            "prior_chapter_text_tail": tail(prior_chapter_text, 2500),  # last ~2500 chars for continuity of voice/scene
        },
        "research": research_corpus,
    }


def select_research_for_prompt(research: Dict[str, Any], brief: GenericChapterBrief, max_items: int = 6) -> Dict[str, Any]:
    """
    Down-select research to the most relevant items for this chapter.
    Shape: {"figures":[...], "locales":[...], "topics":[...]}
    """
    setting = (brief.scenes[0].location if brief.scenes else brief.meta.chapter_title).lower()
    figure = (brief.scenes[0].characters_on_stage[0] if brief.scenes and brief.scenes[0].characters_on_stage else brief.meta.chapter_title).lower()

    def pick(items, keyname):
        out = []
        for it in items or []:
            name = (it.get("name") or "").lower()
            if name and (name in setting or name in figure):
                out.append(it)
        # top up if we have space
        for it in (items or []):
            if it not in out:
                out.append(it)
        # trim
        return out[: max_items // 2]

    return {
        "figures": pick(research.get("figures"), "name"),
        "locales": pick(research.get("locales"), "name"),
        "topics": (research.get("topics") or [])[: max_items // 3],
    }


# ---------- Prompting ----------

def make_prompt(ctx: Dict[str, Any]) -> str:
    b = ctx["book_model"]
    cons = ctx["constraints"]
    brief = ctx["chapter_brief"]

    # Safety/POV rules (hard locks)
    style_checks = (brief.get("style_checks") or {})
    forbid_terms = style_checks.get("forbid_inner_monologue_terms", [])
    pov_rule = dget(cons, "pov.rule", "")

    scenes_block = format_scenes(brief.get("scenes") or [])
    research_block = format_research(ctx.get("research") or {})
    beats = "\n- ".join(brief.get("narrative_beats", [])) or "Follow act-appropriate escalation."

    return textwrap.dedent(f"""
    You are a professional novelist. Write the next chapter as publishable prose in **Markdown**.

    ## Canon (LOCKED)
    - Book: {b['book']['title']} by {b['book']['author']}
    - Structure: {fmt(b.get('structure'))}
    - Audience: {fmt(b.get('audience'))}
    - Genre: {fmt(b.get('genre'))}
    - Tone: {cons.get('tone')}
    - Pace: {cons.get('pace')}
    - POV: {fmt(cons.get('pov'))}
    - Safety: {fmt(cons.get('safety'))}

    ## Summary (LOCKED)
    {ctx['book_summary']}

    ## Rolling Continuity
    - Prior chapter (summary): {ctx['rolling']['prior_chapter_summary'] or 'N/A'}
    - Cumulative summary so far: {ctx['rolling']['cumulative_summary'] or 'N/A'}
    - Tail of prior chapter (to match voice/ongoing beats):\n{ctx['rolling']['prior_chapter_text_tail'] or 'N/A'}

    ## Chapter Brief (LOCKED)
    - Act: {brief.meta.act} | Chapter {brief.meta.chapter_number}: {brief.meta.chapter_title}
    - Target words (±10%): {brief.meta.target_words}
    - Beats: 
      - {beats}
    - Setups to plant: {", ".join(brief.get("setups", [])) or "—"}
    - Payoffs to deliver: {", ".join(brief.get("payoffs", [])) or "—"}
    - Foreshadowing cues: {", ".join(brief.get("foreshadowing", [])) or "—"}

    ## Scene Plan (Guidance)
    {scenes_block}

    ## Research Notes (facts only—do not contradict)
    {research_block}

    ## Style Locks
    - Do not include inner monologue or omniscient mind-reading.
    - Avoid these tokens in narration (dialogue is fine): {", ".join(forbid_terms) if forbid_terms else "—"}
    - Enforce POV rule: {pov_rule}
    - Show, don’t tell. Use observable action, dialogue, and concrete sensory detail.
    - Keep the tone: {cons.get('tone')}. Keep the pace: {cons.get('pace')}.

    ## Output
    - Write **one complete chapter** in Markdown.
    - Start with: `# Chapter {brief.meta.chapter_number}: {brief.meta.chapter_title}`
    - No author notes, no outlines, no bullet lists—**prose only** after the header.
    - Stay strictly within canon and research. If a fact is unknown, stay neutral; do not invent lore beyond the provided materials.

    Begin.
    """).strip()


def make_repair_prompt(ctx: Dict[str, Any], prior_text: str, issues: List[str]) -> str:
    brief = ctx["chapter_brief"]
    fixes = "\n".join(f"- {i}" for i in issues)
    return textwrap.dedent(f"""
    You produced a chapter that needs fixes. Apply the following repairs and output a corrected **Markdown** chapter.

    ### Required Repairs
    {fixes}

    ### Chapter Header (keep identical)
    # Chapter {brief.meta.chapter_number}: {brief.meta.chapter_title}

    ### Your Previous Draft (for reference only)
    {prior_text[:12000]}

    Re-write cleanly, preserving the intended plot beats and constraints from the brief. Output only the corrected chapter.
    """).strip()


# ---------- Validation & Repairs ----------

def validate(text: str, brief: GenericChapterBrief, constraints: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    target = brief.meta.target_words
    wc = count_words(text)
    low, high = int(target*0.9), int(target*1.1)
#    if wc < low: issues.append(f"Increase length to at least {low} words (now {wc}).")
#    if wc > high: issues.append(f"Reduce length to at most {high} words (now {wc}).")

    # POV sanity checks (objective: no narrator interiority)
    pov = (constraints.get("pov") or {}).get("type", "").lower()
    if "objective" in pov:
        # Strip dialogue to avoid false positives, then look for interiority verbs.
        narration = strip_dialogue(text)
        forbidden = (brief.get("style_checks") or {}).get("forbid_inner_monologue_terms", [])
        hits = [w for w in forbidden if re.search(rf"\\b{re.escape(w)}\\b", narration, flags=re.IGNORECASE)]
        if hits:
            issues.append(f"Remove inner monologue from narration: found {sorted(set(hits))}.")
        # Also flag 1st-person narration outside quotes.
        if re.search(r"(?<![A-Za-z])I(?![A-Za-z])", narration):  # rough heuristic
            issues.append("POV breach: first-person narration detected outside dialogue.")

    # Simple tone/pace nudge (optional; informational)
    # You can extend this with classifiers if you want.
    return issues


def enforce_max_words(text: str, target: int) -> str:
    # hard cap at 115% to be safe against model drift
    cap = int(target * 1.15)
    words = text.split()
    if len(words) <= cap:
        return text
    return " ".join(words[:cap]).rstrip() + " …"


def strip_dialogue(text: str) -> str:
    # Remove things inside double or curly quotes to avoid false positives
    txt = re.sub(r"“[^”]*”", "", text)
    txt = re.sub(r"\"[^\"]*\"", "", txt)
    txt = re.sub(r"‘[^’]*’", "", txt)
    txt = re.sub(r"'[^']*'", "", txt)
    return txt


def count_words(text: str) -> int:
    # Simple word count
    return len(re.findall(r"\b\w+\b", text))


# ---------- Summaries / Continuity ----------

def summarize_chapter(text: str, brief: GenericChapterBrief, llm: LLMFn) -> str:
    prompt = textwrap.dedent(f"""
    Summarize the following chapter in 6–10 bullet points focused on **observable** events, locations, and on-page outcomes.
    Avoid character interiority or speculation. Use concise present-tense lines.

    Chapter title: {brief.meta.chapter_title}

    Text:
    {text[:16000]}
    """).strip()
    return llm(prompt).strip()


def extract_continuity(text: str, brief: GenericChapterBrief, llm: LLMFn) -> Dict[str, Any]:
    prompt = textwrap.dedent(f"""
    Extract a continuity pack as JSON with keys:
      - "facts": short strings of canonical facts established on-page
      - "entities": {{ "characters":[...], "locales":[...], "objects":[...] }}
      - "open_threads": short strings of unresolved items to track
      - "callbacks": prior setups that were paid off here (strings)

    Rules: list only items **explicitly present on the page**. No speculation.

    Chapter: {brief.meta.chapter_number} – {brief.meta.chapter_title}
    Text:
    {text[:16000]}

    Output JSON only.
    """).strip()

    raw = llm(prompt).strip()
    return safe_parse_json(raw, default={"facts": [], "entities": {"characters":[], "locales":[], "objects":[]}, "open_threads": [], "callbacks": []})


def update_rolling_summary(current: str, new_summary: str, max_len: int = 2000) -> str:
    merged = (current + "\n" + new_summary).strip()
    if len(merged) <= max_len:
        return merged
    # naive trim: keep the last portion
    return merged[-max_len:]


# ---------- IO helpers ----------

def save_markdown_chapter(text: str, brief: GenericChapterBrief, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    ch = brief.meta.chapter_number
    title = brief.meta.chapter_title
    fname = f"{ch:02d}-{slugify(title)}.md"
    path = os.path.join(out_dir, fname)

    header = f"# Chapter {ch}: {title}\n\n"
    payload = text
    # If model forgot header, add it
    if not text.strip().lower().startswith("# chapter"):
        payload = header + text.lstrip()

    with open(path, "w", encoding="utf-8") as f:
        f.write(payload)
    return path


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value or "chapter"


# ---------- Formatting ----------

def format_scenes(scenes: List[Dict[str, Any]]) -> str:
    if not scenes:
        return "—"
    lines = []
    for s in scenes:
        who = ", ".join(s.get("characters_on_stage", []))
        lines.append(f"- Scene {s['scene']} @ {s.get('location')} ({s.get('time')}): goal={s.get('objective')}; conflict={s.get('conflict')}; exit_on={s.get('exit_on')}.")
        if who:
            lines.append(f"  - On stage: {who}")
    return "\n".join(lines)


def format_research(research: Dict[str, Any]) -> str:
    blocks = []
    for key in ("locales", "figures", "topics"):
        items = research.get(key) or []
        if not items: 
            continue
        label = key.capitalize()
        rows = []
        for it in items:
            name = it.get("name", "?")
            usage = it.get("usage") or it.get("notes") or ""
            rows.append(f"  - {name}: {usage}")
        blocks.append(f"{label}:\n" + "\n".join(rows))
    return "\n".join(blocks) if blocks else "—"


def fmt(x: Any) -> str:
    if not x: return "—"
    if isinstance(x, dict):
        return ", ".join(f"{k}: {v}" for k, v in x.items() if v is not None)
    return str(x)


def dget(d: Dict[str, Any], dotted: str, default=None):
    cur = d
    for p in dotted.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


# ---------- JSON safety ----------

def safe_parse_json(s: str, default: Any) -> Any:
    import json
    try:
        return json.loads(s)
    except Exception:
        return default


# ---------- Small utilities ----------

def tail(s: Optional[str], n_chars: int) -> str:
    if not s: return ""
    s = s.strip()
    return s[-n_chars:] if len(s) > n_chars else s
