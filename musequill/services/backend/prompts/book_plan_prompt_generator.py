# book_plan_prompt_generator.py

import json
import math
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from musequill.services.backend.model.book import BookModelType


@dataclass
class BookPlanConfig:
    """Configuration for the BookPlan prompt generation."""
    model_name: str = "llama3.3:70b"
    max_context_length: int = 128000
    temperature: float = 0.7
    include_examples: bool = True
    detail_level: str = "comprehensive"  # "basic", "detailed", "comprehensive"


class BookPlanPromptGenerator:
    """
    Generates comprehensive BookPlan prompts optimized for an LLM (e.g., Ollama llama3.3:70b).
    Produces a single instruction block that demands STRICT JSON output for a high-level,
    chapter-by-chapter plan (acts -> chapters) with global scaffolding and creative constraints.
    """

    def __init__(self, config: Optional[BookPlanConfig] = None):
        self.config = config or BookPlanConfig()

    # ---------- PUBLIC API ----------

    def generate_BookPlan_prompt(self, book_model: BookModelType, book_summary: str) -> str:
        """
        Build the full prompt for the LLM to generate a high-level book plan.

        Args:
            book_model: Validated BookModelType instance
            book_summary: Rich, human-readable synopsis of the intended book

        Returns:
            Prompt string (instructions + context + JSON schema + optional examples)
        """
        # Defensive truncation for huge summaries
        summary = self._truncate(book_summary, max_chars=int(self.config.max_context_length * 0.35))

        # Extract core signals
        target_chapters, act_count, cadence = self._infer_structure(book_model)
        creative_constraints = self._creative_constraints(book_model)
        signals = self._signals_from_model(book_model)

        # Few-shot examples (kept compact to save tokens)
        examples_block = ""
        if self.config.include_examples:
            examples_block = self._few_shot_examples()

        # JSON Schema the model must follow
        schema_block = self._json_schema_block()

        # Detail level note
        detail_note = {
            "basic": "Aim for concise bullets; keep chapter beats to 2–3 items.",
            "detailed": "Provide 3–6 beats per chapter and include motifs/foreshadowing when relevant.",
            "comprehensive": "Provide 5–9 beats per chapter, plus motifs, foreshadowing, and intra-act turning points."
        }.get(self.config.detail_level, "Provide 3–6 beats per chapter and include motifs/foreshadowing when relevant.")

        # Build instruction header (clear, assertive, JSON-only)
        header = f"""You are a master story architect. Create a high-level, chapter-by-chapter BOOK PLAN as STRICT JSON.
Follow the schema exactly. Do not include any prose outside of the JSON. No preamble. No commentary.
The plan should be creative, structured, and **usable as scaffolding** for later expansion.

# MODEL & CONTEXT
Model: {self.config.model_name}
Detail level: {self.config.detail_level}
Guidance: {detail_note}

# CREATIVE CONSTRAINTS
- Honor genre, tone, POV, and conflict type.
- Maintain internal logic and continuity.
- Balance macro-structure (Acts) with micro-structure (Chapters).
- Use clear, concise, cinematic beats (not full scene prose).
- Keep names consistent with characters; introduce new names only if justified by role.
- Include subtle setups/payoffs where appropriate; avoid deus ex machina.

# OUTPUT
Return a single JSON object that validates against the schema below. Absolutely no extra text.
"""

        # Source pack
        source_pack = f"""
# SOURCE: BOOK MODEL (condensed)
{json.dumps(signals, ensure_ascii=False, indent=2)}

# SOURCE: BOOK SUMMARY (truncated if long)
\"\"\"{summary}\"\"\"

# STRUCTURE TARGETS (heuristics)
- Target chapter count (approx): {target_chapters}
- Act count: {act_count}
- Pacing cadence: {cadence}
"""

        # Task statement
        task = f"""
# TASK
Using the sources above, produce a high-level plan that:
1) Maps Acts -> Chapters with a coherent escalation of stakes and compounding consequences.
2) Encodes the book’s thematic promise and distinctive voice (via motifs and turning points), not purple prose.
3) Aligns with the audience and style declared in the model.
4) Leaves enough negative space for later scene invention (we want scaffolding, not full scenes).
"""

        # Rubric for the LLM
        rubric = """
# QUALITY RUBRIC (the plan should satisfy all)
- Cohesion: Through-lines, setups/payoffs, cause-effect clarity.
- Character: Arc beats show internal & external change.
- Stakes: Escalate meaningfully; choices carry cost.
- Rhythm: Alternating intensities (quiet build vs. kinetic release).
- Uniqueness: Fresh angle that matches genre expectations without cliché.
- Expandability: Each chapter has 3–9 crisp beats that can grow into scenes.
"""

        # Inject compact examples and schema
        prompt = (
            header
            + ("\n" + examples_block if examples_block else "")
            + "\n"
            + schema_block
            + "\n"
            + source_pack
            + "\n"
            + task
            + "\n"
            + rubric
            + "\n"
            + "# FINAL INSTRUCTIONS\n"
              "Output ONLY the JSON. Do not add markdown. Do not add explanations. "
              "Conform to the schema. Use UTF-8 characters. Keep lines under 200 characters.\n"
        )

        # Final safety trim
        return self._truncate(prompt, self.config.max_context_length)

    def save_prompt_to_file(self, prompt: str, filename: str = "book_BookPlan_prompt.txt") -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt)

    def get_prompt_stats(self, prompt: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        stats = {
            'total_characters': len(prompt),
            'total_words': len(prompt.split()),
            'total_lines': len(prompt.split('\n')),
            'estimated_tokens': int(len(prompt.split()) * 1.3),
            'recommended_model_settings': self._get_recommended_model_settings(prompt, payload)
        }
        if payload:
            stats['template_complexity_score'] = self._calculate_complexity_score(payload)
        return stats

    # ---------- SETTINGS HELPERS (already used by your code) ----------

    def _get_recommended_model_settings(self, prompt: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        estimated_tokens = len(prompt.split()) * 1.3
        complexity_score = self._calculate_complexity_score(payload) if payload else 0.5
        creativity_boost = self._calculate_creativity_boost(payload)

        settings = {
            "temperature": 0.85 + creativity_boost,
            "top_p": 0.92,
            "top_k": 50,
            "repeat_penalty": 1.05,
            "num_ctx": min(32768, int(estimated_tokens * 1.5)),
            "num_predict": 8192,
            "stop": ["# END OF PLAN", "---END---", "\n\n# FINAL", "***END***"]
        }
        genre_adjustments = self._get_genre_specific_settings(payload)
        settings.update(genre_adjustments)

        if complexity_score > 0.7:
            settings["temperature"] = min(1.2, settings["temperature"] + 0.15)
            settings["top_p"] = 0.95
            settings["top_k"] = 60
            settings["num_predict"] = 12288
        elif complexity_score < 0.3:
            settings["temperature"] = max(0.7, settings["temperature"] - 0.1)
            settings["top_p"] = 0.88
            settings["top_k"] = 35

        if self._is_children_book(payload):
            settings["temperature"] = min(1.1, settings["temperature"] + 0.1)
            settings["top_p"] = 0.96
        elif self._is_literary_fiction(payload):
            settings["temperature"] = settings["temperature"] + 0.05
            settings["top_p"] = 0.90

        if payload and len(payload) > 6:
            settings["temperature"] = min(1.15, settings["temperature"] + 0.08)
            settings["num_predict"] = max(settings["num_predict"], 10240)

        settings["temperature"] = max(0.6, min(1.3, settings["temperature"]))
        return settings

    def _calculate_creativity_boost(self, payload: Optional[Dict[str, Any]]) -> float:
        if not payload:
            return 0.0
        boost = 0.0
        if 'phase1' in payload:
            genre = payload['phase1'].get('genre', '').lower()
            creative_genres = {
                'fantasy': 0.15, 'sci-fi': 0.12, 'science fiction': 0.12,
                'magical realism': 0.18, 'surreal': 0.20, 'experimental': 0.25,
                'children': 0.10, 'adventure': 0.08, 'romance': 0.06
            }
            for g, b in creative_genres.items():
                if g in genre:
                    boost = max(boost, b)
        if 'phase3' in payload:
            world_data = payload['phase3']
            creative_elements = ['magic', 'mythology', 'supernatural', 'alternate', 'parallel']
            if any(e in str(world_data).lower() for e in creative_elements):
                boost += 0.08
        if 'phase4' in payload:
            char_data = payload['phase4']
            if 'mythology' in str(char_data).lower() or len(str(char_data)) > 200:
                boost += 0.05
        return min(0.3, boost)

    def _get_genre_specific_settings(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not payload or 'phase1' not in payload:
            return {}
        genre = payload['phase1'].get('genre', '').lower()
        if any(g in genre for g in ['fantasy', 'sci-fi', 'science fiction']):
            return {"temperature": 1.0, "top_p": 0.94, "repeat_penalty": 1.02}
        elif any(g in genre for g in ['mystery', 'thriller', 'crime']):
            return {"temperature": 0.8, "top_p": 0.87, "top_k": 45}
        elif 'romance' in genre:
            return {"temperature": 0.9, "top_p": 0.93, "repeat_penalty": 1.0}
        elif 'historical' in genre:
            return {"temperature": 0.75, "top_p": 0.89, "top_k": 40}
        return {}

    # ---------- COMPLEXITY SCORING ----------

    def _calculate_complexity_score(self, payload: Optional[Dict[str, Any]]) -> float:
        """
        Compute a 0..1 complexity score for *planning* difficulty.
        This is intentionally heuristic (and genre-aware) to help tune decoding.

        Expected payload shape (loose):
          {
            "phase1": {"genre": "...", "audience": "...", "length": "..."},
            "phase2": {"structure": "...", ...},
            "phase3": {"world": "...", "technology": "..."},
            "phase4": {"characters": {...}},
            "research": [...bool/flags...],
            ...
          }
        """
        if not payload:
            return 0.5

        score = 0.0
        # Genre & style signals
        genre = (payload.get("phase1", {}) or {}).get("genre", "").lower()
        audience = (payload.get("phase1", {}) or {}).get("audience", "").lower()
        length = (payload.get("phase1", {}) or {}).get("length", "")

        # 1) Genre complexity base
        if any(g in genre for g in ["epic", "high fantasy", "magical realism", "space opera", "hard sci", "hard sci-fi", "science fiction"]):
            score += 0.20
        if any(g in genre for g in ["mystery", "thriller", "crime", "political"]):
            score += 0.12
        if "romance" in genre:
            score += 0.08
        if "literary" in genre:
            score += 0.10

        # 2) Audience & tone constraints
        if any(kid in audience for kid in ["middle grade", "children", "ya", "young adult"]):
            # Simpler language, but structural clarity matters
            score += 0.05
        else:
            score += 0.07  # adult nuance expectations

        # 3) Length → implied chapter count
        est_ch = self._estimate_chapter_count_from_length(length)
        if est_ch >= 35:
            score += 0.12
        elif est_ch >= 25:
            score += 0.08
        elif est_ch >= 18:
            score += 0.05
        else:
            score += 0.03

        # 4) World/tech complexity
        world_blob = json.dumps(payload.get("phase3", {}), ensure_ascii=False).lower()
        if any(w in world_blob for w in ["magic", "myth", "pantheon", "parallel", "multiverse", "court", "kingdom"]):
            score += 0.12
        if any(t in world_blob for t in ["cyberpunk", "biotech", "nanotech", "time travel", "temporal", "ai alignment"]):
            score += 0.12

        # 5) Character web complexity
        chars_blob = json.dumps(payload.get("phase4", {}), ensure_ascii=False).lower()
        # Count likely named entities & roles
        approx_names = max(0, len(re.findall(r"\b[A-Z][a-z]{2,}\b", chars_blob)))
        if approx_names >= 12:
            score += 0.15
        elif approx_names >= 8:
            score += 0.10
        elif approx_names >= 5:
            score += 0.07
        else:
            score += 0.04
        if any(r in chars_blob for r in ["ensemble", "multiple pov", "multi-pov"]):
            score += 0.08

        # 6) Research demands
        research_blob = json.dumps(payload.get("research", {}), ensure_ascii=False).lower()
        if any(x in research_blob for x in ["context\": true", "requires citations", "procedural accuracy", "medical", "legal", "historical"]):
            score += 0.06

        # 7) Structure expectations
        struct = (payload.get("phase2", {}) or {}).get("structure", "").lower()
        if any(s in struct for s in ["five act", "7-point", "save the cat", "heroine", "hero's journey", "fichtean", "snowflake"]):
            score += 0.06

        # Bound 0..1
        return max(0.0, min(1.0, score))

    # ---------- INTERNAL HELPERS ----------

    def _truncate(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        safe = text[:max_chars].rsplit("\n", 1)[0]
        if not safe:
            safe = text[:max_chars]
        return safe + "\n[TRUNCATED]"

    def _signals_from_model(self, bm: BookModelType) -> Dict[str, Any]:
        """
        Condense BookModelType into a stable, model-facing dict (no giant blocks).
        """
        return {
            "book": {
                "title": bm.book.title,
                "author": bm.book.author,
                "idea": bm.book.idea,
                "type": bm.book.type,
                "length": bm.book.length,
                "language": bm.book.language,
                "bootstrap": bm.book.bootstrap or ""
            },
            "genre": {
                "primary": {"type": bm.genre.primary.type, "description": bm.genre.primary.description},
                "sub": {"type": bm.genre.sub.type, "description": bm.genre.sub.description},
            },
            "audience": {"type": bm.audience.type, "age": bm.audience.age},
            "writing_style": bm.writing_style,
            "structure": {"type": bm.structure.type, "description": bm.structure.description},
            "characters": {
                "protagonist": bm.characters.protagonist,
                "protagonists": bm.characters.protagonists,
                "narrator": bm.characters.narrator
            },
            "conflict": {"type": bm.conflict.type, "description": bm.conflict.description},
            "pov": {"type": bm.pov.type, "description": bm.pov.description},
            "personality": {"type": bm.personality.type, "description": bm.personality.description},
            "plot": {"type": bm.plot.type, "description": bm.plot.description},
            "pace": {"type": bm.pace.type, "description": bm.pace.description},
            "research": [
                {"type": r.type, "description": r.description, "context": bool(r.context)}
                for r in (bm.research or [])
            ],
            "technology": {"type": bm.technology.type, "description": bm.technology.description},
            "tone": {"type": bm.tone.type, "description": bm.tone.description},
            "world": {"type": bm.world.type, "description": bm.world.description},
            "style": {"type": bm.style.type, "description": bm.style.description},
        }

    def _estimate_chapter_count_from_length(self, length: str) -> int:
        """
        Heuristic: parse "40,000-60,000 words" → average → chapters ~ 2500-3500 words each.
        """
        nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", length)]
        if not nums:
            return 20
        if len(nums) == 1:
            words = nums[0]
        else:
            words = sum(nums) // len(nums)
        # Favor tighter chapters for commercial pacing
        per_chapter = 2800 if words >= 60000 else 2500 if words >= 45000 else 2200
        return max(12, min(48, int(round(words / per_chapter))))

    def _infer_structure(self, bm: BookModelType) -> Tuple[int, int, str]:
        """
        Decide target chapter count, act count, and pacing cadence.
        """
        tgt = self._estimate_chapter_count_from_length(bm.book.length)
        # Act count: 3 for most; allow 4 for epic/lit/complex
        genre = (bm.genre.primary.type + " " + bm.genre.sub.type).lower()
        complex_genre = any(k in genre for k in ["epic", "space opera", "literary", "political", "saga"])
        act_count = 4 if (tgt >= 32 and complex_genre) else 3

        # Cadence: blend of pace + tone
        pace = (bm.pace.type + " " + bm.pace.description).lower()
        tone = (bm.tone.type + " " + bm.tone.description).lower()
        if "fast" in pace or "propulsive" in pace:
            cadence = "fast-start, mid-gather, finale-sprint"
        elif "measured" in pace or "slow" in pace:
            cadence = "slow-burn open, rising mid, deliberate crescendo"
        else:
            cadence = "balanced open, rising mid, decisive finale"

        return tgt, act_count, cadence

    def _creative_constraints(self, bm: BookModelType) -> Dict[str, Any]:
        return {
            "genre": f"{bm.genre.primary.type} / {bm.genre.sub.type}",
            "audience": f"{bm.audience.type} ({bm.audience.age})",
            "tone": bm.tone.type,
            "pov": bm.pov.type,
            "conflict": bm.conflict.type,
        }

    # ---------- PROMPT BUILDING BLOCKS ----------

    def _json_schema_block(self) -> str:
        """
        A compact, LLM-friendly JSON schema. Strict but pragmatic for high-level planning.
        """
        schema = {
            "type": "object",
            "required": ["metadata", "global_pillars", "acts"],
            "properties": {
                "metadata": {
                    "type": "object",
                    "required": ["title", "logline", "theme", "target_chapters", "act_count", "audience_fit", "content_warnings"],
                    "properties": {
                        "title": {"type": "string"},
                        "logline": {"type": "string"},
                        "theme": {"type": "string"},
                        "target_chapters": {"type": "integer", "minimum": 10, "maximum": 60},
                        "act_count": {"type": "integer", "enum": [3, 4]},
                        "audience_fit": {"type": "string"},
                        "content_warnings": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "global_pillars": {
                    "type": "object",
                    "required": ["promise", "stakes", "arcs", "motifs", "pacing_cadence"],
                    "properties": {
                        "promise": {"type": "string"},
                        "stakes": {"type": "array", "items": {"type": "string"}},
                        "arcs": {"type": "array", "items": {"type": "string"}},
                        "motifs": {"type": "array", "items": {"type": "string"}},
                        "pacing_cadence": {"type": "string"}
                    }
                },
                "acts": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 4,
                    "items": {
                        "type": "object",
                        "required": ["act_number", "objective", "turning_points", "chapters"],
                        "properties": {
                            "act_number": {"type": "integer"},
                            "objective": {"type": "string"},
                            "turning_points": {"type": "array", "items": {"type": "string"}},
                            "chapters": {
                                "type": "array",
                                "minItems": 3,
                                "items": {
                                    "type": "object",
                                    "required": ["number", "title", "pov", "setting", "beats", "complications", "outcome", "hook"],
                                    "properties": {
                                        "number": {"type": "integer"},
                                        "title": {"type": "string"},
                                        "pov": {"type": "string"},
                                        "setting": {"type": "string"},
                                        "beats": {"type": "array", "minItems": 3, "maxItems": 9, "items": {"type": "string"}},
                                        "complications": {"type": "array", "items": {"type": "string"}},
                                        "outcome": {"type": "string"},
                                        "hook": {"type": "string"},
                                        "motifs": {"type": "array", "items": {"type": "string"}},
                                        "foreshadowing": {"type": "array", "items": {"type": "string"}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        # Present as a compact block the model can reliably read
        return "# JSON SCHEMA (enforced)\n" + json.dumps(schema, ensure_ascii=False)

    def _few_shot_examples(self) -> str:
        """
        Two ultra-compact exemplars: different genres; emphasize structure over prose.
        """
        ex1 = {
            "metadata": {
                "title": "Starwinds",
                "logline": "A courier with a forbidden AI charts a rebellion across a divided star cluster.",
                "theme": "Trust vs. control; personhood of intelligence.",
                "target_chapters": 24,
                "act_count": 3,
                "audience_fit": "Adult Sci-Fi",
                "content_warnings": ["violence"]
            },
            "global_pillars": {
                "promise": "Tense, idea-driven space intrigue with personal stakes.",
                "stakes": ["AI erasure", "civilian casualties", "loss of autonomy"],
                "arcs": ["Courier learns to trust allies", "AI claims personhood"],
                "motifs": ["stars as maps", "locked doors", "old lullaby"],
                "pacing_cadence": "fast-start, mid-gather, finale-sprint"
            },
            "acts": [
                {
                    "act_number": 1,
                    "objective": "Establish courier, AI secret, and opposing powers.",
                    "turning_points": ["AI reveals illegal upgrade", "Ambush on refuel station"],
                    "chapters": [
                        {
                            "number": 1,
                            "title": "Dead Drop at Perihelion",
                            "pov": "1st: Courier",
                            "setting": "Refuel ring over a dwarf star",
                            "beats": ["Pickup goes sideways", "AI warns of tail", "Narrow burn to escape"],
                            "complications": ["Tail knows ship signature"],
                            "outcome": "Courier commits to riskier route",
                            "hook": "Encrypted lullaby repeats in comms",
                            "motifs": ["stars as maps"],
                            "foreshadowing": ["betrayal by station chief"]
                        }
                    ]
                }
            ]
        }

        ex2 = {
            "metadata": {
                "title": "Vows in Winter",
                "logline": "Two married forty-somethings in NYC confront the price of self-honesty.",
                "theme": "Truth vs. obligation; tenderness under pressure.",
                "target_chapters": 20,
                "act_count": 3,
                "audience_fit": "Adult Romance",
                "content_warnings": ["infidelity", "alcohol use"]
            },
            "global_pillars": {
                "promise": "Witty, emotionally precise, morally complex love story.",
                "stakes": ["families' stability", "reputation", "careers"],
                "arcs": ["From self-protective banter to vulnerable choice"],
                "motifs": ["bridges", "mirrors", "coffee lids"],
                "pacing_cadence": "balanced open, rising mid, decisive finale"
            },
            "acts": [
                {
                    "act_number": 1,
                    "objective": "Meet-cute; chemistry and boundaries.",
                    "turning_points": ["ER night shift confession", "Unplanned second encounter"],
                    "chapters": [
                        {
                            "number": 1,
                            "title": "Yellow Cab Physics",
                            "pov": "Close 3rd: Noah",
                            "setting": "East 98th near Mount Sinai, NYC",
                            "beats": ["Late client call", "Jaywalk, near-miss", "Ava triages a sprain"],
                            "complications": ["Viral clip threatens reputation"],
                            "outcome": "They exchange first honest barbs",
                            "hook": "Ava’s text: 'You owe me coffee.'",
                            "motifs": ["bridges", "coffee lids"],
                            "foreshadowing": ["tabloid photographer at scene"]
                        }
                    ]
                }
            ]
        }

        return (
            "# EXAMPLES (abbreviated; format only)\n"
            + json.dumps(ex1, ensure_ascii=False)
            + "\n"
            + json.dumps(ex2, ensure_ascii=False)
            + "\n"
        )

    # ---------- SIMPLE TYPE FLAGS ----------

    def _is_children_book(self, payload: Optional[Dict[str, Any]]) -> bool:
        if not payload:
            return False
        a = (payload.get("phase1", {}) or {}).get("audience", "").lower()
        return any(k in a for k in ["children", "middle grade", "7-12", "kid", "juvenile"])

    def _is_literary_fiction(self, payload: Optional[Dict[str, Any]]) -> bool:
        if not payload:
            return False
        g = (payload.get("phase1", {}) or {}).get("genre", "").lower()
        return "literary" in g
