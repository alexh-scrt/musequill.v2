#!/usr/bin/env python3
"""
Chapter Planning Schema and Models

Defines Pydantic models for high-level chapter planning output schema.
This creates a structured format for LLM-generated chapter plans.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum


class ActType(str, Enum):
    """Story act classification."""
    I = "I"
    II = "II" 
    III = "III"


class LocaleFunction(str, Enum):
    """Function of story locations."""
    ORDINARY_WORLD = "ordinary world"
    THRESHOLD = "threshold"
    TRIAL_MENTOR_SITE = "trial/mentor site"
    ALLY_REFUGE = "ally refuge"
    TEMPTATION_TEST = "temptation/test"
    ORDEAL = "ordeal"
    RETURN_THRESHOLD = "return threshold"
    RETURN_POINT = "return point"


class HeroJourneyStage(str, Enum):
    """Campbell's Hero's Journey stages."""
    ORDINARY_WORLD = "Ordinary World"
    CALL_TO_ADVENTURE = "Call to Adventure"
    REFUSAL_OF_CALL = "Refusal of the Call"
    MEETING_MENTOR = "Meeting the Mentor"
    CROSSING_THRESHOLD = "Crossing the Threshold"
    TESTS_ALLIES_ENEMIES = "Tests, Allies, Enemies"
    APPROACH_INMOST_CAVE = "Approach to the Inmost Cave"
    ORDEAL = "Ordeal"
    REWARD = "Reward (Seizing the Sword)"
    ROAD_BACK = "The Road Back"
    RESURRECTION = "Resurrection"
    RETURN_ELIXIR = "Return with the Elixir"


class ProjectMetadata(BaseModel):
    """Core project information."""
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author name")
    audience: Dict[str, str] = Field(..., description="Target audience type and age range")
    length_words: str = Field(..., description="Target word count range")
    pov: Dict[str, str] = Field(..., description="Point of view type and narrative rules")
    tone: str = Field(..., description="Overall tone of the story")
    pace: str = Field(..., description="Story pacing style")


class CoreLocale(BaseModel):
    """Story location with function and visual elements."""
    name: str = Field(..., description="Location name")
    function: str = Field(..., description="Narrative function in story")
    visuals: List[str] = Field(..., description="Key visual elements and atmosphere")


class MagicRule(BaseModel):
    """Soft magic system rule."""
    rule: str = Field(..., description="A rule governing how magic works in the world")


class WorldBible(BaseModel):
    """Complete world building reference."""
    core_locales: List[CoreLocale] = Field(..., description="Primary story locations")
    soft_magic_rules: List[str] = Field(..., description="Rules governing magic system")
    safety_dial: str = Field(..., description="Content safety guidelines")


class CharacterTraits(BaseModel):
    """Observable character traits and progression."""
    name: str = Field(..., description="Character name")
    species: Optional[str] = Field(None, description="Character species if non-human")
    observable_traits: List[str] = Field(..., description="Externally observable characteristics")
    skills_progression: Optional[List[str]] = Field(None, description="Skills developed over story")
    role: Optional[str] = Field(None, description="Character role in story")
    teaches: Optional[str] = Field(None, description="What this character teaches protagonist")


class Characters(BaseModel):
    """Complete character roster."""
    protagonist: CharacterTraits = Field(..., description="Main character details")
    mythic_figures: List[CharacterTraits] = Field(..., description="Mythological/magical characters")
    meadow_cast: Optional[List[CharacterTraits]] = Field(None, description="Supporting cast")


class HeroJourneyBeat(BaseModel):
    """Hero's Journey story beat."""
    stage: HeroJourneyStage = Field(..., description="Hero's journey stage")
    summary: str = Field(..., description="What happens in this stage")
    target_chapters: str = Field(..., description="Which chapters cover this beat")


class ChapterOutline(BaseModel):
    """Detailed chapter structure."""
    ch: int = Field(..., description="Chapter number")
    title: str = Field(..., description="Chapter title")
    act: ActType = Field(..., description="Story act (I, II, III)")
    setting: str = Field(..., description="Primary location")
    figure: Optional[str] = Field(None, description="Key character featured")
    external_goal: str = Field(..., description="Character's external objective")
    obstacle: str = Field(..., description="What prevents achieving the goal")
    turn: str = Field(..., description="Key plot turn or revelation")
    cliffhanger: str = Field(..., description="Chapter ending hook")
    words: str = Field(..., description="Target word count range")


class SetupPayoff(BaseModel):
    """Story element setup and payoff tracking."""
    setup: str = Field(..., description="Element introduced early")
    payoff: str = Field(..., description="How the element pays off later")


class EscalationPlan(BaseModel):
    """Story escalation and narrative structure."""
    stakes_progression: List[str] = Field(..., description="How stakes escalate")
    setups_payoffs: List[SetupPayoff] = Field(..., description="Story element callbacks")


class StyleGuide(BaseModel):
    """Writing style guidelines."""
    voice: List[str] = Field(..., description="Narrative voice guidelines")
    dialogue_rules: List[str] = Field(..., description="Dialogue writing rules")
    objective_pov_guardrails: List[str] = Field(..., description="POV restriction guidelines")


class ActPacing(BaseModel):
    """Pacing targets for story acts."""
    chapters: str = Field(..., description="Chapter range")
    words_total: str = Field(..., description="Total word count target")


class PacingTargets(BaseModel):
    """Complete story pacing structure."""
    act_I: ActPacing = Field(..., description="Act I pacing")
    act_II: ActPacing = Field(..., description="Act II pacing") 
    act_III: ActPacing = Field(..., description="Act III pacing")


