from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


class BookLength(str, Enum):
    """Comprehensive book length categories with industry-standard word counts for AI generation."""
    
    # MICRO CONTENT
    FLASH_FICTION = "flash_fiction"         # 100-1,000 words
    MICRO_FICTION = "micro_fiction"         # 50-300 words
    
    # SHORT FORM FICTION
    SHORT_STORY = "short_story"             # 1,000-7,500 words
    NOVELETTE = "novelette"                 # 7,500-17,500 words
    NOVELLA = "novella"                     # 17,500-40,000 words
    
    # NOVEL CATEGORIES
    SHORT_NOVEL = "short_novel"             # 40,000-60,000 words
    STANDARD_NOVEL = "standard_novel"       # 60,000-90,000 words
    LONG_NOVEL = "long_novel"               # 90,000-120,000 words
    EPIC_NOVEL = "epic_novel"               # 120,000-200,000 words
    MEGA_NOVEL = "mega_novel"               # 200,000+ words
    
    # CHILDREN'S LITERATURE
    BABY_BOARD_BOOK = "baby_board_book"     # 0-100 words
    TODDLER_PICTURE_BOOK = "toddler_picture_book"  # 100-500 words
    PICTURE_BOOK = "picture_book"           # 500-1,000 words
    EARLY_READER = "early_reader"           # 1,000-2,500 words
    CHAPTER_BOOK = "chapter_book"           # 3,000-10,000 words
    MIDDLE_GRADE = "middle_grade"           # 25,000-45,000 words
    UPPER_MIDDLE_GRADE = "upper_middle_grade"  # 40,000-65,000 words
    YOUNG_ADULT = "young_adult"             # 45,000-85,000 words
    NEW_ADULT = "new_adult"                 # 60,000-90,000 words
    
    # NON-FICTION CATEGORIES
    BLOG_POST = "blog_post"                 # 300-2,000 words
    ARTICLE = "article"                     # 500-3,000 words
    ESSAY = "essay"                         # 1,000-5,000 words
    LONG_FORM_ARTICLE = "long_form_article" # 3,000-10,000 words
    GUIDE = "guide"                         # 5,000-25,000 words
    SHORT_NON_FICTION = "short_non_fiction" # 25,000-50,000 words
    STANDARD_NON_FICTION = "standard_non_fiction"  # 50,000-80,000 words
    COMPREHENSIVE_NON_FICTION = "comprehensive_non_fiction"  # 80,000-150,000 words
    ACADEMIC_BOOK = "academic_book"         # 80,000-120,000 words
    REFERENCE_BOOK = "reference_book"       # 100,000-300,000 words
    
    # SPECIALIZED CATEGORIES
    SCREENPLAY = "screenplay"               # 15,000-25,000 words (90-120 pages)
    STAGE_PLAY = "stage_play"              # 15,000-30,000 words
    POETRY_CHAPBOOK = "poetry_chapbook"     # 500-1,500 words
    POETRY_COLLECTION = "poetry_collection" # 1,500-5,000 words
    GRAPHIC_NOVEL_SCRIPT = "graphic_novel_script"  # 10,000-30,000 words
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.FLASH_FICTION: "Flash Fiction",
            self.MICRO_FICTION: "Micro Fiction",
            self.SHORT_STORY: "Short Story",
            self.NOVELETTE: "Novelette",
            self.NOVELLA: "Novella",
            self.SHORT_NOVEL: "Short Novel",
            self.STANDARD_NOVEL: "Standard Novel",
            self.LONG_NOVEL: "Long Novel",
            self.EPIC_NOVEL: "Epic Novel",
            self.MEGA_NOVEL: "Mega Novel",
            self.BABY_BOARD_BOOK: "Baby Board Book",
            self.TODDLER_PICTURE_BOOK: "Toddler Picture Book",
            self.PICTURE_BOOK: "Picture Book",
            self.EARLY_READER: "Early Reader",
            self.CHAPTER_BOOK: "Chapter Book",
            self.MIDDLE_GRADE: "Middle Grade",
            self.UPPER_MIDDLE_GRADE: "Upper Middle Grade",
            self.YOUNG_ADULT: "Young Adult",
            self.NEW_ADULT: "New Adult",
            self.BLOG_POST: "Blog Post",
            self.ARTICLE: "Article",
            self.ESSAY: "Essay",
            self.LONG_FORM_ARTICLE: "Long-Form Article",
            self.GUIDE: "Guide",
            self.SHORT_NON_FICTION: "Short Non-Fiction",
            self.STANDARD_NON_FICTION: "Standard Non-Fiction",
            self.COMPREHENSIVE_NON_FICTION: "Comprehensive Non-Fiction",
            self.ACADEMIC_BOOK: "Academic Book",
            self.REFERENCE_BOOK: "Reference Book",
            self.SCREENPLAY: "Screenplay",
            self.STAGE_PLAY: "Stage Play",
            self.POETRY_CHAPBOOK: "Poetry Chapbook",
            self.POETRY_COLLECTION: "Poetry Collection",
            self.GRAPHIC_NOVEL_SCRIPT: "Graphic Novel Script",
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def word_count_range(self) -> Tuple[int, int]:
        """Get the word count range for this length category."""
        ranges = {
            # Micro content
            self.MICRO_FICTION: (50, 300),
            self.FLASH_FICTION: (100, 1000),
            
            # Short form fiction
            self.SHORT_STORY: (1000, 7500),
            self.NOVELETTE: (7500, 17500),
            self.NOVELLA: (17500, 40000),
            
            # Novel categories (updated based on 2024-2025 standards)
            self.SHORT_NOVEL: (40000, 60000),
            self.STANDARD_NOVEL: (60000, 90000),
            self.LONG_NOVEL: (90000, 120000),
            self.EPIC_NOVEL: (120000, 200000),
            self.MEGA_NOVEL: (200000, 500000),
            
            # Children's literature (based on current industry standards)
            self.BABY_BOARD_BOOK: (0, 100),
            self.TODDLER_PICTURE_BOOK: (100, 500),
            self.PICTURE_BOOK: (500, 1000),
            self.EARLY_READER: (1000, 2500),
            self.CHAPTER_BOOK: (3000, 10000),
            self.MIDDLE_GRADE: (25000, 45000),
            self.UPPER_MIDDLE_GRADE: (40000, 65000),
            self.YOUNG_ADULT: (45000, 85000),
            self.NEW_ADULT: (60000, 90000),
            
            # Non-fiction (trending shorter in 2024-2025)
            self.BLOG_POST: (300, 2000),
            self.ARTICLE: (500, 3000),
            self.ESSAY: (1000, 5000),
            self.LONG_FORM_ARTICLE: (3000, 10000),
            self.GUIDE: (5000, 25000),
            self.SHORT_NON_FICTION: (25000, 50000),
            self.STANDARD_NON_FICTION: (50000, 80000),
            self.COMPREHENSIVE_NON_FICTION: (80000, 150000),
            self.ACADEMIC_BOOK: (80000, 120000),
            self.REFERENCE_BOOK: (100000, 300000),
            
            # Specialized
            self.SCREENPLAY: (15000, 25000),
            self.STAGE_PLAY: (15000, 30000),
            self.POETRY_CHAPBOOK: (500, 1500),
            self.POETRY_COLLECTION: (1500, 5000),
            self.GRAPHIC_NOVEL_SCRIPT: (10000, 30000),
        }
        return ranges.get(self, (50000, 90000))
    
    @property
    def min_words(self) -> int:
        """Minimum word count for this category."""
        return self.word_count_range[0]
    
    @property
    def max_words(self) -> int:
        """Maximum word count for this category."""
        return self.word_count_range[1]
    
    @property
    def target_words(self) -> int:
        """Recommended target word count (midpoint of range)."""
        min_words, max_words = self.word_count_range
        return (min_words + max_words) // 2
    
    @property
    def target_age_range(self) -> Optional[str]:
        """Target age range for this book length category."""
        age_ranges = {
            # Children's literature
            self.BABY_BOARD_BOOK: "0-2 years",
            self.TODDLER_PICTURE_BOOK: "2-4 years",
            self.PICTURE_BOOK: "3-8 years",
            self.EARLY_READER: "5-8 years",
            self.CHAPTER_BOOK: "6-10 years",
            self.MIDDLE_GRADE: "8-12 years",
            self.UPPER_MIDDLE_GRADE: "10-14 years",
            self.YOUNG_ADULT: "12+ years",
            self.NEW_ADULT: "18-30 years",
            
            # Adult content
            self.SHORT_STORY: "Adult",
            self.NOVELETTE: "Adult", 
            self.NOVELLA: "Adult",
            self.SHORT_NOVEL: "Adult",
            self.STANDARD_NOVEL: "Adult",
            self.LONG_NOVEL: "Adult",
            self.EPIC_NOVEL: "Adult",
            self.MEGA_NOVEL: "Adult",
        }
        return age_ranges.get(self, None)
    
    @property
    def is_fiction(self) -> bool:
        """Whether this category is typically fiction."""
        fiction_categories = {
            self.MICRO_FICTION, self.FLASH_FICTION, self.SHORT_STORY,
            self.NOVELETTE, self.NOVELLA, self.SHORT_NOVEL, self.STANDARD_NOVEL,
            self.LONG_NOVEL, self.EPIC_NOVEL, self.MEGA_NOVEL,
            self.PICTURE_BOOK, self.EARLY_READER, self.CHAPTER_BOOK,
            self.MIDDLE_GRADE, self.UPPER_MIDDLE_GRADE, self.YOUNG_ADULT,
            self.NEW_ADULT, self.SCREENPLAY, self.STAGE_PLAY, self.GRAPHIC_NOVEL_SCRIPT
        }
        return self in fiction_categories
    
    @property
    def publishing_viability(self) -> str:
        """How viable this length is for traditional publishing."""
        high_viability = {
            self.STANDARD_NOVEL, self.MIDDLE_GRADE, self.YOUNG_ADULT,
            self.PICTURE_BOOK, self.STANDARD_NON_FICTION
        }
        moderate_viability = {
            self.SHORT_NOVEL, self.LONG_NOVEL, self.UPPER_MIDDLE_GRADE,
            self.COMPREHENSIVE_NON_FICTION, self.SHORT_NON_FICTION,
            self.EARLY_READER, self.CHAPTER_BOOK
        }
        low_viability = {
            self.NOVELLA, self.EPIC_NOVEL, self.MEGA_NOVEL,
            self.FLASH_FICTION, self.SHORT_STORY, self.NOVELETTE
        }
        
        if self in high_viability:
            return "high"
        elif self in moderate_viability:
            return "moderate"
        elif self in low_viability:
            return "low"
        else:
            return "specialized"
    
    @property
    def ai_generation_difficulty(self) -> str:
        """Difficulty level for AI to generate content of this length."""
        easy = {
            self.MICRO_FICTION, self.FLASH_FICTION, self.SHORT_STORY,
            self.BLOG_POST, self.ARTICLE, self.ESSAY, self.PICTURE_BOOK,
            self.POETRY_CHAPBOOK
        }
        medium = {
            self.NOVELETTE, self.EARLY_READER, self.CHAPTER_BOOK,
            self.GUIDE, self.SHORT_NON_FICTION, self.LONG_FORM_ARTICLE
        }
        hard = {
            self.NOVELLA, self.SHORT_NOVEL, self.MIDDLE_GRADE,
            self.STANDARD_NON_FICTION, self.YOUNG_ADULT
        }
        very_hard = {
            self.STANDARD_NOVEL, self.LONG_NOVEL, self.EPIC_NOVEL,
            self.MEGA_NOVEL, self.COMPREHENSIVE_NON_FICTION,
            self.ACADEMIC_BOOK, self.REFERENCE_BOOK
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
    def estimated_reading_time(self) -> str:
        """Estimated reading time for average reader (250 words/minute)."""
        target = self.target_words
        minutes = target / 250
        
        if minutes < 60:
            return f"{int(minutes)} minutes"
        elif minutes < 1440:  # Less than 24 hours
            hours = minutes / 60
            return f"{hours:.1f} hours"
        else:
            days = minutes / 1440
            return f"{days:.1f} days"
    
    @property
    def page_count_estimate(self) -> str:
        """Estimated page count (250 words per page standard)."""
        min_pages = self.min_words // 250
        max_pages = self.max_words // 250
        
        if min_pages == max_pages:
            return f"~{min_pages} pages"
        else:
            return f"{min_pages}-{max_pages} pages"
    
    @classmethod
    def from_string(cls, value: str) -> 'BookLength':
        """Create BookLength from string with comprehensive fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid book length value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for length in cls:
            if length.value == normalized_value:
                return length
        
        # Fuzzy matching with common variations
        fuzzy_matches = {
            # Fiction variations
            "flash": cls.FLASH_FICTION,
            "micro": cls.MICRO_FICTION,
            "short_story": cls.SHORT_STORY,
            "story": cls.SHORT_STORY,
            "novelette": cls.NOVELETTE,
            "novella": cls.NOVELLA,
            "short_novel": cls.SHORT_NOVEL,
            "novel": cls.STANDARD_NOVEL,
            "standard": cls.STANDARD_NOVEL,
            "long_novel": cls.LONG_NOVEL,
            "epic": cls.EPIC_NOVEL,
            "mega": cls.MEGA_NOVEL,
            
            # Children's book variations
            "board_book": cls.BABY_BOARD_BOOK,
            "baby": cls.BABY_BOARD_BOOK,
            "toddler": cls.TODDLER_PICTURE_BOOK,
            "picture": cls.PICTURE_BOOK,
            "early": cls.EARLY_READER,
            "chapter": cls.CHAPTER_BOOK,
            "middle_grade": cls.MIDDLE_GRADE,
            "mg": cls.MIDDLE_GRADE,
            "upper_mg": cls.UPPER_MIDDLE_GRADE,
            "young_adult": cls.YOUNG_ADULT,
            "ya": cls.YOUNG_ADULT,
            "new_adult": cls.NEW_ADULT,
            "na": cls.NEW_ADULT,
            
            # Non-fiction variations
            "blog": cls.BLOG_POST,
            "post": cls.BLOG_POST,
            "article": cls.ARTICLE,
            "essay": cls.ESSAY,
            "guide": cls.GUIDE,
            "non_fiction": cls.STANDARD_NON_FICTION,
            "nonfiction": cls.STANDARD_NON_FICTION,
            "business_book": cls.STANDARD_NON_FICTION,
            "self_help": cls.STANDARD_NON_FICTION,
            "memoir": cls.STANDARD_NON_FICTION,
            "biography": cls.COMPREHENSIVE_NON_FICTION,
            "academic": cls.ACADEMIC_BOOK,
            "textbook": cls.ACADEMIC_BOOK,
            "reference": cls.REFERENCE_BOOK,
            
            # Specialized variations
            "screenplay": cls.SCREENPLAY,
            "script": cls.SCREENPLAY,
            "play": cls.STAGE_PLAY,
            "poetry": cls.POETRY_COLLECTION,
            "poems": cls.POETRY_COLLECTION,
            "chapbook": cls.POETRY_CHAPBOOK,
            "graphic": cls.GRAPHIC_NOVEL_SCRIPT,
        }
        
        # Check fuzzy matches
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, length in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return length
        
        # Check if the normalized value contains any length as a substring
        for length in cls:
            clean_length_value = length.value.replace("_", "")
            clean_input = normalized_value.replace("_", "")
            if clean_length_value in clean_input or clean_input in clean_length_value:
                return length
        
        available_lengths = [length.value for length in cls]
        raise ValueError(
            f"Unknown book length: '{value}'. "
            f"Available lengths include: {', '.join(sorted(available_lengths[:10]))}..."
        )
    
    @classmethod
    def from_word_count(cls, word_count: int) -> 'BookLength':
        """Determine appropriate book length category from word count."""
        if not isinstance(word_count, int) or word_count < 0:
            raise ValueError(f"Word count must be a non-negative integer, got: {word_count}")
        
        # Find the best matching category
        best_match = None
        best_fit_score = float('inf')
        
        for length in cls:
            min_words, max_words = length.word_count_range
            
            if min_words <= word_count <= max_words:
                # Perfect fit - word count is within range
                return length
            
            # Calculate how far outside the range the word count is
            if word_count < min_words:
                distance = min_words - word_count
            else:  # word_count > max_words
                distance = word_count - max_words
            
            # Prefer closer matches
            if distance < best_fit_score:
                best_fit_score = distance
                best_match = length
        
        return best_match or cls.STANDARD_NOVEL  # Fallback
    
    @classmethod
    def get_children_categories(cls) -> List['BookLength']:
        """Get all children's book length categories."""
        return [
            cls.BABY_BOARD_BOOK, cls.TODDLER_PICTURE_BOOK, cls.PICTURE_BOOK,
            cls.EARLY_READER, cls.CHAPTER_BOOK, cls.MIDDLE_GRADE,
            cls.UPPER_MIDDLE_GRADE, cls.YOUNG_ADULT, cls.NEW_ADULT
        ]
    
    @classmethod
    def get_fiction_categories(cls) -> List['BookLength']:
        """Get all fiction length categories."""
        return [length for length in cls if length.is_fiction]
    
    @classmethod
    def get_non_fiction_categories(cls) -> List['BookLength']:
        """Get all non-fiction length categories."""
        return [length for length in cls if not length.is_fiction]
    
    @classmethod
    def get_ai_friendly_categories(cls) -> List['BookLength']:
        """Get categories that are easier for AI to generate."""
        return [length for length in cls if length.ai_generation_difficulty in ["easy", "medium"]]
    
    @classmethod
    def get_publishable_categories(cls) -> List['BookLength']:
        """Get categories with high publishing viability."""
        return [length for length in cls if length.publishing_viability == "high"]
    
    def is_appropriate_for_genre(self, genre: str) -> bool:
        """Check if this length is appropriate for a given genre."""
        genre_lower = genre.lower()
        
        # Genre-specific length preferences
        long_genres = ["fantasy", "science_fiction", "historical_fiction", "epic"]
        short_genres = ["romance", "mystery", "thriller", "contemporary"]
        children_genres = ["children", "middle_grade", "young_adult", "picture_book"]
        
        if any(g in genre_lower for g in long_genres):
            return self in [self.STANDARD_NOVEL, self.LONG_NOVEL, self.EPIC_NOVEL]
        elif any(g in genre_lower for g in short_genres):
            return self in [self.SHORT_NOVEL, self.STANDARD_NOVEL]
        elif any(g in genre_lower for g in children_genres):
            return self in self.get_children_categories()
        
        return True  # Default to allowing any length
    
    def __str__(self) -> str:
        return self.display_name
    
    def __repr__(self) -> str:
        return f"BookLength.{self.name}"


@dataclass
class LengthRecommendation:
    """Recommendation for book length based on genre and target audience."""
    length: BookLength
    compatibility_score: float
    reasons: List[str]
    
    def __str__(self) -> str:
        return f"{self.length.display_name} ({self.length.target_words:,} words) - Score: {self.compatibility_score:.1f}"


class LengthRecommender:
    """Recommends book lengths based on genre, audience, and publishing goals."""
    
    @classmethod
    def recommend_length(cls,
                        genre: Optional[str] = None,
                        target_audience: Optional[str] = None,
                        publishing_goal: Optional[str] = None,
                        ai_generation: bool = True) -> List[LengthRecommendation]:
        """
        Recommend book lengths based on criteria.
        
        Args:
            genre: Target genre (e.g., "fantasy", "romance", "mystery")
            target_audience: Target audience (e.g., "adult", "young_adult", "children")
            publishing_goal: Publishing goal (e.g., "traditional", "self", "web")
            ai_generation: Whether this is for AI generation
            
        Returns:
            List of length recommendations sorted by compatibility score
        """
        recommendations = []
        
        for length in BookLength:
            score = 0.0
            reasons = []
            
            # Genre compatibility (30% weight)
            if genre:
                if length.is_appropriate_for_genre(genre):
                    score += 30
                    reasons.append(f"Good fit for {genre}")
                
                # Special genre bonuses
                if "fantasy" in genre.lower() or "science_fiction" in genre.lower():
                    if length in [BookLength.STANDARD_NOVEL, BookLength.LONG_NOVEL, BookLength.EPIC_NOVEL]:
                        score += 10
                        reasons.append("Allows for world-building")
                
                if "romance" in genre.lower():
                    if length in [BookLength.SHORT_NOVEL, BookLength.STANDARD_NOVEL]:
                        score += 10
                        reasons.append("Perfect for romance pacing")
            
            # Target audience compatibility (25% weight)
            if target_audience:
                audience_lower = target_audience.lower()
                
                if "children" in audience_lower or "kid" in audience_lower:
                    if length in BookLength.get_children_categories():
                        score += 25
                        reasons.append(f"Designed for children")
                elif "young_adult" in audience_lower or "ya" in audience_lower:
                    if length == BookLength.YOUNG_ADULT:
                        score += 25
                        reasons.append("Perfect for YA audience")
                elif "adult" in audience_lower:
                    if length.target_age_range == "Adult" or length.target_age_range is None:
                        score += 25
                        reasons.append("Suitable for adult readers")
            
            # Publishing goal compatibility (25% weight)
            if publishing_goal:
                goal_lower = publishing_goal.lower()
                
                if "traditional" in goal_lower:
                    if length.publishing_viability == "high":
                        score += 25
                        reasons.append("High traditional publishing viability")
                    elif length.publishing_viability == "moderate":
                        score += 15
                        reasons.append("Moderate traditional publishing viability")
                elif "self" in goal_lower:
                    score += 20  # Self-publishing is more flexible
                    reasons.append("Flexible for self-publishing")
                elif "web" in goal_lower or "online" in goal_lower:
                    if length.ai_generation_difficulty in ["easy", "medium"]:
                        score += 25
                        reasons.append("Good for web/online publishing")
            
            # AI generation difficulty (20% weight)
            if ai_generation:
                ai_scores = {"easy": 20, "medium": 15, "hard": 10, "very_hard": 5}
                ai_score = ai_scores.get(length.ai_generation_difficulty, 0)
                score += ai_score
                reasons.append(f"AI difficulty: {length.ai_generation_difficulty}")
            
            if score > 0:
                recommendations.append(LengthRecommendation(length, score, reasons))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x.compatibility_score, reverse=True)
        return recommendations


