from __future__ import annotations
import json, os, time, logging, requests
from typing import Any, Dict, Tuple, Optional
from pydantic import ValidationError
from jsonschema import validate as js_validate, Draft202012Validator

from .book_plan import BookPlan, book_plan_json_schema
from .schema_util import _json_skeleton

log = logging.getLogger(__name__)

# ---- Runtime knobs ----
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("BOOK_PLANNER_MODEL", "llama3.3:70b")
STRUCTURED_OK = os.getenv("OLLAMA_STRUCTURED", "1") == "1"
TIMEOUT_S = int(os.getenv("OLLAMA_TIMEOUT", "240"))
MAX_RETRIES = int(os.getenv("PLANNER_MAX_RETRIES", "3"))

SYS = (
  "You are a planning engine for children's fiction. "
  "Output ONLY machine-readable JSON that matches the provided JSON Schema exactly. "
  "No markdown or commentary. No extra keys. Keep POV objective (no inner thoughts). "
  "Ensure age-appropriate 'mild peril' with visible solutions."
)

# --- at top of book_planner.py ---
JSON_STOP_TOKENS = ["\n\n#", "\n\n##", "\n\n###", "\n\nCritical", "\n\nAnalysis", "\n\nRecommendation"]

# def _json_skeleton(schema: dict) -> str:
#     """
#     Emit a minimal skeleton object with correct keys but empty values.
#     Works best if top-level is an object.
#     """
#     # Minimal hand-crafted skeleton for BookPlan: faster than deriving from schema
#     return json.dumps({
#         "project": {
#             "title": "", "author": "",
#             "audience": {"type": "children", "age": ""},
#             "length_words": "", "pov": {"type": "third_person_objective", "rule": ""},
#             "tone": "", "pace": ""
#         },
#         "logline": "",
#         "themes": [],
#         "world_bible": {"core_locales": [], "soft_magic_rules": [], "safety_dial": ""},
#         "characters": {
#             "protagonist": {"name": "", "species": "", "observable_traits": [], "skills_progression": []},
#             "mythic_figures": []
#         },
#         "hero_journey_beats": [],
#         "pacing_targets": {"act_I": {}, "act_II": {}, "act_III": {}},
#         "chapter_outline": [],
#         "setups_payoffs": [],
#         "style_guide": {
#             "voice": [], "dialogue_rules": [], "objective_pov_guardrails": []
#         },
#         "research_briefs": [],
#         "risks": [],
#         "production_notes": {"artifacts": [], "milestones": []}
#     }, ensure_ascii=False)

def _to_json_or_raise(text: str) -> dict:
    try:
        return json.loads(text.strip())
    except Exception:
        return json.loads(_extract_json(text))

def _post(url: str, payload: dict, timeout: int) -> str:
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    # /api/chat: {"message":{"content": "..."}}
    if "message" in data:
        return data.get("message", {}).get("content", "")
    # /api/generate: {"response": "...", "done": true}
    if "response" in data:
        return data.get("response", "")
    return ""

def _fewshot_assistant_example(schema: dict) -> list:
    """One assistant turn that is a tiny valid JSON, to anchor the format."""
    tiny = {
        "project": {
            "title": "T", "author": "A",
            "audience": {"type": "children", "age": "7-12"},
            "length_words": "40,000–60,000",
            "pov": {"type": "third_person_objective", "rule": "observable only"},
            "tone": "witty, warm, lightly suspenseful",
            "pace": "fast"
        },
        "logline": "L",
        "themes": ["Courage"],
        "world_bible": {"core_locales": [], "soft_magic_rules": [], "safety_dial": "mild"},
        "characters": {"protagonist": {"name": "P", "species": "bunny", "observable_traits": [], "skills_progression": []}, "mythic_figures": []},
        "hero_journey_beats": [],
        "pacing_targets": {"act_I": {}, "act_II": {}, "act_III": {}},
        "chapter_outline": [],
        "setups_payoffs": [],
        "style_guide": {"voice": [], "dialogue_rules": [], "objective_pov_guardrails": []},
        "research_briefs": [],
        "risks": [],
        "production_notes": {"artifacts": [], "milestones": []}
    }
    return [{"role": "assistant", "content": json.dumps(tiny, ensure_ascii=False)}]

def ollama_chat_strict(messages: list, schema: dict, timeout: int) -> str:
    """
    Try: (1) structured chat, (2) json-mode chat with few-shot + skeleton, (3) /api/generate.
    Enforce stops and temperature=0. Returns raw text (ideally JSON).
    """
    options = {"temperature": 0, "top_p": 0.9, "stop": JSON_STOP_TOKENS}
    # 1) Structured (if available)
    if STRUCTURED_OK:
        payload = {"model": OLLAMA_MODEL, "messages": messages, "stream": False, "options": options, "format": schema}
        txt = _post(f"{OLLAMA_URL}/api/chat", payload, timeout)
        if txt.strip().startswith("{") or txt.strip().startswith("["):
            return txt

    # 2) JSON mode with few-shot + skeleton coercion
    skeleton = _json_skeleton(schema)
    coercion = (
        "Return ONLY valid JSON matching the schema. No prose, no markdown. "
        "Fill this skeleton's keys and keep the same shape. Do not add keys.\n"
        f"SKELETON:\n{skeleton}"
    )
    msgs2 = [{"role": "system", "content": SYS}] + _fewshot_assistant_example(schema) + messages + [
        {"role": "user", "content": coercion}
    ]
    payload2 = {"model": OLLAMA_MODEL, "messages": msgs2, "stream": False, "options": options, "format": "json"}
    txt2 = _post(f"{OLLAMA_URL}/api/chat", payload2, timeout)
    if txt2.strip().startswith("{") or txt2.strip().startswith("["):
        return txt2

    # 3) /api/generate with single prompt (often stricter)
    combined = []
    for m in messages:
        combined.append(f"{m['role'].upper()}: {m['content']}")
    combined.append("USER: Return ONLY valid JSON. Fill the skeleton above. END.")
    prompt = "\n\n".join(combined) + "\n"
    payload3 = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": options,
    }
    return _post(f"{OLLAMA_URL}/api/generate", payload3, timeout)


