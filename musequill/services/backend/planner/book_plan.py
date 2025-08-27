from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

Act = Literal["I", "II", "III"]

class Audience(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    type: Literal["children", "young_adult", "adult"]
    age: Optional[str] = Field(None, description="e.g. '7-12'")

class POV(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    type: Literal["first_person", "third_person_limited", "third_person_objective", "omniscient"]
    rule: Optional[str] = None

class Project(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    title: str
    author: str
    audience: Audience
    length_words: Optional[str] = Field(None, description="e.g. '40,000–60,000'")
    pov: POV
    tone: str
    pace: str

class Locale(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    function: str
    visuals: List[str]

class WorldBible(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    core_locales: List[Locale] = Field(default_factory=list)
    soft_magic_rules: List[str] = Field(default_factory=list)
    safety_dial: Optional[str] = None

class MythicFigure(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    role: str
    observable_traits: List[str] = Field(default_factory=list)
    teaches: Optional[str] = None

class Protagonist(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    species: Optional[str] = None
    observable_traits: List[str] = Field(default_factory=list)
    skills_progression: List[str] = Field(default_factory=list)

class CharacterSet(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    protagonist: Protagonist
    mythic_figures: List[MythicFigure] = Field(default_factory=list)

class Beat(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    stage: str
    summary: str
    target_chapters: str  # e.g., "5–12" or "3"

class PacingTargets(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    act_I: dict
    act_II: dict
    act_III: dict

class ChapterItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    ch: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=160)
    act: Act
    setting: str
    figure: Optional[str] = None
    external_goal: str
    obstacle: str
    turn: str
    cliffhanger: str
    words: str = Field(..., pattern=r"^\d+(\.\d+)?–\d+(\.\d+)?k$")  # e.g. "1.6–2.2k"

class SetupPayoff(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    setup: str
    payoff: str

class ResearchBrief(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    topic: str
    notes: List[str] = Field(default_factory=list)
    child_safe_filtering_notes: Optional[str] = None

class RiskItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    risk: str
    impact: Literal["low", "medium", "high"]
    mitigation: str

class StyleGuide(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    voice: List[str] = Field(default_factory=list)
    dialogue_rules: List[str] = Field(default_factory=list)
    objective_pov_guardrails: List[str] = Field(default_factory=list)

class ProductionNotes(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    artifacts: List[str] = Field(default_factory=list)
    milestones: List[str] = Field(default_factory=list)

class BookPlan(BaseModel):
    """
    SINGLE source of truth for the planning contract.
    """
    model_config = ConfigDict(extra="forbid", strict=True)

    project: Project
    logline: str
    themes: List[str]
    world_bible: WorldBible
    characters: CharacterSet
    hero_journey_beats: List[Beat]
    pacing_targets: PacingTargets

    # The actionable outputs that downstream steps depend on:
    chapter_outline: List[ChapterItem] = Field(..., min_items=12, max_items=60)
    setups_payoffs: List[SetupPayoff] = Field(default_factory=list)

    # Ops/guardrails/enablement:
    style_guide: StyleGuide
    research_briefs: List[ResearchBrief] = Field(default_factory=list)
    risks: List[RiskItem] = Field(default_factory=list)
    production_notes: ProductionNotes

def book_plan_json_schema() -> dict:
    return BookPlan.model_json_schema()
