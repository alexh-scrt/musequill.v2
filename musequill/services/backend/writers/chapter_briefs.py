# chapter_briefs.py

from typing import Any, Dict, List, Optional, Tuple
import re
from poc.qa_session import QASession
from poc.llm_ollama import llm

from musequill.services.backend.writers import (
    GenericPlan,
    Chapter,
    GenericBookPlan
)

from musequill.services.backend.model import (
    BookModelType
)

# ----------------------------
# Public API
# ----------------------------

cached_characters: Dict[str, str] = {}

def make_chapter_brief(
    *,
    book_model: BookModelType,
    book_plan: GenericBookPlan,
    book_summary: str,
    chapter: Chapter
) -> Dict[str, Any]:

    # --- Canon from book_plan metadata ---
    title = book_plan.metadata.title or book_model.book.title
    author = book_model.book.author
    structure_type = (book_model.structure.type or "Three-Act").strip()
    theme = book_plan.metadata.theme or "No theme specified"
    logline = book_plan.metadata.logline

    # --- Global constraints - prioritize book_plan over book_model ---
    pov_type = book_plan.global_settings.pov or book_model.pov.type or "third_person_objective"
    pov = {"type": pov_type, "rule": book_model.pov.description or ""}
    tone = book_plan.global_settings.tone or book_model.tone.type or "neutral"
    pace = book_model.pace.type or "medium"

    # --- Safety from audience with content warnings ---
    audience = {"type": book_model.audience.type, "age": book_model.audience.age}
    safety = _safety_profile(audience)
    if book_plan.metadata.content_warnings:
        safety["content_warnings"] = book_plan.metadata.content_warnings

    # --- Determine act for this chapter ---
    chapter_act = _determine_act_for_chapter(chapter.chapter, book_plan)
    
    # --- Extract act-specific information ---
    act_info = _get_act_info(chapter_act, book_plan)
    
    # --- Extract chapter-specific beats from book_plan ---
    chapter_beats = _get_chapter_beats(chapter.chapter, book_plan)

    # --- Create enhanced chapter_item with book_plan data ---
    chapter_item = {
        "ch": chapter.chapter,
        "title": chapter.title,
        "description": chapter.description,
        "word_count": 2500,  # Default word count
        "act": chapter_act,
        "act_description": act_info.get("description", ""),
        "act_turning_points": act_info.get("turning_points", []),
        "act_motifs": act_info.get("motifs", []),
        "chapter_beats": chapter_beats,
        "theme": theme,
        "logline": logline
    }

    # --- Narrative beats enhanced with book_plan context ---
    beats = _beats_for_structure_enhanced(structure_type, chapter_act, act_info, chapter_beats)

    # --- Scene planning with enhanced context ---
    target_words = int(chapter_item.get("word_count", 2500))
    n_scenes = _scene_count(target_words, pace)
    scenes = _scenes_from_item_enhanced(
        chapter_item=chapter_item,
        pov=pov,
        n_scenes=n_scenes,
        default_protagonist=_guess_protagonist_name(book_model, book_summary),
        figure_pool=[]
    )

    # --- Hooks & craft enhanced with chapter beats ---
    setups, payoffs, foreshadowing = _hooks_from_chapter_enhanced(chapter_item, structure_type, chapter_beats)

    # --- Motifs enhanced with act and book_plan data ---
    motifs = _motifs_from_inputs_enhanced(structure_type, act_info.get("motifs", []))
    sensory_palette = _sensory_from_setting()

    # --- Dialogue cues enhanced with tone & theme ---
    dialogue_cues = _dialogue_cues_enhanced(tone, pov, theme)

    # --- Style checks by POV ---
    style_checks = _style_checks_by_pov(pov)

    return {
        "meta": {
            "book_title": title,
            "author": author,
            "theme": theme,
            "logline": logline,
            "act": chapter_act,
            "act_description": act_info.get("description", ""),
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
        "narrative_beats": beats,
        "chapter_specific_beats": chapter_beats,
        "act_turning_points": act_info.get("turning_points", []),
        "scenes": scenes,
        "setups": setups,
        "payoffs": payoffs,
        "foreshadowing": foreshadowing,
        "motifs": motifs,
        "act_motifs": act_info.get("motifs", []),
        "sensory_palette": sensory_palette,
        "dialogue_cues": dialogue_cues,
        "style_checks": style_checks
    }


def make_all_chapter_briefs_from_plan(
    *,
    book_model: BookModelType,
    book_plan: GenericBookPlan,
    chapter_plan: GenericPlan,
    book_summary: str
) -> List[Dict[str, Any]]:
    """
    Convenience wrapper that extracts the right parts from your book_plan and
    generates briefs for every chapter_plan item.

    research_corpus can override/augment book_plan["research_selection"] with
    richer fields like role/tags/snippets.
    """

    briefs: List[Dict[str, Any]] = []
    for ch in chapter_plan.chapter_outline:
        briefs.append(
            make_chapter_brief(
                book_model=book_model,
                book_plan=book_plan,
                book_summary=book_summary,
                chapter=ch,
            )
        )
    return briefs


# ----------------------------
# Book Plan Extraction Helpers
# ----------------------------

def _determine_act_for_chapter(chapter_number: int, book_plan: GenericBookPlan) -> str:
    """Determine which act a chapter belongs to based on book_plan acts."""
    if not book_plan.acts:
        # Fallback to simple three-act division
        target_chapters = book_plan.metadata.target_chapters or 20
        if chapter_number <= target_chapters // 3:
            return "I"
        elif chapter_number <= (target_chapters * 2) // 3:
            return "II"
        else:
            return "III"
    
    # Calculate act boundaries from book_plan
    chapter_count = 0
    for act_entry in sorted(book_plan.acts, key=lambda a: a.act):
        chapter_count += act_entry.chapters or 0
        if chapter_number <= chapter_count:
            return str(act_entry.act)
    
    # Fallback to last act if chapter exceeds bounds
    return str(book_plan.acts[-1].act) if book_plan.acts else "III"

def _get_act_info(act_number: str, book_plan: GenericBookPlan) -> Dict[str, Any]:
    """Extract act-specific information from book_plan."""
    for act_entry in book_plan.acts:
        if str(act_entry.act) == str(act_number):
            return {
                "description": act_entry.description,
                "turning_points": act_entry.turning_points,
                "motifs": act_entry.motifs,
                "chapters": act_entry.chapters
            }
    return {"description": "", "turning_points": [], "motifs": [], "chapters": None}

def _get_chapter_beats(chapter_number: int, book_plan: GenericBookPlan) -> List[str]:
    """Extract chapter-specific beats from book_plan."""
    for chapter_beats in book_plan.chapter_beats:
        if chapter_beats.chapter == chapter_number:
            return chapter_beats.beats
    return []

def _beats_for_structure_enhanced(
    structure_type: str, 
    act: str, 
    act_info: Dict[str, Any], 
    chapter_beats: List[str]
) -> List[str]:
    """Enhanced beats that incorporate book_plan context."""
    # Get base structure beats
    base_beats = _beats_for_structure(structure_type, act)
    
    # Enhance with act-specific context
    enhanced_beats = []
    act_description = act_info.get("description", "")
    
    for beat in base_beats:
        if act_description:
            enhanced_beat = f"{beat} (Act context: {act_description})"
        else:
            enhanced_beat = beat
        enhanced_beats.append(enhanced_beat)
    
    # Add chapter-specific beats if available
    if chapter_beats:
        enhanced_beats.extend([f"Chapter beat: {beat}" for beat in chapter_beats])
    
    return enhanced_beats

def _scenes_from_item_enhanced(
    *,
    chapter_item: Dict[str, Any],
    pov: Dict[str, Any],
    n_scenes: int,
    default_protagonist: str,
    figure_pool: List[str]
) -> List[Dict[str, Any]]:
    """Enhanced scene planning with book_plan context."""
    # Start with base scene structure
    scenes = _scenes_from_item(
        chapter_item=chapter_item,
        pov=pov,
        n_scenes=n_scenes,
        default_protagonist=default_protagonist,
        figure_pool=figure_pool
    )
    
    # Enhance each scene with book_plan context
    chapter_beats = chapter_item.get("chapter_beats", [])
    act_turning_points = chapter_item.get("act_turning_points", [])
    theme = chapter_item.get("theme", "")
    
    for i, scene in enumerate(scenes):
        # Add thematic elements
        if theme:
            scene["thematic_element"] = f"Reinforce theme: {theme}"
        
        # Add chapter beat context to scenes
        if chapter_beats and i < len(chapter_beats):
            scene["chapter_beat_focus"] = chapter_beats[i]
        
        # Add act turning point awareness
        if act_turning_points:
            scene["act_context"] = f"Act turning points: {', '.join(act_turning_points)}"
    
    return scenes

def _hooks_from_chapter_enhanced(
    chapter_item: Dict[str, Any], 
    structure_type: str, 
    chapter_beats: List[str]
) -> Tuple[List[str], List[str], List[str]]:
    """Enhanced hooks incorporating chapter beats."""
    # Get base hooks
    setups, payoffs, foreshadow = _hooks_from_chapter(chapter_item, structure_type)
    
    # Enhance with chapter beats
    if chapter_beats:
        for beat in chapter_beats:
            setups.append(f"Chapter beat setup: {beat}")
            # Create payoff implications from beats
            if any(keyword in beat.lower() for keyword in ["reveal", "discover", "learn"]):
                payoffs.append(f"Beat payoff: Information from '{beat}' affects future decisions")
            if any(keyword in beat.lower() for keyword in ["tension", "conflict", "problem"]):
                foreshadow.append(f"Beat foreshadowing: '{beat}' hints at larger complications")
    
    return setups, payoffs, foreshadow

def _motifs_from_inputs_enhanced(structure_type: str, act_motifs: List[str]) -> List[str]:
    """Enhanced motifs that include act-specific motifs from book_plan."""
    # Get base motifs from structure
    base_motifs = _motifs_from_inputs(structure_type)
    
    # Add act-specific motifs
    enhanced_motifs = base_motifs.copy()
    enhanced_motifs.extend(act_motifs)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_motifs = []
    for motif in enhanced_motifs:
        if motif not in seen:
            seen.add(motif)
            unique_motifs.append(motif)
    
    return unique_motifs or ["recurring images", "procedural progress"]

def _dialogue_cues_enhanced(tone: str, pov: Dict[str, Any], theme: str) -> List[str]:
    """Enhanced dialogue cues that incorporate theme."""
    # Get base dialogue cues
    base_cues = _dialogue_cues(tone, pov)
    
    # Add theme-aware dialogue suggestions
    enhanced_cues = base_cues.copy()
    if theme:
        enhanced_cues.append(f"Echo theme through character choices: {theme}")
        enhanced_cues.append(f"Subtext should reflect thematic tension: {theme}")
    
    return enhanced_cues

# ----------------------------
# Helpers (generic, no book-specific content)
# ----------------------------

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

def _guess_protagonist_name(book_model: BookModelType, book_summary: str) -> str:
    # Try to get protagonist name from book model
    if hasattr(book_model.characters, 'protagonist') and book_model.characters.protagonist.strip():
        return book_model.characters.protagonist.strip()
    
    # Use QA session to extract from book summary if available
    qa = QASession(llm_fn=llm)
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

def _motifs_from_inputs(structure_type: str) -> List[str]:
    motifs = []
    # From structure:
    if "hero" in structure_type.lower(): motifs.append("thresholds/ordeals")
    if "mystery" in structure_type.lower(): motifs.append("clues/red herrings")
    if "romance" in structure_type.lower(): motifs.append("push-pull gestures")
    if "heist" in structure_type.lower(): motifs.append("plan/ improvise beats")

    # Keep unique, short
    seen, out = set(), []
    for m in motifs:
        if not m or m in seen: 
            continue
        seen.add(m)
        out.append(m)
    return out or ["recurring images", "procedural progress"]

def _sensory_from_setting() -> Dict[str, List[str]]:
    # Generate generic sensory palette without research data
    cues = {"sight": [], "sound": [], "smell": [], "touch": []}
    
    # Default neutral palette
    cues["sight"].extend(["landmarks", "movement cues"])
    cues["sound"].extend(["ambient noise", "footfalls", "voices"])
    cues["smell"].extend(["air quality", "nearby materials"])
    cues["touch"].extend(["ground texture", "temperature changes"])
    
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
