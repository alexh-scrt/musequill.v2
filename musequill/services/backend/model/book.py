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
    bootstrap: Optional[str]


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
    protagonists: List[str]
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
    
    def to_markdown(self) -> str:
        """Render a nicely structured Markdown view of the book. Skips null/empty values."""

        def _has(val) -> bool:
            if val is None:
                return False
            if isinstance(val, str):
                return val.strip() != ""
            if isinstance(val, (list, tuple, set)):
                return any(_has(x) for x in val)
            if isinstance(val, dict):
                return any(_has(v) for v in val.values())
            return True

        def _kv(label: str, value: str, indent: int = 0) -> str:
            """Key–value bullet line if value present."""
            if not _has(value):
                return ""
            return f'{" " * indent}- **{label}:** {value}'

        def _section(title: str) -> str:
            return f"\n## {title}\n"

        lines = []

        # Title & Author
        if _has(self.book.title):
            lines.append(f"# {self.book.title}")
        if _has(self.book.author):
            lines.append(f"**Author:** {self.book.author}")

        # Book basics
        lines.append(_section("Book"))
        if _has(self.book.idea):
            lines.append(_kv("Idea", self.book.idea))
        if _has(self.book.type):
            lines.append(_kv("Type", self.book.type))
        if _has(self.book.length):
            lines.append(_kv("Length", self.book.length))
        if _has(self.book.language):
            lines.append(_kv("Language", self.book.language))
        if _has(self.writing_style):
            lines.append(_kv("Writing Style", self.writing_style))

        # Optional bootstrap as blockquote
        if _has(self.book.bootstrap):
            lines.append("\n### Bootstrap\n")
            lines.append("> " + self.book.bootstrap.replace("\n", "\n> "))

        # Genre
        lines.append(_section("Genre"))
        if _has(self.genre.primary.type) or _has(self.genre.primary.description):
            primary = self.genre.primary.type
            if _has(self.genre.primary.description):
                primary = f"{primary} — {self.genre.primary.description}" if _has(primary) else self.genre.primary.description
            lines.append(_kv("Primary", primary))
        if _has(self.genre.sub.type) or _has(self.genre.sub.description):
            sub = self.genre.sub.type
            if _has(self.genre.sub.description):
                sub = f"{sub} — {self.genre.sub.description}" if _has(sub) else self.genre.sub.description
            lines.append(_kv("Sub-genre", sub))

        # Audience
        lines.append(_section("Audience"))
        if _has(self.audience.type):
            lines.append(_kv("Type", self.audience.type))
        if _has(self.audience.age):
            lines.append(_kv("Age", self.audience.age))

        # Structure
        lines.append(_section("Structure"))
        if _has(self.structure.type):
            lines.append(_kv("Type", self.structure.type))
        if _has(self.structure.description):
            lines.append(_kv("Description", self.structure.description))

        # Characters
        lines.append(_section("Characters"))
        if _has(self.characters.protagonist):
            lines.append(_kv("Protagonist", self.characters.protagonist))
        if _has(self.characters.protagonists):
            lines.append("- **Protagonists:**")
            for p in self.characters.protagonists:
                if _has(p):
                    lines.append(f"  - {p}")
        if _has(self.characters.narrator):
            lines.append(_kv("Narrator", self.characters.narrator))

        # Conflict
        lines.append(_section("Conflict"))
        if _has(self.conflict.type):
            lines.append(_kv("Type", self.conflict.type))
        if _has(self.conflict.description):
            lines.append(_kv("Description", self.conflict.description))

        # POV
        lines.append(_section("Point of View"))
        if _has(self.pov.type):
            lines.append(_kv("Type", self.pov.type))
        if _has(self.pov.description):
            lines.append(_kv("Description", self.pov.description))

        # Personality
        lines.append(_section("Protagonist Personality"))
        if _has(self.personality.type):
            lines.append(_kv("Type", self.personality.type))
        if _has(self.personality.description):
            lines.append(_kv("Description", self.personality.description))

        # Plot
        lines.append(_section("Plot"))
        if _has(self.plot.type):
            lines.append(_kv("Type", self.plot.type))
        if _has(self.plot.description):
            lines.append(_kv("Description", self.plot.description))

        # Pace
        lines.append(_section("Pace"))
        if _has(self.pace.type):
            lines.append(_kv("Type", self.pace.type))
        if _has(self.pace.description):
            lines.append(_kv("Description", self.pace.description))

        # Research
        if _has(self.research):
            lines.append(_section("Research"))
            for r in self.research:
                # Render each research item compactly
                line = []
                if _has(r.type):
                    line.append(f"**{r.type}**")
                if _has(r.description):
                    line.append(f"— {r.description}")
                # context is a required bool; include explicitly
                line.append(f"(context: {'yes' if getattr(r, 'context', False) else 'no'})")
                lines.append(f"- " + " ".join(line))

        # Technology, Tone, World, Style
        lines.append(_section("Setting & Aesthetics"))
        if _has(self.technology.type) or _has(self.technology.description):
            tech = self.technology.type
            if _has(self.technology.description):
                tech = f"{tech} — {self.technology.description}" if _has(tech) else self.technology.description
            lines.append(_kv("Technology", tech))
        if _has(self.tone.type) or _has(self.tone.description):
            tone = self.tone.type
            if _has(self.tone.description):
                tone = f"{tone} — {self.tone.description}" if _has(tone) else self.tone.description
            lines.append(_kv("Tone", tone))
        if _has(self.world.type) or _has(self.world.description):
            world = self.world.type
            if _has(self.world.description):
                world = f"{world} — {self.world.description}" if _has(world) else self.world.description
            lines.append(_kv("World", world))
        if _has(self.style.type) or _has(self.style.description):
            style = self.style.type
            if _has(self.style.description):
                style = f"{style} — {self.style.description}" if _has(style) else self.style.description
            lines.append(_kv("Style", style))

        # Remove blank lines and join
        final = "\n".join([ln for ln in lines if _has(ln)])
        return final.strip() + "\n"



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