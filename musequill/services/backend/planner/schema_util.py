import json
from copy import deepcopy
from typing import Any, Dict, List, Tuple

def _json_skeleton(schema: Dict[str, Any]) -> str:
    """
    Build a minimal JSON 'skeleton' instance for the given JSON Schema.

    Rules of thumb:
      - Objects: include ALL declared properties (required + optional), with minimal values.
      - Arrays: return [] (empty) unless 'minItems' > 0; then synthesize 1 item.
      - string/number/integer/boolean/null: minimal defaults ("", 0, 0, false, null).
      - enum/const/default/examples honored in that priority order: const > default > first enum > first example.
      - $ref is resolved from $defs/definitions within the root schema.
      - anyOf/oneOf: pick the first branch that yields a non-empty instance; else first branch.
      - allOf: merged constraints by deep-merging object properties; if conflicting, later wins.
      - Prevents infinite recursion with a visited set + depth cap.

    Returns a JSON string.
    """
    root = deepcopy(schema)
    defs = root.get("$defs") or root.get("definitions") or {}

    # For $ref resolution like "#/$defs/Thing" or "#/definitions/Thing"
    def _resolve_ref(ref: str) -> Dict[str, Any]:
        if not ref.startswith("#/"):
            # external refs not supported here; return empty object
            return {}
        parts = ref.lstrip("#/").split("/")
        cur: Dict[str, Any] = root
        for p in parts:
            if p in cur:
                cur = cur[p]
            else:
                return {}
        return cur

    def _merge_objects(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(a)
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(out.get(k), dict):
                out[k] = _merge_objects(out[k], v)
            else:
                out[k] = v
        return out

    def _first_non_none(*vals):
        for v in vals:
            if v is not None:
                return v
        return None

    # Track recursion (schema identity) to avoid cycles
    seen: set = set()
    MAX_DEPTH = 40

    def build(sch: Dict[str, Any], depth: int = 0) -> Any:
        if depth > MAX_DEPTH:
            return {}
        sid = id(sch)
        if sid in seen:
            # Break cycles gracefully
            t = sch.get("type")
            return {} if t == "object" else [] if t == "array" else None
        seen.add(sid)

        # $ref
        if "$ref" in sch:
            return build(_resolve_ref(sch["$ref"]), depth + 1)

        # allOf: merge subschemas (best-effort)
        if "allOf" in sch:
            merged: Dict[str, Any] = {}
            for sub in sch["allOf"]:
                sub_resolved = build_schema_from_branch(sub, depth + 1)
                if isinstance(sub_resolved, dict):
                    merged = _merge_objects(merged, sub_resolved)
            if merged:
                return merged
            # If not object-like, try building from merged schema shape
            tmp = {}
            for sub in sch["allOf"]:
                tmp = _merge_objects(tmp, sub if isinstance(sub, dict) else {})
            return build(tmp or {}, depth + 1)

        # anyOf / oneOf: pick first workable branch
        for key in ("anyOf", "oneOf"):
            if key in sch and isinstance(sch[key], list) and sch[key]:
                for sub in sch[key]:
                    try:
                        val = build(sub, depth + 1)
                        if val is not None:
                            return val
                    except Exception:
                        continue
                return build(sch[key][0], depth + 1)

        # const beats default/enum/examples
        if "const" in sch:
            return deepcopy(sch["const"])

        # default
        if "default" in sch:
            return deepcopy(sch["default"])

        # enum
        if "enum" in sch and isinstance(sch["enum"], list) and sch["enum"]:
            return deepcopy(sch["enum"][0])

        # examples
        if "examples" in sch and isinstance(sch["examples"], list) and sch["examples"]:
            return deepcopy(sch["examples"][0])

        # normalize type (could be list)
        t = sch.get("type")
        if isinstance(t, list):
            # choose first concrete type
            t = next((x for x in t if x in ("object", "array", "string", "number", "integer", "boolean", "null")), t[0] if t else None)

        # Object
        if t == "object" or ("properties" in sch) or ("required" in sch):
            props = sch.get("properties", {})
            required = sch.get("required", [])
            addl = sch.get("additionalProperties", False)

            result: Dict[str, Any] = {}
            # include ALL declared properties (required + optional) to preserve shape
            for name, ps in props.items():
                result[name] = build(ps, depth + 1)

            # if additionalProperties is a schema, synthesize a representative key
            if isinstance(addl, dict):
                result["additional"] = build(addl, depth + 1)

            return result

        # Array
        if t == "array" or ("items" in sch):
            min_items = int(sch.get("minItems", 0) or 0)
            items_schema = sch.get("items", {})
            if min_items <= 0:
                return []
            # synthesize at least one item to show shape
            return [build(items_schema, depth + 1)]

        # Primitive fallbacks
        if t == "string":
            return ""
        if t == "integer":
            return 0
        if t == "number":
            return 0
        if t == "boolean":
            return False
        if t == "null":
            return None

        # As a last resort, try to infer by presence of keywords
        if "properties" in sch:
            return build({"type": "object", **sch}, depth + 1)
        if "items" in sch:
            return build({"type": "array", **sch}, depth + 1)

        # Unknown: return empty object
        return {}

    def build_schema_from_branch(branch: Dict[str, Any], depth: int) -> Any:
        # helper to try building when a branch is object-shaped
        v = build(branch, depth)
        return v

    instance = build(root, 0)
    return json.dumps(instance, ensure_ascii=False, separators=(",", ":"))
