from enum import Enum
from typing import Dict, List


class FantasySubGenre(str, Enum):
    """Fantasy subgenres optimized for AI book generation and market demand."""
    
    HIGH_FANTASY = "high_fantasy"
    URBAN_FANTASY = "urban_fantasy"
    DARK_FANTASY = "dark_fantasy"
    EPIC_FANTASY = "epic_fantasy"
    COZY_FANTASY = "cozy_fantasy"
    ROMANTASY = "romantasy"  # Fantasy Romance hybrid
    PORTAL_FANTASY = "portal_fantasy"
    FAIRY_TALE_RETELLING = "fairy_tale_retelling"
    SWORD_AND_SORCERY = "sword_and_sorcery"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()
    
    @property
    def description(self) -> str:
        """Description of the subgenre."""
        descriptions = {
            self.HIGH_FANTASY: "Fantasy set in entirely fictional worlds with complex magic systems",
            self.URBAN_FANTASY: "Fantasy elements integrated into modern urban settings",
            self.DARK_FANTASY: "Fantasy with horror elements and darker themes",
            self.EPIC_FANTASY: "Large-scale fantasy with world-spanning conflicts",
            self.COZY_FANTASY: "Low-stakes fantasy focused on comfort and community",
            self.ROMANTASY: "Fantasy with romance as a central plot element",
            self.PORTAL_FANTASY: "Characters travel from our world to fantasy realms",
            self.FAIRY_TALE_RETELLING: "Modern reinterpretations of classic fairy tales",
            self.SWORD_AND_SORCERY: "Action-oriented fantasy with combat and magic"
        }
        return descriptions.get(self, "")
    
    @property
    def market_popularity(self) -> str:
        """Market popularity level based on current trends."""
        high_popularity = {
            self.ROMANTASY, self.URBAN_FANTASY, self.COZY_FANTASY,
            self.FAIRY_TALE_RETELLING, self.DARK_FANTASY
        }
        medium_popularity = {
            self.HIGH_FANTASY, self.EPIC_FANTASY, self.PORTAL_FANTASY
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
            self.COZY_FANTASY: "40,000-60,000 words",
            self.ROMANTASY: "60,000-80,000 words",
            self.URBAN_FANTASY: "70,000-90,000 words",
            self.EPIC_FANTASY: "100,000-150,000 words",
            self.HIGH_FANTASY: "80,000-120,000 words"
        }
        return length_map.get(self, "70,000-100,000 words")
    
    @property
    def difficulty_level(self) -> str:
        """AI generation difficulty level."""
        easy = {self.COZY_FANTASY, self.ROMANTASY, self.FAIRY_TALE_RETELLING}
        medium = {self.URBAN_FANTASY, self.PORTAL_FANTASY, self.DARK_FANTASY}
        hard = {self.HIGH_FANTASY, self.EPIC_FANTASY, self.SWORD_AND_SORCERY}
        
        if self in easy:
            return "easy"
        elif self in medium:
            return "medium"
        else:
            return "hard"
    
    @classmethod
    def from_string(cls, value: str) -> 'FantasySubGenre':
        """Create from string with fuzzy matching."""
        value_lower = value.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == value_lower:
                return subgenre
        
        # Fuzzy matching
        fuzzy_matches = {
            "high": cls.HIGH_FANTASY,
            "urban": cls.URBAN_FANTASY,
            "dark": cls.DARK_FANTASY,
            "epic": cls.EPIC_FANTASY,
            "cozy": cls.COZY_FANTASY,
            "romance": cls.ROMANTASY,
            "romantic_fantasy": cls.ROMANTASY,
            "fantasy_romance": cls.ROMANTASY,
            "portal": cls.PORTAL_FANTASY,
            "fairy_tale": cls.FAIRY_TALE_RETELLING,
            "retelling": cls.FAIRY_TALE_RETELLING,
            "sword": cls.SWORD_AND_SORCERY
        }
        
        if value_lower in fuzzy_matches:
            return fuzzy_matches[value_lower]
        
        raise ValueError(f"Unknown fantasy subgenre: {value}")
    
    @classmethod
    def get_trending_subgenres(cls) -> List['FantasySubGenre']:
        """Get currently trending fantasy subgenres."""
        return [
            cls.ROMANTASY,
            cls.COZY_FANTASY,
            cls.DARK_FANTASY,
            cls.FAIRY_TALE_RETELLING,
            cls.URBAN_FANTASY
        ]
    
    @classmethod
    def get_ai_friendly_subgenres(cls) -> List['FantasySubGenre']:
        """Get subgenres that are easier for AI to generate."""
        return [
            cls.COZY_FANTASY,
            cls.ROMANTASY,
            cls.FAIRY_TALE_RETELLING,
            cls.PORTAL_FANTASY,
            cls.URBAN_FANTASY
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage
if __name__ == "__main__":
    # Test the enum
    romantasy = FantasySubGenre.ROMANTASY
    print(f"Subgenre: {romantasy}")
    print(f"Description: {romantasy.description}")
    print(f"Market popularity: {romantasy.market_popularity}")
    print(f"Typical length: {romantasy.typical_length}")
    print(f"AI difficulty: {romantasy.difficulty_level}")
    
    print("\nTrending fantasy subgenres:")
    for subgenre in FantasySubGenre.get_trending_subgenres():
        print(f"  {subgenre} - {subgenre.market_popularity} popularity, {subgenre.difficulty_level} difficulty")