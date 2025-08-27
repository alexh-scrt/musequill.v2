from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import re


# ============================================================================
# Character Development Enumerations
# ============================================================================

class CharacterRole(str, Enum):
    """Character role types in narrative structure."""
    PROTAGONIST = "protagonist"
    PROTAGONISTS = "protagonists"
    ANTAGONIST = "antagonist"
    DEUTERAGONIST = "deuteragonist"  # Second main character
    LOVE_INTEREST = "love_interest"
    MENTOR = "mentor"
    ALLY = "ally"
    THRESHOLD_GUARDIAN = "threshold_guardian"
    HERALD = "herald"
    TRICKSTER = "trickster"
    SHAPESHIFTER = "shapeshifter"
    SUPPORTING = "supporting"
    MINOR = "minor"
    NARRATOR = "narrator"
    FOIL = "foil"  # Character who contrasts with protagonist

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.PROTAGONIST: "Protagonist",
            self.PROTAGONISTS: "Protagonists",
            self.ANTAGONIST: "Antagonist",
            self.DEUTERAGONIST: "Deuteragonist",
            self.LOVE_INTEREST: "Love Interest",
            self.MENTOR: "Mentor",
            self.ALLY: "Ally",
            self.THRESHOLD_GUARDIAN: "Threshold Guardian",
            self.HERALD: "Herald",
            self.TRICKSTER: "Trickster",
            self.SHAPESHIFTER: "Shapeshifter",
            self.SUPPORTING: "Supporting Character",
            self.MINOR: "Minor Character",
            self.NARRATOR: "Narrator",
            self.FOIL: "Foil Character",
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Detailed description of the character role."""
        descriptions = {
            self.PROTAGONIST: "The main character who drives the story forward, faces the central conflict, and undergoes the most significant character development throughout the narrative.",
            self.PROTAGONISTS: "The main characters who drive the story forward, face the central conflict, and undergo the most significant character development throughout the narrative.",
            self.ANTAGONIST: "The primary opponent or obstacle that creates conflict for the protagonist, whether a person, force, or circumstance that opposes the main character's goals.",
            self.DEUTERAGONIST: "The second most important character in the story, often serving as a close companion, rival, or secondary protagonist with their own significant arc.",
            self.LOVE_INTEREST: "A character who serves as the romantic focus for the protagonist or other main characters, driving romantic subplots and emotional development.",
            self.MENTOR: "A wise, experienced character who guides, teaches, and supports the protagonist, often providing crucial knowledge, skills, or wisdom needed for their journey.",
            self.ALLY: "A loyal friend, companion, or supporter who assists the protagonist in achieving their goals, providing aid, emotional support, or practical help.",
            self.THRESHOLD_GUARDIAN: "A character who tests the protagonist's resolve and commitment, often appearing early in the journey to challenge whether they're ready to proceed.",
            self.HERALD: "A character who announces the call to adventure or the need for change, often delivering news, warnings, or opportunities that set the plot in motion.",
            self.TRICKSTER: "A character who provides comic relief, disrupts the status quo, and often serves as a catalyst for change through humor, mischief, or unconventional wisdom.",
            self.SHAPESHIFTER: "A character whose loyalty, intentions, or true nature remain unclear or change throughout the story, creating uncertainty and complexity in relationships.",
            self.SUPPORTING: "Characters who play important roles in the plot and character development but are not central to the main narrative arc.",
            self.MINOR: "Characters with small but necessary roles, often appearing briefly to advance plot points, provide information, or populate the story world.",
            self.NARRATOR: "The character or voice that tells the story, who may or may not be a character within the narrative itself.",
            self.FOIL: "A character whose contrasting qualities, values, or choices highlight and emphasize the protagonist's characteristics through comparison and contrast.",
        }
        return descriptions.get(self, f"Character serving as {self.display_name.lower()}")

    @property
    def narrative_importance(self) -> str:
        """Level of importance in the narrative structure."""
        importance_map = {
            self.PROTAGONIST: "primary",
            self.PROTAGONISTS: "primary",
            self.ANTAGONIST: "primary",
            self.DEUTERAGONIST: "major",
            self.LOVE_INTEREST: "major",
            self.MENTOR: "major",
            self.ALLY: "secondary",
            self.THRESHOLD_GUARDIAN: "secondary",
            self.HERALD: "secondary",
            self.TRICKSTER: "secondary",
            self.SHAPESHIFTER: "major",
            self.SUPPORTING: "secondary",
            self.MINOR: "tertiary",
            self.NARRATOR: "structural",
            self.FOIL: "secondary",
        }
        return importance_map.get(self, "secondary")

    @property
    def typical_functions(self) -> List[str]:
        """Common narrative functions this role serves."""
        function_map = {
            self.PROTAGONIST: ["drives plot", "character growth", "reader identification", "goal pursuit"],
            self.PROTAGONISTS: ["drive plot", "character growth", "reader identification", "goal pursuit"],
            self.ANTAGONIST: ["creates conflict", "opposes protagonist", "tests limits", "represents obstacles"],
            self.DEUTERAGONIST: ["supports protagonist", "parallel development", "alternate perspective", "major subplot"],
            self.LOVE_INTEREST: ["romantic tension", "emotional stakes", "character motivation", "relationship development"],
            self.MENTOR: ["provides wisdom", "teaches skills", "offers guidance", "represents experience"],
            self.ALLY: ["provides support", "loyal friendship", "practical help", "emotional backing"],
            self.THRESHOLD_GUARDIAN: ["tests commitment", "challenges readiness", "creates obstacles", "forces growth"],
            self.HERALD: ["calls to action", "delivers news", "initiates change", "presents opportunities"],
            self.TRICKSTER: ["comic relief", "disrupts order", "provides insight", "challenges assumptions"],
            self.SHAPESHIFTER: ["creates uncertainty", "relationship complexity", "plot twists", "trust issues"],
            self.SUPPORTING: ["advances plot", "provides information", "represents themes", "populates world"],
            self.MINOR: ["specific function", "brief interaction", "plot device", "world building"],
            self.NARRATOR: ["story delivery", "perspective control", "information management", "reader connection"],
            self.FOIL: ["contrasts protagonist", "highlights traits", "alternative path", "thematic comparison"],
        }
        return function_map.get(self, ["narrative support"])

    @classmethod
    def from_string(cls, value: str) -> 'CharacterRole':
        """Create CharacterRole from string with fuzzy matching."""
        value_lower = value.lower().strip()
        
        # Direct value matching
        try:
            return cls(value_lower)
        except ValueError:
            pass
        
        # Fuzzy matching with prioritized longer matches
        mappings = {
            # Primary roles
            "main character": cls.PROTAGONIST,
            "main characters": cls.PROTAGONISTS,
            "hero": cls.PROTAGONIST,
            "heroes": cls.PROTAGONISTS,
            "heroine": cls.PROTAGONIST,
            "primary character": cls.PROTAGONIST,
            "primary characters": cls.PROTAGONISTS,
            "protagonist": cls.PROTAGONIST,
            "protagonists": cls.PROTAGONISTS,
            "lead character": cls.PROTAGONIST,
            "lead characters": cls.PROTAGONISTS,
            "lead": cls.PROTAGONIST,
            "leads": cls.PROTAGONISTS,
            "lead protagonist": cls.PROTAGONIST,
            "lead protagonists": cls.PROTAGONISTS,
            "lead hero": cls.PROTAGONIST,
            "lead heroine": cls.PROTAGONIST,

            # Opposite roles
            "antagonist": cls.ANTAGONIST,
            "villain": cls.ANTAGONIST,
            "bad guy": cls.ANTAGONIST,
            "enemy": cls.ANTAGONIST,
            "opponent": cls.ANTAGONIST,
            
            # Secondary roles
            "second main character": cls.DEUTERAGONIST,
            "secondary protagonist": cls.DEUTERAGONIST,
            "co-protagonist": cls.DEUTERAGONIST,
            "romantic interest": cls.LOVE_INTEREST,
            "love interest": cls.LOVE_INTEREST,
            "romantic partner": cls.LOVE_INTEREST,
            "teacher": cls.MENTOR,
            "guide": cls.MENTOR,
            "wise one": cls.MENTOR,
            "friend": cls.ALLY,
            "companion": cls.ALLY,
            "supporter": cls.ALLY,
            "helper": cls.ALLY,
            
            # Archetypal roles
            "threshold guardian": cls.THRESHOLD_GUARDIAN,
            "guardian": cls.THRESHOLD_GUARDIAN,
            "gatekeeper": cls.THRESHOLD_GUARDIAN,
            "messenger": cls.HERALD,
            "announcer": cls.HERALD,
            "comic relief": cls.TRICKSTER,
            "joker": cls.TRICKSTER,
            "shape shifter": cls.SHAPESHIFTER,
            "shape-shifter": cls.SHAPESHIFTER,
            "betrayer": cls.SHAPESHIFTER,
            
            # Supporting roles
            "supporting character": cls.SUPPORTING,
            "side character": cls.SUPPORTING,
            "minor character": cls.MINOR,
            "background character": cls.MINOR,
            "storyteller": cls.NARRATOR,
            "voice": cls.NARRATOR,
            "contrast character": cls.FOIL,
            "opposite": cls.FOIL,
        }
        
        # Sort by length (longest first) for better matching
        sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        for keyword, role in sorted_mappings:
            if keyword in value_lower:
                return role
        
        raise ValueError(f"Unknown character role: {value}")

    @classmethod
    def get_primary_roles(cls) -> List['CharacterRole']:
        """Get primary character roles."""
        return [cls.PROTAGONIST, cls.PROTAGONISTS, cls.ANTAGONIST]

    @classmethod
    def get_major_roles(cls) -> List['CharacterRole']:
        """Get major character roles."""
        return [
            cls.PROTAGONIST, cls.PROTAGONISTS, cls.ANTAGONIST, cls.DEUTERAGONIST, 
            cls.LOVE_INTEREST, cls.MENTOR, cls.SHAPESHIFTER
        ]

    @classmethod
    def get_archetypal_roles(cls) -> List['CharacterRole']:
        """Get roles based on archetypal functions."""
        return [
            cls.MENTOR, cls.ALLY, cls.THRESHOLD_GUARDIAN, cls.HERALD,
            cls.TRICKSTER, cls.SHAPESHIFTER, cls.FOIL
        ]

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"CharacterRole.{self.name}"


class CharacterArchetype(str, Enum):
    """Character archetypes based on psychology and mythology."""
    THE_HERO = "the_hero"
    THE_INNOCENT = "the_innocent"
    THE_EXPLORER = "the_explorer"
    THE_SAGE = "the_sage"
    THE_OUTLAW = "the_outlaw"
    THE_MAGICIAN = "the_magician"
    THE_REGULAR_PERSON = "the_regular_person"
    THE_LOVER = "the_lover"
    THE_JESTER = "the_jester"
    THE_CAREGIVER = "the_caregiver"
    THE_RULER = "the_ruler"
    THE_CREATOR = "the_creator"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.THE_HERO: "The Hero",
            self.THE_INNOCENT: "The Innocent",
            self.THE_EXPLORER: "The Explorer",
            self.THE_SAGE: "The Sage",
            self.THE_OUTLAW: "The Outlaw",
            self.THE_MAGICIAN: "The Magician",
            self.THE_REGULAR_PERSON: "The Regular Person",
            self.THE_LOVER: "The Lover",
            self.THE_JESTER: "The Jester",
            self.THE_CAREGIVER: "The Caregiver",
            self.THE_RULER: "The Ruler",
            self.THE_CREATOR: "The Creator",
        }
        return names.get(self, self.value.replace("_", " ").title())

    @property
    def description(self) -> str:
        """Detailed description of the character archetype."""
        descriptions = {
            self.THE_HERO: "Courageous characters who rise to challenges, overcome obstacles, and inspire others through their bravery and determination to do what's right.",
            self.THE_INNOCENT: "Pure, optimistic characters who see the good in everyone and everything, often serving as moral compasses and representing hope and faith.",
            self.THE_EXPLORER: "Adventurous, curious characters driven by a desire for freedom, discovery, and new experiences, always seeking to push boundaries and explore the unknown.",
            self.THE_SAGE: "Wise, knowledgeable characters who seek truth and share wisdom, often serving as mentors and representing intelligence, insight, and understanding.",
            self.THE_OUTLAW: "Rebellious characters who challenge authority and conventional rules, often fighting for justice or change, representing revolution and nonconformity.",
            self.THE_MAGICIAN: "Visionary characters who understand how the world works and can transform reality, representing power, knowledge, and the ability to make dreams come true.",
            self.THE_REGULAR_PERSON: "Relatable, down-to-earth characters who represent common folk, emphasizing belonging, community, and the virtue of being genuine and unpretentious.",
            self.THE_LOVER: "Passionate characters driven by love, relationships, and emotional connections, representing romance, commitment, and the power of human bonds.",
            self.THE_JESTER: "Playful, humorous characters who bring joy and levity, often using humor to reveal truth and help others not take themselves too seriously.",
            self.THE_CAREGIVER: "Nurturing, protective characters motivated by helping others, representing compassion, generosity, and selfless service to those in need.",
            self.THE_RULER: "Authoritative characters who take responsibility and control, striving to create order and stability, representing leadership and the desire to build lasting legacies.",
            self.THE_CREATOR: "Imaginative, artistic characters driven to create something new and meaningful, representing creativity, vision, and the desire for self-expression.",
        }
        return descriptions.get(self, f"Character embodying {self.display_name.lower()} archetype")

    @property
    def core_motivation(self) -> str:
        """Primary motivation driving this archetype."""
        motivation_map = {
            self.THE_HERO: "To prove worth through courageous action",
            self.THE_INNOCENT: "To be happy and live in harmony",
            self.THE_EXPLORER: "To experience freedom and find purpose",
            self.THE_SAGE: "To understand the world and share wisdom",
            self.THE_OUTLAW: "To overturn what isn't working",
            self.THE_MAGICIAN: "To understand laws of the universe",
            self.THE_REGULAR_PERSON: "To belong and connect with others",
            self.THE_LOVER: "To attain love and experience romance",
            self.THE_JESTER: "To enjoy life and help others have fun",
            self.THE_CAREGIVER: "To help and protect others",
            self.THE_RULER: "To create prosperity and success",
            self.THE_CREATOR: "To create something of enduring value",
        }
        return motivation_map.get(self, "To fulfill their purpose")

    @property
    def greatest_fear(self) -> str:
        """What this archetype fears most."""
        fear_map = {
            self.THE_HERO: "Weakness, vulnerability, cowardice",
            self.THE_INNOCENT: "Doing something wrong or bad",
            self.THE_EXPLORER: "Being trapped, conformity, inner emptiness",
            self.THE_SAGE: "Being deceived, ignorance, illusion",
            self.THE_OUTLAW: "Being powerless, ineffectual",
            self.THE_MAGICIAN: "Unintended negative consequences",
            self.THE_REGULAR_PERSON: "Being left out, standing out too much",
            self.THE_LOVER: "Being alone, unloved, emotionally unavailable",
            self.THE_JESTER: "Being boring, taking life too seriously",
            self.THE_CAREGIVER: "Selfishness, ingratitude from others",
            self.THE_RULER: "Chaos, being overthrown, loss of control",
            self.THE_CREATOR: "Having a mediocre vision or execution",
        }
        return fear_map.get(self, "Failure to fulfill their role")

    @property
    def typical_traits(self) -> List[str]:
        """Common personality traits for this archetype."""
        trait_map = {
            self.THE_HERO: ["brave", "determined", "honorable", "self-sacrificing"],
            self.THE_INNOCENT: ["optimistic", "trusting", "pure", "hopeful"], 
            self.THE_EXPLORER: ["adventurous", "independent", "curious", "restless"],
            self.THE_SAGE: ["wise", "knowledgeable", "thoughtful", "patient"],
            self.THE_OUTLAW: ["rebellious", "passionate", "freedom-loving", "unconventional"],
            self.THE_MAGICIAN: ["visionary", "inventive", "charismatic", "transformative"],
            self.THE_REGULAR_PERSON: ["down-to-earth", "relatable", "humble", "loyal"],
            self.THE_LOVER: ["passionate", "devoted", "romantic", "emotional"],
            self.THE_JESTER: ["humorous", "playful", "clever", "irreverent"],
            self.THE_CAREGIVER: ["nurturing", "selfless", "protective", "generous"],
            self.THE_RULER: ["responsible", "authoritative", "organized", "ambitious"],
            self.THE_CREATOR: ["creative", "imaginative", "artistic", "original"],
        }
        return trait_map.get(self, ["archetypal", "purposeful"])

    @classmethod
    def from_string(cls, value: str) -> 'CharacterArchetype':
        """Create CharacterArchetype from string with fuzzy matching."""
        value_lower = value.lower().strip()
        
        # Direct value matching
        try:
            return cls(value_lower)
        except ValueError:
            pass
        
        # Remove "the" prefix for matching
        if value_lower.startswith("the "):
            value_lower = value_lower[4:]
        
        # Fuzzy matching
        mappings = {
            "hero": cls.THE_HERO,
            "champion": cls.THE_HERO,
            "warrior": cls.THE_HERO,
            "innocent": cls.THE_INNOCENT,
            "child": cls.THE_INNOCENT,
            "pure one": cls.THE_INNOCENT,
            "explorer": cls.THE_EXPLORER,
            "adventurer": cls.THE_EXPLORER,
            "wanderer": cls.THE_EXPLORER,
            "seeker": cls.THE_EXPLORER,
            "sage": cls.THE_SAGE,
            "wise one": cls.THE_SAGE,
            "mentor": cls.THE_SAGE,
            "teacher": cls.THE_SAGE,
            "outlaw": cls.THE_OUTLAW,
            "rebel": cls.THE_OUTLAW,
            "revolutionary": cls.THE_OUTLAW,
            "magician": cls.THE_MAGICIAN,
            "wizard": cls.THE_MAGICIAN,
            "transformer": cls.THE_MAGICIAN,
            "regular person": cls.THE_REGULAR_PERSON,
            "everyman": cls.THE_REGULAR_PERSON,
            "common person": cls.THE_REGULAR_PERSON,
            "ordinary person": cls.THE_REGULAR_PERSON,
            "lover": cls.THE_LOVER,
            "romantic": cls.THE_LOVER,
            "partner": cls.THE_LOVER,
            "jester": cls.THE_JESTER,
            "fool": cls.THE_JESTER,
            "joker": cls.THE_JESTER,
            "comedian": cls.THE_JESTER,
            "caregiver": cls.THE_CAREGIVER,
            "nurturer": cls.THE_CAREGIVER,
            "helper": cls.THE_CAREGIVER,
            "protector": cls.THE_CAREGIVER,
            "ruler": cls.THE_RULER,
            "leader": cls.THE_RULER,
            "king": cls.THE_RULER,
            "queen": cls.THE_RULER,
            "boss": cls.THE_RULER,
            "creator": cls.THE_CREATOR,
            "artist": cls.THE_CREATOR,
            "inventor": cls.THE_CREATOR,
            "builder": cls.THE_CREATOR,
        }
        
        for keyword, archetype in mappings.items():
            if keyword in value_lower:
                return archetype
        
        raise ValueError(f"Unknown character archetype: {value}")

    @classmethod
    def get_positive_archetypes(cls) -> List['CharacterArchetype']:
        """Get archetypes typically seen as positive."""
        return [
            cls.THE_HERO, cls.THE_INNOCENT, cls.THE_SAGE, cls.THE_CAREGIVER,
            cls.THE_EXPLORER, cls.THE_CREATOR, cls.THE_LOVER
        ]

    @classmethod
    def get_complex_archetypes(cls) -> List['CharacterArchetype']:
        """Get archetypes with more complex moral positions."""
        return [
            cls.THE_OUTLAW, cls.THE_MAGICIAN, cls.THE_RULER, cls.THE_JESTER,
            cls.THE_REGULAR_PERSON
        ]

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"CharacterArchetype.{self.name}"

