# book_plan.py
# MusQuill.Ink — robust book planner that guarantees a full, schema-valid chapter plan
from __future__ import annotations

import json
import math
import time
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    import jsonschema  # type: ignore
except Exception:
    jsonschema = None  # validation becomes best-effort

import json
import math
import time
from copy import deepcopy
from typing import Any, Dict, List, Tuple, Optional

import requests

# ---------- CONFIG ----------

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.3:70b"
TIMEOUT_S = 120
MAX_RETRIES = 3
STRUCTURED_OK = True  # set False if your Ollama build ignores `format`

JSON_STOP_TOKENS = [
    "\n\n#", "\n\n##", "\n\n###", "\n\nAnalysis", "\n\nCritique", "\n\nExplanation"
]

# SYS = (
#     "You are a book planning engine. Output ONLY machine-readable JSON that matches the provided JSON Schema exactly. "
#     "No markdown or commentary. No extra keys. Respect const-locked fields. "
#     "Stay within the book SUMMARY boundaries; POV is objective (no inner thoughts); mild peril with visible solutions."
# )



# ----------------------------
# Tunables & global constants
# ----------------------------

DEFAULT_TOTAL_CHAPTERS = 24
ACT_CHAPTER_SPLIT = {"I": 12, "II": 9, "III": 3}  # sums to 24
ACT_WORD_SPLIT = {"I": 0.45, "II": 0.40, "III": 0.15}  # children pacing profile

MAX_RETRIES = 2
TIMEOUT_S = 180
JSON_STOP_TOKENS = ["```", "</json>", "\n\n\n"]


# --- sanitizers & backfill helpers --------------------------------------

