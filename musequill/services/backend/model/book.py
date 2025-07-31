"""
Pydantic models for book templates and story generation.

This module defines the data structures used to represent book templates
and their various components like genre, audience, structure, etc.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class BookInfo(BaseModel):
    """Information about the book itself."""
    title: str
    author: str
    idea: str
    type: str
    length: str
    language: str


class GenreType(BaseModel):
    """Genre classification with type and description."""
    type: str
    description: str


class Genre(BaseModel):
    """Primary and sub-genre classifications."""
    primary: GenreType
    sub: GenreType


class Audience(BaseModel):
    """Target audience information."""
    type: str
    age: str


class Structure(BaseModel):
    """Story structure information."""
    type: str
    description: str


class Characters(BaseModel):
    """Character role definitions."""
    protagonist: str
    narrator: str


class Conflict(BaseModel):
    """Type of conflict in the story."""
    type: str
    description: str


class POV(BaseModel):
    """Point of view narrative style."""
    type: str
    description: str


class Personality(BaseModel):
    """Protagonist personality traits."""
    type: str
    description: str


class Plot(BaseModel):
    """Plot structure and type."""
    type: str
    description: str


class Pace(BaseModel):
    """Story pacing information."""
    type: str
    description: str


class Research(BaseModel):
    """Research requirements for the story."""
    type: str
    description: str
    context: bool


class Technology(BaseModel):
    """Technological setting/era."""
    type: str
    description: str


class Tone(BaseModel):
    """Story tone and mood."""
    type: str
    description: str


class World(BaseModel):
    """World-building and setting type."""
    type: str
    description: str


class Style(BaseModel):
    """Writing style characteristics."""
    type: str
    description: str


class BookModelType(BaseModel):
    """
    Complete book template model containing all story elements.
    
    This is the main model that encapsulates all aspects of a book template
    including plot, characters, genre, audience, and stylistic elements.
    """
    book: BookInfo
    genre: Genre
    audience: Audience
    writing_style: str
    structure: Structure
    characters: Characters
    conflict: Conflict
    pov: POV
    personality: Personality
    plot: Plot
    pace: Pace
    research: List[Research]
    technology: Technology
    tone: Tone
    world: World
    style: Style

    class Config:
        """Pydantic configuration."""
        # Allow field names to use underscores while JSON uses underscores
        allow_population_by_field_name = True
        # Validate assignment to ensure data integrity
        validate_assignment = True
        # Allow extra fields (for future extensibility)
        extra = "forbid"
    
    def get_summary(self) -> str:
        """
        Get a brief summary of the book template.
        
        Returns:
            A formatted string summarizing key aspects of the book.
        """
        return (
            f"{self.book.title} by {self.book.author}\n"
            f"Genre: {self.genre.primary.type} / {self.genre.sub.type}\n"
            f"Audience: {self.audience.type} ({self.audience.age})\n"
            f"Length: {self.book.length}\n"
            f"Structure: {self.structure.type}\n"
            f"Tone: {self.tone.type}, Pace: {self.pace.type}\n"
            f"World: {self.world.type}"
        )
    
    def get_writing_guidelines(self) -> dict:
        """
        Extract writing guidelines from the template.
        
        Returns:
            Dictionary containing key writing guidelines.
        """
        return {
            "writing_style": self.writing_style,
            "pov": self.pov.type,
            "tone": self.tone.type,
            "pace": self.pace.type,
            "style": self.style.type,
            "target_length": self.book.length,
            "language": self.book.language
        }
    
    def get_story_elements(self) -> dict:
        """
        Extract core story elements from the template.
        
        Returns:
            Dictionary containing key story elements.
        """
        return {
            "plot_type": self.plot.type,
            "conflict_type": self.conflict.type,
            "structure": self.structure.type,
            "world_type": self.world.type,
            "technology_era": self.technology.type,
            "protagonist_personality": self.personality.type
        }


# Utility functions for working with BookModelType

def create_book_model_from_json(json_data: dict) -> BookModelType:
    """
    Create a BookModelType instance from JSON data.
    
    Args:
        json_data: Dictionary containing the book template data
        
    Returns:
        BookModelType instance
        
    Raises:
        ValidationError: If the JSON data doesn't match the expected structure
    """
    return BookModelType(**json_data)


def validate_book_template(template_data: dict) -> tuple[bool, str]:
    """
    Validate a book template against the BookModelType schema.
    
    Args:
        template_data: Dictionary containing template data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        BookModelType(**template_data)
        return True, "Template is valid"
    except Exception as e:
        return False, str(e)