# Example usage and testing
if __name__ == "__main__":
    print("=== Enhanced Book Length System Demo ===\n")
    
    # Test basic functionality
    standard_novel = BookLength.STANDARD_NOVEL
    print(f"Length: {standard_novel}")
    print(f"Word range: {standard_novel.word_count_range}")
    print(f"Target words: {standard_novel.target_words:,}")
    print(f"Reading time: {standard_novel.estimated_reading_time}")
    print(f"Page estimate: {standard_novel.page_count_estimate}")
    print(f"AI difficulty: {standard_novel.ai_generation_difficulty}")
    print(f"Publishing viability: {standard_novel.publishing_viability}")
    
    print("\n" + "="*50)
    
    # Test from_word_count
    test_word_counts = [500, 5000, 35000, 75000, 150000]
    print("Word count to length mapping:")
    for word_count in test_word_counts:
        length = BookLength.from_word_count(word_count)
        print(f"  {word_count:,} words -> {length} ({length.word_count_range})")
    
    print("\n" + "="*50)
    
    # Test from_string
    test_inputs = ["novel", "ya", "picture book", "short story", "memoir"]
    print("String to length mapping:")
    for test_input in test_inputs:
        try:
            length = BookLength.from_string(test_input)
            print(f"  '{test_input}' -> {length}")
        except ValueError as e:
            print(f"  '{test_input}' -> ERROR: {e}")
    
    print("\n" + "="*50)
    
    # Test recommendations
    print("Length recommendations for Fantasy YA:")
    recommendations = LengthRecommender.recommend_length(
        genre="fantasy",
        target_audience="young_adult",
        publishing_goal="traditional",
        ai_generation=True
    )
    
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. {rec}")
        print(f"   Reasons: {', '.join(rec.reasons)}")
        print()
    
    print("="*50)
    
    # Show categories
    print("AI-friendly categories:")
    for length in BookLength.get_ai_friendly_categories()[:8]:
        print(f"  - {length} ({length.target_words:,} words)")
    
    print(f"\nChildren's categories:")
    for length in BookLength.get_children_categories():
        print(f"  - {length} ({length.target_age_range})")