def _strip_unknown_top_level_keys(obj: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove any top-level keys not declared in schema.properties.
    This prevents 'additionalProperties' violations caused by LLM drift.
    """
    allowed = set(schema.get("properties", {}).keys())
    return {k: v for k, v in obj.items() if k in allowed}


def _normalize_name_objects(seq: List[Any], keep: int) -> List[Dict[str, Any]]:
    """Coerce list entries into {'name': ...} dicts and de-duplicate by name."""
    out: List[Dict[str, Any]] = []
    for item in seq or []:
        if isinstance(item, dict) and "name" in item and isinstance(item["name"], str) and item["name"].strip():
            out.append({"name": item["name"].strip(), **({} if "role" not in item else {"role": item["role"]}),
                        **({} if "source_snippet" not in item else {"source_snippet": item["source_snippet"]})})
        elif isinstance(item, str) and item.strip():
            out.append({"name": item.strip()})
    # de-dup, preserve order
    seen = set()
    deduped: List[Dict[str, Any]] = []
    for d in out:
        n = d["name"]
        if n not in seen:
            seen.add(n)
            deduped.append(d)
    return deduped[:keep]


def ensure_research_selection(plan: Dict[str, Any],
                              book_model: Dict[str, Any],
                              summary_text: str) -> Dict[str, Any]:
    """
    Ensure research_selection exists and meets minItems=3 for both arrays.
    Uses canonical mythic names from book_model/summary if needed.
    """
    rs = plan.setdefault("research_selection", {})
    figs = rs.get("mythic_figures", [])
    locs = rs.get("locales", [])

    idea = _safe_get(book_model, "book.idea", "") or ""
    haystack = f"{idea}\n{summary_text}".lower()

    # Preferred mythic figures we expect to be present
    preferred_figs = [n for n in ["Baba Yaga", "Leshy", "Domovoi", "Rusalka"]
                      if n.lower() in haystack] or ["Baba Yaga", "Leshy", "Domovoi"]

    figs = _normalize_name_objects(figs, keep=999)
    for name in preferred_figs:
        if len(figs) >= 3:
            break
        if all(d["name"] != name for d in figs):
            figs.append({"name": name})

    # Locales we can safely seed
    default_locales = ["Meadow", "Forest Edge", "Enchanted Forest"]
    locs = _normalize_name_objects(locs, keep=999)
    for name in default_locales:
        if len(locs) >= 3:
            break
        if all(d["name"] != name for d in locs):
            locs.append({"name": name})

    rs["mythic_figures"] = figs[:3]
    rs["locales"] = locs[:3]
    plan["research_selection"] = rs
    return plan


# ----------------------------
# Public entry point
# ----------------------------

def plan_book(
    *,
    book_model: Dict[str, Any],
    blueprint: Dict[str, Any],
    research: Dict[str, Any],
    planning_text: str,
    summary_text: str,
    max_total_words: int = 60000,
    expected_chapters: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build a locked schema, pre-seed a full chapter skeleton (I->II->III),
    call the LLM with strict instructions, and post-enforce act coverage and
    word budgets. Returns a fully-populated, JSON-serializable dict.

    Parameters
    ----------
    chat_fn:
        Callable(messages, schema, skeleton, timeout_seconds) -> raw_model_output (str)
        Typically your `ollama_chat_strict`.
    """
    tone = _safe_get(book_model, "tone.type", default="witty")
    pace = _safe_get(book_model, "pace.type", default="fast paced")

    total_chapters = expected_chapters or DEFAULT_TOTAL_CHAPTERS
    if sum(ACT_CHAPTER_SPLIT.values()) != total_chapters:
        raise ValueError(
            f"ACT_CHAPTER_SPLIT must sum to expected chapters ({total_chapters}); "
            f"got {ACT_CHAPTER_SPLIT}"
        )

    word_targets = _compute_word_targets(max_total_words)

    base_schema = base_book_plan_schema()
    run_schema = specialize_schema(
        base_schema=base_schema,
        book_model=book_model,
        blueprint=blueprint,
        summary_text=summary_text,
        tone=tone,
        pace=pace,
        expected_chapters=total_chapters,
        locked_act_counts=ACT_CHAPTER_SPLIT,
        locked_word_targets=word_targets,
    )

    chapter_seed = build_chapter_seed(total_chapters, ACT_CHAPTER_SPLIT)
    skeleton = seed_into_skeleton(run_schema, chapter_seed)

    messages = build_prompt(
        book_model=book_model,
        blueprint=blueprint,
        research=research,
        planning_text=planning_text,
        summary_text=summary_text,
        max_total_words=max_total_words,
    )

    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = ollama_chat_strict(messages, run_schema, skeleton, TIMEOUT_S)
            obj = try_parse_json(raw)

            # 1) Strip accidental top-level extras like title/author/blueprint
            obj = _strip_unknown_top_level_keys(obj, run_schema)

            # 2) Lock constraints + canon
            obj.setdefault("constraints", {})
            obj["constraints"].setdefault("max_total_words", max_total_words)
            obj = enforce_const_locks(
                obj, book_model=book_model, blueprint=blueprint,
                summary_text=summary_text, tone=tone, pace=pace
            )

            # 3) Ensure full acts/chapters
            obj = ensure_full_acts_and_counts(
                obj, act_counts=ACT_CHAPTER_SPLIT, expected_chapters=total_chapters
            )

            # 4) Reattach pacing locks
            obj["pacing"] = {"acts": ACT_CHAPTER_SPLIT, "word_targets": word_targets}

            # 5) Backfill research_selection to meet minItems=3 each
            obj = ensure_research_selection(obj, book_model=book_model, summary_text=summary_text)

            # 6) Enforce word budgets
            obj = enforce_word_budget(obj)

            # 7) Final locks and last sanity strip (if LLM re-added junk)
            obj = enforce_const_locks(
                obj, book_model=book_model, blueprint=blueprint,
                summary_text=summary_text, tone=tone, pace=pace
            )
            obj = _strip_unknown_top_level_keys(obj, run_schema)

            # 8) Validate
            _validate_against_schema(obj, run_schema)
            return obj

        except Exception as e:
            last_err = f"Attempt {attempt} failed: {e}"
            if attempt < MAX_RETRIES:
                time.sleep(0.5)

    raise RuntimeError(f"book planning failed: {last_err}")


# ----------------------------
# Schema builders
# ----------------------------

def base_book_plan_schema() -> Dict[str, Any]:
    """
    Base JSON Schema defining the output structure.
    We add specializations (consts, lengths, contains) later.
    """
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "MusQuill Book Plan",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "constraints": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "summary": {"type": "string"},
                    "max_total_words": {"type": "integer", "minimum": 10000},
                    "pov": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "type": {"type": "string"},
                            "rule": {"type": "string"},
                        },
                        "required": ["type", "rule"],
                    },
                    "tone": {"type": "string"},
                    "pace": {"type": "string"},
                },
                "required": ["summary", "max_total_words", "pov", "tone", "pace"],
            },
            "research_selection": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "mythic_figures": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "name": {"type": "string"},
                                "role": {"type": "string"},
                                "source_snippet": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    },
                    "locales": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "name": {"type": "string"},
                                "function": {"type": "string"},
                                "source_snippet": {"type": "string"},
                            },
                            "required": ["name"],
                        },
                    },
                },
                "required": ["mythic_figures", "locales"],
            },
            "pacing": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "acts": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "I": {"type": "integer", "minimum": 1},
                            "II": {"type": "integer", "minimum": 1},
                            "III": {"type": "integer", "minimum": 1},
                        },
                        "required": ["I", "II", "III"],
                    },
                    "word_targets": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "I": {"type": "integer", "minimum": 1000},
                            "II": {"type": "integer", "minimum": 1000},
                            "III": {"type": "integer", "minimum": 1000},
                        },
                        "required": ["I", "II", "III"],
                    },
                },
                "required": ["acts", "word_targets"],
            },
            "chapter_plan": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "ch": {"type": "integer", "minimum": 1},
                        "title": {"type": "string"},
                        "act": {"type": "string", "enum": ["I", "II", "III"]},
                        "setting": {"type": "string"},
                        "figure": {"type": ["string", "null"]},
                        "external_goal": {"type": "string"},
                        "obstacle": {"type": "string"},
                        "turn": {"type": "string"},
                        "cliffhanger": {"type": "string"},
                        "word_count": {"type": "integer", "minimum": 300},
                    },
                    "required": [
                        "ch",
                        "title",
                        "act",
                        "setting",
                        "figure",
                        "external_goal",
                        "obstacle",
                        "turn",
                        "cliffhanger",
                        "word_count",
                    ],
                },
            },
            "canon": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "book_model": {"type": "object"},
                    "blueprint": {"type": "object"},
                },
                "required": ["book_model", "blueprint"],
            },
        },
        "required": ["constraints", "research_selection", "pacing", "chapter_plan", "canon"],
    }