def _extract_json(text: str) -> str:
    start = text.find("{")
    if start == -1:
        start = text.find("[")
    if start == -1:
        raise ValueError("No JSON found")
    stack = []
    for i, c in enumerate(text[start:], start):
        if c in "{[":
            stack.append(c)
        elif c in "}]":
            if not stack:
                raise ValueError("Unbalanced JSON")
            opening = stack.pop()
            if (opening, c) not in (("{", "}"), ("[", "]")):
                raise ValueError("Mismatched braces")
            if not stack:
                return text[start:i+1]
    raise ValueError("Incomplete JSON")

def _ollama_chat(messages: list, format_payload: Any) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,   # determinism matters for schema tasks
            "top_p": 0.9
        },
        "format": format_payload  # JSON Schema (preferred) or "json"
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=TIMEOUT_S)
    r.raise_for_status()
    data = r.json()
    return data.get("message", {}).get("content", "")

def _validate(obj: dict, schema: dict) -> Tuple[bool, Optional[str]]:
    try:
        Draft202012Validator.check_schema(schema)
        js_validate(instance=obj, schema=schema)
        BookPlan.model_validate(obj)  # stricter Pydantic pass
        return True, None
    except Exception as e:
        return False, str(e)

def _repair(bad_json: str, schema: dict, error: str) -> str:
    messages = [
        {"role": "system", "content": SYS},
        {"role": "user", "content":
            "Your JSON failed validation. Fix it to match this schema EXACTLY.\n\n"
            "### JSON (verbatim):\n" + bad_json + "\n\n"
            "### Validation error:\n" + error + "\n\n"
            "### JSON Schema:\n" + json.dumps(schema, ensure_ascii=False) + "\n\n"
            "Return ONLY corrected JSON. No comments."}
    ]
    return _ollama_chat(messages, schema if STRUCTURED_OK else "json")

def _build_prompt(
    book_model: Dict[str, Any],
    blueprint: Dict[str, Any],
    research: Dict[str, Any],
    planning_text: str,
    summary_text: str
) -> str:
    """
    Keep instructions short and reference the materials verbatim to reduce drift.
    We ask only for fields present in BookPlan and remind the model of guardrails.
    """
    return (
        "Create a comprehensive BOOK PLAN as a single JSON object with fields that "
        "match the provided JSON Schema (you will see it separately from the prompt).\n\n"
        "MATERIALS:\n"
        "== BOOK MODEL ==\n" + json.dumps(book_model, ensure_ascii=False) + "\n\n"
        "== BLUEPRINT ==\n" + json.dumps(blueprint, ensure_ascii=False) + "\n\n"
        "== RESEARCH (structured excerpts) ==\n" + json.dumps(research, ensure_ascii=False) + "\n\n"
        "== HIGH-LEVEL PLANNING NOTES ==\n" + planning_text + "\n\n"
        "== BOOK SUMMARY ==\n" + summary_text + "\n\n"
        "CONSTRAINTS:\n"
        "- POV: objective third person only (no inner thoughts; use observable cues).\n"
        "- Safety: mild peril with visible, age-appropriate solutions.\n"
        "- Tone: witty, warm, lightly suspenseful.\n"
        "- Keep `act` as I/II/III and `words` ranges like '1.6–2.2k'.\n"
        "- No extra keys beyond the schema."
    )

def plan_book(book_model, blueprint, research, planning_text, summary_text) -> BookPlan:
    schema = book_plan_json_schema()
    messages = [
        {"role": "system", "content": SYS},
        {"role": "user", "content": _build_prompt(book_model, blueprint, research, planning_text, summary_text)}
    ]
    attempts, last_err = 0, None
    while attempts < MAX_RETRIES:
        attempts += 1
        try:
            raw = ollama_chat_strict(messages, schema, TIMEOUT_S)

            try:
                obj = _to_json_or_raise(raw)
            except Exception:
                # Force a coercion retry once with a super-terse command
                coercion_msg = {"role": "user", "content": "Your last output was invalid. Respond with ONLY valid JSON for the schema. No text."}
                raw2 = ollama_chat_strict(messages + [coercion_msg], schema, TIMEOUT_S)
                obj = _to_json_or_raise(raw2)

            ok, err = _validate(obj, schema)
            if ok:
                return BookPlan.model_validate(obj)

            fixed_raw = _repair(json.dumps(obj, ensure_ascii=False), schema, err or "validation error")
            obj2 = _to_json_or_raise(fixed_raw)
            ok2, err2 = _validate(obj2, schema)
            if ok2:
                return BookPlan.model_validate(obj2)
            last_err = err2
        except Exception as e:
            last_err = str(e)
            log.exception("plan_book attempt %d failed: %s", attempts, e)
        time.sleep(0.6)
    raise RuntimeError(f"Book planning failed after {MAX_RETRIES} attempts: {last_err}")

