from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import re


class PacingStyle(str, Enum):
    """Comprehensive story pacing preferences for different narrative approaches."""
    
    # BASIC PACING STYLES
    FAST_PACED = "fast_paced"
    MODERATE_PACED = "moderate_paced"
    SLOW_BURN = "slow_burn"
    VARIABLE = "variable"
    BREAKNECK = "breakneck"
    LEISURELY = "leisurely"
    MEASURED = "measured"
    ESCALATING = "escalating"
    
    # RHYTHM & TEMPO STYLES
    RHYTHMIC = "rhythmic"
    STACCATO = "staccato"
    FLOWING = "flowing"
    SYNCOPATED = "syncopated"
    ACCELERATING = "accelerating"
    DECELERATING = "decelerating"
    PULSING = "pulsing"
    STEADY = "steady"
    
    # TENSION-BASED PACING
    BUILDING_TENSION = "building_tension"
    CONSTANT_TENSION = "constant_tension"
    TENSION_RELEASE = "tension_release"
    PRESSURE_COOKER = "pressure_cooker"
    EXPLOSIVE = "explosive"
    SIMMERING = "simmering"
    CRESCENDO = "crescendo"
    WAVES = "waves"
    
    # STRUCTURAL PACING
    EPISODIC = "episodic"
    CHAPTER_DRIVEN = "chapter_driven"
    SCENE_FOCUSED = "scene_focused"
    MONTAGE = "montage"
    CYCLICAL = "cyclical"
    LINEAR = "linear"
    FRAGMENTED = "fragmented"
    LAYERED = "layered"
    
    # GENRE-SPECIFIC PACING
    THRILLER_PACE = "thriller_pace"
    MYSTERY_PACE = "mystery_pace"
    ROMANCE_PACE = "romance_pace"
    HORROR_PACE = "horror_pace"
    ADVENTURE_PACE = "adventure_pace"
    LITERARY_PACE = "literary_pace"
    COMEDY_PACE = "comedy_pace"
    DRAMA_PACE = "drama_pace"
    
    # EMOTIONAL PACING
    CONTEMPLATIVE = "contemplative"
    URGENT = "urgent"
    BREATHLESS = "breathless"
    MEDITATIVE = "meditative"
    FRANTIC = "frantic"
    CALM = "calm"
    INTENSE = "intense"
    RELAXED = "relaxed"
    
    # CINEMATIC PACING
    CINEMATIC = "cinematic"
    MONTAGE_STYLE = "montage_style"
    SLOW_MOTION = "slow_motion"
    QUICK_CUTS = "quick_cuts"
    ESTABLISHING = "establishing"
    CHASE_SEQUENCE = "chase_sequence"
    DIALOGUE_HEAVY = "dialogue_heavy"
    ACTION_PACKED = "action_packed"
    
    # READER ENGAGEMENT STYLES
    PAGE_TURNER = "page_turner"
    THOUGHTFUL = "thoughtful"
    IMMERSIVE = "immersive"
    CLIFFHANGER_DRIVEN = "cliffhanger_driven"
    HOOK_HEAVY = "hook_heavy"
    REVELATION_BASED = "revelation_based"
    ANTICIPATION_BUILDING = "anticipation_building"
    SATISFYING = "satisfying"
    
    # NARRATIVE FLOW STYLES
    SEAMLESS = "seamless"
    CHOPPY = "choppy"
    INTERRUPTED = "interrupted"
    STREAM_LIKE = "stream_like"
    PUNCTUATED = "punctuated"
    CONTINUOUS = "continuous"
    STOP_AND_START = "stop_and_start"
    UNDULATING = "undulating"

    @property
    def display_name(self) -> str:
        """Return a human-readable display name for the pacing style."""
        # Handle special cases for better display names
        special_cases = {
            "fast_paced": "Fast-Paced",
            "moderate_paced": "Moderate-Paced", 
            "slow_burn": "Slow Burn",
            "page_turner": "Page-Turner",
            "stop_and_start": "Stop-and-Start",
            "thriller_pace": "Thriller Pace",
            "mystery_pace": "Mystery Pace",
            "romance_pace": "Romance Pace",
            "horror_pace": "Horror Pace",
            "adventure_pace": "Adventure Pace",
            "literary_pace": "Literary Pace",
            "comedy_pace": "Comedy Pace",
            "drama_pace": "Drama Pace",
            "montage_style": "Montage Style",
            "slow_motion": "Slow Motion",
            "quick_cuts": "Quick Cuts",
            "chase_sequence": "Chase Sequence",
            "dialogue_heavy": "Dialogue Heavy",
            "action_packed": "Action Packed",
            "cliffhanger_driven": "Cliffhanger Driven",
            "hook_heavy": "Hook Heavy",
            "revelation_based": "Revelation Based",
            "anticipation_building": "Anticipation Building",
            "stream_like": "Stream-Like",
        }
        
        if self.value in special_cases:
            return special_cases[self.value]
        
        # Default formatting: replace underscores with spaces and title case
        return self.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        """Return a detailed description of the pacing style."""
        descriptions = {
            "fast_paced": "Quick, energetic narrative flow with rapid scene changes and minimal downtime",
            "moderate_paced": "Balanced pacing with a mix of action and reflection, suitable for most readers",
            "slow_burn": "Gradual build-up with deliberate pacing, focusing on character development and atmosphere",
            "variable": "Dynamic pacing that changes throughout the story based on narrative needs",
            "breakneck": "Extremely fast pacing with non-stop action and intensity",
            "leisurely": "Relaxed, unhurried pacing that allows readers to savor details and atmosphere",
            "measured": "Carefully controlled pacing with deliberate timing and rhythm",
            "escalating": "Gradually increasing pace that builds to climactic moments",
            "rhythmic": "Pacing that follows a consistent, musical-like rhythm throughout",
            "staccato": "Short, sharp bursts of action separated by brief pauses",
            "flowing": "Smooth, continuous narrative flow without jarring transitions",
            "syncopated": "Irregular pacing with unexpected beats and rhythms",
            "accelerating": "Steadily increasing pace throughout the narrative",
            "decelerating": "Gradually slowing pace, often toward resolution",
            "pulsing": "Alternating between fast and slow moments in regular intervals",
            "steady": "Consistent, unchanging pace maintained throughout",
            "building_tension": "Pacing designed to gradually increase suspense and anticipation",
            "constant_tension": "Maintaining high tension throughout without relief",
            "tension_release": "Alternating between high tension and moments of relief",
            "pressure_cooker": "Intense, building pressure with delayed release",
            "explosive": "Sudden bursts of intense action or revelation",
            "simmering": "Low-level tension that slowly builds beneath the surface",
            "crescendo": "Building to a powerful climax with increasing intensity and volume",
            "waves": "Pacing that rises and falls like ocean waves",
            "episodic": "Structured around distinct episodes or segments",
            "chapter_driven": "Pacing controlled by chapter structure and breaks",
            "scene_focused": "Emphasis on individual scenes with clear pacing within each",
            "montage": "Quick succession of scenes or images to show passage of time",
            "cyclical": "Returning to similar pacing patterns throughout the story",
            "linear": "Straightforward, chronological pacing without jumps",
            "fragmented": "Broken up pacing with gaps and jumps in narrative flow",
            "layered": "Multiple pacing levels operating simultaneously",
            "thriller_pace": "Fast-paced with constant danger and suspense",
            "mystery_pace": "Deliberate pacing with clues revealed at strategic moments",
            "romance_pace": "Alternating between tension and intimate moments",
            "horror_pace": "Building dread with moments of shock and terror",
            "adventure_pace": "Exciting, fast-moving with frequent action sequences",
            "literary_pace": "Thoughtful pacing that emphasizes language and meaning",
            "comedy_pace": "Timing focused on humor with setup and punchline rhythm",
            "drama_pace": "Emotional pacing that builds to dramatic confrontations",
            "contemplative": "Slow, thoughtful pacing encouraging reflection",
            "urgent": "Fast pacing that creates sense of immediate need",
            "breathless": "Extremely fast pacing that leaves readers breathless",
            "meditative": "Peaceful, reflective pacing for inner contemplation",
            "frantic": "Chaotic, overwhelming pace that mirrors character stress",
            "calm": "Peaceful, unrushed pacing that soothes the reader",
            "intense": "High-energy pacing that demands full attention",
            "relaxed": "Easy-going pace that doesn't pressure the reader",
            "cinematic": "Pacing that mimics film techniques and timing",
            "montage_style": "Quick cuts between scenes like a film montage",
            "slow_motion": "Deliberately slowed pacing for dramatic effect",
            "quick_cuts": "Rapid transitions between scenes and perspectives",
            "establishing": "Slower pacing to set up scenes and atmosphere",
            "chase_sequence": "Fast-paced action focused on pursuit and escape",
            "dialogue_heavy": "Pacing controlled by conversation and character interaction",
            "action_packed": "Continuous action with minimal downtime",
            "page_turner": "Addictive pacing that compels continued reading",
            "thoughtful": "Pacing that encourages deep thinking and analysis",
            "immersive": "Pacing designed to fully absorb the reader",
            "cliffhanger_driven": "Pacing structured around suspenseful chapter endings",
            "hook_heavy": "Frequent compelling moments to maintain interest",
            "revelation_based": "Pacing controlled by strategic information reveals",
            "anticipation_building": "Pacing designed to create expectation and excitement",
            "satisfying": "Pacing that provides emotional fulfillment",
            "seamless": "Smooth transitions without noticeable pacing shifts",
            "choppy": "Abrupt changes in pacing and narrative flow",
            "interrupted": "Pacing broken by flashbacks, asides, or other interruptions",
            "stream_like": "Continuous flow like a stream of consciousness",
            "punctuated": "Regular breaks or pauses in the narrative flow",
            "continuous": "Unbroken pacing without major interruptions",
            "stop_and_start": "Alternating between action and complete stops",
            "undulating": "Gentle rises and falls in pacing like rolling hills",
        }
        
        return descriptions.get(self.value, f"A {self.display_name.lower()} approach to story pacing")

    @property
    def intensity_level(self) -> str:
        """Return the intensity level of this pacing style."""
        high_intensity = {
            "breakneck", "explosive", "frantic", "breathless", "urgent", 
            "thriller_pace", "action_packed", "chase_sequence", "constant_tension",
            "pressure_cooker", "intense", "quick_cuts", "page_turner"
        }
        
        low_intensity = {
            "leisurely", "slow_burn", "contemplative", "meditative", "calm",
            "relaxed", "literary_pace", "thoughtful", "establishing", "slow_motion"
        }
        
        if self.value in high_intensity:
            return "high"
        elif self.value in low_intensity:
            return "low"
        else:
            return "medium"

    @property
    def typical_genres(self) -> List[str]:
        """Return genres that typically use this pacing style."""
        genre_mappings = {
            "fast_paced": ["action", "thriller", "adventure", "science fiction"],
            "moderate_paced": ["general fiction", "contemporary", "young adult", "romance"],
            "slow_burn": ["literary fiction", "character study", "historical", "mystery"],
            "variable": ["epic fantasy", "literary fiction", "complex narratives"],
            "breakneck": ["action thriller", "suspense", "spy fiction"],
            "leisurely": ["literary fiction", "memoir", "pastoral", "slice of life"],
            "measured": ["literary fiction", "historical", "philosophical"],
            "escalating": ["thriller", "horror", "suspense", "mystery"],
            "thriller_pace": ["thriller", "suspense", "crime", "espionage"],
            "mystery_pace": ["mystery", "detective", "cozy mystery", "procedural"],
            "romance_pace": ["romance", "romantic comedy", "historical romance"],
            "horror_pace": ["horror", "supernatural", "gothic", "psychological thriller"],
            "adventure_pace": ["adventure", "action", "quest fantasy", "survival"],
            "literary_pace": ["literary fiction", "experimental", "philosophical"],
            "comedy_pace": ["comedy", "satire", "humorous fiction", "romantic comedy"],
            "drama_pace": ["drama", "family saga", "contemporary fiction"],
            "contemplative": ["literary fiction", "philosophical", "spiritual"],
            "urgent": ["thriller", "disaster", "medical drama", "crisis fiction"],
            "breathless": ["action", "chase thriller", "fast-paced suspense"],
            "meditative": ["spiritual", "philosophical", "nature writing"],
            "frantic": ["psychological thriller", "crisis drama", "urban fiction"],
            "calm": ["pastoral", "slice of life", "gentle fiction"],
            "intense": ["psychological drama", "high-stakes thriller"],
            "relaxed": ["cozy mystery", "comfort fiction", "gentle romance"],
            "cinematic": ["techno-thriller", "blockbuster fiction", "movie tie-ins"],
            "page_turner": ["commercial fiction", "bestsellers", "beach reads"],
            "thoughtful": ["book club fiction", "literary", "philosophical"],
            "immersive": ["fantasy epic", "science fiction", "world-building heavy"],
            "cliffhanger_driven": ["serial fiction", "chapter books", "episodic"],
        }
        
        return genre_mappings.get(self.value, ["general fiction"])

    @classmethod
    def from_string(cls, pacing_string: str) -> "PacingStyle":
        """
        Convert a string description into a PacingStyle enum value.
        
        Supports direct value matching, display name matching, and fuzzy matching
        with common synonyms and related terms.
        
        Args:
            pacing_string: String description of pacing style
            
        Returns:
            Matching PacingStyle enum value
            
        Raises:
            ValueError: If no suitable match is found
        """
        if not pacing_string or not isinstance(pacing_string, str):
            raise ValueError("Invalid pacing style value")
        
        # Clean and normalize input
        cleaned_value = pacing_string.strip().lower()
        
        # Direct enum value match first
        for style in cls:
            if style.value == cleaned_value:
                return style
        
        # Display name match
        for style in cls:
            if style.display_name.lower() == cleaned_value:
                return style
        
        # Fuzzy matching with synonyms
        fuzzy_mappings = {
            # Speed terms
            "fast": cls.FAST_PACED,
            "quick": cls.FAST_PACED,
            "rapid": cls.FAST_PACED,
            "speedy": cls.FAST_PACED,
            "slow": cls.SLOW_BURN,
            "gradual": cls.SLOW_BURN,
            "moderate": cls.MODERATE_PACED,
            "medium": cls.MODERATE_PACED,
            "balanced": cls.MODERATE_PACED,
            
            # Intensity terms
            "intense": cls.INTENSE,
            "extreme": cls.BREAKNECK,
            "wild": cls.FRANTIC,
            "crazy": cls.FRANTIC,
            "calm": cls.CALM,
            "peaceful": cls.CALM,
            "relaxed": cls.RELAXED,
            "chill": cls.RELAXED,
            
            # Rhythm terms
            "steady": cls.STEADY,
            "consistent": cls.STEADY,
            "flowing": cls.FLOWING,
            "smooth": cls.SEAMLESS,
            "choppy": cls.CHOPPY,
            "jerky": cls.CHOPPY,
            
            # Tension terms
            "tense": cls.BUILDING_TENSION,
            "suspenseful": cls.BUILDING_TENSION,
            "explosive": cls.EXPLOSIVE,
            "dramatic": cls.DRAMA_PACE,
            
            # Genre-related
            "thriller": cls.THRILLER_PACE,
            "thrill": cls.THRILLER_PACE,
            "mystery": cls.MYSTERY_PACE,
            "romance": cls.ROMANCE_PACE,
            "horror": cls.HORROR_PACE,
            "adventure": cls.ADVENTURE_PACE,
            "literary": cls.LITERARY_PACE,
            "comedy": cls.COMEDY_PACE,
            "funny": cls.COMEDY_PACE,
            "dramatic": cls.DRAMA_PACE,
            
            # Reader experience
            "addictive": cls.PAGE_TURNER,
            "compelling": cls.PAGE_TURNER,
            "engaging": cls.IMMERSIVE,
            "absorbing": cls.IMMERSIVE,
            "thoughtful": cls.THOUGHTFUL,
            "reflective": cls.CONTEMPLATIVE,
        }
        
        # Check fuzzy mappings
        if cleaned_value in fuzzy_mappings:
            return fuzzy_mappings[cleaned_value]
        
        # Check if any part of the input matches a mapping
        for key, style in fuzzy_mappings.items():
            if key in cleaned_value or cleaned_value in key:
                return style
        
        # No match found
        raise ValueError(f"No matching pacing style found for: {pacing_string}")

    @classmethod
    def get_high_intensity_styles(cls) -> List["PacingStyle"]:
        """Return pacing styles with high intensity levels."""
        return [style for style in cls if style.intensity_level == "high"]

    @classmethod
    def get_low_intensity_styles(cls) -> List["PacingStyle"]:
        """Return pacing styles with low intensity levels."""
        return [style for style in cls if style.intensity_level == "low"]

    @classmethod
    def get_genre_specific_styles(cls) -> List["PacingStyle"]:
        """Return pacing styles that are genre-specific."""
        genre_styles = {
            cls.THRILLER_PACE, cls.MYSTERY_PACE, cls.ROMANCE_PACE,
            cls.HORROR_PACE, cls.ADVENTURE_PACE, cls.LITERARY_PACE,
            cls.COMEDY_PACE, cls.DRAMA_PACE
        }
        return list(genre_styles)

    @classmethod
    def get_cinematic_styles(cls) -> List["PacingStyle"]:
        """Return pacing styles that use cinematic techniques."""
        cinematic_styles = {
            cls.CINEMATIC, cls.MONTAGE_STYLE, cls.SLOW_MOTION,
            cls.QUICK_CUTS, cls.CHASE_SEQUENCE, cls.MONTAGE
        }
        return list(cinematic_styles)

    @classmethod
    def get_reader_engagement_styles(cls) -> List["PacingStyle"]:
        """Return pacing styles focused on reader engagement."""
        engagement_styles = {
            cls.PAGE_TURNER, cls.IMMERSIVE, cls.CLIFFHANGER_DRIVEN,
            cls.HOOK_HEAVY, cls.ANTICIPATION_BUILDING, cls.SATISFYING
        }
        return list(engagement_styles)

    def __str__(self) -> str:
        """Return the display name when converted to string."""
        return self.display_name

    def __repr__(self) -> str:
        """Return a detailed representation of the pacing style."""
        return f"PacingStyle.{self.name}"