def specialize_schema(
    *,
    base_schema: Dict[str, Any],
    book_model: Dict[str, Any],
    blueprint: Dict[str, Any],
    summary_text: str,
    tone: str,
    pace: str,
    expected_chapters: int,
    locked_act_counts: Dict[str, int],
    locked_word_targets: Dict[str, int],
) -> Dict[str, Any]:
    """Lock canon, constraints, counts, and ensure presence of all acts."""
    spec = deepcopy(base_schema)

    # Lock canon
    spec["properties"]["canon"]["properties"]["book_model"]["const"] = deepcopy(book_model)
    spec["properties"]["canon"]["properties"]["blueprint"]["const"] = deepcopy(blueprint)

    # Lock constraints
    cons = spec["properties"]["constraints"]["properties"]
    cons["summary"]["const"] = summary_text
    cons["tone"]["const"] = tone
    cons["pace"]["const"] = pace
    cons["pov"]["properties"]["type"]["const"] = "third_person_objective"
    cons["pov"]["properties"]["rule"]["const"] = "no inner thoughts; only observable actions, dialogue, and sensory details"

    # research_selection minimums (kept flexible but >0)
    rs = spec["properties"]["research_selection"]["properties"]
    rs["mythic_figures"]["minItems"] = 3
    rs["locales"]["minItems"] = 3

    # Lock pacing: chapter counts per act + word targets
    spec["properties"]["pacing"]["properties"]["acts"]["const"] = deepcopy(locked_act_counts)
    spec["properties"]["pacing"]["properties"]["word_targets"]["const"] = deepcopy(locked_word_targets)

    # Enforce exact chapter array length
    chs = spec["properties"]["chapter_plan"]
    chs["minItems"] = expected_chapters
    chs["maxItems"] = expected_chapters

    # Ensure all acts appear at least once
    spec.setdefault("allOf", [])
    spec["allOf"].extend([
        {"properties": {"chapter_plan": {"contains": {"type": "object", "properties": {"act": {"const": "I"}}}, "minContains": 1}}},
        {"properties": {"chapter_plan": {"contains": {"type": "object", "properties": {"act": {"const": "II"}}}, "minContains": 1}}},
        {"properties": {"chapter_plan": {"contains": {"type": "object", "properties": {"act": {"const": "III"}}}, "minContains": 1}}}
    ])
    return spec


