from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import json
from dataclasses import dataclass

# Import all the genre and subgenre enums
# (In practice, these would be imported from separate files)

class GenreType(str, Enum):
    """Optimized genre types for AI book generation based on market popularity and demand."""
    
    # TOP PERFORMING GENRES (Highest Priority)
    ROMANCE = "romance"
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    THRILLER = "thriller"
    SCIENCE_FICTION = "science_fiction"
    
    # HIGH PERFORMING FICTION GENRES
    YOUNG_ADULT = "young_adult"
    HISTORICAL_FICTION = "historical_fiction"
    HORROR = "horror"
    CONTEMPORARY = "contemporary"
    PARANORMAL = "paranormal"
    DYSTOPIAN = "dystopian"
    ADVENTURE = "adventure"
    CRIME = "crime"
    
    # EMERGING/TRENDING GENRES
    ROMANTASY = "romantasy"  # Romance + Fantasy hybrid - trending high
    DARK_ACADEMIA = "dark_academia"
    COZY_FANTASY = "cozy_fantasy"
    CLI_FI = "cli_fi"  # Climate Fiction - emerging genre
    
    # LITERARY & DRAMA
    LITERARY_FICTION = "literary_fiction"
    DRAMA = "drama"
    COMING_OF_AGE = "coming_of_age"
    
    # SPECIALIZED FICTION
    WESTERN = "western"
    COMEDY = "comedy"
    SATIRE = "satire"
    
    # HIGH-DEMAND NON-FICTION
    SELF_HELP = "self_help"
    MEMOIR = "memoir"
    BIOGRAPHY = "biography"
    BUSINESS = "business"
    HEALTH = "health"
    TRUE_CRIME = "true_crime"
    
    # PRACTICAL NON-FICTION
    TRAVEL = "travel"
    COOKING = "cooking"
    HISTORY = "history"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    REFERENCE = "reference"
    
    # SPECIALIZED NON-FICTION
    PHILOSOPHY = "philosophy"
    RELIGION = "religion"
    POLITICS = "politics"
    PSYCHOLOGY = "psychology"
    
    # CHILDREN & SPECIALIZED
    CHILDREN = "children"
    PICTURE_BOOK = "picture_book"
    POETRY = "poetry"
    TEXTBOOK = "textbook"
    
    # UTILITY
    OTHER = "other"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()
    
    @property
    def is_fiction(self) -> bool:
        """Check if this genre is fiction."""
        fiction_genres = {
            self.ROMANCE, self.FANTASY, self.MYSTERY, self.THRILLER, 
            self.SCIENCE_FICTION, self.YOUNG_ADULT, self.HISTORICAL_FICTION,
            self.HORROR, self.CONTEMPORARY, self.PARANORMAL, self.DYSTOPIAN,
            self.ADVENTURE, self.CRIME, self.ROMANTASY, self.DARK_ACADEMIA,
            self.COZY_FANTASY, self.CLI_FI, self.LITERARY_FICTION, self.DRAMA,
            self.COMING_OF_AGE, self.WESTERN, self.COMEDY, self.SATIRE
        }
        return self in fiction_genres
    
    @property
    def is_high_demand(self) -> bool:
        """Check if this genre is in high demand based on market research."""
        high_demand_genres = {
            self.ROMANCE, self.FANTASY, self.MYSTERY, self.THRILLER,
            self.SCIENCE_FICTION, self.YOUNG_ADULT, self.ROMANTASY,
            self.SELF_HELP, self.MEMOIR, self.TRUE_CRIME, self.COZY_FANTASY
        }
        return self in high_demand_genres
    
    @property
    def market_size(self) -> str:
        """Estimated market size category."""
        large_market = {
            self.ROMANCE, self.FANTASY, self.MYSTERY, self.THRILLER,
            self.YOUNG_ADULT, self.SELF_HELP
        }
        medium_market = {
            self.SCIENCE_FICTION, self.HISTORICAL_FICTION, self.HORROR,
            self.MEMOIR, self.BIOGRAPHY, self.BUSINESS, self.TRUE_CRIME,
            self.ROMANTASY, self.CONTEMPORARY
        }
        
        if self in large_market:
            return "large"
        elif self in medium_market:
            return "medium"
        else:
            return "small"
    
    @classmethod
    def from_string(cls, value: str) -> 'GenreType':
        """Create GenreType from string with fuzzy matching and case-insensitive support.
        
        Args:
            value: String representation of the genre
            
        Returns:
            GenreType enum member
            
        Raises:
            ValueError: If the genre string is not recognized
            
        Examples:
            >>> GenreType.from_string("romance")
            <GenreType.ROMANCE: 'romance'>
            >>> GenreType.from_string("Romantic Fantasy")
            <GenreType.ROMANTASY: 'romantasy'>
            >>> GenreType.from_string("sci-fi")
            <GenreType.SCIENCE_FICTION: 'science_fiction'>
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid genre value: {value}")
        
        # Normalize input: lowercase, strip whitespace, replace hyphens with underscores
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match with enum values
        for genre in cls:
            if genre.value == normalized_value:
                return genre
        
        # Fuzzy matching for common variations and aliases
        fuzzy_matches = {
            # Romance variations
            "romantic": cls.ROMANCE,
            "love_story": cls.ROMANCE,
            "love": cls.ROMANCE,
            
            # Fantasy variations
            "fantasies": cls.FANTASY,
            
            # Science Fiction variations
            "sci_fi": cls.SCIENCE_FICTION,
            "scifi": cls.SCIENCE_FICTION,
            "sf": cls.SCIENCE_FICTION,
            "science_fiction": cls.SCIENCE_FICTION,
            
            # Romantasy variations
            "romantic_fantasy": cls.ROMANTASY,
            "romance_fantasy": cls.ROMANTASY,
            "fantasy_romance": cls.ROMANTASY,
            "romantsy": cls.ROMANTASY,  # Common misspelling
            
            # Young Adult variations
            "ya": cls.YOUNG_ADULT,
            "young_adults": cls.YOUNG_ADULT,
            "teen": cls.YOUNG_ADULT,
            "teenage": cls.YOUNG_ADULT,
            
            # Mystery/Thriller variations
            "mysteries": cls.MYSTERY,
            "detective": cls.MYSTERY,
            "whodunit": cls.MYSTERY,
            "thrillers": cls.THRILLER,
            "suspense": cls.THRILLER,
            
            # Horror variations
            "scary": cls.HORROR,
            "spooky": cls.HORROR,
            
            # Historical Fiction variations
            "historical": cls.HISTORICAL_FICTION,
            "period_fiction": cls.HISTORICAL_FICTION,
            "historical_novel": cls.HISTORICAL_FICTION,
            
            # Self-Help variations
            "self_help": cls.SELF_HELP,
            "selfhelp": cls.SELF_HELP,
            "personal_development": cls.SELF_HELP,
            "motivation": cls.SELF_HELP,
            "motivational": cls.SELF_HELP,
            
            # True Crime variations
            "true_crime": cls.TRUE_CRIME,
            "truecrime": cls.TRUE_CRIME,
            "real_crime": cls.TRUE_CRIME,
            
            # Climate Fiction variations
            "climate_fiction": cls.CLI_FI,
            "climate": cls.CLI_FI,
            
            # Literary Fiction variations
            "literary": cls.LITERARY_FICTION,
            "literature": cls.LITERARY_FICTION,
            "lit_fic": cls.LITERARY_FICTION,
            
            # Business variations
            "entrepreneur": cls.BUSINESS,
            "entrepreneurship": cls.BUSINESS,
            "startup": cls.BUSINESS,
            
            # Biography variations
            "bio": cls.BIOGRAPHY,
            "life_story": cls.BIOGRAPHY,
            
            # Children's variations
            "kids": cls.CHILDREN,
            "childrens": cls.CHILDREN,
            "child": cls.CHILDREN,
            
            # Technology variations
            "tech": cls.TECHNOLOGY,
            "computers": cls.TECHNOLOGY,
            
            # Other common variations
            "nonfiction": cls.REFERENCE,
            "non_fiction": cls.REFERENCE,
        }
        
        # Check fuzzy matches
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching for compound terms (e.g., "fantasy romance" -> ROMANTASY)
        if "fantasy" in normalized_value and ("romance" in normalized_value or "romantic" in normalized_value):
            return cls.ROMANTASY
        elif "romance" in normalized_value and "fantasy" in normalized_value:
            return cls.ROMANTASY
        elif "dark" in normalized_value and "academia" in normalized_value:
            return cls.DARK_ACADEMIA
        elif "cozy" in normalized_value and "fantasy" in normalized_value:
            return cls.COZY_FANTASY
        elif "coming" in normalized_value and "age" in normalized_value:
            return cls.COMING_OF_AGE
        
        # Check if the normalized value contains any genre as a substring
        for genre in cls:
            if genre.value in normalized_value or normalized_value in genre.value:
                return genre
        
        # If no match found, raise descriptive error
        available_genres = [genre.value for genre in cls]
        raise ValueError(
            f"Unknown genre: '{value}'. "
            f"Available genres: {', '.join(sorted(available_genres[:10]))}..."
        )
    
    @classmethod
    def get_trending_genres(cls) -> List['GenreType']:
        """Get currently trending genres based on market research."""
        return [
            cls.ROMANTASY,
            cls.COZY_FANTASY,
            cls.DARK_ACADEMIA,
            cls.CLI_FI,
            cls.ROMANCE,
            cls.FANTASY,
            cls.TRUE_CRIME
        ]
    
    @classmethod
    def get_ai_friendly_genres(cls) -> List['GenreType']:
        """Get genres that work well for AI generation."""
        return [
            cls.ROMANCE,
            cls.FANTASY,
            cls.MYSTERY,
            cls.THRILLER,
            cls.SCIENCE_FICTION,
            cls.ROMANTASY,
            cls.YOUNG_ADULT,
            cls.SELF_HELP,
            cls.BUSINESS,
            cls.HEALTH,
            cls.TRAVEL,
            cls.COOKING
        ]
    
    @classmethod
    def get_high_roi_genres(cls) -> List['GenreType']:
        """Get genres with highest return on investment."""
        return [
            cls.ROMANCE,
            cls.FANTASY,
            cls.ROMANTASY,
            cls.MYSTERY,
            cls.PARANORMAL,
            cls.SELF_HELP
        ]
    
    def __str__(self) -> str:
        """String representation using display name."""
        return self.display_name
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"GenreType.{self.name}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'value': self.value,
            'display_name': self.display_name,
            'is_fiction': self.is_fiction,
            'is_high_demand': self.is_high_demand,
            'market_size': self.market_size
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GenreType':
        """Create from dictionary."""
        return cls(data['value'])


class SubGenreType(str, Enum):
    """All subgenres consolidated with comprehensive from_string support."""
    
    # Romance subgenres
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
    
    # Fantasy subgenres
    HIGH_FANTASY = "high_fantasy"
    URBAN_FANTASY = "urban_fantasy"
    DARK_FANTASY = "dark_fantasy"
    EPIC_FANTASY = "epic_fantasy"
    COZY_FANTASY_SUB = "cozy_fantasy_sub"
    ROMANTASY_SUB = "romantasy_sub"
    PORTAL_FANTASY = "portal_fantasy"
    FAIRY_TALE_RETELLING = "fairy_tale_retelling"
    SWORD_AND_SORCERY = "sword_and_sorcery"
    
    # Mystery/Thriller subgenres
    COZY_MYSTERY = "cozy_mystery"
    POLICE_PROCEDURAL = "police_procedural"
    DETECTIVE_FICTION = "detective_fiction"
    NOIR = "noir"
    PSYCHOLOGICAL_THRILLER = "psychological_thriller"
    DOMESTIC_THRILLER = "domestic_thriller"
    LEGAL_THRILLER = "legal_thriller"
    TECHNO_THRILLER = "techno_thriller"
    SPY_THRILLER = "spy_thriller"
    MEDICAL_THRILLER = "medical_thriller"
    
    # Science Fiction subgenres
    SPACE_OPERA = "space_opera"
    CYBERPUNK = "cyberpunk"
    DYSTOPIAN_SF = "dystopian_sf"
    HARD_SF = "hard_sf"
    SOFT_SF = "soft_sf"
    TIME_TRAVEL = "time_travel"
    POST_APOCALYPTIC = "post_apocalyptic"
    ALIEN_CONTACT = "alien_contact"
    BIOPUNK = "biopunk"
    CLI_FI_SUB = "cli_fi_sub"
    
    # Young Adult subgenres
    YA_FANTASY = "ya_fantasy"
    YA_ROMANCE = "ya_romance"
    YA_DYSTOPIAN = "ya_dystopian"
    YA_CONTEMPORARY = "ya_contemporary"
    YA_THRILLER = "ya_thriller"
    YA_SCIENCE_FICTION = "ya_science_fiction"
    COMING_OF_AGE_SUB = "coming_of_age_sub"
    YA_PARANORMAL = "ya_paranormal"
    YA_HISTORICAL = "ya_historical"
    
    # Horror subgenres
    PSYCHOLOGICAL_HORROR = "psychological_horror"
    SUPERNATURAL_HORROR = "supernatural_horror"
    GOTHIC_HORROR = "gothic_horror"
    COSMIC_HORROR = "cosmic_horror"
    BODY_HORROR = "body_horror"
    HAUNTED_HOUSE = "haunted_house"
    ZOMBIE = "zombie"
    VAMPIRE = "vampire"
    SLASHER = "slasher"
    
    # Non-Fiction subgenres
    MOTIVATIONAL = "motivational"
    PERSONAL_FINANCE = "personal_finance"
    CAREER_DEVELOPMENT = "career_development"
    RELATIONSHIP_ADVICE = "relationship_advice"
    MINDFULNESS = "mindfulness"
    PRODUCTIVITY = "productivity"
    ENTREPRENEURSHIP = "entrepreneurship"
    LEADERSHIP = "leadership"
    MARKETING = "marketing"
    BUSINESS_STRATEGY = "business_strategy"
    FITNESS = "fitness"
    NUTRITION = "nutrition"
    MENTAL_HEALTH = "mental_health"
    ALTERNATIVE_MEDICINE = "alternative_medicine"
    COOKING_SUB = "cooking_sub"
    TRAVEL_GUIDE = "travel_guide"
    DIY_CRAFTS = "diy_crafts"
    TECHNOLOGY_GUIDE = "technology_guide"
    TRUE_CRIME_SUB = "true_crime_sub"
    CELEBRITY_BIOGRAPHY = "celebrity_biography"
    HISTORICAL_BIOGRAPHY = "historical_biography"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").replace("sub", "").strip().title()
    
    @classmethod
    def from_string(cls, value: str) -> 'SubGenreType':
        """Create SubGenreType from string with comprehensive fuzzy matching.
        
        Args:
            value: String representation of the subgenre
            
        Returns:
            SubGenreType enum member
            
        Raises:
            ValueError: If the subgenre string is not recognized
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid subgenre value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for subgenre in cls:
            if subgenre.value == normalized_value:
                return subgenre
        
        # Fuzzy matching dictionary
        fuzzy_matches = {
            # Romance subgenres
            "contemporary": cls.CONTEMPORARY_ROMANCE,
            "historical": cls.HISTORICAL_ROMANCE,
            "paranormal": cls.PARANORMAL_ROMANCE,
            "suspense": cls.ROMANTIC_SUSPENSE,
            "dark": cls.DARK_ROMANCE,
            "comedy": cls.ROMANTIC_COMEDY,
            "sports": cls.SPORTS_ROMANCE,
            "billionaire": cls.BILLIONAIRE_ROMANCE,
            "enemies": cls.ENEMIES_TO_LOVERS,
            "second_chance": cls.SECOND_CHANCE_ROMANCE,
            
            # Fantasy subgenres
            "high": cls.HIGH_FANTASY,
            "urban": cls.URBAN_FANTASY,
            "epic": cls.EPIC_FANTASY,
            "cozy": cls.COZY_FANTASY_SUB,
            "romantasy": cls.ROMANTASY_SUB,
            "portal": cls.PORTAL_FANTASY,
            "fairy_tale": cls.FAIRY_TALE_RETELLING,
            "retelling": cls.FAIRY_TALE_RETELLING,
            "sword": cls.SWORD_AND_SORCERY,
            
            # Mystery/Thriller subgenres
            "cozy_mystery": cls.COZY_MYSTERY,
            "police": cls.POLICE_PROCEDURAL,
            "detective": cls.DETECTIVE_FICTION,
            "psychological": cls.PSYCHOLOGICAL_THRILLER,
            "domestic": cls.DOMESTIC_THRILLER,
            "legal": cls.LEGAL_THRILLER,
            "techno": cls.TECHNO_THRILLER,
            "spy": cls.SPY_THRILLER,
            "medical": cls.MEDICAL_THRILLER,
            
            # Science Fiction subgenres
            "space": cls.SPACE_OPERA,
            "cyber": cls.CYBERPUNK,
            "dystopian": cls.DYSTOPIAN_SF,
            "hard": cls.HARD_SF,
            "soft": cls.SOFT_SF,
            "time": cls.TIME_TRAVEL,
            "apocalyptic": cls.POST_APOCALYPTIC,
            "alien": cls.ALIEN_CONTACT,
            "bio": cls.BIOPUNK,
            "climate": cls.CLI_FI_SUB,
            
            # Non-fiction subgenres
            "motivation": cls.MOTIVATIONAL,
            "finance": cls.PERSONAL_FINANCE,
            "career": cls.CAREER_DEVELOPMENT,
            "relationship": cls.RELATIONSHIP_ADVICE,
            "meditation": cls.MINDFULNESS,
            "productivity": cls.PRODUCTIVITY,
            "entrepreneur": cls.ENTREPRENEURSHIP,
            "leadership": cls.LEADERSHIP,
            "marketing": cls.MARKETING,
            "strategy": cls.BUSINESS_STRATEGY,
            "fitness": cls.FITNESS,
            "nutrition": cls.NUTRITION,
            "mental_health": cls.MENTAL_HEALTH,
            "cooking": cls.COOKING_SUB,
            "travel": cls.TRAVEL_GUIDE,
            "diy": cls.DIY_CRAFTS,
            "tech": cls.TECHNOLOGY_GUIDE,
            "crime": cls.TRUE_CRIME_SUB,
            "celebrity": cls.CELEBRITY_BIOGRAPHY,
        }
        
        # Check fuzzy matches
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching for compound terms
        for key, subgenre in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return subgenre
        
        # Check if the normalized value contains any subgenre as a substring
        for subgenre in cls:
            clean_subgenre_value = subgenre.value.replace("_sub", "")
            if clean_subgenre_value in normalized_value or normalized_value in clean_subgenre_value:
                return subgenre
        
        # If no match found, raise descriptive error
        available_subgenres = [sg.value for sg in cls]
        raise ValueError(
            f"Unknown subgenre: '{value}'. "
            f"Available subgenres include: {', '.join(sorted(available_subgenres[:10]))}..."
        )
    
    def __str__(self) -> str:
        return self.display_name

