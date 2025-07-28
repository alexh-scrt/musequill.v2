from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


class StoryStructure(str, Enum):
    """Enhanced story structure types for AI book generation."""
    
    # Classic Structures
    THREE_ACT = "three_act"
    HERO_JOURNEY = "hero_journey"
    FREYTAG_PYRAMID = "freytag_pyramid"
    
    # Modern Structures
    SEVEN_POINT = "seven_point"
    SAVE_THE_CAT = "save_the_cat"
    STORY_CIRCLE = "story_circle"
    
    # Specialized Structures
    SNOWFLAKE = "snowflake"
    FICHTEAN_CURVE = "fichtean_curve"
    IN_MEDIAS_RES = "in_medias_res"
    KISHOTENKETSU = "kishotenketsu"  # Japanese four-act structure
    NESTED_LOOPS = "nested_loops"    # Multiple storylines
    
    # Genre-Specific Structures
    ROMANCE_BEAT_SHEET = "romance_beat_sheet"
    MYSTERY_STRUCTURE = "mystery_structure"
    THRILLER_PACING = "thriller_pacing"
    
    # Non-Traditional
    EPISODIC = "episodic"
    CIRCULAR = "circular"
    EXPERIMENTAL = "experimental"
    CUSTOM = "custom"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.THREE_ACT: "Three-Act Structure",
            self.HERO_JOURNEY: "Hero's Journey",
            self.FREYTAG_PYRAMID: "Freytag's Pyramid",
            self.SEVEN_POINT: "Seven-Point Story Structure",
            self.SAVE_THE_CAT: "Save the Cat Beat Sheet",
            self.SNOWFLAKE: "Snowflake Method",
            self.STORY_CIRCLE: "Story Circle",
            self.FICHTEAN_CURVE: "Fichtean Curve",
            self.IN_MEDIAS_RES: "In Medias Res",
            self.KISHOTENKETSU: "Kishotenketsu",
            self.NESTED_LOOPS: "Nested Loops",
            self.ROMANCE_BEAT_SHEET: "Romance Beat Sheet",
            self.MYSTERY_STRUCTURE: "Mystery Structure",
            self.THRILLER_PACING: "Thriller Pacing Structure",
            self.EPISODIC: "Episodic Structure",
            self.CIRCULAR: "Circular Structure",
            self.EXPERIMENTAL: "Experimental Structure",
            self.CUSTOM: "Custom Structure"
        }
        return names.get(self, self.value.replace("_", " ").title())

    @property
    def description(self) -> str:
        """Brief description of the structure."""
        descriptions = {
            self.THREE_ACT: "Classic beginning, middle, and end structure with setup, confrontation, and resolution",
            self.HERO_JOURNEY: "Joseph Campbell's monomyth pattern with departure, initiation, and return",
            self.FREYTAG_PYRAMID: "Five-part dramatic structure with exposition, rising action, climax, falling action, and denouement",
            self.SEVEN_POINT: "Dan Wells' structure focusing on character arc from beginning to end",
            self.SAVE_THE_CAT: "Blake Snyder's 15-beat screenplay structure adapted for novels",
            self.SNOWFLAKE: "Randy Ingermanson's step-by-step development method starting simple and expanding",
            self.STORY_CIRCLE: "Dan Harmon's simplified hero's journey with 8 steps",
            self.FICHTEAN_CURVE: "Rising action with multiple crisis points building to climax",
            self.IN_MEDIAS_RES: "Starting in the middle of action then revealing backstory",
            self.KISHOTENKETSU: "Japanese four-act structure: introduction, development, twist, conclusion",
            self.NESTED_LOOPS: "Multiple interconnected storylines that weave together",
            self.ROMANCE_BEAT_SHEET: "Romance-specific structure with meet-cute, conflict, and HEA",
            self.MYSTERY_STRUCTURE: "Mystery-focused structure with clues, red herrings, and revelation",
            self.THRILLER_PACING: "Fast-paced structure with constant tension and plot twists",
            self.EPISODIC: "Series of connected episodes or chapters with individual arcs",
            self.CIRCULAR: "Story that ends where it began, creating a complete circle",
            self.EXPERIMENTAL: "Non-traditional or innovative narrative structure",
            self.CUSTOM: "Create your own unique structure tailored to your story"
        }
        return descriptions.get(self, "")
    
    @property
    def complexity_level(self) -> str:
        """Complexity level for implementation and AI generation."""
        simple = {
            self.THREE_ACT, self.IN_MEDIAS_RES, self.EPISODIC, 
            self.CIRCULAR, self.CUSTOM
        }
        moderate = {
            self.HERO_JOURNEY, self.FREYTAG_PYRAMID, self.STORY_CIRCLE,
            self.ROMANCE_BEAT_SHEET, self.MYSTERY_STRUCTURE
        }
        complex = {
            self.SEVEN_POINT, self.SAVE_THE_CAT, self.FICHTEAN_CURVE,
            self.KISHOTENKETSU, self.NESTED_LOOPS, self.THRILLER_PACING
        }
        advanced = {
            self.SNOWFLAKE, self.EXPERIMENTAL
        }
        
        if self in simple:
            return "simple"
        elif self in moderate:
            return "moderate"
        elif self in complex:
            return "complex"
        else:
            return "advanced"
    
    @property
    def typical_length(self) -> str:
        """Typical story length this structure works best for."""
        short_form = {self.IN_MEDIAS_RES, self.KISHOTENKETSU, self.CIRCULAR}
        medium_form = {
            self.THREE_ACT, self.FREYTAG_PYRAMID, self.STORY_CIRCLE,
            self.ROMANCE_BEAT_SHEET, self.MYSTERY_STRUCTURE
        }
        long_form = {
            self.HERO_JOURNEY, self.SEVEN_POINT, self.SAVE_THE_CAT,
            self.FICHTEAN_CURVE, self.SNOWFLAKE, self.NESTED_LOOPS,
            self.THRILLER_PACING, self.EPISODIC
        }
        
        if self in short_form:
            return "short (under 50k words)"
        elif self in medium_form:
            return "medium (50k-80k words)"
        elif self in long_form:
            return "long (80k+ words)"
        else:
            return "flexible (any length)"
    
    @property
    def number_of_acts(self) -> int:
        """Number of major acts or sections in this structure."""
        act_counts = {
            self.THREE_ACT: 3,
            self.HERO_JOURNEY: 3,
            self.FREYTAG_PYRAMID: 5,
            self.SEVEN_POINT: 7,
            self.SAVE_THE_CAT: 3,  # Though it has 15 beats, it's still 3 acts
            self.STORY_CIRCLE: 8,
            self.KISHOTENKETSU: 4,
            self.FICHTEAN_CURVE: 1,  # Continuous rising action
            self.ROMANCE_BEAT_SHEET: 3,
            self.MYSTERY_STRUCTURE: 4,
            self.THRILLER_PACING: 3,
        }
        return act_counts.get(self, 3)  # Default to 3 acts
    
    @property
    def ai_generation_difficulty(self) -> str:
        """How difficult this structure is for AI to generate."""
        easy = {
            self.THREE_ACT, self.IN_MEDIAS_RES, self.EPISODIC,
            self.ROMANCE_BEAT_SHEET, self.CUSTOM
        }
        medium = {
            self.HERO_JOURNEY, self.FREYTAG_PYRAMID, self.STORY_CIRCLE,
            self.MYSTERY_STRUCTURE, self.CIRCULAR
        }
        hard = {
            self.SEVEN_POINT, self.SAVE_THE_CAT, self.FICHTEAN_CURVE,
            self.THRILLER_PACING, self.KISHOTENKETSU
        }
        very_hard = {
            self.SNOWFLAKE, self.NESTED_LOOPS, self.EXPERIMENTAL
        }
        
        if self in easy:
            return "easy"
        elif self in medium:
            return "medium"
        elif self in hard:
            return "hard"
        else:
            return "very_hard"
    
    @property
    def genre_compatibility(self) -> List[str]:
        """Genres that work particularly well with this structure."""
        compatibility = {
            self.THREE_ACT: ["all"],  # Universal
            self.HERO_JOURNEY: ["fantasy", "adventure", "science_fiction", "young_adult"],
            self.FREYTAG_PYRAMID: ["drama", "literary_fiction", "historical_fiction"],
            self.SEVEN_POINT: ["fantasy", "science_fiction", "mystery", "thriller"],
            self.SAVE_THE_CAT: ["comedy", "romance", "young_adult", "contemporary"],
            self.SNOWFLAKE: ["fantasy", "science_fiction", "epic_fantasy"],
            self.STORY_CIRCLE: ["comedy", "drama", "contemporary", "coming_of_age"],
            self.FICHTEAN_CURVE: ["thriller", "mystery", "suspense", "action"],
            self.IN_MEDIAS_RES: ["thriller", "mystery", "action", "war"],
            self.KISHOTENKETSU: ["literary_fiction", "slice_of_life", "experimental"],
            self.NESTED_LOOPS: ["epic_fantasy", "science_fiction", "literary_fiction"],
            self.ROMANCE_BEAT_SHEET: ["romance", "romantic_comedy", "contemporary_romance"],
            self.MYSTERY_STRUCTURE: ["mystery", "detective", "cozy_mystery", "noir"],
            self.THRILLER_PACING: ["thriller", "suspense", "action", "spy"],
            self.EPISODIC: ["adventure", "travel", "coming_of_age", "biographical"],
            self.CIRCULAR: ["literary_fiction", "experimental", "philosophical"],
            self.EXPERIMENTAL: ["literary_fiction", "postmodern", "experimental"],
            self.CUSTOM: ["all"]
        }
        return compatibility.get(self, ["general"])
    
    @classmethod
    def from_string(cls, value: str) -> 'StoryStructure':
        """Create StoryStructure from string with fuzzy matching.
        
        Args:
            value: String representation of the story structure
            
        Returns:
            StoryStructure enum member
            
        Raises:
            ValueError: If the structure string is not recognized
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid story structure value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for structure in cls:
            if structure.value == normalized_value:
                return structure
        
        # Fuzzy matching
        fuzzy_matches = {
            # Common variations
            "three_act": cls.THREE_ACT,
            "3_act": cls.THREE_ACT,
            "three_acts": cls.THREE_ACT,
            "hero": cls.HERO_JOURNEY,
            "heros_journey": cls.HERO_JOURNEY,
            "monomyth": cls.HERO_JOURNEY,
            "freytag": cls.FREYTAG_PYRAMID,
            "pyramid": cls.FREYTAG_PYRAMID,
            "seven_point": cls.SEVEN_POINT,
            "7_point": cls.SEVEN_POINT,
            "save_cat": cls.SAVE_THE_CAT,
            "beat_sheet": cls.SAVE_THE_CAT,
            "snowflake": cls.SNOWFLAKE,
            "story_circle": cls.STORY_CIRCLE,
            "circle": cls.STORY_CIRCLE,
            "fichtean": cls.FICHTEAN_CURVE,
            "medias_res": cls.IN_MEDIAS_RES,
            "middle": cls.IN_MEDIAS_RES,
            "kishotenketsu": cls.KISHOTENKETSU,
            "japanese": cls.KISHOTENKETSU,
            "nested": cls.NESTED_LOOPS,
            "loops": cls.NESTED_LOOPS,
            "romance": cls.ROMANCE_BEAT_SHEET,
            "mystery": cls.MYSTERY_STRUCTURE,
            "thriller": cls.THRILLER_PACING,
            "episodic": cls.EPISODIC,
            "episodes": cls.EPISODIC,
            "circular": cls.CIRCULAR,
            "experimental": cls.EXPERIMENTAL,
            "custom": cls.CUSTOM,
        }
        
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, structure in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return structure
        
        # Check if the normalized value contains any structure as a substring
        for structure in cls:
            if structure.value in normalized_value or normalized_value in structure.value:
                return structure
        
        available_structures = [s.value for s in cls]
        raise ValueError(
            f"Unknown story structure: '{value}'. "
            f"Available structures: {', '.join(sorted(available_structures[:10]))}..."
        )
    
    @classmethod
    def get_structures_for_genre(cls, genre: str) -> List['StoryStructure']:
        """Get recommended structures for a specific genre."""
        genre_lower = genre.lower()
        recommended = []
        
        for structure in cls:
            if "all" in structure.genre_compatibility or genre_lower in structure.genre_compatibility:
                recommended.append(structure)
        
        return recommended
    
    @classmethod
    def get_ai_friendly_structures(cls) -> List['StoryStructure']:
        """Get structures that are easier for AI to generate."""
        return [s for s in cls if s.ai_generation_difficulty in ["easy", "medium"]]
    
    @classmethod
    def get_structures_by_complexity(cls, complexity: str) -> List['StoryStructure']:
        """Get structures by complexity level."""
        return [s for s in cls if s.complexity_level == complexity.lower()]
    
    @classmethod
    def get_structures_by_length(cls, length_preference: str) -> List['StoryStructure']:
        """Get structures suitable for specific story lengths."""
        length_map = {
            "short": "short",
            "medium": "medium", 
            "long": "long",
            "novella": "medium",
            "novel": "long",
            "flash": "short"
        }
        
        target_length = length_map.get(length_preference.lower(), length_preference.lower())
        return [s for s in cls if target_length in s.typical_length.lower()]
    
    def get_structure_outline(self) -> List[str]:
        """Get a basic outline/beat list for this structure."""
        outlines = {
            self.THREE_ACT: [
                "Act I: Setup (25%)",
                "  - Inciting Incident",
                "  - Plot Point 1",
                "Act II: Confrontation (50%)",
                "  - Midpoint",
                "  - Plot Point 2",
                "Act III: Resolution (25%)",
                "  - Climax",
                "  - Denouement"
            ],
            self.HERO_JOURNEY: [
                "Ordinary World",
                "Call to Adventure", 
                "Refusal of the Call",
                "Meeting the Mentor",
                "Crossing the Threshold",
                "Tests, Allies, Enemies",
                "Approach to the Inmost Cave",
                "Ordeal",
                "Reward",
                "The Road Back",
                "Resurrection",
                "Return with the Elixir"
            ],
            self.FREYTAG_PYRAMID: [
                "Exposition",
                "Rising Action",
                "Climax",
                "Falling Action", 
                "Denouement"
            ],
            self.ROMANCE_BEAT_SHEET: [
                "Meet-Cute / First Meeting",
                "Initial Attraction",
                "First Conflict/Misunderstanding",
                "Growing Closer",
                "First Kiss/Physical Intimacy",
                "Major Conflict/Black Moment",
                "Realization of Love",
                "Grand Gesture",
                "Happy Ending"
            ]
        }
        
        return outlines.get(self, [f"Beat {i+1}" for i in range(self.number_of_acts)])
    
    def __str__(self) -> str:
        return self.display_name
    
    def __repr__(self) -> str:
        return f"StoryStructure.{self.name}"


@dataclass
class StructureRecommendation:
    """Recommendation for story structure based on genre and preferences."""
    structure: StoryStructure
    compatibility_score: float
    reasons: List[str]
    
    def __str__(self) -> str:
        return f"{self.structure.display_name} (Score: {self.compatibility_score:.1f})"


class StructureRecommender:
    """Recommends story structures based on genre and preferences."""
    
    @classmethod
    def recommend_structure(cls, 
                          genre: str,
                          length_preference: Optional[str] = None,
                          complexity_preference: Optional[str] = None,
                          ai_generation: bool = True) -> List[StructureRecommendation]:
        """
        Recommend story structures based on criteria.
        
        Args:
            genre: Target genre
            length_preference: Preferred story length
            complexity_preference: Preferred complexity level
            ai_generation: Whether this is for AI generation
            
        Returns:
            List of structure recommendations sorted by compatibility score
        """
        recommendations = []
        
        for structure in StoryStructure:
            score = 0.0
            reasons = []
            
            # Genre compatibility (40% weight)
            if "all" in structure.genre_compatibility:
                score += 40
                reasons.append("Universal structure")
            elif genre.lower() in structure.genre_compatibility:
                score += 40
                reasons.append(f"Excellent for {genre}")
            elif any(g in genre.lower() for g in structure.genre_compatibility):
                score += 20
                reasons.append(f"Good for similar genres")
            
            # Length compatibility (20% weight)
            if length_preference:
                if length_preference.lower() in structure.typical_length.lower():
                    score += 20
                    reasons.append(f"Perfect for {length_preference} stories")
                elif "flexible" in structure.typical_length:
                    score += 10
                    reasons.append("Flexible length")
            
            # Complexity preference (20% weight)
            if complexity_preference:
                if complexity_preference.lower() == structure.complexity_level:
                    score += 20
                    reasons.append(f"Matches {complexity_preference} complexity")
                elif abs(["simple", "moderate", "complex", "advanced"].index(complexity_preference.lower()) - 
                        ["simple", "moderate", "complex", "advanced"].index(structure.complexity_level)) <= 1:
                    score += 10
                    reasons.append("Similar complexity level")
            
            # AI generation difficulty (20% weight)
            if ai_generation:
                ai_scores = {"easy": 20, "medium": 15, "hard": 10, "very_hard": 5}
                score += ai_scores.get(structure.ai_generation_difficulty, 0)
                reasons.append(f"AI difficulty: {structure.ai_generation_difficulty}")
            
            if score > 0:
                recommendations.append(StructureRecommendation(structure, score, reasons))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x.compatibility_score, reverse=True)
        return recommendations


# Example usage and testing
if __name__ == "__main__":
    print("=== Story Structure Enhancement Demo ===\n")
    
    # Test basic functionality
    structure = StoryStructure.THREE_ACT
    print(f"Structure: {structure}")
    print(f"Description: {structure.description}")
    print(f"Complexity: {structure.complexity_level}")
    print(f"Typical Length: {structure.typical_length}")
    print(f"AI Difficulty: {structure.ai_generation_difficulty}")
    print(f"Genre Compatibility: {', '.join(structure.genre_compatibility)}")
    
    print(f"\nOutline for {structure}:")
    for beat in structure.get_structure_outline():
        print(f"  {beat}")
    
    print("\n" + "="*50)
    
    # Test from_string functionality
    test_inputs = ["three act", "hero's journey", "romance", "mystery structure", "experimental"]
    
    print("Testing from_string method:")
    for test_input in test_inputs:
        try:
            result = StoryStructure.from_string(test_input)
            print(f"✓ '{test_input}' -> {result}")
        except ValueError as e:
            print(f"✗ '{test_input}' -> {e}")
    
    print("\n" + "="*50)
    
    # Test recommendations
    print("Structure Recommendations for Romance:")
    recommendations = StructureRecommender.recommend_structure(
        genre="romance",
        length_preference="medium",
        complexity_preference="simple",
        ai_generation=True
    )
    
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. {rec}")
        print(f"   Reasons: {', '.join(rec.reasons)}")
        print()
    
    print("="*50)
    
    # Test genre-specific filtering
    fantasy_structures = StoryStructure.get_structures_for_genre("fantasy")
    print(f"Recommended structures for Fantasy ({len(fantasy_structures)}):")
    for struct in fantasy_structures[:5]:
        print(f"  - {struct} ({struct.complexity_level})")
    
    print(f"\nAI-friendly structures ({len(StoryStructure.get_ai_friendly_structures())}):")
    for struct in StoryStructure.get_ai_friendly_structures():
        print(f"  - {struct}")