from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


# ---------- Leaf models ----------

class POVSpec(BaseModel):
    """Point-of-view constraints."""
    model_config = ConfigDict(extra="forbid")
    type: Optional[str] = None
    rule: Optional[str] = None

    @field_validator("type", "rule")
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class SafetySpec(BaseModel):
    """Safety/content boundaries for the chapter."""
    model_config = ConfigDict(extra="forbid")
    peril_level: Optional[str] = None
    solutions_visible: Optional[bool] = None
    age_floor: Optional[int] = Field(None, ge=0)
    age_ceiling: Optional[int] = Field(None, ge=0)
    content_warnings: List[str] = Field(default_factory=list)

    @field_validator("content_warnings")
    @classmethod
    def _clean_warnings(cls, v: List[str]) -> List[str]:
        return [w.strip() for w in v if w and w.strip()]

    @model_validator(mode="after")
    def _age_bounds(self) -> "SafetySpec":
        if (
            self.age_floor is not None
            and self.age_ceiling is not None
            and self.age_floor > self.age_ceiling
        ):
            raise ValueError("age_floor cannot exceed age_ceiling.")
        return self


class Constraints(BaseModel):
    """Chapter-wide execution constraints."""
    model_config = ConfigDict(extra="forbid")
    pov: Optional[POVSpec] = None
    tone: Optional[str] = None
    pace: Optional[str] = None
    safety: Optional[SafetySpec] = None

    @field_validator("tone", "pace")
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class Meta(BaseModel):
    """Metadata describing the chapter in context of the book."""
    model_config = ConfigDict(extra="forbid")
    book_title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    theme: Optional[str] = None
    logline: Optional[str] = None
    act: Optional[str] = None  # keep free-form to allow labels like "I" or "1"
    act_description: Optional[str] = None
    chapter_number: int = Field(..., ge=1)
    chapter_title: str = Field(..., min_length=1)
    target_words: Optional[int] = Field(None, ge=1)

    @field_validator("book_title", "author", "theme", "logline", "act",
                     "act_description", "chapter_title")
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class Scene(BaseModel):
    """Atomic scene block within the chapter."""
    model_config = ConfigDict(extra="forbid")
    scene: int = Field(..., ge=1)
    location: Optional[str] = None
    time: Optional[str] = None
    characters_on_stage: List[str] = Field(default_factory=list)
    objective: Optional[str] = None
    conflict: Optional[str] = None
    escalation: Optional[str] = None
    visible_solution: Optional[str] = None
    exit_on: Optional[str] = None
    objective_pov_notes: Optional[str] = None
    thematic_element: Optional[str] = None
    chapter_beat_focus: Optional[str] = None
    act_context: Optional[str] = None

    @field_validator(
        "location", "time", "objective", "conflict", "escalation",
        "visible_solution", "exit_on", "objective_pov_notes", "thematic_element",
        "chapter_beat_focus", "act_context"
    )
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

    @field_validator("characters_on_stage")
    @classmethod
    def _clean_cast(cls, v: List[str]) -> List[str]:
        return [c.strip() for c in v if c and c.strip()]


class SensoryPalette(BaseModel):
    """Optional sensory references to anchor descriptive writing."""
    model_config = ConfigDict(extra="forbid")
    sight: List[str] = Field(default_factory=list)
    sound: List[str] = Field(default_factory=list)
    smell: List[str] = Field(default_factory=list)
    touch: List[str] = Field(default_factory=list)

    @field_validator("sight", "sound", "smell", "touch")
    @classmethod
    def _clean_lists(cls, v: List[str]) -> List[str]:
        return [x.strip() for x in v if x and x.strip()]


class StyleChecks(BaseModel):
    """House-style nudges and guardrails."""
    model_config = ConfigDict(extra="forbid")
    forbid_inner_monologue_terms: List[str] = Field(default_factory=list)
    allow_show_dont_tell_examples: List[str] = Field(default_factory=list)

    @field_validator("forbid_inner_monologue_terms", "allow_show_dont_tell_examples")
    @classmethod
    def _clean_lists(cls, v: List[str]) -> List[str]:
        return [x.strip() for x in v if x and x.strip()]


# ---------- Root model ----------

class GenericChapterBrief(BaseModel):
    """
    Content-agnostic chapter brief:
      - meta
      - constraints
      - canon_summary
      - narrative_beats[]
      - chapter_specific_beats[]
      - act_turning_points[]
      - scenes[]
      - setups[], payoffs[], foreshadowing[]
      - motifs[], act_motifs[]
      - sensory_palette
      - dialogue_cues[]
      - style_checks
    """
    model_config = ConfigDict(extra="forbid")

    meta: Meta
    constraints: Constraints = Field(default_factory=Constraints)
    canon_summary: Optional[str] = None

    narrative_beats: List[str] = Field(default_factory=list)
    chapter_specific_beats: List[str] = Field(default_factory=list)
    act_turning_points: List[str] = Field(default_factory=list)

    scenes: List[Scene] = Field(default_factory=list)

    setups: List[str] = Field(default_factory=list)
    payoffs: List[str] = Field(default_factory=list)
    foreshadowing: List[str] = Field(default_factory=list)

    motifs: List[str] = Field(default_factory=list)
    act_motifs: List[str] = Field(default_factory=list)

    sensory_palette: Optional[SensoryPalette] = None
    dialogue_cues: List[str] = Field(default_factory=list)

    style_checks: Optional[StyleChecks] = None

    # ---------- Validators ----------

    @field_validator(
        "canon_summary",
        "dialogue_cues",
        "narrative_beats",
        "chapter_specific_beats",
        "act_turning_points",
        "setups",
        "payoffs",
        "foreshadowing",
        "motifs",
        "act_motifs",
    )
    @classmethod
    def _normalize_lists_and_text(
        cls, v  # type: ignore[override]
    ):
        # For strings: strip. For lists of strings: strip each & drop empties.
        if isinstance(v, str):
            return v.strip()
        if isinstance(v, list):
            return [x.strip() for x in v if isinstance(x, str) and x.strip()]
        return v

    @model_validator(mode="after")
    def _integrity_checks(self) -> "GenericChapterBrief":
        # Require at least one high-level beat and one chapter-specific beat
        if not self.narrative_beats:
            raise ValueError("narrative_beats must contain at least one item.")
        if not self.chapter_specific_beats:
            raise ValueError("chapter_specific_beats must contain at least one item.")

        # Require at least one scene
        if not self.scenes:
            raise ValueError("scenes must contain at least one scene entry.")

        # Unique scene numbers
        s_nums = [s.scene for s in self.scenes]
        if len(s_nums) != len(set(s_nums)):
            raise ValueError("scenes contains duplicate scene numbers.")

        # Meta: basic sanity
        if self.meta.target_words is not None and self.meta.target_words < 1:
            raise ValueError("meta.target_words, if provided, must be >= 1.")

        return self

    # ---------- Convenience I/O ----------

    def to_json_dict(self) -> Dict:
        """JSON-friendly dict (exclude None values)."""
        return self.model_dump(mode="json", exclude_none=True)

    def to_json_str(self, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent, exclude_none=True)

    @classmethod
    def from_json_str(cls, text: str) -> "GenericChapterBrief":
        return cls.model_validate_json(text)