# ----------------------------
# Skeleton & prompt
# ----------------------------

def _compute_word_targets(max_total_words: int) -> Dict[str, int]:
    i = int(max_total_words * ACT_WORD_SPLIT["I"])
    ii = int(max_total_words * ACT_WORD_SPLIT["II"])
    iii = max_total_words - (i + ii)
    return {"I": i, "II": ii, "III": iii}


def build_chapter_seed(expected_chapters: int,
                       act_counts: Dict[str, int]) -> List[Dict[str, Any]]:
    order = (["I"] * act_counts["I"] +
             ["II"] * act_counts["II"] +
             ["III"] * act_counts["III"])

    seed: List[Dict[str, Any]] = []
    for idx, act in enumerate(order, start=1):
        seed.append({
            "ch": idx,
            "title": "",
            "act": act,
            "setting": "",
            "figure": None,
            "external_goal": "",
            "obstacle": "",
            "turn": "",
            "cliffhanger": "",
            "word_count": 1800,  # default; we’ll re-balance later
        })
    return seed


def seed_into_skeleton(schema: Dict[str, Any],
                       chapter_seed: List[Dict[str, Any]]) -> str:
    """Create an instance skeleton string from schema and splice the chapter seed."""
    sk = json.loads(_json_skeleton(schema))
    sk["chapter_plan"] = chapter_seed
    sk["research_selection"] = {"mythic_figures": [], "locales": []}
    return json.dumps(sk, ensure_ascii=False, separators=(",", ":"))


def build_prompt(
    *,
    book_model: Dict[str, Any],
    blueprint: Dict[str, Any],
    research: Dict[str, Any],
    planning_text: str,
    summary_text: str,
    max_total_words: int,
) -> List[Dict[str, str]]:
    sys_msg = (
        "You are a planning engine for children's fiction. Output ONLY machine-readable JSON "
        "that matches the provided JSON Schema exactly. No markdown or commentary. No extra keys. "
        "Keep POV objective (no inner thoughts). Ensure age-appropriate 'mild peril' with visible solutions."
    )

    user_msg = (
        "TASK: Fill the provided JSON skeleton WITHOUT changing locked fields or array lengths.\n"
        "RULES:\n"
        "- Do NOT delete or reorder chapters. Fill EVERY chapter object.\n"
        "- `pacing.acts` are CHAPTER COUNTS (locked). `pacing.word_targets` are per-act budgets; "
        "sum chapter `word_count` per act to match budgets as closely as possible.\n"
        "- Keep POV objective; tone witty; pace fast; safety = mild peril with visible solutions.\n"
        "- Choose mythic figures/locales from RESEARCH and summarize selections in `research_selection`.\n"
        "- Stay strictly within BOOK SUMMARY boundaries; do not invent off-topic genres or settings.\n"
        "- JSON only.\n\n"
        "MATERIALS:\n"
        "== BOOK_MODEL (locked) ==\n" + json.dumps(book_model, ensure_ascii=False) + "\n\n"
        "== BLUEPRINT (locked) ==\n" + json.dumps(blueprint, ensure_ascii=False) + "\n\n"
        "== SUMMARY (locked) ==\n" + summary_text + "\n\n"
        "== HIGH-LEVEL PLAN (advisory) ==\n" + planning_text + "\n\n"
        "== RESEARCH (for selection only) ==\n" + json.dumps(research, ensure_ascii=False) + "\n\n"
        f"WORD BUDGET: max_total_words={max_total_words}\n"
        "OUTPUT: JSON only."
    )
    return [{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}]


