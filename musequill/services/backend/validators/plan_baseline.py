from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set

@dataclass
class PlanBaselines:
    """
    Generic baselines the plan should respect.
    Keep this minimal and content-agnostic.
    Provide only what you care to enforce.
    """
    # Hard identity (optional; empty = skip)
    title: Optional[str] = None
    author: Optional[str] = None

    # Expectations / guardrails
    allowed_genres: Set[str] = field(default_factory=set)          # e.g., {"Romance", "Fantasy"} (empty = skip)
    disallowed_genres: Set[str] = field(default_factory=set)       # e.g., {"Thriller", "Sci-Fi"}
    required_entities: Set[str] = field(default_factory=set)       # "lockbox" names that must appear in characters OR in text
    forbidden_terms: Set[str] = field(default_factory=set)         # e.g., {"spaceship", "dragon"} if contemporary only
    require_empty_fields: Dict[Tuple[str, ...], list] = field(default_factory=dict)
    # Example: {("world_bible","soft_magic_rules"): []} if you extend your model with that field later

    # Structure/completeness heuristics
    min_characters: int = 1
    min_chapters: int = 8
    max_chapters: Optional[int] = None
    min_beats: int = 3

    # Soft expectations (scored but non-fatal)
    preferred_theme_keywords: Set[str] = field(default_factory=set)  # e.g., {"self-honesty", "obligation"}
    preferred_setting_keywords: Set[str] = field(default_factory=set) # e.g., {"New York", "NYC"}
    max_logline_chars: int = 280  # keep tight, tweet-length guidance
