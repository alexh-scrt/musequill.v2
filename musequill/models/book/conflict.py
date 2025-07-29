from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union


class ConflictType(str, Enum):
    """Types of conflict in stories."""
    PERSON_VS_PERSON = "person_vs_person"
    PERSON_VS_SELF = "person_vs_self"
    PERSON_VS_SOCIETY = "person_vs_society"
    PERSON_VS_NATURE = "person_vs_nature"
    PERSON_VS_TECHNOLOGY = "person_vs_technology"
    PERSON_VS_SUPERNATURAL = "person_vs_supernatural"
    PERSON_VS_FATE = "person_vs_fate"
    PERSON_VS_GOD = "person_vs_god"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.PERSON_VS_PERSON: "Person vs Person",
            self.PERSON_VS_SELF: "Person vs Self",
            self.PERSON_VS_SOCIETY: "Person vs Society",
            self.PERSON_VS_NATURE: "Person vs Nature",
            self.PERSON_VS_TECHNOLOGY: "Person vs Technology",
            self.PERSON_VS_SUPERNATURAL: "Person vs Supernatural",
            self.PERSON_VS_FATE: "Person vs Fate",
            self.PERSON_VS_GOD: "Person vs God",
        }
        return names.get(self, self.value.replace("_", " ").title())

    @property
    def description(self) -> str:
        """Detailed description of the conflict type."""
        descriptions = {
            self.PERSON_VS_PERSON: "A conflict between the protagonist and another character, such as an antagonist, rival, or enemy. This includes physical confrontations, ideological battles, and interpersonal struggles where characters have opposing goals.",
            self.PERSON_VS_SELF: "An internal conflict where the protagonist struggles with their own emotions, desires, fears, or moral dilemmas. This includes battles with guilt, self-doubt, addiction, identity crises, and personal growth challenges.",
            self.PERSON_VS_SOCIETY: "A conflict between the protagonist and social institutions, cultural norms, laws, or societal expectations. This includes fighting against injustice, challenging traditions, or resisting oppressive systems.",
            self.PERSON_VS_NATURE: "A conflict between the protagonist and natural forces, including weather, disasters, wilderness survival, or environmental challenges. This emphasizes human resilience against the power of the natural world.",
            self.PERSON_VS_TECHNOLOGY: "A conflict involving technology as an antagonistic force, including AI rebellion, technological dependence, digital surveillance, or the dehumanizing effects of advanced technology on society and individuals.",
            self.PERSON_VS_SUPERNATURAL: "A conflict between the protagonist and supernatural or paranormal forces, including ghosts, demons, magic, curses, or otherworldly entities that operate beyond natural laws.",
            self.PERSON_VS_FATE: "A conflict where the protagonist struggles against destiny, predetermined outcomes, or seemingly inevitable circumstances. This includes fighting against prophecies, trying to change predetermined outcomes, or accepting one's role in larger cosmic plans.",
            self.PERSON_VS_GOD: "A conflict between the protagonist and divine forces, religious institutions, or spiritual beliefs. This includes questioning faith, challenging divine will, or struggling with religious doctrine and spiritual crises.",
        }
        return descriptions.get(self, f"A conflict involving {self.display_name.lower()}")

    @property
    def complexity_level(self) -> str:
        """Writing complexity level for this conflict type."""
        complexity_map = {
            self.PERSON_VS_PERSON: "intermediate",
            self.PERSON_VS_SELF: "advanced", 
            self.PERSON_VS_SOCIETY: "advanced",
            self.PERSON_VS_NATURE: "basic",
            self.PERSON_VS_TECHNOLOGY: "intermediate",
            self.PERSON_VS_SUPERNATURAL: "intermediate",
            self.PERSON_VS_FATE: "advanced",
            self.PERSON_VS_GOD: "expert",
        }
        return complexity_map.get(self, "intermediate")

    @property
    def typical_genres(self) -> List[str]:
        """Genres that commonly use this conflict type."""
        genre_map = {
            self.PERSON_VS_PERSON: ["thriller", "crime", "war", "drama", "romance", "historical_fiction"],
            self.PERSON_VS_SELF: ["literary_fiction", "drama", "coming_of_age", "psychological_thriller", "memoir"],
            self.PERSON_VS_SOCIETY: ["dystopian", "social_commentary", "historical_fiction", "political_thriller", "literary_fiction"],
            self.PERSON_VS_NATURE: ["survival", "adventure", "disaster", "wilderness", "environmental_fiction"],
            self.PERSON_VS_TECHNOLOGY: ["science_fiction", "cyberpunk", "dystopian", "techno_thriller", "speculative_fiction"],
            self.PERSON_VS_SUPERNATURAL: ["horror", "fantasy", "paranormal", "supernatural_thriller", "urban_fantasy"],
            self.PERSON_VS_FATE: ["tragedy", "epic_fantasy", "mythology", "philosophical_fiction", "existential_drama"],
            self.PERSON_VS_GOD: ["religious_fiction", "philosophical_fiction", "epic_fantasy", "mythology", "spiritual_drama"],
        }
        return genre_map.get(self, ["general_fiction"])

    @property
    def narrative_focus(self) -> str:
        """Primary narrative focus for this conflict type."""
        focus_map = {
            self.PERSON_VS_PERSON: "external_action",
            self.PERSON_VS_SELF: "internal_development",
            self.PERSON_VS_SOCIETY: "thematic_exploration",
            self.PERSON_VS_NATURE: "survival_tension",
            self.PERSON_VS_TECHNOLOGY: "conceptual_exploration",
            self.PERSON_VS_SUPERNATURAL: "atmospheric_tension",
            self.PERSON_VS_FATE: "philosophical_exploration",
            self.PERSON_VS_GOD: "spiritual_exploration",
        }
        return focus_map.get(self, "balanced")

    @property
    def emotional_tone(self) -> List[str]:
        """Common emotional tones associated with this conflict."""
        tone_map = {
            self.PERSON_VS_PERSON: ["tension", "confrontation", "rivalry", "determination"],
            self.PERSON_VS_SELF: ["introspection", "anxiety", "growth", "self-discovery"],
            self.PERSON_VS_SOCIETY: ["rebellion", "frustration", "hope", "injustice"],
            self.PERSON_VS_NATURE: ["survival", "awe", "struggle", "resilience"],
            self.PERSON_VS_TECHNOLOGY: ["paranoia", "alienation", "innovation", "fear"],
            self.PERSON_VS_SUPERNATURAL: ["mystery", "fear", "wonder", "otherworldly"],
            self.PERSON_VS_FATE: ["inevitability", "tragedy", "acceptance", "defiance"],
            self.PERSON_VS_GOD: ["reverence", "doubt", "spiritual_crisis", "enlightenment"],
        }
        return tone_map.get(self, ["conflict", "tension"])

    @classmethod
    def from_string(cls, value: str) -> 'ConflictType':
        """Create ConflictType from string with fuzzy matching."""
        value_lower = value.lower().strip()
        
        # Direct value matching
        try:
            return cls(value_lower)
        except ValueError:
            pass
        
        # Fuzzy matching with prioritized longer matches
        import re
        
        mappings = {
            # Person vs Person variants
            "character vs character": cls.PERSON_VS_PERSON,
            "protagonist vs antagonist": cls.PERSON_VS_PERSON,
            "interpersonal": cls.PERSON_VS_PERSON,
            "rivalry": cls.PERSON_VS_PERSON,
            "enemy": cls.PERSON_VS_PERSON,
            "villain": cls.PERSON_VS_PERSON,
            
            # Person vs Self variants
            "internal conflict": cls.PERSON_VS_SELF,
            "psychological": cls.PERSON_VS_SELF,
            "inner struggle": cls.PERSON_VS_SELF,
            "self doubt": cls.PERSON_VS_SELF,
            "identity crisis": cls.PERSON_VS_SELF,
            "moral dilemma": cls.PERSON_VS_SELF,
            
            # Person vs Society variants
            "social conflict": cls.PERSON_VS_SOCIETY,
            "system": cls.PERSON_VS_SOCIETY,
            "institution": cls.PERSON_VS_SOCIETY,
            "government": cls.PERSON_VS_SOCIETY,
            "law": cls.PERSON_VS_SOCIETY,
            "culture": cls.PERSON_VS_SOCIETY,
            "tradition": cls.PERSON_VS_SOCIETY,
            
            # Person vs Nature variants
            "environmental": cls.PERSON_VS_NATURE,
            "wilderness": cls.PERSON_VS_NATURE,
            "disaster": cls.PERSON_VS_NATURE,
            "survival": cls.PERSON_VS_NATURE,
            "natural forces": cls.PERSON_VS_NATURE,
            "weather": cls.PERSON_VS_NATURE,
            
            # Person vs Technology variants
            "artificial intelligence": cls.PERSON_VS_TECHNOLOGY,  # Put longer matches first
            "tech": cls.PERSON_VS_TECHNOLOGY,
            "machine": cls.PERSON_VS_TECHNOLOGY,
            "robot": cls.PERSON_VS_TECHNOLOGY,
            "digital": cls.PERSON_VS_TECHNOLOGY,
            "cyber": cls.PERSON_VS_TECHNOLOGY,
            
            # Person vs Supernatural variants
            "paranormal": cls.PERSON_VS_SUPERNATURAL,
            "otherworldly": cls.PERSON_VS_SUPERNATURAL,
            "ghost": cls.PERSON_VS_SUPERNATURAL,
            "magic": cls.PERSON_VS_SUPERNATURAL,
            "demon": cls.PERSON_VS_SUPERNATURAL,
            "curse": cls.PERSON_VS_SUPERNATURAL,
            "spirit": cls.PERSON_VS_SUPERNATURAL,  # Keep spirit for supernatural
            
            # Person vs Fate variants
            "predetermined": cls.PERSON_VS_FATE,  # Put longer matches first
            "destiny": cls.PERSON_VS_FATE,
            "prophecy": cls.PERSON_VS_FATE,
            "inevitable": cls.PERSON_VS_FATE,
            "cosmic": cls.PERSON_VS_FATE,
            
            # Person vs God variants
            "spiritual": cls.PERSON_VS_GOD,  # Put before "spirit" to avoid conflict
            "religious": cls.PERSON_VS_GOD,
            "divine": cls.PERSON_VS_GOD,
            "deity": cls.PERSON_VS_GOD,
            "faith": cls.PERSON_VS_GOD,
            "sacred": cls.PERSON_VS_GOD,
        }
        
        # Special handling for word-boundary sensitive keywords
        word_boundary_keywords = {
            "ai": cls.PERSON_VS_TECHNOLOGY,  # Match "ai" only as whole word
        }
        
        # First check word-boundary sensitive keywords
        for keyword, conflict_type in word_boundary_keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', value_lower):
                return conflict_type
        
        # Sort mappings by keyword length (longest first) to prioritize specific matches
        sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        # Then check general substring matches, starting with longest keywords
        for keyword, conflict_type in sorted_mappings:
            if keyword in value_lower:
                return conflict_type
        
        raise ValueError(f"Unknown conflict type: {value}")

    @classmethod
    def get_conflicts_for_genre(cls, genre: str) -> List['ConflictType']:
        """Get conflict types commonly used in a specific genre."""
        genre_lower = genre.lower()
        
        genre_mappings = {
            "fantasy": [cls.PERSON_VS_SUPERNATURAL, cls.PERSON_VS_FATE, cls.PERSON_VS_PERSON, cls.PERSON_VS_SELF],
            "science_fiction": [cls.PERSON_VS_TECHNOLOGY, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_NATURE, cls.PERSON_VS_SELF],
            "horror": [cls.PERSON_VS_SUPERNATURAL, cls.PERSON_VS_SELF, cls.PERSON_VS_PERSON, cls.PERSON_VS_FATE],
            "thriller": [cls.PERSON_VS_PERSON, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_TECHNOLOGY, cls.PERSON_VS_SELF],
            "literary_fiction": [cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_FATE, cls.PERSON_VS_GOD],
            "romance": [cls.PERSON_VS_SELF, cls.PERSON_VS_PERSON, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_FATE],
            "mystery": [cls.PERSON_VS_PERSON, cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_SUPERNATURAL],
            "adventure": [cls.PERSON_VS_NATURE, cls.PERSON_VS_PERSON, cls.PERSON_VS_SUPERNATURAL, cls.PERSON_VS_SOCIETY],
            "dystopian": [cls.PERSON_VS_SOCIETY, cls.PERSON_VS_TECHNOLOGY, cls.PERSON_VS_SELF, cls.PERSON_VS_FATE],
            "historical_fiction": [cls.PERSON_VS_SOCIETY, cls.PERSON_VS_PERSON, cls.PERSON_VS_SELF, cls.PERSON_VS_FATE],
            "young_adult": [cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_PERSON, cls.PERSON_VS_FATE],
            "survival": [cls.PERSON_VS_NATURE, cls.PERSON_VS_SELF, cls.PERSON_VS_PERSON, cls.PERSON_VS_SOCIETY],
            "religious": [cls.PERSON_VS_GOD, cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_FATE],
        }
        
        # Find matching conflicts
        recommended = set()
        for genre_key, conflicts in genre_mappings.items():
            if genre_key in genre_lower:
                recommended.update(conflicts)
        
        # If no specific mapping found, return common conflicts
        if not recommended:
            recommended = {cls.PERSON_VS_PERSON, cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY}
        
        return sorted(list(recommended), key=lambda x: x.display_name)

    @classmethod
    def get_external_conflicts(cls) -> List['ConflictType']:
        """Get all external conflict types."""
        return [
            cls.PERSON_VS_PERSON, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_NATURE,
            cls.PERSON_VS_TECHNOLOGY, cls.PERSON_VS_SUPERNATURAL, cls.PERSON_VS_FATE, cls.PERSON_VS_GOD
        ]

    @classmethod
    def get_internal_conflicts(cls) -> List['ConflictType']:
        """Get all internal conflict types."""
        return [cls.PERSON_VS_SELF]

    @classmethod
    def get_classic_conflicts(cls) -> List['ConflictType']:
        """Get the traditional literary conflict types."""
        return [
            cls.PERSON_VS_PERSON, cls.PERSON_VS_SELF, cls.PERSON_VS_SOCIETY, cls.PERSON_VS_NATURE
        ]

    @classmethod
    def get_modern_conflicts(cls) -> List['ConflictType']:
        """Get more contemporary conflict types."""
        return [
            cls.PERSON_VS_TECHNOLOGY, cls.PERSON_VS_SUPERNATURAL, cls.PERSON_VS_FATE, cls.PERSON_VS_GOD
        ]

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"ConflictType.{self.name}"