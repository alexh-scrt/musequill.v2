"""
Musequill Backend Models Package.

This package contains Pydantic models for data validation and serialization
used throughout the Musequill backend services.
"""

from .book import (
    BookModelType,
    BookInfo,
    Genre,
    GenreType,
    Audience,
    Structure,
    Characters,
    Conflict,
    POV,
    Personality,
    Plot,
    Pace,
    Research,
    Technology,
    Tone,
    World,
    Style,
    create_book_model_from_json,
    validate_book_template
)

__all__ = [
    "BookModelType",
    "BookInfo",
    "Genre", 
    "GenreType",
    "Audience",
    "Structure",
    "Characters",
    "Conflict",
    "POV",
    "Personality",
    "Plot",
    "Pace",
    "Research",
    "Technology",
    "Tone",
    "World",
    "Style",
    "create_book_model_from_json",
    "validate_book_template"
]