from __future__ import annotations
from typing import Dict, List, Mapping, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


# ---------- Leaf models ----------

class Character(BaseModel):
    """Generic character entry."""
    model_config = ConfigDict(extra="forbid")
    description: str = Field(..., min_length=1)
    goals: List[str] = Field(..., min_items=1)

    @field_validator("goals")
    @classmethod
    def _trim_goals(cls, v: List[str]) -> List[str]:
        return [g.strip() for g in v if g and g.strip()]


class HeroBeat(BaseModel):
    """Generic hero/journey beat—beat names are free-form strings."""
    model_config = ConfigDict(extra="forbid")
    beat: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class Chapter(BaseModel):
    """Generic chapter entry."""
    model_config = ConfigDict(extra="forbid")
    chapter: int = Field(..., ge=1)
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class ActDescription(BaseModel):
    """Free-form act or phase description (keyed by any act label)."""
    model_config = ConfigDict(extra="forbid")
    description: str = Field(..., min_length=1)


class Project(BaseModel):
    """Project metadata—fully generic content-wise."""
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    genre: str = Field(..., min_length=1)
    sub_genre: Optional[str] = Field(None)
    length: Optional[str] = Field(None)


class WorldBible(BaseModel):
    """World/setting details—fully generic."""
    model_config = ConfigDict(extra="forbid")
    setting: str = Field(..., min_length=1)
    time_period: Optional[str] = Field(None)
    technology: Optional[str] = Field(None)


class StyleGuide(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tone: Optional[str] = None
    pacing: Optional[str] = None


class PacingTargets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    word_count: Optional[str] = None
    chapter_length: Optional[str] = None


# ---------- Root model ----------

class GenericPlan(BaseModel):
    """
    Content-agnostic high-level chapter plan.
    Matches the sample shape but makes no assumptions about story content.
    """
    model_config = ConfigDict(extra="forbid")

    project: Project
    logline: str = Field(..., min_length=1)
    themes: List[str] = Field(default_factory=list)

    world_bible: WorldBible
    characters: Dict[str, Character] = Field(default_factory=dict)

    hero_journey_beats: List[HeroBeat] = Field(default_factory=list)
    chapter_outline: List[Chapter] = Field(default_factory=list)

    # Acts/phases are arbitrary keys (e.g., "act1", "act2", "setup", "payoff")
    escalation_plan: Dict[str, ActDescription] = Field(default_factory=dict)

    style_guide: StyleGuide = Field(default_factory=StyleGuide)
    pacing_targets: PacingTargets = Field(default_factory=PacingTargets)

    research_checklist: List[str] = Field(default_factory=list)
    production_notes: List[str] = Field(default_factory=list)

    # ---------- Validators ----------

    @field_validator("themes", "research_checklist", "production_notes")
    @classmethod
    def _strip_nonempty_items(cls, v: List[str]) -> List[str]:
        """Trim and drop empty items; keep list as-is if user passes empty."""
        return [item.strip() for item in v if item and item.strip()]

    @field_validator("characters")
    @classmethod
    def _nonempty_character_goals(cls, v: Dict[str, Character]) -> Dict[str, Character]:
        # Nothing content-specific; Character model already enforces nonempty goals.
        return v

    @field_validator("escalation_plan")
    @classmethod
    def _validate_escalation_plan(cls, v: Dict[str, ActDescription]) -> Dict[str, ActDescription]:
        # Allow empty dict, but if present, require non-empty descriptions (handled by ActDescription)
        return v

    @model_validator(mode="after")
    def _integrity_checks(self) -> "GenericPlan":
        # Chapters must have unique numbers
        nums = [c.chapter for c in self.chapter_outline]
        if len(nums) != len(set(nums)):
            raise ValueError("chapter_outline contains duplicate chapter numbers.")

        # Optional: ensure chapter numbers are positive and (if desired) strictly increasing
        # Commented out (generic), uncomment to enforce order:
        # if nums != sorted(nums):
        #     raise ValueError("chapter numbers must be in ascending order.")

        # Optional: minimal useful content checks (still content-agnostic)
        if not self.project.title.strip():
            raise ValueError("project.title must be non-empty.")
        if not self.characters:
            # Keep generic, but nudge toward usefulness
            raise ValueError("characters must contain at least one character entry.")

        if not self.chapter_outline:
            raise ValueError("chapter_outline must contain at least one chapter.")

        if not self.hero_journey_beats:
            # Generic requirement: at least one beat; beat names are free-form
            raise ValueError("hero_journey_beats must contain at least one beat.")

        return self