class HighLevelChapterPlan(BaseModel):
    """Complete high-level chapter planning structure."""
    
    # Core project info
    project: ProjectMetadata = Field(..., description="Project metadata and parameters")
    logline: str = Field(..., description="One-sentence story summary")
    themes: List[str] = Field(..., description="Core story themes")
    
    # World building
    world_bible: WorldBible = Field(..., description="Complete world reference")
    characters: Characters = Field(..., description="Character roster and details")
    
    # Story structure
    hero_journey_beats: List[HeroJourneyBeat] = Field(..., description="Hero's journey breakdown")
    chapter_outline: List[ChapterOutline] = Field(..., description="Detailed chapter plans")
    escalation_plan: EscalationPlan = Field(..., description="Story escalation structure")
    
    # Writing guidelines
    style_guide: StyleGuide = Field(..., description="Writing style guidelines")
    pacing_targets: PacingTargets = Field(..., description="Pacing and word count targets")
    
    # Production support
    research_checklist: List[str] = Field(..., description="Research requirements")
    production_notes: List[str] = Field(..., description="Production and formatting notes")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        extra = "ignore"
        validate_assignment = True


# JSON Schema export for LLM prompts
CHAPTER_PLANNING_SCHEMA = HighLevelChapterPlan.model_json_schema()

# Example output structure for LLM reference
EXAMPLE_CHAPTER_PLAN = {
  "project": {
    "title": "Hearts on Margin",
    "author": "Alex Hart",
    "audience": {"type": "adults", "age": "35-60"},
    "length_words": "40,000-60,000",
    "pov": {"type": "third person limited (alternating)", "rule": "No head-hopping; chapter POV alternates between Noah and Ava."},
    "tone": "witty, emotionally nuanced",
    "pace": "slow burn with brisk banter"
  },
  "logline": "A Goldman Sachs trader and a Mount Sinai anesthesiologist fall into a forbidden connection and must decide between preservation and reinvention.",
  "themes": ["Self-honesty vs obligation", "Reputation vs desire", "Family, cost, and reinvention"],
  "world_bible": {
    "core_locales": [
      {"name": "Mount Sinai OR suite", "function": "ordinary world", "visuals": ["bright fluorescent light", "blue caps", "pre-op monitors"]},
      {"name": "Goldman Sachs trading floor", "function": "trial/mentor site", "visuals": ["order books", "risk screens", "compliance corridor"]},
      {"name": "Central Park (Bethesda Terrace)", "function": "ally refuge", "visuals": ["stone arcade", "fountain", "buskers"]}
    ],
    "soft_magic_rules": [],
    "safety_dial": "mature themes (infidelity), no graphic content"
  },
  "characters": {
    "protagonist": {
      "name": "Noah Bennett",
      "species": "",
      "observable_traits": ["witty under pressure", "risk-calibrated", "emotionally guarded"],
      "skills_progression": ["honest communication", "boundary-setting"],
      "role": "co-protagonist",
      "teaches": "Timing matters, but courage costs"
    },
    "mythic_figures": [],
    "meadow_cast": [
      {
        "name": "Dr. Ava Kline",
        "species": "",
        "observable_traits": ["clinical calm", "compassionate", "guarded"],
        "skills_progression": ["self-advocacy", "prioritizing self-honesty"],
        "role": "co-protagonist",
        "teaches": "Care includes oneself"
      }
    ]
  },
  "hero_journey_beats": [
    {"stage": "Ordinary World", "summary": "Noah on the trading floor; Ava in OR pre-op; both competent and lonely in motion.", "target_chapters": "1-2"}
  ],
  "chapter_outline": [
    {
      "ch": 1,
      "title": "Impact and Intake",
      "act": "I",
      "setting": "Mount Sinai ER",
      "figure": "Dr. Ava Kline",
      "external_goal": "Noah seeks to get cleared and make his client meeting",
      "obstacle": "Pain, imaging delays, hospital protocol",
      "turn": "Ava intubates a different case; Noah sees her poise",
      "cliffhanger": "Noah jokes; Ava deflects; unexpected warmth",
      "words": "1.8–2.4k"
    }
  ],
  "escalation_plan": {
    "stakes_progression": [
      "Private messages → risk at work → suspicion at home → public proximity at gala → press risk"
    ],
    "setups_payoffs": [
      {"setup": "Encrypted messaging discipline", "payoff": "Paper trail nearly exposes them"},
      {"setup": "Ava’s ‘no personal entanglements’ rule", "payoff": "She chooses to break it, then owns it"}
    ]
  },
  "style_guide": {
    "voice": [
      "Conversational third limited with crisp scene work and banter",
      "Use concrete NYC sensory detail as subtext"
    ],
    "dialogue_rules": [
      "Witty, short beats; subtext over exposition",
      "No info-dumps; reveal professions via action"
    ],
    "objective_pov_guardrails": [
      "One close POV per chapter (Noah or Ava)",
      "Scene transitions required on POV change"
    ]
  },
  "pacing_targets": {
    "act_I": {"chapters": "1–6", "words_total": "12–18k"},
    "act_II": {"chapters": "7–14", "words_total": "18–28k"},
    "act_III": {"chapters": "15–20", "words_total": "10–14k"}
  },
  "research_checklist": [
    "Mount Sinai perioperative flow for same-day trauma",
    "GS risk, compliance, and personal device rules",
    "NY family law: adultery, custody optics, prenup contours"
  ],
  "production_notes": [
    "Alternate POV strictly; title each chapter with setting to keep NYC texture",
    "No slang contractions in strings (schema requirement)"
  ]
}
