from enum import Enum
from typing import Dict, List


class ScienceFictionSubGenre(str, Enum):
    """Science Fiction subgenres optimized for AI book generation."""
    
    SPACE_OPERA = "space_opera"
    CYBERPUNK = "cyberpunk"
    DYSTOPIAN = "dystopian"
    HARD_SF = "hard_sf"
    SOFT_SF = "soft_sf"
    TIME_TRAVEL = "time_travel"
    POST_APOCALYPTIC = "post_apocalyptic"
    ALIEN_CONTACT = "alien_contact"
    BIOPUNK = "biopunk"
    CLI_FI = "cli_fi"  # Climate Fiction
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        special_cases = {
            "cli_fi": "Climate Fiction",
            "hard_sf": "Hard Science Fiction",
            "soft_sf": "Soft Science Fiction"
        }
        return special_cases.get(self.value, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Description of the subgenre."""
        descriptions = {
            self.SPACE_OPERA: "Epic adventures across galactic civilizations",
            self.CYBERPUNK: "High-tech dystopian futures with corporate dominance",
            self.DYSTOPIAN: "Oppressive societies and totalitarian governments",
            self.HARD_SF: "Scientifically rigorous science fiction",
            self.SOFT_SF: "Focus on social sciences and human behavior",
            self.TIME_TRAVEL: "Stories involving travel through time",
            self.POST_APOCALYPTIC: "Survival in the aftermath of civilization's collapse",
            self.ALIEN_CONTACT: "First contact or ongoing relationships with alien species",
            self.BIOPUNK: "Biotechnology and genetic engineering themes",
            self.CLI_FI: "Climate change and environmental disaster scenarios"
        }
        return descriptions.get(self, "")
    
    @property
    def market_popularity(self) -> str:
        """Market popularity level based on current trends."""
        high_popularity = {
            self.DYSTOPIAN, self.POST_APOCALYPTIC, self.CLI_FI,
            self.TIME_TRAVEL, self.SPACE_OPERA
        }
        medium_popularity = {
            self.CYBERPUNK, self.ALIEN_CONTACT, self.SOFT_SF
        }
        
        if self in high_popularity:
            return "high"
        elif self in medium_popularity:
            return "medium"
        else:
            return "moderate"
    
    @property
    def science_complexity(self) -> str:
        """Level of scientific complexity required."""
        high_complexity = {self.HARD_SF, self.BIOPUNK, self.CLI_FI}
        medium_complexity = {self.TIME_TRAVEL, self.ALIEN_CONTACT, self.CYBERPUNK}
        
        if self in high_complexity:
            return "high"
        elif self in medium_complexity:
            return "medium"
        else:
            return "low"
    
    @property
    def typical_length(self) -> str:
        """Typical book length for this subgenre."""
        length_map = {
            self.SPACE_OPERA: "80,000-120,000 words",
            self.DYSTOPIAN: "70,000-90,000 words",
            self.POST_APOCALYPTIC: "70,000-90,000 words",
            self.HARD_SF: "80,000-100,000 words",
            self.CLI_FI: "70,000-90,000 words"
        }
        return length_map.get(self, "70,000-90,000 words")
    
    @property
    def ai_generation_difficulty(self) -> str:
        """Difficulty level for AI generation."""
        easy = {self.DYSTOPIAN, self.POST_APOCALYPTIC, self.TIME_TRAVEL}
        medium = {self.SOFT_SF, self.ALIEN_CONTACT, self.CLI_FI}
        hard = {self.HARD_SF, self.SPACE_OPERA, self.CYBERPUNK, self.BIOPUNK}
        
        if self in easy:
            return "easy"
        elif self in medium:
            return "medium"
        else:
            return "hard"
    
    @classmethod
    def from_string(cls, value: str) -> 'ScienceFictionSubGenre':
        """Create from string with fuzzy matching."""
        value_lower = value.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == value_lower:
                return subgenre
        
        # Fuzzy matching
        fuzzy_matches = {
            "space": cls.SPACE_OPERA,
            "opera": cls.SPACE_OPERA,
            "cyber": cls.CYBERPUNK,
            "punk": cls.CYBERPUNK,
            "dystopia": cls.DYSTOPIAN,
            "hard": cls.HARD_SF,
            "soft": cls.SOFT_SF,
            "time": cls.TIME_TRAVEL,
            "apocalyptic": cls.POST_APOCALYPTIC,
            "post_apocalypse": cls.POST_APOCALYPTIC,
            "alien": cls.ALIEN_CONTACT,
            "contact": cls.ALIEN_CONTACT,
            "bio": cls.BIOPUNK,
            "climate": cls.CLI_FI,
            "climate_fiction": cls.CLI_FI
        }
        
        if value_lower in fuzzy_matches:
            return fuzzy_matches[value_lower]
        
        raise ValueError(f"Unknown science fiction subgenre: {value}")
    
    @classmethod
    def get_trending_subgenres(cls) -> List['ScienceFictionSubGenre']:
        """Get currently trending science fiction subgenres."""
        return [
            cls.CLI_FI,
            cls.DYSTOPIAN,
            cls.POST_APOCALYPTIC,
            cls.CYBERPUNK,
            cls.TIME_TRAVEL
        ]
    
    @classmethod
    def get_ai_friendly_subgenres(cls) -> List['ScienceFictionSubGenre']:
        """Get subgenres that are easier for AI to generate."""
        return [
            cls.DYSTOPIAN,
            cls.POST_APOCALYPTIC,
            cls.TIME_TRAVEL,
            cls.SOFT_SF,
            cls.CLI_FI
        ]
    
    @classmethod
    def get_hard_science_subgenres(cls) -> List['ScienceFictionSubGenre']:
        """Get subgenres requiring strong scientific knowledge."""
        return [
            cls.HARD_SF,
            cls.BIOPUNK,
            cls.CLI_FI,
            cls.SPACE_OPERA
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage
if __name__ == "__main__":
    # Test the enum
    cli_fi = ScienceFictionSubGenre.CLI_FI
    print(f"Subgenre: {cli_fi}")
    print(f"Description: {cli_fi.description}")
    print(f"Market popularity: {cli_fi.market_popularity}")
    print(f"Science complexity: {cli_fi.science_complexity}")
    print(f"AI difficulty: {cli_fi.ai_generation_difficulty}")
    
    print("\nTrending sci-fi subgenres:")
    for subgenre in ScienceFictionSubGenre.get_trending_subgenres():
        print(f"  {subgenre} - {subgenre.market_popularity} popularity")
    
    print("\nAI-friendly sci-fi subgenres:")
    for subgenre in ScienceFictionSubGenre.get_ai_friendly_subgenres():
        print(f"  {subgenre} - {subgenre.ai_generation_difficulty} difficulty")