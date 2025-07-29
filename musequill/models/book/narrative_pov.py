from enum import Enum
from typing import List, Dict


class NarrativePOV(str, Enum):
    """
    Comprehensive point of view options for narrative writing.
    
    Each POV defines the relationship between narrator, characters, and reader,
    affecting intimacy, reliability, scope, and storytelling possibilities.
    """
    
    # Traditional POVs
    FIRST_PERSON = "first_person"
    SECOND_PERSON = "second_person"  
    THIRD_PERSON_LIMITED = "third_person_limited"
    THIRD_PERSON_OMNISCIENT = "third_person_omniscient"
    THIRD_PERSON_OBJECTIVE = "third_person_objective"
    
    # Multiple Perspective POVs
    MULTIPLE_POV = "multiple_pov"
    ALTERNATING_POV = "alternating_pov"
    ROTATING_POV = "rotating_pov"
    DUAL_POV = "dual_pov"
    
    # Specialized Narrative Forms
    EPISTOLARY = "epistolary"
    STREAM_OF_CONSCIOUSNESS = "stream_of_consciousness"
    FRAME_NARRATIVE = "frame_narrative"
    UNRELIABLE_NARRATOR = "unreliable_narrator"
    
    # Distance and Temporal POVs
    CLOSE_THIRD_PERSON = "close_third_person"
    DISTANT_THIRD_PERSON = "distant_third_person"
    PRESENT_TENSE_FIRST = "present_tense_first"
    PAST_TENSE_FIRST = "past_tense_first"
    FUTURE_TENSE = "future_tense"
    
    # Contemporary and Experimental POVs
    SOCIAL_MEDIA = "social_media"
    MULTIMEDIA_NARRATIVE = "multimedia_narrative"
    COLLECTIVE_VOICE = "collective_voice"
    ANTHROPOMORPHIC = "anthropomorphic"
    INANIMATE_NARRATOR = "inanimate_narrator"
    
    # Specialized Literary POVs
    DRAMATIC_MONOLOGUE = "dramatic_monologue"
    INTERIOR_MONOLOGUE = "interior_monologue"
    FREE_INDIRECT_DISCOURSE = "free_indirect_discourse"
    CINEMATIC_POV = "cinematic_pov"

    @property
    def display_name(self) -> str:
        """Human-readable name for the POV."""
        names = {
            self.FIRST_PERSON: "First Person",
            self.SECOND_PERSON: "Second Person", 
            self.THIRD_PERSON_LIMITED: "Third Person Limited",
            self.THIRD_PERSON_OMNISCIENT: "Third Person Omniscient",
            self.THIRD_PERSON_OBJECTIVE: "Third Person Objective",
            self.MULTIPLE_POV: "Multiple POV",
            self.ALTERNATING_POV: "Alternating POV",
            self.ROTATING_POV: "Rotating POV",
            self.DUAL_POV: "Dual POV",
            self.EPISTOLARY: "Epistolary",
            self.STREAM_OF_CONSCIOUSNESS: "Stream of Consciousness",
            self.FRAME_NARRATIVE: "Frame Narrative",
            self.UNRELIABLE_NARRATOR: "Unreliable Narrator",
            self.CLOSE_THIRD_PERSON: "Close Third Person",
            self.DISTANT_THIRD_PERSON: "Distant Third Person",
            self.PRESENT_TENSE_FIRST: "Present Tense First Person",
            self.PAST_TENSE_FIRST: "Past Tense First Person",
            self.FUTURE_TENSE: "Future Tense",
            self.SOCIAL_MEDIA: "Social Media Format",
            self.MULTIMEDIA_NARRATIVE: "Multimedia Narrative",
            self.COLLECTIVE_VOICE: "Collective Voice",
            self.ANTHROPOMORPHIC: "Anthropomorphic Narrator",
            self.INANIMATE_NARRATOR: "Inanimate Narrator",
            self.DRAMATIC_MONOLOGUE: "Dramatic Monologue",
            self.INTERIOR_MONOLOGUE: "Interior Monologue",
            self.FREE_INDIRECT_DISCOURSE: "Free Indirect Discourse",
            self.CINEMATIC_POV: "Cinematic POV"
        }
        return names.get(self, self.value.replace('_', ' ').title())

    @property
    def description(self) -> str:
        """Detailed description of the POV and its characteristics."""
        descriptions = {
            self.FIRST_PERSON: "Narrator tells their own story using 'I', 'me', 'my'. Creates intimacy and authenticity but limits perspective to one character's knowledge and experience.",
            
            self.SECOND_PERSON: "Addresses the reader directly as 'you', making them a character in the story. Rare but powerful for immersive or instructional narratives.",
            
            self.THIRD_PERSON_LIMITED: "Narrator uses 'he/she/they' but stays within one character's perspective, accessing only their thoughts, feelings, and observations.",
            
            self.THIRD_PERSON_OMNISCIENT: "All-knowing narrator who can access any character's thoughts, jump between perspectives, and provide information beyond any single character's knowledge.",
            
            self.THIRD_PERSON_OBJECTIVE: "Narrator reports only observable actions and dialogue without revealing internal thoughts or feelings of any character, like a camera recording events.",
            
            self.MULTIPLE_POV: "Story told through several different characters' perspectives, each providing their unique viewpoint on events, often in separate chapters or sections.",
            
            self.ALTERNATING_POV: "Systematic switching between two or more character perspectives, often following a pattern or structure throughout the narrative.",
            
            self.ROTATING_POV: "Cyclical movement through multiple character perspectives, giving each narrator roughly equal narrative time and importance.",
            
            self.DUAL_POV: "Story told through exactly two character perspectives, often representing different sides of a conflict or relationship.",
            
            self.EPISTOLARY: "Story told through documents like letters, diary entries, emails, text messages, or other written records, creating authenticity and immediacy.",
            
            self.STREAM_OF_CONSCIOUSNESS: "Unfiltered flow of a character's thoughts and perceptions, mimicking the natural, often chaotic patterns of human consciousness.",
            
            self.FRAME_NARRATIVE: "Story within a story structure, where an outer narrator introduces and contains an inner narrative, often adding layers of meaning and perspective.",
            
            self.UNRELIABLE_NARRATOR: "Narrator whose credibility is compromised due to mental state, bias, limited knowledge, or deliberate deception, requiring readers to question the truth.",
            
            self.CLOSE_THIRD_PERSON: "Third person narration that stays very close to one character's consciousness, almost like first person but using third person pronouns.",
            
            self.DISTANT_THIRD_PERSON: "Third person narration that maintains emotional and psychological distance from characters, providing a more objective, overview perspective.",
            
            self.PRESENT_TENSE_FIRST: "First person narration in present tense, creating immediacy and urgency as events unfold in real-time from the narrator's perspective.",
            
            self.PAST_TENSE_FIRST: "Traditional first person narration in past tense, where the narrator reflects on events that have already occurred, allowing for hindsight and reflection.",
            
            self.FUTURE_TENSE: "Rare narration that tells the story as if it will happen, creating a prophetic or predetermined quality to events.",
            
            self.SOCIAL_MEDIA: "Story told through social media posts, comments, messages, and digital interactions, reflecting contemporary communication patterns.",
            
            self.MULTIMEDIA_NARRATIVE: "Story incorporates various media formats like emails, news articles, transcripts, photos, and documents to tell the story through multiple channels.",
            
            self.COLLECTIVE_VOICE: "Narration from a group perspective using 'we' or representing the voice of a community, family, or collective entity.",
            
            self.ANTHROPOMORPHIC: "Story told from the perspective of animals, plants, or other non-human entities given human-like consciousness and voice.",
            
            self.INANIMATE_NARRATOR: "Narration from the perspective of objects, places, or abstract concepts, offering unique and often philosophical viewpoints on human experience.",
            
            self.DRAMATIC_MONOLOGUE: "Single character speaks continuously to a silent listener or audience, revealing character and situation through their speech patterns and content.",
            
            self.INTERIOR_MONOLOGUE: "Direct presentation of a character's unspoken thoughts, typically more organized and coherent than stream of consciousness.",
            
            self.FREE_INDIRECT_DISCOURSE: "Blends third person narration with a character's consciousness, allowing access to thoughts and feelings while maintaining narrative distance.",
            
            self.CINEMATIC_POV: "Narration that mimics film techniques with visual focus, scene cuts, and objective observation, emphasizing what can be seen and heard."
        }
        return descriptions.get(self, f"Point of view using {self.display_name.lower()} perspective.")

    @property
    def advantages(self) -> List[str]:
        """Key advantages of using this POV."""
        advantages_map = {
            self.FIRST_PERSON: ["High intimacy", "Authentic voice", "Reader identification", "Emotional immediacy"],
            self.SECOND_PERSON: ["Reader immersion", "Unique perspective", "Direct engagement", "Memorable impact"],
            self.THIRD_PERSON_LIMITED: ["Balance of intimacy and objectivity", "Clear focus", "Manageable scope", "Reader empathy"],
            self.THIRD_PERSON_OMNISCIENT: ["Complete story access", "Multiple perspectives", "Broad scope", "Narrative flexibility"],
            self.THIRD_PERSON_OBJECTIVE: ["Unbiased presentation", "Reader interpretation", "Dramatic tension", "Mystery potential"],
            self.MULTIPLE_POV: ["Rich character development", "Complex storytelling", "Multiple truths", "Broad perspective"],
            self.EPISTOLARY: ["Authenticity", "Multiple voices", "Historical feel", "Documentary realism"],
            self.STREAM_OF_CONSCIOUSNESS: ["Psychological depth", "Realistic thought patterns", "Artistic expression", "Character intimacy"],
            self.UNRELIABLE_NARRATOR: ["Reader engagement", "Mystery and suspense", "Complex characterization", "Multiple interpretations"]
        }
        return advantages_map.get(self, ["Unique narrative perspective", "Distinctive storytelling approach"])

    @property
    def challenges(self) -> List[str]:
        """Key challenges or limitations of this POV."""
        challenges_map = {
            self.FIRST_PERSON: ["Limited perspective", "Knowledge restrictions", "Potential monotony", "Narrator must survive"],
            self.SECOND_PERSON: ["Reader resistance", "Difficult to maintain", "Limited applications", "Can feel gimmicky"],
            self.THIRD_PERSON_LIMITED: ["Restricted information", "Single viewpoint limitations", "Potential bias", "Knowledge gaps"],
            self.THIRD_PERSON_OMNISCIENT: ["Head-hopping risks", "Maintaining consistency", "Overwhelming scope", "Distance from characters"],
            self.THIRD_PERSON_OBJECTIVE: ["Emotional distance", "Limited interiority", "Reader confusion", "Challenging characterization"],
            self.MULTIPLE_POV: ["Complex structure", "Uneven character development", "Reader confusion", "Pacing challenges"],
            self.EPISTOLARY: ["Format limitations", "Credibility issues", "Pacing problems", "Character voice consistency"],
            self.STREAM_OF_CONSCIOUSNESS: ["Reader difficulty", "Lack of structure", "Potential confusion", "Editing challenges"],
            self.UNRELIABLE_NARRATOR: ["Reader frustration", "Truth revelation timing", "Character consistency", "Plot confusion"]
        }
        return challenges_map.get(self, ["Requires careful execution", "May not suit all stories"])

    @property
    def suitable_genres(self) -> List[str]:
        """Genres where this POV works particularly well."""
        genre_map = {
            self.FIRST_PERSON: ["memoir", "young_adult", "mystery", "horror", "romance", "coming_of_age"],
            self.SECOND_PERSON: ["experimental", "choose_your_own_adventure", "self_help", "instructional"],
            self.THIRD_PERSON_LIMITED: ["literary_fiction", "romance", "mystery", "fantasy", "contemporary"],
            self.THIRD_PERSON_OMNISCIENT: ["epic_fantasy", "historical_fiction", "family_saga", "literary_fiction"],
            self.THIRD_PERSON_OBJECTIVE: ["crime", "thriller", "literary_fiction", "short_stories"],
            self.MULTIPLE_POV: ["epic_fantasy", "family_drama", "historical_fiction", "ensemble_stories"],
            self.EPISTOLARY: ["historical_fiction", "horror", "romance", "young_adult", "literary_fiction"],
            self.STREAM_OF_CONSCIOUSNESS: ["literary_fiction", "modernist", "psychological_fiction", "experimental"],
            self.SOCIAL_MEDIA: ["contemporary", "young_adult", "satire", "thriller", "romance"],
            self.UNRELIABLE_NARRATOR: ["mystery", "psychological_thriller", "literary_fiction", "horror"]
        }
        return genre_map.get(self, ["general_fiction", "literary_fiction"])

    @property
    def complexity_level(self) -> str:
        """Writing difficulty level for this POV."""
        complexity_map = {
            self.FIRST_PERSON: "beginner",
            self.THIRD_PERSON_LIMITED: "beginner", 
            self.THIRD_PERSON_OBJECTIVE: "intermediate",
            self.THIRD_PERSON_OMNISCIENT: "intermediate",
            self.MULTIPLE_POV: "advanced",
            self.SECOND_PERSON: "advanced",
            self.EPISTOLARY: "intermediate",
            self.STREAM_OF_CONSCIOUSNESS: "expert",
            self.UNRELIABLE_NARRATOR: "advanced",
            self.FREE_INDIRECT_DISCOURSE: "expert",
            self.FRAME_NARRATIVE: "advanced"
        }
        return complexity_map.get(self, "intermediate")

    @classmethod
    def get_beginner_povs(cls) -> List['NarrativePOV']:
        """Get POVs suitable for beginning writers."""
        return [pov for pov in cls if pov.complexity_level == "beginner"]

    @classmethod
    def get_povs_for_genre(cls, genre: str) -> List['NarrativePOV']:
        """Get recommended POVs for a specific genre."""
        genre_lower = genre.lower()
        return [pov for pov in cls if genre_lower in [g.lower() for g in pov.suitable_genres]]

    @classmethod
    def get_experimental_povs(cls) -> List['NarrativePOV']:
        """Get experimental or unconventional POVs."""
        return [
            cls.SECOND_PERSON, cls.STREAM_OF_CONSCIOUSNESS, cls.SOCIAL_MEDIA,
            cls.MULTIMEDIA_NARRATIVE, cls.COLLECTIVE_VOICE, cls.ANTHROPOMORPHIC,
            cls.INANIMATE_NARRATOR, cls.FUTURE_TENSE
        ]

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"NarrativePOV.{self.name}"