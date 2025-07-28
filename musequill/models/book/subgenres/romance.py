from enum import Enum
from typing import Dict, List


class RomanceSubGenre(str, Enum):
    """Romance subgenres optimized for AI book generation and market demand."""
    
    # Most popular romance subgenres based on market research
    CONTEMPORARY_ROMANCE = "contemporary_romance"
    HISTORICAL_ROMANCE = "historical_romance"
    PARANORMAL_ROMANCE = "paranormal_romance"
    ROMANTIC_SUSPENSE = "romantic_suspense"
    DARK_ROMANCE = "dark_romance"
    ROMANTIC_COMEDY = "romantic_comedy"
    SPORTS_ROMANCE = "sports_romance"
    BILLIONAIRE_ROMANCE = "billionaire_romance"
    ENEMIES_TO_LOVERS = "enemies_to_lovers"
    SECOND_CHANCE_ROMANCE = "second_chance_romance"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()
    
    @property
    def description(self) -> str:
        """Description of the subgenre."""
        descriptions = {
            self.CONTEMPORARY_ROMANCE: "Modern-day romance in realistic settings",
            self.HISTORICAL_ROMANCE: "Romance set in historical periods",
            self.PARANORMAL_ROMANCE: "Romance with supernatural elements",
            self.ROMANTIC_SUSPENSE: "Romance combined with thriller/mystery elements",
            self.DARK_ROMANCE: "Romance with morally complex themes and darker content",
            self.ROMANTIC_COMEDY: "Light-hearted romance with humor",
            self.SPORTS_ROMANCE: "Romance centered around athletes or sports",
            self.BILLIONAIRE_ROMANCE: "Romance featuring wealthy protagonists",
            self.ENEMIES_TO_LOVERS: "Romance trope where antagonists become lovers",
            self.SECOND_CHANCE_ROMANCE: "Romance about rekindling past relationships"
        }
        return descriptions.get(self, "")
    
    @property
    def market_popularity(self) -> str:
        """Market popularity level."""
        high_popularity = {
            self.CONTEMPORARY_ROMANCE, self.DARK_ROMANCE, self.ENEMIES_TO_LOVERS,
            self.BILLIONAIRE_ROMANCE, self.PARANORMAL_ROMANCE
        }
        medium_popularity = {
            self.HISTORICAL_ROMANCE, self.ROMANTIC_SUSPENSE, self.ROMANTIC_COMEDY,
            self.SECOND_CHANCE_ROMANCE
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
        return "50,000-80,000 words"  # Standard romance novel length
    
    @classmethod
    def from_string(cls, value: str) -> 'RomanceSubGenre':
        """Create from string with fuzzy matching."""
        value_lower = value.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == value_lower:
                return subgenre
        
        # Fuzzy matching
        fuzzy_matches = {
            "contemporary": cls.CONTEMPORARY_ROMANCE,
            "historical": cls.HISTORICAL_ROMANCE,
            "paranormal": cls.PARANORMAL_ROMANCE,
            "suspense": cls.ROMANTIC_SUSPENSE,
            "dark": cls.DARK_ROMANCE,
            "comedy": cls.ROMANTIC_COMEDY,
            "sports": cls.SPORTS_ROMANCE,
            "billionaire": cls.BILLIONAIRE_ROMANCE,
            "enemies": cls.ENEMIES_TO_LOVERS,
            "second_chance": cls.SECOND_CHANCE_ROMANCE
        }
        
        if value_lower in fuzzy_matches:
            return fuzzy_matches[value_lower]
        
        raise ValueError(f"Unknown romance subgenre: {value}")
    
    @classmethod
    def get_trending_subgenres(cls) -> List['RomanceSubGenre']:
        """Get currently trending romance subgenres."""
        return [
            cls.DARK_ROMANCE,
            cls.ENEMIES_TO_LOVERS,
            cls.BILLIONAIRE_ROMANCE,
            cls.PARANORMAL_ROMANCE,
            cls.CONTEMPORARY_ROMANCE
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage
if __name__ == "__main__":
    # Test the enum
    dark_romance = RomanceSubGenre.DARK_ROMANCE
    print(f"Subgenre: {dark_romance}")
    print(f"Description: {dark_romance.description}")
    print(f"Market popularity: {dark_romance.market_popularity}")
    print(f"Typical length: {dark_romance.typical_length}")
    
    print("\nTrending romance subgenres:")
    for subgenre in RomanceSubGenre.get_trending_subgenres():
        print(f"  {subgenre} - {subgenre.market_popularity} popularity")