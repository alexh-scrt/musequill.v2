# chapter_planner.py

from typing import Any, Dict, List, Optional, Tuple
import re
import random
import json
from poc.qa_session import QASession
from poc.llm_ollama import llm

# ----------------------------
# Public API
# ----------------------------

cached_characters: Dict[str, str] = {}

def make_chapter_brief(
    *,
    book_model: Dict[str, Any],
    book_summary: str,
    constraints: Dict[str, Any],
    research: Dict[str, Any],
    chapter_item: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Construct a chapter brief from canon + constraints + research + a chapter plan item.
    This function is genre-agnostic, structure-aware, and POV-safe.

    Required inputs (minimal shape):
      book_model: {
        "book": {"title": str, "author": str},
        "structure": {"type": str},                 # e.g., "Hero's Journey", "Three-Act", "Mystery", ...
        "audience": {"type": str, "age": "7-12"},   # optional; used for safety profile
        "tone": {"type": str} or "tone": str        # optional; fallback to constraints.tone
      }
      book_summary: str
      constraints: {
        "pov": {"type": str, "rule": str},
        "tone": str,
        "pace": str
      }
      research: {
        # flexible; any of these keys are optional
        "figures": [{"name": str, "role": str|None, "source_snippet": str|None, "tags": List[str]|None}, ...],
        "locales": [{"name": str, "function": str|None, "source_snippet": str|None, "tags": List[str]|None}, ...],
        "topics": [{"name": str, "notes": str|None, "tags": List[str]|None}, ...],
      }
      chapter_item: {
        "ch": int,
        "title": str,
        "act": "I"|"II"|"III",
        "setting": str|None,
        "figure": str|None,
        "external_goal": str,
        "obstacle": str,
        "turn": str,
        "cliffhanger": str,
        "word_count": int
      }
    """
    # --- Canon ---
    title, author = _safe_get(book_model, "book.title", default="Untitled"), _safe_get(book_model, "book.author", default="Unknown Author")
    structure_type = (_safe_get(book_model, "structure.type", default="Three-Act") or "Three-Act").strip()

    # --- Global constraints (locked) ---
    pov = constraints.get("pov", {"type": "third_person_objective", "rule": ""})
    tone = _first_of([_safe_get(book_model, "tone.type"), constraints.get("tone")], default="neutral")
    pace = constraints.get("pace", "medium")

    # --- Safety from audience ---
    audience = _safe_get(book_model, "audience", default={})
    safety = _safety_profile(audience)

    # --- Research selection for this chapter ---
    chapter_research = _select_research(
        research=research,
        chapter_setting=chapter_item.get("setting"),
        chapter_figure=chapter_item.get("figure"),
        chapter_goal=chapter_item.get("external_goal"),
        chapter_obstacle=chapter_item.get("obstacle"),
    )

    # --- Beats per structure/act ---
    beats = _beats_for_structure(structure_type, chapter_item["act"])

    # --- Scene planning ---
    target_words = int(chapter_item.get("word_count", 1500))
    n_scenes = _scene_count(target_words, pace)
    scenes = _scenes_from_item(
        chapter_item=chapter_item,
        pov=pov,
        n_scenes=n_scenes,
        default_protagonist=_guess_protagonist_name(book_model, book_summary),
        figure_pool=[f.get("name") for f in (research.get("figures") or []) if isinstance(f, dict) and f.get("name")]
    )

    # --- Hooks & craft ---
    setups, payoffs, foreshadowing = _hooks_from_chapter(chapter_item, structure_type)

    # --- Motifs & palettes (generic, influenced by research/setting/tone) ---
    motifs = _motifs_from_inputs(chapter_item, research, structure_type)
    sensory_palette = _sensory_from_setting(chapter_item.get("setting"), research)

    # --- Dialogue cues by tone & POV ---
    dialogue_cues = _dialogue_cues(tone, pov)

    # --- Style checks by POV ---
    style_checks = _style_checks_by_pov(pov)

    return {
        "meta": {
            "book_title": title,
            "author": author,
            "act": chapter_item["act"],
            "chapter_number": chapter_item["ch"],
            "chapter_title": chapter_item["title"],
            "target_words": target_words
        },
        "constraints": {
            "pov": pov,
            "tone": tone,
            "pace": pace,
            "safety": safety
        },
        "canon_summary": book_summary.strip(),
        "research_refs": chapter_research,
        "narrative_beats": beats,
        "scenes": scenes,
        "setups": setups,
        "payoffs": payoffs,
        "foreshadowing": foreshadowing,
        "motifs": motifs,
        "sensory_palette": sensory_palette,
        "dialogue_cues": dialogue_cues,
        "style_checks": style_checks
    }


def make_all_chapter_briefs_from_plan(
    *,
    book_plan: Dict[str, Any],
    research_corpus: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Convenience wrapper that extracts the right parts from your book_plan and
    generates briefs for every chapter_plan item.

    research_corpus can override/augment book_plan["research_selection"] with
    richer fields like role/tags/snippets.
    """
    book_model = book_plan["canon"]["book_model"]
    book_summary = book_plan["constraints"]["summary"]
    constraints = {
        "pov": book_plan["constraints"]["pov"],
        "tone": book_plan["constraints"]["tone"],
        "pace": book_plan["constraints"]["pace"]
    }

    # Normalize research into the generic shape {figures, locales, topics}
    research = _normalize_research(book_plan.get("research_selection"), research_corpus)

    briefs: List[Dict[str, Any]] = []
    for ch in book_plan.get("chapter_plan", []):
        briefs.append(
            make_chapter_brief(
                book_model=book_model,
                book_summary=book_summary,
                constraints=constraints,
                research=research,
                chapter_item=ch,
            )
        )
    return briefs


# ----------------------------
# Helpers (generic, no book-specific content)
# ----------------------------

def _safe_get(d: Dict[str, Any], dotted: str, default=None):
    cur = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur

def _first_of(options: List[Optional[str]], default: str) -> str:
    for o in options:
        if isinstance(o, str) and o.strip():
            return o.strip()
    return default

def _age_bounds_from_str(age_str: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    if not age_str:
        return None, None
    m = re.search(r"(\d+)\D+(\d+)", age_str)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo > hi: lo, hi = hi, lo
        return lo, hi
    return None, None

def _safety_profile(audience: Dict[str, Any]) -> Dict[str, Any]:
    a_type = (audience.get("type") or "").lower()
    lo, hi = _age_bounds_from_str(audience.get("age"))
    # Defaults by audience:
    if a_type in {"children", "middle grade", "mg"} or (hi and hi <= 12):
        return {"peril_level": "mild", "solutions_visible": True, "age_floor": lo or 7, "age_ceiling": hi or 12}
    if a_type in {"ya", "young adult"} or (lo and 12 < lo <= 18):
        return {"peril_level": "moderate", "solutions_visible": True, "age_floor": lo or 13, "age_ceiling": hi or 18}
    # adult / unspecified
    return {"peril_level": "moderate", "solutions_visible": False, "age_floor": lo, "age_ceiling": hi}

def _normalize_research(selection: Optional[Dict[str, Any]], corpus: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    global cached_characters
    # Merge plan-level selection with corpus; be permissive about shapes.
    figures, locales, topics = [], [], []

    def norm_fig(x):
        description: Optional[str] = None
        character_name = x.get("name") if isinstance(x, dict) else str(x)
        if character_name not in cached_characters:
            if corpus is not None:
                qa = QASession(llm)
                qa.add_context("research_character", json.dumps(corpus))
                description = qa.ask(f"Who is {x.get("name") if isinstance(x, dict) else str(x)}")
            if description is not None:
                cached_characters[character_name] = description
        if character_name in cached_characters:
            character_name = f'{character_name} - {cached_characters[character_name]}'
        return {
            "name": character_name,
            "role": (x.get("role") if isinstance(x, dict) else None),
            "source_snippet": (x.get("source_snippet") if isinstance(x, dict) else None),
            "tags": x.get("tags") if isinstance(x, dict) else None,
        }

    def norm_loc(x):
        return {
            "name": x.get("name") if isinstance(x, dict) else str(x),
            "function": (x.get("function") if isinstance(x, dict) else None),
            "source_snippet": (x.get("source_snippet") if isinstance(x, dict) else None),
            "tags": x.get("tags") if isinstance(x, dict) else None,
        }

    if selection:
        for f in selection.get("mythic_figures", []) + selection.get("figures", []):
            figures.append(norm_fig(f))
        for l in selection.get("locales", []):
            locales.append(norm_loc(l))

    if corpus:
        for f in corpus.get("figures", []):
            figures.append(norm_fig(f))
        for l in corpus.get("locales", []):
            locales.append(norm_loc(l))
        for t in corpus.get("topics", []):
            topics.append({
                "name": t.get("name") if isinstance(t, dict) else str(t),
                "notes": t.get("notes") if isinstance(t, dict) else None,
                "tags": t.get("tags") if isinstance(t, dict) else None,
            })

    # Deduplicate by name
    def dedupe(items, key="name"):
        seen, out = set(), []
        for it in items:
            n = it.get(key)
            if not n or n in seen: 
                continue
            seen.add(n)
            out.append(it)
        return out

    return {
        "figures": dedupe(figures),
        "locales": dedupe(locales),
        "topics": dedupe(topics)
    }

def _select_research(
    *,
    research: Dict[str, Any],
    chapter_setting: Optional[str],
    chapter_figure: Optional[str],
    chapter_goal: Optional[str],
    chapter_obstacle: Optional[str],
) -> List[Dict[str, str]]:
    picks: List[Dict[str, str]] = []

    # 1) Locale match first
    if chapter_setting:
        loc = _best_match(research.get("locales", []), chapter_setting)
        if loc:
            picks.append({
                "name": loc["name"],
                "type": "locale",
                "snippet": (loc.get("source_snippet") or "")[:400],
                "usage": f"Ground scene sensory details in {loc['name']}."
            })

    # 2) Figure match second
    if chapter_figure:
        fig = _best_match(research.get("figures", []), chapter_figure)
        if fig:
            role = fig.get("role") or "figure"
            picks.append({
                "name": fig["name"],
                "type": "figure",
                "snippet": (fig.get("source_snippet") or "")[:400],
                "usage": f"Use {fig['name']} as a {role} impacting the goal/obstacle."
            })

    # 3) Supplement with a topic or extra locale/figure to total ~3 refs
    if len(picks) < 3:
        pool = (research.get("topics") or []) + (research.get("locales") or []) + (research.get("figures") or [])
        random.shuffle(pool)
        for item in pool:
            if len(picks) >= 3:
                break
            name = item.get("name")
            if not name or any(p["name"] == name for p in picks):
                continue
            itype = "topic" if "notes" in item else ("locale" if "function" in item else "figure")
            picks.append({
                "name": name,
                "type": itype,
                "snippet": (item.get("source_snippet") or item.get("notes") or "")[:400],
                "usage": _generic_usage_line(itype, name, chapter_goal, chapter_obstacle)
            })

    # Guarantee at least 2
    if len(picks) < 2:
        picks.append({"name": "General Setting", "type": "topic", "snippet": "", "usage": "Use environmental cues for authenticity."})
        picks.append({"name": "Conflict Pattern", "type": "topic", "snippet": "", "usage": "Escalate conflict through tangible stakes."})
    return picks

def _best_match(items: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    # naive: exact or case-insensitive containment
    name_low = name.lower()
    for it in items:
        if (it.get("name") or "").lower() == name_low:
            return it
    for it in items:
        if name_low in (it.get("name") or "").lower():
            return it
    return items[0] if items else None

def _generic_usage_line(itype: str, name: str, goal: Optional[str], obstacle: Optional[str]) -> str:
    if itype == "locale":
        return f"Embed local textures of {name} to shape the scene while pursuing '{goal or 'the objective'}'."
    if itype == "figure":
        return f"Let {name} complicate or aid the attempt to overcome '{obstacle or 'the obstacle'}'."
    return f"Apply {name} to theme or procedure influencing the chapter’s beats."

def _beats_for_structure(structure_type: str, act: str) -> List[str]:
    st = structure_type.lower()
    if "hero" in st:  # Hero's Journey
        if act == "I":
            return ["Ordinary World & Hook", "Call/Refusal/Threshold", "First Tests & Allies"]
        if act == "II":
            return ["Road of Trials", "Midpoint Reversal/Boon", "Approach to Ordeal"]
        return ["Ordeal & Reward", "Return with Boon", "New Normal/Closing Image"]
    if "mystery" in st or "investigation" in st:
        if act == "I":
            return ["Crime/Question Posed", "Initial Leads", "First Red Herring"]
        if act == "II":
            return ["Deepening Clues", "Midpoint Revelation", "Complication/Setback"]
        return ["Showdown & Reveal", "Resolution of Threads", "Aftermath"]
    if "romance" in st:
        if act == "I":
            return ["Meet Cute / Catalyst", "Fun & Games / Spark", "First Rift"]
        if act == "II":
            return ["Deepening Bond", "Breakup/All Is Lost", "Gesture/Realization"]
        return ["Grand Gesture", "Commitment Choice", "HEA/HFN Image"]
    if "heist" in st:
        if act == "I":
            return ["Problem & Target", "Team Assembly", "Plan Formation"]
        if act == "II":
            return ["Practice/Setbacks", "Plan Goes Sideways", "Improvised Path"]
        return ["Execution Twist", "Getaway/Consequences", "Debrief/Tag"]
    # Three-Act / default
    if act == "I":
        return ["Set-up & Hook", "Inciting Incident", "First Turn to Act II"]
    if act == "II":
        return ["Progress & Complications", "Midpoint Shift", "Crisis/Second Turn"]
    return ["Climax", "Resolution", "Aftermath/Closing Image"]

def _scene_count(target_words: int, pace: str) -> int:
    pace_low = (pace or "").lower()
    # Aim for 500–1200 words per scene depending on pace
    if "fast" in pace_low:
        approx = max(2, round(target_words / 800))
    elif "slow" in pace_low:
        approx = max(2, round(target_words / 1200))
    else:
        approx = max(2, round(target_words / 1000))
    return min(7, max(2, approx))

def _guess_protagonist_name(book_model: Dict[str, Any], book_summary: str) -> str:
    chars = book_model.get("characters") or {}
    # If the model provides a specific name field, prefer it; else generic.
    for key in ("protagonist_name", "main_character", "hero_name", "lead_name"):
        if key in chars and isinstance(chars[key], str) and chars[key].strip():
            return chars[key].strip()
    qa = QASession(llm_fn=llm)  # or your preferred local model
    qa.add_context("book_summary", book_summary)

    answer = qa.ask("Who is the main character in the book?")

    description = qa.ask("Describe the main character in one sentence.")

    return f'{answer.strip() or "Unnamed Protagonist"} - {description.strip() or "No description available."}'

def _scenes_from_item(
    *,
    chapter_item: Dict[str, Any],
    pov: Dict[str, Any],
    n_scenes: int,
    default_protagonist: str,
    figure_pool: List[str]
) -> List[Dict[str, Any]]:
    scenes: List[Dict[str, Any]] = []
    setting = chapter_item.get("setting") or "Primary Setting"
    figure = chapter_item.get("figure")
    if not figure and figure_pool:
        # rotate by chapter index
        idx = max(0, chapter_item.get("ch", 1) - 1) % len(figure_pool)
        figure = figure_pool[idx]

    # Use chapter-level signals across scenes
    goal = chapter_item.get("external_goal") or "Pursue objective"
    obstacle = chapter_item.get("obstacle") or "Opposition"
    turn = chapter_item.get("turn") or "New information changes the approach"
    cliff = chapter_item.get("cliffhanger") or "Unresolved beat propels forward"

    # Assign times of day by act (purely presentational; genre-agnostic)
    act_time = {"I": "day", "II": "dusk", "III": "dawn"}.get(chapter_item["act"], "day")

    for i in range(1, n_scenes + 1):
        who = [default_protagonist]
        if figure and i >= 2:
            who.append(figure)

        scenes.append({
            "scene": i,
            "location": f"{setting}" if i < n_scenes else f"{setting} – deeper/alternate angle",
            "time": act_time,
            "characters_on_stage": who,
            "objective": goal if i == 1 else f"{goal} (continued)",
            "conflict": obstacle if i < n_scenes else f"{obstacle} (heightened)",
            "escalation": "Complication emerges; resources narrow" if i < n_scenes else turn,
            "visible_solution": _visible_solution_hint(pov),
            "exit_on": cliff if i == n_scenes else "A new lead/path forces a cut",
            "objective_pov_notes": _objective_pov_note(pov)
        })
    return scenes

def _visible_solution_hint(pov: Dict[str, Any]) -> str:
    p = (pov.get("type") or "").lower()
    if "objective" in p:
        return "Progress via observable actions, dialogue, and environment cues (no inner thoughts)."
    if "first_person" in p:
        return "Progress via concrete actions and voiced intention; minimize summarizing feelings."
    return "Progress via shown behavior and externalized intention; avoid abstract telling."

def _objective_pov_note(pov: Dict[str, Any]) -> str:
    rule = (pov.get("rule") or "").strip()
    if rule:
        return rule
    p = (pov.get("type") or "").lower()
    if "objective" in p:
        return "Camera-only narration: observable action, dialogue, and sensory detail; zero interiority."
    if "limited" in p:
        return "Constrain interiority to viewpoint character; prefer sensory detail and action."
    return "Favor show-don’t-tell; keep any interiority purposeful and brief."

def _hooks_from_chapter(ch: Dict[str, Any], structure_type: str) -> Tuple[List[str], List[str], List[str]]:
    setups = [f"Establish goal: {ch.get('external_goal') or 'goal visible on-page'}"]
    payoffs = [f"Turn exploited: {ch.get('turn') or 'new info changes plan'}"]
    foreshadow = [f"Seed later beat: {ch.get('cliffhanger') or 'looming unresolved element'}"]

    st = structure_type.lower()
    if "hero" in st and ch["act"] == "III":
        payoffs.append("Return/boon echoes earlier setup")
    if "mystery" in st and ch["act"] == "II":
        setups.append("Red herring planted fairly")
        payoffs.append("Clue combination yields progress")
    if "romance" in st and ch["act"] == "II":
        foreshadow.append("Gesture/decision that will matter at reconciliation")
    return setups, payoffs, foreshadow

def _motifs_from_inputs(ch: Dict[str, Any], research: Dict[str, Any], structure_type: str) -> List[str]:
    motifs = []
    # From structure:
    if "hero" in structure_type.lower(): motifs.append("thresholds/ordeals")
    if "mystery" in structure_type.lower(): motifs.append("clues/red herrings")
    if "romance" in structure_type.lower(): motifs.append("push-pull gestures")
    if "heist" in structure_type.lower(): motifs.append("plan/ improvise beats")

    # From research setting/figure tags
    setting = (ch.get("setting") or "").lower()
    figure = (ch.get("figure") or "").lower()
    for loc in research.get("locales", []):
        n = (loc.get("name") or "").lower()
        if n and n in setting:
            motifs.extend((loc.get("tags") or [])[:2])
            break
    for fig in research.get("figures", []):
        n = (fig.get("name") or "").lower()
        if n and n in figure:
            motifs.extend((fig.get("tags") or [])[:2])
            break

    # Keep unique, short
    seen, out = set(), []
    for m in motifs:
        if not m or m in seen: 
            continue
        seen.add(m)
        out.append(m)
    return out or ["recurring images", "procedural progress"]

def _sensory_from_setting(setting: Optional[str], research: Dict[str, Any]) -> Dict[str, List[str]]:
    # Try to pull a few cues from locale snippet/tags; otherwise neutral palette.
    cues = {"sight": [], "sound": [], "smell": [], "touch": []}
    setting_low = (setting or "").lower()
    loc = None
    for l in research.get("locales", []):
        if setting_low and setting_low in (l.get("name") or "").lower():
            loc = l
            break
    # Heuristic extraction from snippet/tags
    snippet = (loc or {}).get("source_snippet") or ""
    tags = (loc or {}).get("tags") or []
    # Super-light extraction
    if snippet:
        if any(w in snippet.lower() for w in ["dark", "shadow", "glow"]): cues["sight"].append("light/shadow contrasts")
        if "water" in snippet.lower(): cues["sound"].append("running water"); cues["smell"].append("damp air")
        if "stone" in snippet.lower(): cues["touch"].append("cool stone")
        if "wood" in snippet.lower() or "tree" in snippet.lower(): cues["smell"].append("resin"); cues["touch"].append("bark texture")
    for t in tags[:3]:
        if "sound" in t.lower(): cues["sound"].append(t)
        elif "smell" in t.lower(): cues["smell"].append(t)
        elif "touch" in t.lower(): cues["touch"].append(t)
        else: cues["sight"].append(t)

    # Fallback neutral palette
    for k, v in cues.items():
        if not v:
            if k == "sight": v.extend(["landmarks", "movement cues"])
            if k == "sound": v.extend(["ambient noise", "footfalls", "voices"])
            if k == "smell": v.extend(["air quality", "nearby materials"])
            if k == "touch": v.extend(["ground texture", "temperature changes"])
    return cues

def _dialogue_cues(tone: str, pov: Dict[str, Any]) -> List[str]:
    t = (tone or "").lower()
    cues = []
    if "witty" in t:
        cues += ["snappy exchanges", "verbal play that reveals info"]
    if "somber" in t or "grim" in t:
        cues += ["sparse lines; weight carried by pauses"]
    if "romantic" in t:
        cues += ["tender/charged brevity over exposition"]
    if not cues:
        cues = ["purposeful lines that move goal/conflict forward"]
    # POV tweaks
    if "objective" in (pov.get("type") or "").lower():
        cues.append("externalized intention (spoken not thought)")
    return cues

def _style_checks_by_pov(pov: Dict[str, Any]) -> Dict[str, Any]:
    p = (pov.get("type") or "").lower()
    if "objective" in p:
        return {
            "forbid_inner_monologue_terms": ["thinks","feels","wonders","hopes","fears","realizes","decides","remembers","regrets","longs"],
            "allow_show_dont_tell_examples": [
                "show hesitation via pauses/body language",
                "show resolve via steady voice and action",
                "convey fear via physical retreat/voice changes"
            ]
        }
    if "limited" in p or "first" in p:
        return {
            "forbid_inner_monologue_terms": ["knows that everyone", "obviously", "clearly" ],  # over-telling / mind reading
            "allow_show_dont_tell_examples": [
                "interiority anchored to immediate sensation",
                "thoughts paired with observable action",
                "avoid abstract summaries of motives"
            ]
        }
    # omniscient/default
    return {
        "forbid_inner_monologue_terms": ["on the nose exposition", "as you know"],
        "allow_show_dont_tell_examples": [
            "externally verifiable details",
            "motivation implied via choices made on-page"
        ]
    }
# ---------------------------- end helpers ----------------------------