# ----------------------------
# Enforcement & validation
# ----------------------------

def enforce_const_locks(
    obj: Dict[str, Any],
    *,
    book_model: Dict[str, Any],
    blueprint: Dict[str, Any],
    summary_text: str,
    tone: str,
    pace: str,
) -> Dict[str, Any]:
    # constraints lock
    cons = obj.setdefault("constraints", {})
    cons["summary"] = summary_text
    cons["pov"] = {
        "type": "third_person_objective",
        "rule": "no inner thoughts; only observable actions, dialogue, and sensory details",
    }
    cons["tone"] = tone
    cons["pace"] = pace

    # canon lock
    can = obj.setdefault("canon", {})
    can["book_model"] = deepcopy(book_model)
    can["blueprint"] = deepcopy(blueprint)

    return obj


def ensure_full_acts_and_counts(
    plan: Dict[str, Any],
    *,
    act_counts: Dict[str, int],
    expected_chapters: int
) -> Dict[str, Any]:
    chapters = plan.get("chapter_plan", [])
    buckets = {"I": [], "II": [], "III": []}

    for ch in chapters:
        act = ch.get("act", "I")
        if act not in buckets:
            act = "I"
        buckets[act].append(ch)

    next_ch = max([c.get("ch", 0) for c in chapters] + [0]) + 1

    def _mk_placeholder(idx: int, act: str) -> Dict[str, Any]:
        title = {
            "I": "Crossing the Birch Edge",
            "II": "Lantern-Leaf Trial",
            "III": "Stone Ford Return"
        }[act]
        return {
            "ch": idx,
            "title": title,
            "act": act,
            "setting": "Enchanted Forest",
            "figure": None,
            "external_goal": "Advance safely",
            "obstacle": "Shifting path",
            "turn": "Pattern spotted; fair trade offered",
            "cliffhanger": "New trail reveals itself",
            "word_count": 1600
        }

    # Fill each act to required count
    for act in ("I", "II", "III"):
        while len(buckets[act]) < act_counts[act]:
            buckets[act].append(_mk_placeholder(next_ch, act))
            next_ch += 1

    # Flatten in I->II->III order and renumber
    ordered = buckets["I"] + buckets["II"] + buckets["III"]
    for i, ch in enumerate(ordered, 1):
        ch["ch"] = i

    plan["chapter_plan"] = ordered[:expected_chapters]
    return plan


