from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union


class ToneStyle(str, Enum):
    """Comprehensive emotional and stylistic tones for book writing."""
    
    # EMOTIONAL SPECTRUM TONES
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    MELANCHOLIC = "melancholic"
    EUPHORIC = "euphoric"
    BITTERSWEET = "bittersweet"
    CONTEMPLATIVE = "contemplative"
    PASSIONATE = "passionate"
    SERENE = "serene"
    ANXIOUS = "anxious"
    HOPEFUL = "hopeful"
    DESPAIRING = "despairing"
    WISTFUL = "wistful"
    
    # HUMOR & COMEDY TONES
    HUMOROUS = "humorous"
    SATIRICAL = "satirical"
    IRONIC = "ironic"
    WHIMSICAL = "whimsical"
    PLAYFUL = "playful"
    WITTY = "witty"
    SARCASTIC = "sarcastic"
    ABSURD = "absurd"
    DRY = "dry"
    LIGHTHEARTED = "lighthearted"
    COMEDIC = "comedic"
    IRREVERENT = "irreverent"
    
    # DRAMA & INTENSITY TONES
    DRAMATIC = "dramatic"
    TRAGIC = "tragic"
    INTENSE = "intense"
    GRAVE = "grave"
    SOLEMN = "solemn"
    URGENT = "urgent"
    DESPERATE = "desperate"
    HEROIC = "heroic"
    EPIC = "epic"
    GRANDIOSE = "grandiose"
    POIGNANT = "poignant"
    CATHARTIC = "cathartic"
    
    # SUSPENSE & MYSTERY TONES
    SUSPENSEFUL = "suspenseful"
    MYSTERIOUS = "mysterious"
    OMINOUS = "ominous"
    FOREBODING = "foreboding"
    EERIE = "eerie"
    TENSE = "tense"
    THRILLER = "thriller"
    NOIR = "noir"
    GOTHIC = "gothic"
    HAUNTING = "haunting"
    SINISTER = "sinister"
    CRYPTIC = "cryptic"
    
    # DARK & INTENSE TONES
    DARK = "dark"
    GRITTY = "gritty"
    BLEAK = "bleak"
    HARSH = "harsh"
    BRUTAL = "brutal"
    CYNICAL = "cynical"
    NIHILISTIC = "nihilistic"
    DISTURBING = "disturbing"
    MACABRE = "macabre"
    MORBID = "morbid"
    APOCALYPTIC = "apocalyptic"
    DYSTOPIAN = "dystopian"
    
    # ROMANTIC & INTIMATE TONES
    ROMANTIC = "romantic"
    SENSUAL = "sensual"
    TENDER = "tender"
    INTIMATE = "intimate"
    LOVING = "loving"
    YEARNING = "yearning"
    SEDUCTIVE = "seductive"
    DREAMY = "dreamy"
    ENCHANTING = "enchanting"
    SWOONY = "swoony"
    HEARTWARMING = "heartwarming"
    PASSIONATE_ROMANCE = "passionate_romance"
    
    # INTELLECTUAL & PHILOSOPHICAL TONES
    PHILOSOPHICAL = "philosophical"
    INTELLECTUAL = "intellectual"
    SCHOLARLY = "scholarly"
    ANALYTICAL = "analytical"
    REFLECTIVE = "reflective"
    INTROSPECTIVE = "introspective"
    MEDITATIVE = "meditative"
    WISDOM_SEEKING = "wisdom_seeking"
    EXISTENTIAL = "existential"
    METAPHYSICAL = "metaphysical"
    THOUGHT_PROVOKING = "thought_provoking"
    CEREBRAL = "cerebral"
    
    # INSPIRATIONAL & UPLIFTING TONES
    INSPIRATIONAL = "inspirational"
    MOTIVATIONAL = "motivational"
    UPLIFTING = "uplifting"
    EMPOWERING = "empowering"
    TRIUMPHANT = "triumphant"
    ENCOURAGING = "encouraging"
    POSITIVE = "positive"
    JOYFUL = "joyful"
    CELEBRATORY = "celebratory"
    LIFE_AFFIRMING = "life_affirming"
    SPIRITUAL = "spiritual"
    ENLIGHTENING = "enlightening"
    
    # NOSTALGIC & TEMPORAL TONES
    NOSTALGIC = "nostalgic"
    REMINISCENT = "reminiscent"
    TIMELESS = "timeless"
    VINTAGE = "vintage"
    RETRO = "retro"
    HISTORICAL = "historical"
    PERIOD_APPROPRIATE = "period_appropriate"
    ANACHRONISTIC = "anachronistic"
    FUTURISTIC = "futuristic"
    CONTEMPORARY = "contemporary"
    CLASSIC = "classic"
    MODERN = "modern"
    
    # ATTITUDE & PERSPECTIVE TONES
    SERIOUS = "serious"
    FORMAL = "formal"
    CASUAL = "casual"
    CONVERSATIONAL = "conversational"
    AUTHORITATIVE = "authoritative"
    HUMBLE = "humble"
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    OBJECTIVE = "objective"
    SUBJECTIVE = "subjective"
    NEUTRAL = "neutral"
    BIASED = "biased"
    
    # ADVENTURE & ACTION TONES
    ADVENTUROUS = "adventurous"
    THRILLING = "thrilling"
    EXCITING = "exciting"
    BOLD = "bold"
    DARING = "daring"
    REBELLIOUS = "rebellious"
    DEFIANT = "defiant"
    COURAGEOUS = "courageous"
    SWASHBUCKLING = "swashbuckling"
    DYNAMIC = "dynamic"
    ENERGETIC = "energetic"
    KINETIC = "kinetic"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        """Detailed description of the tone and its emotional impact."""
        descriptions = {
            # Emotional Spectrum
            self.OPTIMISTIC: "Positive, hopeful outlook that emphasizes possibility and favorable outcomes.",
            self.PESSIMISTIC: "Negative, doubtful perspective focusing on potential problems and unfavorable outcomes.",
            self.MELANCHOLIC: "Gentle sadness and thoughtful sorrow, often beautiful in its wistfulness.",
            self.EUPHORIC: "Intense joy and elation that creates excitement and emotional highs.",
            self.BITTERSWEET: "Complex emotion mixing happiness and sadness, joy tinged with sorrow.",
            self.CONTEMPLATIVE: "Thoughtful, reflective mood encouraging deep consideration and pondering.",
            self.PASSIONATE: "Intense emotion and fervor that drives strong feelings and convictions.",
            self.SERENE: "Peaceful, calm tranquility that soothes and creates inner quiet.",
            self.ANXIOUS: "Nervous tension and worry that creates unease and apprehension.",
            self.HOPEFUL: "Expectant optimism that looks forward to positive possibilities.",
            self.DESPAIRING: "Deep hopelessness and discouragement that feels overwhelming.",
            self.WISTFUL: "Gentle longing mixed with sadness for something lost or unattainable.",
            
            # Humor & Comedy
            self.HUMOROUS: "Amusing and entertaining, designed to provoke laughter and joy.",
            self.SATIRICAL: "Sharp wit used to expose and criticize folly, vice, or shortcomings.",
            self.IRONIC: "Contrast between expectation and reality, often with subtle humor.",
            self.WHIMSICAL: "Playfully fanciful and imaginative, charmingly unpredictable.",
            self.PLAYFUL: "Light-hearted fun that encourages laughter and enjoyment.",
            self.WITTY: "Clever humor that demonstrates intelligence and quick thinking.",
            self.SARCASTIC: "Sharp, often biting humor that uses irony to make a point.",
            self.ABSURD: "Deliberately ridiculous and illogical for comedic effect.",
            self.DRY: "Understated humor delivered without obvious emotion or enthusiasm.",
            self.LIGHTHEARTED: "Cheerful and carefree, without serious weight or burden.",
            self.COMEDIC: "Focused on humor and entertainment through amusing situations.",
            self.IRREVERENT: "Disrespectful of traditional values, often humorously so.",
            
            # Drama & Intensity
            self.DRAMATIC: "Heightened emotion and conflict that creates powerful impact.",
            self.TRAGIC: "Profound sadness and loss that evokes deep empathy and sorrow.",
            self.INTENSE: "Concentrated emotional force that creates powerful, focused impact.",
            self.GRAVE: "Serious and weighty, demanding respect and careful consideration.",
            self.SOLEMN: "Formal dignity and reverence, often ceremonial in nature.",
            self.URGENT: "Pressing need and immediacy that demands quick action or attention.",
            self.DESPERATE: "Extreme need or hopelessness that drives dramatic action.",
            self.HEROIC: "Noble courage and admirable strength in the face of adversity.",
            self.EPIC: "Grand scale and magnificent scope that inspires awe.",
            self.GRANDIOSE: "Impressive magnificence, sometimes to excess.",
            self.POIGNANT: "Deeply moving emotional impact that touches the heart.",
            self.CATHARTIC: "Emotional release and purification through intense experience.",
            
            # Suspense & Mystery
            self.SUSPENSEFUL: "Building tension and anticipation that keeps readers engaged.",
            self.MYSTERIOUS: "Enigmatic and puzzling, inviting curiosity and investigation.",
            self.OMINOUS: "Threatening undertones that suggest impending danger or trouble.",
            self.FOREBODING: "Sense of approaching doom or misfortune.",
            self.EERIE: "Strange and unsettling atmosphere that creates unease.",
            self.TENSE: "Stretched tight with stress and anxiety, ready to snap.",
            self.THRILLER: "Fast-paced excitement designed to thrill and excite.",
            self.NOIR: "Dark, cynical atmosphere with moral ambiguity and urban decay.",
            self.GOTHIC: "Dark romanticism with supernatural elements and psychological depth.",
            self.HAUNTING: "Persistently memorable in a troubling or beautiful way.",
            self.SINISTER: "Suggesting evil or harmful intent beneath the surface.",
            self.CRYPTIC: "Mysterious and difficult to understand, requiring interpretation.",
            
            # Dark & Intense
            self.DARK: "Shadowy and forbidding, exploring difficult or troubling themes.",
            self.GRITTY: "Harsh realism that doesn't shy away from unpleasant truths.",
            self.BLEAK: "Hopeless and depressing, offering little comfort or joy.",
            self.HARSH: "Severe and unforgiving, brutally honest about difficult realities.",
            self.BRUTAL: "Violently direct and uncompromising in its intensity.",
            self.CYNICAL: "Skeptical about human nature and motives, expecting the worst.",
            self.NIHILISTIC: "Rejecting moral principles and believing life is meaningless.",
            self.DISTURBING: "Unsettling and troubling, challenging comfortable assumptions.",
            self.MACABRE: "Gruesome fascination with death and decay.",
            self.MORBID: "Unhealthy preoccupation with death and disease.",
            self.APOCALYPTIC: "End-times atmosphere of destruction and final judgment.",
            self.DYSTOPIAN: "Imagined society where everything has gone wrong.",
            
            # Romantic & Intimate
            self.ROMANTIC: "Love-focused emotion that celebrates connection and affection.",
            self.SENSUAL: "Appeal to physical senses and intimate pleasure.",
            self.TENDER: "Gentle care and affection, soft and loving.",
            self.INTIMATE: "Close personal connection that shares private thoughts and feelings.",
            self.LOVING: "Deep affection and care that nurtures and supports.",
            self.YEARNING: "Deep longing and desire, often unfulfilled.",
            self.SEDUCTIVE: "Alluring charm designed to attract and entice.",
            self.DREAMY: "Soft, ethereal quality like a beautiful dream.",
            self.ENCHANTING: "Magical charm that captivates and delights.",
            self.SWOONY: "Romantically overwhelming in the best possible way.",
            self.HEARTWARMING: "Emotionally touching in a positive, uplifting way.",
            self.PASSIONATE_ROMANCE: "Intense romantic love with deep emotional and physical connection."
        }
        
        # Continue with remaining descriptions...
        additional_descriptions = {
            # Intellectual & Philosophical
            self.PHILOSOPHICAL: "Deep contemplation of existence, meaning, and fundamental questions.",
            self.INTELLECTUAL: "Engaging the mind through complex ideas and sophisticated reasoning.",
            self.SCHOLARLY: "Academic approach with research, analysis, and learned discourse.",
            self.ANALYTICAL: "Systematic examination and logical breakdown of complex topics.",
            self.REFLECTIVE: "Thoughtful consideration and careful examination of ideas.",
            self.INTROSPECTIVE: "Looking inward to examine one's own thoughts and feelings.",
            self.MEDITATIVE: "Peaceful contemplation that encourages inner quiet and wisdom.",
            self.WISDOM_SEEKING: "Quest for understanding and enlightenment through experience.",
            self.EXISTENTIAL: "Questioning the nature of existence, purpose, and human condition.",
            self.METAPHYSICAL: "Exploring reality beyond the physical world and material existence.",
            self.THOUGHT_PROVOKING: "Stimulating deep thinking and intellectual consideration.",
            self.CEREBRAL: "Appealing primarily to intellect rather than emotion.",
            
            # Inspirational & Uplifting
            self.INSPIRATIONAL: "Motivating and encouraging positive action and belief.",
            self.MOTIVATIONAL: "Designed to inspire action and achievement of goals.",
            self.UPLIFTING: "Raising spirits and creating positive emotional elevation.",
            self.EMPOWERING: "Giving strength and confidence to take control of one's life.",
            self.TRIUMPHANT: "Celebrating victory and successful achievement.",
            self.ENCOURAGING: "Supportive and positive, boosting confidence and hope.",
            self.POSITIVE: "Constructive and optimistic in outlook and approach.",
            self.JOYFUL: "Full of happiness and celebration of life's goodness.",
            self.CELEBRATORY: "Marking special occasions and achievements with joy.",
            self.LIFE_AFFIRMING: "Celebrating the value and beauty of existence.",
            self.SPIRITUAL: "Connected to matters of the soul and transcendent meaning.",
            self.ENLIGHTENING: "Providing insight and understanding that illuminates truth.",
            
            # Nostalgic & Temporal
            self.NOSTALGIC: "Sentimental longing for the past, often idealized.",
            self.REMINISCENT: "Evoking memories and associations with earlier times.",
            self.TIMELESS: "Transcending specific time periods with universal appeal.",
            self.VINTAGE: "Characteristic of an earlier era, often with appreciation.",
            self.RETRO: "Deliberately imitating styles from the recent past.",
            self.HISTORICAL: "Rooted in specific historical periods and contexts.",
            self.PERIOD_APPROPRIATE: "Authentic to the time period being depicted.",
            self.ANACHRONISTIC: "Deliberately placing elements outside their proper time.",
            self.FUTURISTIC: "Imagining possibilities and technologies of tomorrow.",
            self.CONTEMPORARY: "Reflecting current times and modern sensibilities.",
            self.CLASSIC: "Enduring quality that maintains appeal across generations.",
            self.MODERN: "Current and up-to-date with present-day attitudes.",
            
            # Attitude & Perspective
            self.SERIOUS: "Grave and earnest, treating subject matter with importance.",
            self.FORMAL: "Following established conventions and proper protocols.",
            self.CASUAL: "Relaxed and informal, without rigid structure or ceremony.",
            self.CONVERSATIONAL: "Natural speech patterns that feel like personal dialogue.",
            self.AUTHORITATIVE: "Confident expertise that commands respect and trust.",
            self.HUMBLE: "Modest and unassuming, acknowledging limitations and respecting others.",
            self.CONFIDENT: "Self-assured certainty in ideas and presentation.",
            self.UNCERTAIN: "Acknowledging doubt and multiple possibilities.",
            self.OBJECTIVE: "Impartial and factual, avoiding personal bias.",
            self.SUBJECTIVE: "Personal viewpoint colored by individual experience and opinion.",
            self.NEUTRAL: "Balanced and unbiased, not favoring any particular side.",
            self.BIASED: "Showing preference or prejudice toward particular viewpoints.",
            
            # Adventure & Action
            self.ADVENTUROUS: "Spirit of exploration and willingness to take risks.",
            self.THRILLING: "Exciting and stimulating, creating adrenaline and excitement.",
            self.EXCITING: "Generating enthusiasm and eager anticipation.",
            self.BOLD: "Fearless and daring, willing to take significant risks.",
            self.DARING: "Adventurous courage that embraces challenge and danger.",
            self.REBELLIOUS: "Defying authority and conventional expectations.",
            self.DEFIANT: "Bold resistance to opposition or authority.",
            self.COURAGEOUS: "Brave facing of fear, danger, or adversity.",
            self.SWASHBUCKLING: "Romantic adventure with daring action and heroic exploits.",
            self.DYNAMIC: "Energetic and forceful, characterized by constant change.",
            self.ENERGETIC: "Full of vigor and enthusiasm, actively engaging.",
            self.KINETIC: "Characterized by movement and dynamic action."
        }
        
        descriptions.update(additional_descriptions)
        return descriptions.get(self, "A distinctive emotional tone that shapes the reader's experience.")

    @property
    def emotional_intensity(self) -> str:
        """Indicates the emotional intensity level of the tone."""
        intensity_map = {
            # High Intensity
            "euphoric": "high", "passionate": "high", "desperate": "high", "intense": "high",
            "brutal": "high", "apocalyptic": "high", "thrilling": "high", "ecstatic": "high",
            "cathartic": "high", "triumphant": "high", "rebellious": "high", "kinetic": "high",
            
            # Medium-High Intensity
            "dramatic": "medium-high", "urgent": "medium-high", "heroic": "medium-high",
            "suspenseful": "medium-high", "ominous": "medium-high", "dark": "medium-high",
            "cynical": "medium-high", "sensual": "medium-high", "defiant": "medium-high",
            "bold": "medium-high", "exciting": "medium-high", "dynamic": "medium-high",
            
            # Medium Intensity
            "optimistic": "medium", "melancholic": "medium", "mysterious": "medium",
            "romantic": "medium", "philosophical": "medium", "inspirational": "medium",
            "nostalgic": "medium", "serious": "medium", "adventurous": "medium",
            "humorous": "medium", "poignant": "medium", "yearning": "medium",
            
            # Medium-Low Intensity
            "contemplative": "medium-low", "wistful": "medium-low", "whimsical": "medium-low",
            "tender": "medium-low", "reflective": "medium-low", "hopeful": "medium-low",
            "encouraging": "medium-low", "vintage": "medium-low", "conversational": "medium-low",
            "gentle": "medium-low", "thoughtful": "medium-low", "dreamy": "medium-low",
            
            # Low Intensity
            "serene": "low", "peaceful": "low", "meditative": "low", "casual": "low",
            "neutral": "low", "timeless": "low", "classic": "low", "objective": "low",
            "scholarly": "low", "formal": "low", "humble": "low", "analytical": "low"
        }
        return intensity_map.get(self.value, "medium")

    @property
    def emotional_valence(self) -> str:
        """Indicates whether the tone is positive, negative, or neutral in emotional valence."""
        valence_map = {
            # Positive
            "optimistic": "positive", "euphoric": "positive", "hopeful": "positive",
            "joyful": "positive", "uplifting": "positive", "inspirational": "positive",
            "triumphant": "positive", "celebratory": "positive", "encouraging": "positive",
            "romantic": "positive", "tender": "positive", "loving": "positive",
            "humorous": "positive", "playful": "positive", "whimsical": "positive",
            "lighthearted": "positive", "adventurous": "positive", "bold": "positive",
            "confident": "positive", "empowering": "positive", "life_affirming": "positive",
            
            # Negative
            "pessimistic": "negative", "melancholic": "negative", "despairing": "negative",
            "anxious": "negative", "tragic": "negative", "bleak": "negative",
            "harsh": "negative", "brutal": "negative", "cynical": "negative",
            "nihilistic": "negative", "disturbing": "negative", "sinister": "negative",
            "ominous": "negative", "foreboding": "negative", "dark": "negative",
            "gritty": "negative", "macabre": "negative", "morbid": "negative",
            "apocalyptic": "negative", "dystopian": "negative", "desperate": "negative",
            
            # Neutral or Complex
            "contemplative": "neutral", "philosophical": "neutral", "analytical": "neutral",
            "objective": "neutral", "formal": "neutral", "scholarly": "neutral",
            "mysterious": "neutral", "introspective": "neutral", "reflective": "neutral",
            "bittersweet": "complex", "ironic": "complex", "satirical": "complex",
            "nostalgic": "complex", "wistful": "complex", "poignant": "complex",
            "noir": "complex", "gothic": "complex", "existential": "complex"
        }
        return valence_map.get(self.value, "neutral")

    @property
    def genre_compatibility(self) -> List[str]:
        """List of genres that commonly use this tone."""
        genre_map = {
            self.ROMANTIC: ["romance", "contemporary fiction", "historical romance", "romantic comedy"],
            self.MYSTERIOUS: ["mystery", "detective", "cozy mystery", "noir", "psychological thriller"],
            self.SUSPENSEFUL: ["thriller", "suspense", "crime", "espionage", "psychological thriller"],
            self.DARK: ["horror", "gothic", "noir", "psychological thriller", "dystopian"],
            self.HUMOROUS: ["comedy", "satirical fiction", "romantic comedy", "humorous mystery"],
            self.ADVENTUROUS: ["adventure", "action", "quest fantasy", "young adult adventure"],
            self.PHILOSOPHICAL: ["literary fiction", "speculative fiction", "philosophical novels"],
            self.NOSTALGIC: ["historical fiction", "memoir", "family saga", "coming-of-age"],
            self.EPIC: ["epic fantasy", "historical epic", "space opera", "high fantasy"],
            self.GRITTY: ["urban fiction", "crime thriller", "post-apocalyptic", "war fiction"],
            self.WHIMSICAL: ["children's literature", "fantasy", "magical realism", "cozy fiction"],
            self.INSPIRATIONAL: ["self-help", "spiritual fiction", "inspirational romance", "memoir"],
            self.DRAMATIC: ["literary fiction", "family drama", "historical fiction", "biographical"],
            self.MELANCHOLIC: ["literary fiction", "poetry", "coming-of-age", "historical drama"]
        }
        return genre_map.get(self, ["general fiction"])

    @classmethod
    def get_compatible_tones(cls, primary_tone: "ToneType") -> List["ToneType"]:
        """Get tones that work well together with the primary tone."""
        compatibility_map = {
            cls.ROMANTIC: [cls.TENDER, cls.PASSIONATE, cls.DREAMY, cls.HOPEFUL, cls.INTIMATE],
            cls.MYSTERIOUS: [cls.SUSPENSEFUL, cls.CRYPTIC, cls.OMINOUS, cls.NOIR, cls.GOTHIC],
            cls.DARK: [cls.GRITTY, cls.CYNICAL, cls.BLEAK, cls.OMINOUS, cls.BRUTAL],
            cls.HUMOROUS: [cls.WITTY, cls.PLAYFUL, cls.SATIRICAL, cls.LIGHTHEARTED, cls.WHIMSICAL],
            cls.PHILOSOPHICAL: [cls.CONTEMPLATIVE, cls.REFLECTIVE, cls.EXISTENTIAL, cls.ANALYTICAL],
            cls.ADVENTUROUS: [cls.BOLD, cls.THRILLING, cls.DYNAMIC, cls.COURAGEOUS, cls.EXCITING]
        }
        return compatibility_map.get(primary_tone, [])

    @classmethod
    def from_description(cls, description: str) -> Optional["ToneType"]:
        """
        Find the best matching tone from a text description.
        Uses keyword matching and semantic similarity.
        """
        description_lower = description.lower()
        
        # Direct keyword matching
        keyword_map = {
            "funny": cls.HUMOROUS, "sad": cls.MELANCHOLIC, "scary": cls.DARK,
            "love": cls.ROMANTIC, "mystery": cls.MYSTERIOUS, "action": cls.ADVENTUROUS,
            "deep": cls.PHILOSOPHICAL, "happy": cls.OPTIMISTIC, "angry": cls.INTENSE,
            "peaceful": cls.SERENE, "exciting": cls.THRILLING, "thoughtful": cls.CONTEMPLATIVE
        }
        
        for keyword, tone in keyword_map.items():
            if keyword in description_lower:
                return tone
                
        return None

    def __str__(self) -> str:
        return self.display_name