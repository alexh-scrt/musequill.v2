from enum import Enum
from typing import Dict, List


class YoungAdultSubGenre(str, Enum):
    """Young Adult subgenres optimized for AI book generation."""
    
    YA_FANTASY = "ya_fantasy"
    YA_ROMANCE = "ya_romance"
    YA_DYSTOPIAN = "ya_dystopian"
    YA_CONTEMPORARY = "ya_contemporary"
    YA_THRILLER = "ya_thriller"
    YA_SCIENCE_FICTION = "ya_science_fiction"
    COMING_OF_AGE = "coming_of_age"
    YA_PARANORMAL = "ya_paranormal"
    YA_HISTORICAL = "ya_historical"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").replace("ya", "YA").title()
    
    @property
    def description(self) -> str:
        """Description of the subgenre."""
        descriptions = {
            self.YA_FANTASY: "Fantasy stories targeting teenage readers",
            self.YA_ROMANCE: "Romance stories for young adult audiences",
            self.YA_DYSTOPIAN: "Dystopian futures through teenage perspectives",
            self.YA_CONTEMPORARY: "Modern realistic fiction for teens",
            self.YA_THRILLER: "Suspenseful stories appropriate for young adults",
            self.YA_SCIENCE_FICTION: "Science fiction targeting teenage readers",
            self.COMING_OF_AGE: "Stories about growing up and self-discovery",
            self.YA_PARANORMAL: "Supernatural elements in young adult fiction",
            self.YA_HISTORICAL: "Historical fiction for young adult readers"
        }
        return descriptions.get(self, "")
    
    @property
    def market_popularity(self) -> str:
        """Market popularity level based on current trends."""
        high_popularity = {
            self.YA_FANTASY, self.YA_ROMANCE, self.YA_CONTEMPORARY,
            self.COMING_OF_AGE
        }
        medium_popularity = {
            self.YA_THRILLER, self.YA_PARANORMAL, self.YA_HISTORICAL
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
        return "50,000-80,000 words"  # Standard YA length
    
    @property
    def target_age_range(self) -> str:
        """Target age range for readers."""
        return "13-18 years"
    
    @property
    def common_themes(self) -> List[str]:
        """Common themes in this subgenre."""
        theme_map = {
            self.YA_FANTASY: ["magic", "adventure", "friendship", "good vs evil"],
            self.YA_ROMANCE: ["first love", "relationships", "identity", "emotions"],
            self.YA_DYSTOPIAN: ["rebellion", "freedom", "social justice", "survival"],
            self.YA_CONTEMPORARY: ["identity", "family", "friendship", "real-world issues"],
            self.YA_THRILLER: ["mystery", "danger", "survival", "trust"],
            self.YA_SCIENCE_FICTION: ["technology", "future", "identity", "ethics"],
            self.COMING_OF_AGE: ["self-discovery", "growth", "transitions", "identity"],
            self.YA_PARANORMAL: ["supernatural", "mystery", "romance", "power"],
            self.YA_HISTORICAL: ["historical events", "cultural identity", "resilience"]
        }
        return theme_map.get(self, [])
    
    @property
    def ai_generation_difficulty(self) -> str:
        """Difficulty level for AI generation."""
        easy = {self.YA_CONTEMPORARY, self.COMING_OF_AGE, self.YA_ROMANCE}
        medium = {self.YA_FANTASY, self.YA_THRILLER, self.YA_PARANORMAL}
        hard = {self.YA_DYSTOPIAN, self.YA_SCIENCE_FICTION, self.YA_HISTORICAL}
        
        if self in easy:
            return "easy"
        elif self in medium:
            return "medium"
        else:
            return "hard"
    
    @classmethod
    def from_string(cls, value: str) -> 'YoungAdultSubGenre':
        """Create from string with fuzzy matching."""
        value_lower = value.lower().strip().replace(" ", "_").replace("-", "_")
        
        # Handle YA prefix variations
        if value_lower.startswith("young_adult_"):
            value_lower = "ya_" + value_lower[12:]
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == value_lower:
                return subgenre
        
        # Fuzzy matching
        fuzzy_matches = {
            "fantasy": cls.YA_FANTASY,
            "romance": cls.YA_ROMANCE,
            "dystopian": cls.YA_DYSTOPIAN,
            "contemporary": cls.YA_CONTEMPORARY,
            "thriller": cls.YA_THRILLER,
            "science_fiction": cls.YA_SCIENCE_FICTION,
            "sci_fi": cls.YA_SCIENCE_FICTION,
            "coming": cls.COMING_OF_AGE,
            "paranormal": cls.YA_PARANORMAL,
            "historical": cls.YA_HISTORICAL
        }
        
        if value_lower in fuzzy_matches:
            return fuzzy_matches[value_lower]
        
        raise ValueError(f"Unknown young adult subgenre: {value}")
    
    @classmethod
    def get_trending_subgenres(cls) -> List['YoungAdultSubGenre']:
        """Get currently trending young adult subgenres."""
        return [
            cls.YA_FANTASY,
            cls.YA_ROMANCE,
            cls.YA_CONTEMPORARY,
            cls.COMING_OF_AGE,
            cls.YA_THRILLER
        ]
    
    @classmethod
    def get_ai_friendly_subgenres(cls) -> List['YoungAdultSubGenre']:
        """Get subgenres that are easier for AI to generate."""
        return [
            cls.YA_CONTEMPORARY,
            cls.COMING_OF_AGE,
            cls.YA_ROMANCE,
            cls.YA_FANTASY,
            cls.YA_THRILLER
        ]
    
    @classmethod
    def get_high_emotion_subgenres(cls) -> List['YoungAdultSubGenre']:
        """Get subgenres that focus heavily on emotional development."""
        return [
            cls.YA_ROMANCE,
            cls.YA_CONTEMPORARY,
            cls.COMING_OF_AGE,
            cls.YA_PARANORMAL
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage
if __name__ == "__main__":
    # Test the enum
    ya_fantasy = YoungAdultSubGenre.YA_FANTASY
    print(f"Subgenre: {ya_fantasy}")
    print(f"Description: {ya_fantasy.description}")
    print(f"Market popularity: {ya_fantasy.market_popularity}")
    print(f"Target age: {ya_fantasy.target_age_range}")
    print(f"Common themes: {', '.join(ya_fantasy.common_themes)}")
    print(f"AI difficulty: {ya_fantasy.ai_generation_difficulty}")
    
    print("\nTrending YA subgenres:")
    for subgenre in YoungAdultSubGenre.get_trending_subgenres():
        print(f"  {subgenre} - {subgenre.market_popularity} popularity")
    
    print("\nHigh-emotion YA subgenres:")
    for subgenre in YoungAdultSubGenre.get_high_emotion_subgenres():
        print(f"  {subgenre}")