@dataclass(frozen=True)
class GenreSubGenrePair:
    """Immutable pair representing a validated genre-subgenre combination."""
    genre: GenreType
    subgenre: SubGenreType
    
    def __post_init__(self):
        if not GenreMapping.is_valid_combination(self.genre, self.subgenre):
            raise ValueError(f"Invalid combination: {self.genre.value} with {self.subgenre.value}")
    
    @property
    def display_name(self) -> str:
        return f"{self.genre.display_name} - {self.subgenre.display_name}"
    
    def __str__(self) -> str:
        return f"{self.genre.value}/{self.subgenre.value}"


class GenreMapping:
    """Comprehensive mapping between genres and their valid subgenres."""
    
    # Master mapping of genres to their valid subgenres
    GENRE_SUBGENRE_MAP: Dict[GenreType, Set[SubGenreType]] = {
        GenreType.ROMANCE: {
            SubGenreType.CONTEMPORARY_ROMANCE,
            SubGenreType.HISTORICAL_ROMANCE,
            SubGenreType.PARANORMAL_ROMANCE,
            SubGenreType.ROMANTIC_SUSPENSE,
            SubGenreType.DARK_ROMANCE,
            SubGenreType.ROMANTIC_COMEDY,
            SubGenreType.SPORTS_ROMANCE,
            SubGenreType.BILLIONAIRE_ROMANCE,
            SubGenreType.ENEMIES_TO_LOVERS,
            SubGenreType.SECOND_CHANCE_ROMANCE,
        },
        
        GenreType.FANTASY: {
            SubGenreType.HIGH_FANTASY,
            SubGenreType.URBAN_FANTASY,
            SubGenreType.DARK_FANTASY,
            SubGenreType.EPIC_FANTASY,
            SubGenreType.PORTAL_FANTASY,
            SubGenreType.FAIRY_TALE_RETELLING,
            SubGenreType.SWORD_AND_SORCERY,
        },
        
        GenreType.ROMANTASY: {
            SubGenreType.ROMANTASY_SUB,
            SubGenreType.PARANORMAL_ROMANCE,
            SubGenreType.DARK_ROMANCE,
            SubGenreType.URBAN_FANTASY,
            SubGenreType.FAIRY_TALE_RETELLING,
        },
        
        GenreType.COZY_FANTASY: {
            SubGenreType.COZY_FANTASY_SUB,
        },
        
        GenreType.MYSTERY: {
            SubGenreType.COZY_MYSTERY,
            SubGenreType.POLICE_PROCEDURAL,
            SubGenreType.DETECTIVE_FICTION,
            SubGenreType.NOIR,
        },
        
        GenreType.THRILLER: {
            SubGenreType.PSYCHOLOGICAL_THRILLER,
            SubGenreType.DOMESTIC_THRILLER,
            SubGenreType.LEGAL_THRILLER,
            SubGenreType.TECHNO_THRILLER,
            SubGenreType.SPY_THRILLER,
            SubGenreType.MEDICAL_THRILLER,
        },
        
        GenreType.SCIENCE_FICTION: {
            SubGenreType.SPACE_OPERA,
            SubGenreType.CYBERPUNK,
            SubGenreType.DYSTOPIAN_SF,
            SubGenreType.HARD_SF,
            SubGenreType.SOFT_SF,
            SubGenreType.TIME_TRAVEL,
            SubGenreType.POST_APOCALYPTIC,
            SubGenreType.ALIEN_CONTACT,
            SubGenreType.BIOPUNK,
        },
        
        GenreType.CLI_FI: {
            SubGenreType.CLI_FI_SUB,
            SubGenreType.POST_APOCALYPTIC,
            SubGenreType.DYSTOPIAN_SF,
        },
        
        GenreType.YOUNG_ADULT: {
            SubGenreType.YA_FANTASY,
            SubGenreType.YA_ROMANCE,
            SubGenreType.YA_DYSTOPIAN,
            SubGenreType.YA_CONTEMPORARY,
            SubGenreType.YA_THRILLER,
            SubGenreType.YA_SCIENCE_FICTION,
            SubGenreType.YA_PARANORMAL,
            SubGenreType.YA_HISTORICAL,
        },
        
        GenreType.COMING_OF_AGE: {
            SubGenreType.COMING_OF_AGE_SUB,
            SubGenreType.YA_CONTEMPORARY,
        },
        
        GenreType.HORROR: {
            SubGenreType.PSYCHOLOGICAL_HORROR,
            SubGenreType.SUPERNATURAL_HORROR,
            SubGenreType.GOTHIC_HORROR,
            SubGenreType.COSMIC_HORROR,
            SubGenreType.BODY_HORROR,
            SubGenreType.HAUNTED_HOUSE,
            SubGenreType.ZOMBIE,
            SubGenreType.VAMPIRE,
            SubGenreType.SLASHER,
        },
        
        GenreType.SELF_HELP: {
            SubGenreType.MOTIVATIONAL,
            SubGenreType.PERSONAL_FINANCE,
            SubGenreType.CAREER_DEVELOPMENT,
            SubGenreType.RELATIONSHIP_ADVICE,
            SubGenreType.MINDFULNESS,
            SubGenreType.PRODUCTIVITY,
        },
        
        GenreType.BUSINESS: {
            SubGenreType.ENTREPRENEURSHIP,
            SubGenreType.LEADERSHIP,
            SubGenreType.MARKETING,
            SubGenreType.BUSINESS_STRATEGY,
        },
        
        GenreType.HEALTH: {
            SubGenreType.FITNESS,
            SubGenreType.NUTRITION,
            SubGenreType.MENTAL_HEALTH,
            SubGenreType.ALTERNATIVE_MEDICINE,
        },
        
        GenreType.COOKING: {
            SubGenreType.COOKING_SUB,
        },
        
        GenreType.TRAVEL: {
            SubGenreType.TRAVEL_GUIDE,
        },
        
        GenreType.TECHNOLOGY: {
            SubGenreType.TECHNOLOGY_GUIDE,
        },
        
        GenreType.TRUE_CRIME: {
            SubGenreType.TRUE_CRIME_SUB,
        },
        
        GenreType.BIOGRAPHY: {
            SubGenreType.CELEBRITY_BIOGRAPHY,
            SubGenreType.HISTORICAL_BIOGRAPHY,
        },
        
        # Add more mappings for other genres as needed
        GenreType.DYSTOPIAN: {
            SubGenreType.DYSTOPIAN_SF,
            SubGenreType.YA_DYSTOPIAN,
            SubGenreType.POST_APOCALYPTIC,
        },
        
        GenreType.PARANORMAL: {
            SubGenreType.PARANORMAL_ROMANCE,
            SubGenreType.SUPERNATURAL_HORROR,
            SubGenreType.YA_PARANORMAL,
            SubGenreType.VAMPIRE,
        },
        
        GenreType.CONTEMPORARY: {
            SubGenreType.CONTEMPORARY_ROMANCE,
            SubGenreType.YA_CONTEMPORARY,
        },
        
        GenreType.HISTORICAL_FICTION: {
            SubGenreType.HISTORICAL_ROMANCE,
            SubGenreType.YA_HISTORICAL,
            SubGenreType.HISTORICAL_BIOGRAPHY,
        },
    }
    
    @classmethod
    def get_subgenres(cls, genre: GenreType) -> Set[SubGenreType]:
        """Get all valid subgenres for a given genre."""
        return cls.GENRE_SUBGENRE_MAP.get(genre, set())
    
    @classmethod
    def get_subgenres_list(cls, genre: GenreType) -> List[SubGenreType]:
        """Get all valid subgenres for a given genre as a sorted list."""
        subgenres = cls.get_subgenres(genre)
        return sorted(subgenres, key=lambda x: x.display_name)
    
    @classmethod
    def get_genre_for_subgenre(cls, subgenre: SubGenreType) -> Optional[GenreType]:
        """Get the primary parent genre for a given subgenre."""
        for genre, subgenres in cls.GENRE_SUBGENRE_MAP.items():
            if subgenre in subgenres:
                return genre
        return None
    
    @classmethod
    def get_all_genres_for_subgenre(cls, subgenre: SubGenreType) -> List[GenreType]:
        """Get all parent genres for a given subgenre (some subgenres belong to multiple genres)."""
        genres = []
        for genre, subgenres in cls.GENRE_SUBGENRE_MAP.items():
            if subgenre in subgenres:
                genres.append(genre)
        return genres
    
    @classmethod
    def is_valid_combination(cls, genre: GenreType, subgenre: SubGenreType) -> bool:
        """Check if a genre-subgenre combination is valid."""
        return subgenre in cls.get_subgenres(genre)
    
    @classmethod
    def create_pair(cls, genre: GenreType, subgenre: SubGenreType) -> GenreSubGenrePair:
        """Create a validated genre-subgenre pair."""
        return GenreSubGenrePair(genre, subgenre)
    
    @classmethod
    def get_all_combinations(cls) -> List[GenreSubGenrePair]:
        """Get all valid genre-subgenre combinations."""
        combinations = []
        for genre, subgenres in cls.GENRE_SUBGENRE_MAP.items():
            for subgenre in subgenres:
                combinations.append(GenreSubGenrePair(genre, subgenre))
        return combinations
    
    @classmethod
    def get_trending_combinations(cls) -> List[GenreSubGenrePair]:
        """Get trending genre-subgenre combinations based on market research."""
        trending_pairs = [
            # Romance trending
            (GenreType.ROMANCE, SubGenreType.DARK_ROMANCE),
            (GenreType.ROMANCE, SubGenreType.ENEMIES_TO_LOVERS),
            (GenreType.ROMANCE, SubGenreType.BILLIONAIRE_ROMANCE),
            
            # Romantasy trending
            (GenreType.ROMANTASY, SubGenreType.ROMANTASY_SUB),
            (GenreType.ROMANTASY, SubGenreType.PARANORMAL_ROMANCE),
            
            # Fantasy trending
            (GenreType.COZY_FANTASY, SubGenreType.COZY_FANTASY_SUB),
            (GenreType.FANTASY, SubGenreType.FAIRY_TALE_RETELLING),
            
            # Thriller trending
            (GenreType.THRILLER, SubGenreType.PSYCHOLOGICAL_THRILLER),
            (GenreType.THRILLER, SubGenreType.DOMESTIC_THRILLER),
            
            # Mystery trending
            (GenreType.MYSTERY, SubGenreType.COZY_MYSTERY),
            
            # Non-fiction trending
            (GenreType.SELF_HELP, SubGenreType.MOTIVATIONAL),
            (GenreType.SELF_HELP, SubGenreType.MINDFULNESS),
            (GenreType.TRUE_CRIME, SubGenreType.TRUE_CRIME_SUB),
        ]
        
        return [cls.create_pair(genre, subgenre) for genre, subgenre in trending_pairs]
    
    @classmethod
    def get_ai_friendly_combinations(cls) -> List[GenreSubGenrePair]:
        """Get genre-subgenre combinations that are easier for AI to generate."""
        ai_friendly_pairs = [
            # Easy romance
            (GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE),
            (GenreType.ROMANCE, SubGenreType.ROMANTIC_COMEDY),
            
            # Easy fantasy
            (GenreType.COZY_FANTASY, SubGenreType.COZY_FANTASY_SUB),
            (GenreType.FANTASY, SubGenreType.FAIRY_TALE_RETELLING),
            
            # Easy non-fiction
            (GenreType.SELF_HELP, SubGenreType.MOTIVATIONAL),
            (GenreType.SELF_HELP, SubGenreType.PRODUCTIVITY),
            (GenreType.COOKING, SubGenreType.COOKING_SUB),
            (GenreType.TRAVEL, SubGenreType.TRAVEL_GUIDE),
            
            # Easy YA
            (GenreType.YOUNG_ADULT, SubGenreType.YA_CONTEMPORARY),
            (GenreType.COMING_OF_AGE, SubGenreType.COMING_OF_AGE_SUB),
        ]
        
        return [cls.create_pair(genre, subgenre) for genre, subgenre in ai_friendly_pairs]
    
    @classmethod
    def search_combinations(cls, 
                          genre_filter: Optional[GenreType] = None,
                          market_popularity: Optional[str] = None,
                          ai_friendly: bool = False) -> List[GenreSubGenrePair]:
        """Search for combinations based on various criteria."""
        all_combinations = cls.get_all_combinations()
        
        if genre_filter:
            all_combinations = [combo for combo in all_combinations if combo.genre == genre_filter]
        
        if ai_friendly:
            ai_friendly_combos = cls.get_ai_friendly_combinations()
            ai_friendly_set = {(combo.genre, combo.subgenre) for combo in ai_friendly_combos}
            all_combinations = [combo for combo in all_combinations 
                              if (combo.genre, combo.subgenre) in ai_friendly_set]
        
        return all_combinations
    
    @classmethod
    def get_statistics(cls) -> Dict[str, int]:
        """Get statistics about the genre-subgenre mappings."""
        total_genres = len(cls.GENRE_SUBGENRE_MAP)
        total_subgenres = len(set().union(*cls.GENRE_SUBGENRE_MAP.values()))
        total_combinations = sum(len(subgenres) for subgenres in cls.GENRE_SUBGENRE_MAP.values())
        
        return {
            "total_genres": total_genres,
            "unique_subgenres": total_subgenres,
            "total_combinations": total_combinations,
            "average_subgenres_per_genre": round(total_combinations / total_genres, 2)
        }
    
    @classmethod
    def to_json(cls) -> str:
        """Export mappings to JSON format."""
        export_data = {}
        for genre, subgenres in cls.GENRE_SUBGENRE_MAP.items():
            export_data[genre.value] = [sg.value for sg in subgenres]
        return json.dumps(export_data, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> None:
        """Import mappings from JSON format (for dynamic updates)."""
        # This would be used for dynamic mapping updates
        # Implementation would update the GENRE_SUBGENRE_MAP
        pass


# Example usage and testing
if __name__ == "__main__":
    print("=== Genre Mapping System Demo ===\n")
    
    # Test basic functionality
    romance_subgenres = GenreMapping.get_subgenres_list(GenreType.ROMANCE)
    print(f"Romance subgenres ({len(romance_subgenres)}):")
    for sg in romance_subgenres[:5]:  # Show first 5
        print(f"  - {sg.display_name}")
    print("  ...\n")
    
    # Test valid combination
    try:
        pair = GenreMapping.create_pair(GenreType.ROMANCE, SubGenreType.DARK_ROMANCE)
        print(f"✓ Valid combination: {pair.display_name}")
    except ValueError as e:
        print(f"✗ Invalid combination: {e}")
    
    # Test invalid combination
    try:
        invalid_pair = GenreMapping.create_pair(GenreType.ROMANCE, SubGenreType.SPACE_OPERA)
        print(f"✓ Valid combination: {invalid_pair.display_name}")
    except ValueError as e:
        print(f"✗ Expected invalid combination: {e}")
    
    print()
    
    # Show trending combinations
    trending = GenreMapping.get_trending_combinations()
    print(f"Trending combinations ({len(trending)}):")
    for combo in trending[:5]:
        print(f"  - {combo.display_name}")
    print("  ...\n")
    
    # Show AI-friendly combinations
    ai_friendly = GenreMapping.get_ai_friendly_combinations()
    print(f"AI-friendly combinations ({len(ai_friendly)}):")
    for combo in ai_friendly[:5]:
        print(f"  - {combo.display_name}")
    print("  ...\n")
    
    # Show statistics
    stats = GenreMapping.get_statistics()
    print("System Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n=== Total mappings created: {stats['total_combinations']} ===")