def enforce_word_budget(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Rebalance chapter word_counts to meet per-act targets and overall max."""
    chapters: List[Dict[str, Any]] = plan.get("chapter_plan", [])
    targets = plan.get("pacing", {}).get("word_targets", {"I": 0, "II": 0, "III": 0})

    # Split by act
    by_act: Dict[str, List[Dict[str, Any]]] = {"I": [], "II": [], "III": []}
    for ch in chapters:
        by_act.setdefault(ch.get("act", "I"), by_act["I"]).append(ch)

    for act in ("I", "II", "III"):
        bucket = by_act[act]
        if not bucket:
            continue
        target = max(int(targets.get(act, 0)), 0)
        # Current sum
        cur_sum = sum(max(int(ch.get("word_count", 0)), 0) for ch in bucket)
        if cur_sum == 0:
            # even split
            even = target // len(bucket) if bucket else 0
            for ch in bucket:
                ch["word_count"] = max(300, even)
        else:
            ratio = target / cur_sum if cur_sum > 0 else 1.0
            # Scale and round; adjust remainder to the largest chapters
            scaled = [max(300, int(round(c["word_count"] * ratio))) for c in bucket]
            diff = target - sum(scaled)
            if diff != 0:
                # distribute the difference
                # sort indices by descending current size (greedy adjust)
                order = sorted(range(len(bucket)), key=lambda i: bucket[i]["word_count"], reverse=True)
                sign = 1 if diff > 0 else -1
                for i in range(abs(diff)):
                    idx = order[i % len(order)]
                    scaled[idx] = max(300, scaled[idx] + sign)
            for ch, wc in zip(bucket, scaled):
                ch["word_count"] = wc

    plan["chapter_plan"] = by_act["I"] + by_act["II"] + by_act["III"]
    return plan


def _validate_against_schema(obj: Dict[str, Any], schema: Dict[str, Any]) -> None:
    if jsonschema is None:
        return
    jsonschema.validate(instance=obj, schema=schema)


# ----------------------------
# Utility helpers
# ----------------------------

def try_parse_json(raw: str) -> Dict[str, Any]:
    # Strip accidental pre/post text
    raw = raw.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end >= 0 and end >= start:
        raw = raw[start:end+1]
    return json.loads(raw)


def _safe_get(root: Dict[str, Any], dotted: str, default: Any = None) -> Any:
    cur: Any = root
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


# ----------------------------
# JSON skeleton generator
# ----------------------------

def _json_skeleton(schema: Dict[str, Any]) -> str:
    """
    Derive a plausible JSON instance from a JSON Schema.
    - Objects: fill required props; others omitted unless needed by our use.
    - Arrays: minItems items, with first item from item schema.
    - Strings: empty string; Integers: 0 (then adjusted by caller).
    - Enums/consts: use that exact value.
    """
    def build(node: Dict[str, Any]) -> Any:
        if "const" in node:
            return deepcopy(node["const"])
        if "enum" in node and isinstance(node["enum"], list) and node["enum"]:
            return deepcopy(node["enum"][0])

        t = node.get("type")
        if isinstance(t, list):
            # Prefer non-null type
            t = [x for x in t if x != "null"][0] if t else None

        if t == "object" or ("properties" in node):
            obj: Dict[str, Any] = {}
            props: Dict[str, Any] = node.get("properties", {})
            req = node.get("required", list(props.keys()))
            for k in req:
                obj[k] = build(props[k])
            return obj

        if t == "array":
            items_schema = node.get("items", {})
            min_items = int(node.get("minItems", 0))
            max_items = int(node.get("maxItems", min_items))
            count = max(min_items, 0)
            if max_items and max_items < count:
                count = max_items
            arr = []
            for _ in range(count):
                arr.append(build(items_schema))
            return arr

        if t == "string":
            return ""
        if t == "integer":
            return 0
        if t == "number":
            return 0.0
        if t == "boolean":
            return False
        if t == "null":
            return None

        # Fallback
        return None

    instance = build(schema)
    return json.dumps(instance, ensure_ascii=False, separators=(",", ":"))


# ---------- OLLAMA CALLS (STRICT) ----------

def _post_json(url: str, payload: Dict[str, Any], timeout: int) -> str:
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if "message" in data:
        return data.get("message", {}).get("content", "")
    if "response" in data:
        return data.get("response", "")
    return ""

def ollama_chat_strict(messages: List[Dict[str, str]],
                       run_schema: Dict[str, Any],
                       skeleton: str,
                       timeout: int = TIMEOUT_S) -> str:
    """
    (1) Try structured chat (format=run_schema).
    (2) If invalid, retry with a coercion user message including the skeleton.
    (3) Fallback to /api/generate with format='json'.
    """
    options = {"temperature": 0, "stop": JSON_STOP_TOKENS}

    if STRUCTURED_OK:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": options,
            "format": run_schema
        }
        txt = _post_json(f"{OLLAMA_URL}/api/chat", payload, timeout)
        if txt.strip().startswith("{"):
            return txt

    # Coercion with skeleton
    msgs2 = messages + [{
        "role": "user",
        "content": (
            "Return ONLY valid JSON that matches the schema. "
            "Fill this skeleton without changing locked const values:\n" + skeleton
        )
    }]
    payload2 = {
        "model": OLLAMA_MODEL,
        "messages": msgs2,
        "stream": False,
        "options": options,
        "format": run_schema if STRUCTURED_OK else "json"
    }
    txt2 = _post_json(f"{OLLAMA_URL}/api/chat", payload2, timeout)
    if txt2.strip().startswith("{"):
        return txt2

    # Fallback /api/generate
    merged_prompt = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in msgs2])
    payload3 = {
        "model": OLLAMA_MODEL,
        "prompt": merged_prompt,
        "stream": False,
        "options": options,
        "format": "json"
    }
    return _post_json(f"{OLLAMA_URL}/api/generate", payload3, timeout)
