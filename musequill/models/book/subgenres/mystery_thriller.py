from enum import Enum
from typing import Dict, List


class MysteryThrillerSubGenre(str, Enum):
    """Mystery and Thriller subgenres optimized for AI book generation."""
    
    # Mystery subgenres
    COZY_MYSTERY = "cozy_mystery"
    POLICE_PROCEDURAL = "police_procedural"
    DETECTIVE_FICTION = "detective_fiction"
    NOIR = "noir"
    
    # Thriller subgenres
    PSYCHOLOGICAL_THRILLER = "psychological_thriller"
    DOMESTIC_THRILLER = "domestic_thriller"
    LEGAL_THRILLER = "legal_thriller"
    TECHNO_THRILLER = "techno_thriller"
    SPY_THRILLER = "spy_thriller"
    MEDICAL_THRILLER = "medical_thriller"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()
    
    @property
    def description(self) -> str:
        """Description of the subgenre."""
        descriptions = {
            self.COZY_MYSTERY: "Gentle mysteries with minimal violence, often in small communities",
            self.POLICE_PROCEDURAL: "Mysteries focusing on realistic police investigation methods",
            self.DETECTIVE_FICTION: "Classic detective stories with amateur or professional sleuths",
            self.NOIR: "Dark, cynical crime fiction with morally ambiguous characters",
            self.PSYCHOLOGICAL_THRILLER: "Suspense driven by characters' mental states and perceptions",
            self.DOMESTIC_THRILLER: "Thrillers set in familiar domestic environments",
            self.LEGAL_THRILLER: "Suspense stories centered around legal proceedings",
            self.TECHNO_THRILLER: "Technology-focused thrillers with high-tech elements",
            self.SPY_THRILLER: "Espionage and international intrigue stories",
            self.MEDICAL_THRILLER: "Medical settings and scenarios drive the suspense"
        }
        return descriptions.get(self, "")
    
    @property
    def is_mystery(self) -> bool:
        """Check if this is primarily a mystery subgenre."""
        mystery_subgenres = {
            self.COZY_MYSTERY, self.POLICE_PROCEDURAL, 
            self.DETECTIVE_FICTION, self.NOIR
        }
        return self in mystery_subgenres
    
    @property
    def is_thriller(self) -> bool:
        """Check if this is primarily a thriller subgenre."""
        return not self.is_mystery
    
    @property
    def market_popularity(self) -> str:
        """Market popularity level."""
        high_popularity = {
            self.PSYCHOLOGICAL_THRILLER, self.DOMESTIC_THRILLER,
            self.COZY_MYSTERY, self.POLICE_PROCEDURAL
        }
        medium_popularity = {
            self.LEGAL_THRILLER, self.DETECTIVE_FICTION,
            self.TECHNO_THRILLER, self.SPY_THRILLER
        }
        
        if self in high_popularity:
            return "high"
        elif self in medium_popularity:
            return "medium"
        else:
            return "moderate"
    
    @property
    def typical_length(self) -> str:
        """Typical book length for this subgenre."""
        length_map = {
            self.COZY_MYSTERY: "60,000-80,000 words",
            self.PSYCHOLOGICAL_THRILLER: "70,000-90,000 words",
            self.DOMESTIC_THRILLER: "70,000-90,000 words",
            self.LEGAL_THRILLER: "80,000-100,000 words",
            self.TECHNO_THRILLER: "80,000-100,000 words"
        }
        return length_map.get(self, "70,000-90,000 words")
    
    @property
    def pacing_style(self) -> str:
        """Typical pacing for this subgenre."""
        fast_paced = {
            self.PSYCHOLOGICAL_THRILLER, self.TECHNO_THRILLER,
            self.SPY_THRILLER, self.MEDICAL_THRILLER
        }
        moderate_paced = {
            self.DOMESTIC_THRILLER, self.LEGAL_THRILLER,
            self.POLICE_PROCEDURAL, self.DETECTIVE_FICTION
        }
        
        if self in fast_paced:
            return "fast"
        elif self in moderate_paced:
            return "moderate"
        else:
            return "steady"
    
    @classmethod
    def from_string(cls, value: str) -> 'MysteryThrillerSubGenre':
        """Create from string with fuzzy matching."""
        value_lower = value.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == value_lower:
                return subgenre
        
        # Fuzzy matching
        fuzzy_matches = {
            "cozy": cls.COZY_MYSTERY,
            "police": cls.POLICE_PROCEDURAL,
            "detective": cls.DETECTIVE_FICTION,
            "psychological": cls.PSYCHOLOGICAL_THRILLER,
            "domestic": cls.DOMESTIC_THRILLER,
            "legal": cls.LEGAL_THRILLER,
            "techno": cls.TECHNO_THRILLER,
            "tech": cls.TECHNO_THRILLER,
            "spy": cls.SPY_THRILLER,
            "medical": cls.MEDICAL_THRILLER
        }
        
        if value_lower in fuzzy_matches:
            return fuzzy_matches[value_lower]
        
        raise ValueError(f"Unknown mystery/thriller subgenre: {value}")
    
    @classmethod
    def get_trending_subgenres(cls) -> List['MysteryThrillerSubGenre']:
        """Get currently trending mystery/thriller subgenres."""
        return [
            cls.PSYCHOLOGICAL_THRILLER,
            cls.DOMESTIC_THRILLER,
            cls.COZY_MYSTERY,
            cls.POLICE_PROCEDURAL,
            cls.LEGAL_THRILLER
        ]
    
    @classmethod
    def get_mystery_subgenres(cls) -> List['MysteryThrillerSubGenre']:
        """Get only mystery subgenres."""
        return [sg for sg in cls if sg.is_mystery]
    
    @classmethod
    def get_thriller_subgenres(cls) -> List['MysteryThrillerSubGenre']:
        """Get only thriller subgenres."""
        return [sg for sg in cls if sg.is_thriller]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage
if __name__ == "__main__":
    # Test the enum
    psych_thriller = MysteryThrillerSubGenre.PSYCHOLOGICAL_THRILLER
    print(f"Subgenre: {psych_thriller}")
    print(f"Description: {psych_thriller.description}")
    print(f"Type: {'Mystery' if psych_thriller.is_mystery else 'Thriller'}")
    print(f"Market popularity: {psych_thriller.market_popularity}")
    print(f"Pacing: {psych_thriller.pacing_style}")
    
    print("\nMystery subgenres:")
    for subgenre in MysteryThrillerSubGenre.get_mystery_subgenres():
        print(f"  {subgenre}")
    
    print("\nThriller subgenres:")
    for subgenre in MysteryThrillerSubGenre.get_thriller_subgenres():
        print(f"  {subgenre}")