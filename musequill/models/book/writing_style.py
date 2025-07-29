from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import re


class WritingStyle(str, Enum):
    """Comprehensive writing styles for different types of book content and audiences."""
    
    # ACADEMIC & SCHOLARLY STYLES
    ACADEMIC = "academic"
    SCHOLARLY = "scholarly"
    SCIENTIFIC = "scientific"
    RESEARCH_ORIENTED = "research_oriented"
    ANALYTICAL = "analytical"
    FORMAL = "formal"
    TECHNICAL = "technical"
    PROFESSIONAL = "professional"
    
    # LITERARY & ARTISTIC STYLES
    LITERARY = "literary"
    POETIC = "poetic"
    LYRICAL = "lyrical"
    EXPERIMENTAL = "experimental"
    STREAM_OF_CONSCIOUSNESS = "stream_of_consciousness"
    MODERNIST = "modernist"
    POSTMODERN = "postmodern"
    MINIMALIST = "minimalist"
    PROSE_POETRY = "prose_poetry"
    
    # CONVERSATIONAL & ACCESSIBLE STYLES
    CONVERSATIONAL = "conversational"
    CASUAL = "casual"
    INFORMAL = "informal"
    FRIENDLY = "friendly"
    APPROACHABLE = "approachable"
    ACCESSIBLE = "accessible"
    PLAIN_LANGUAGE = "plain_language"
    COLLOQUIAL = "colloquial"
    
    # NARRATIVE & STORYTELLING STYLES
    NARRATIVE = "narrative"
    DESCRIPTIVE = "descriptive"
    ATMOSPHERIC = "atmospheric"
    CINEMATIC = "cinematic"
    VISUAL = "visual"
    IMMERSIVE = "immersive"
    EVOCATIVE = "evocative"
    DRAMATIC = "dramatic"
    THEATRICAL = "theatrical"
    
    # GENRE-SPECIFIC STYLES
    NOIR = "noir"
    GOTHIC = "gothic"
    ROMANTIC = "romantic"
    EPIC = "epic"
    MYTHIC = "mythic"
    PASTORAL = "pastoral"
    SATIRICAL = "satirical"
    COMEDIC = "comedic"
    TRAGIC = "tragic"
    HORROR = "horror"
    SUSPENSEFUL = "suspenseful"
    
    # JOURNALISTIC & REPORTORIAL STYLES
    JOURNALISTIC = "journalistic"
    REPORTORIAL = "reportorial"
    INVESTIGATIVE = "investigative"
    DOCUMENTARY = "documentary"
    OBJECTIVE = "objective"
    FACTUAL = "factual"
    NEWS_STYLE = "news_style"
    MAGAZINE_STYLE = "magazine_style"
    
    # INSTRUCTIONAL & EDUCATIONAL STYLES
    INSTRUCTIONAL = "instructional"
    EDUCATIONAL = "educational"
    TUTORIAL = "tutorial"
    HOW_TO = "how_to"
    STEP_BY_STEP = "step_by_step"
    EXPLANATORY = "explanatory"
    PEDAGOGICAL = "pedagogical"
    DIDACTIC = "didactic"
    
    # BUSINESS & COMMERCIAL STYLES
    BUSINESS = "business"
    CORPORATE = "corporate"
    MARKETING = "marketing"
    PERSUASIVE = "persuasive"
    SALES_ORIENTED = "sales_oriented"
    PROMOTIONAL = "promotional"
    EXECUTIVE = "executive"
    CONSULTANT = "consultant"
    
    # PERSONAL & INTIMATE STYLES
    PERSONAL = "personal"
    INTIMATE = "intimate"
    CONFESSIONAL = "confessional"
    MEMOIR_STYLE = "memoir_style"
    DIARY_STYLE = "diary_style"
    EPISTOLARY = "epistolary"
    REFLECTIVE = "reflective"
    INTROSPECTIVE = "introspective"
    
    # CONTEMPORARY & MODERN STYLES
    CONTEMPORARY = "contemporary"
    MODERN = "modern"
    TRENDY = "trendy"
    SOCIAL_MEDIA = "social_media"
    BLOG_STYLE = "blog_style"
    MILLENNIAL = "millennial"
    GEN_Z = "gen_z"
    INTERNET_NATIVE = "internet_native"
    
    # CLASSICAL & TRADITIONAL STYLES
    CLASSICAL = "classical"
    TRADITIONAL = "traditional"
    VICTORIAN = "victorian"
    EDWARDIAN = "edwardian"
    RENAISSANCE = "renaissance"
    BAROQUE = "baroque"
    NEOCLASSICAL = "neoclassical"
    
    # RHYTHMIC & STYLISTIC PATTERNS
    RHYTHMIC = "rhythmic"
    MUSICAL = "musical"
    FLOWING = "flowing"
    STACCATO = "staccato"
    CHOPPY = "choppy"
    SPARSE = "sparse"
    VERBOSE = "verbose"
    ORNATE = "ornate"
    ECONOMICAL = "economical"
    
    # VOICE & TONE STYLES
    AUTHORITATIVE = "authoritative"
    CONFIDENT = "confident"
    HUMBLE = "humble"
    WITTY = "witty"
    SARCASTIC = "sarcastic"
    IRONIC = "ironic"
    SINCERE = "sincere"
    EARNEST = "earnest"
    PLAYFUL = "playful"
    SERIOUS = "serious"
    
    # SPECIAL PURPOSE STYLES
    CHILDREN_FRIENDLY = "children_friendly"
    YOUNG_ADULT = "young_adult"
    THERAPEUTIC = "therapeutic"
    INSPIRATIONAL = "inspirational"
    MOTIVATIONAL = "motivational"
    PHILOSOPHICAL = "philosophical"
    SPIRITUAL = "spiritual"
    SELF_HELP = "self_help"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        """Detailed description of the writing style."""
        descriptions = {
            # Academic & Scholarly
            self.ACADEMIC: "Formal, precise language with citations, evidence-based arguments, and scholarly terminology appropriate for academic publications.",
            self.SCHOLARLY: "Intellectual discourse with depth of analysis, complex arguments, and references to established knowledge in the field.",
            self.SCIENTIFIC: "Objective, methodical presentation with precise terminology, hypothesis-driven structure, and empirical evidence.",
            self.RESEARCH_ORIENTED: "Systematic investigation approach with thorough documentation, methodology explanation, and comprehensive source integration.",
            self.ANALYTICAL: "Logical breakdown of complex topics with systematic examination, critical thinking, and reasoned conclusions.",
            self.FORMAL: "Structured, professional language following established conventions with proper grammar and sophisticated vocabulary.",
            self.TECHNICAL: "Specialized terminology and precise instructions for professional or expert audiences in specific fields.",
            self.PROFESSIONAL: "Business-appropriate language that maintains authority while remaining accessible to workplace audiences.",
            
            # Literary & Artistic
            self.LITERARY: "Sophisticated prose with artistic merit, complex themes, rich symbolism, and elevated language that prioritizes aesthetic value.",
            self.POETIC: "Language that emphasizes rhythm, imagery, and emotional resonance with attention to sound and metaphorical expression.",
            self.LYRICAL: "Musical quality in prose with flowing, melodious language that emphasizes beauty and emotional expression.",
            self.EXPERIMENTAL: "Innovative approaches to narrative structure, language, and form that challenge conventional writing expectations.",
            self.STREAM_OF_CONSCIOUSNESS: "Unfiltered flow of thoughts and perceptions that mirrors the natural patterns of human consciousness.",
            self.MODERNIST: "Early 20th-century literary techniques emphasizing psychological depth, fragmentation, and subjective experience.",
            self.POSTMODERN: "Self-aware, often meta-fictional approach that questions narrative conventions and blurs genre boundaries.",
            self.MINIMALIST: "Economical use of language with precise word choice, understated emotion, and significant use of subtext.",
            self.PROSE_POETRY: "Hybrid form combining poetic techniques with prose structure, emphasizing imagery and rhythm.",
            
            # Conversational & Accessible
            self.CONVERSATIONAL: "Natural, speech-like quality that feels like a personal conversation between writer and reader.",
            self.CASUAL: "Relaxed, informal tone with everyday language that creates a comfortable, unpretentious reading experience.",
            self.INFORMAL: "Comfortable, approachable language without rigid structure, suitable for general audiences.",
            self.FRIENDLY: "Warm, welcoming tone that establishes personal connection and puts readers at ease.",
            self.APPROACHABLE: "Accessible language that makes complex topics understandable without talking down to readers.",
            self.ACCESSIBLE: "Clear, straightforward communication designed to reach the broadest possible audience.",
            self.PLAIN_LANGUAGE: "Simple, direct communication that prioritizes clarity and comprehension over stylistic flourishes.",
            self.COLLOQUIAL: "Everyday speech patterns and expressions that reflect natural conversation and regional dialects.",
            
            # Narrative & Storytelling
            self.NARRATIVE: "Story-driven approach with clear plot progression, character development, and engaging storytelling techniques.",
            self.DESCRIPTIVE: "Rich, detailed imagery that creates vivid mental pictures and sensory experiences for readers.",
            self.ATMOSPHERIC: "Emphasis on mood and setting that creates immersive environments and emotional contexts.",
            self.CINEMATIC: "Visual storytelling approach with scene-setting, dialogue, and pacing borrowed from film techniques.",
            self.VISUAL: "Strong emphasis on imagery and description that helps readers visualize scenes and concepts clearly.",
            self.IMMERSIVE: "Technique that draws readers completely into the world of the text through detailed world-building.",
            self.EVOCATIVE: "Language chosen specifically to trigger emotional responses and create powerful reader connections.",
            self.DRAMATIC: "Heightened emotional content with conflict, tension, and significant character stakes.",
            self.THEATRICAL: "Performance-oriented writing with strong dialogue, dramatic timing, and stage-worthy scenes.",
            
            # Genre-Specific
            self.NOIR: "Dark, cynical tone with urban settings, moral ambiguity, and atmosphere of corruption and danger.",
            self.GOTHIC: "Dark romantic style emphasizing mystery, supernatural elements, and psychological complexity.",
            self.ROMANTIC: "Focus on love, relationships, and emotional connection with optimistic or passionate tone.",
            self.EPIC: "Grand scope and heroic themes with elevated language suitable for large-scale adventures.",
            self.MYTHIC: "Archetypal storytelling with universal themes and symbolic resonance across cultures.",
            self.PASTORAL: "Idealized rural life with peaceful, nature-focused imagery and simple, harmonious themes.",
            self.SATIRICAL: "Humor and irony used to critique society, institutions, or human behavior.",
            self.COMEDIC: "Humor-focused writing designed to entertain and amuse through wit and amusing situations.",
            self.TRAGIC: "Serious themes of loss, suffering, and human limitation with emotional depth and gravity.",
            self.HORROR: "Designed to frighten, unsettle, and create suspense through threatening or supernatural elements.",
            self.SUSPENSEFUL: "Building tension and anticipation through pacing, uncertainty, and dramatic stakes.",
            
            # Journalistic & Reportorial
            self.JOURNALISTIC: "Objective reporting style with facts, sources, and balanced presentation of information.",
            self.REPORTORIAL: "Information-gathering approach with systematic investigation and factual presentation.",
            self.INVESTIGATIVE: "Deep-dive research style uncovering hidden information through thorough examination.",
            self.DOCUMENTARY: "Factual presentation with comprehensive coverage and objective analysis of real events.",
            self.OBJECTIVE: "Neutral, unbiased presentation that avoids personal opinion or emotional manipulation.",
            self.FACTUAL: "Information-based writing that prioritizes accuracy, verification, and evidence.",
            self.NEWS_STYLE: "Inverted pyramid structure with key information first and decreasing importance.",
            self.MAGAZINE_STYLE: "Feature writing with human interest, personality, and engaging narrative elements.",
            
            # Instructional & Educational
            self.INSTRUCTIONAL: "Step-by-step guidance designed to teach specific skills or knowledge effectively.",
            self.EDUCATIONAL: "Learning-focused approach that presents information in digestible, progressive format.",
            self.TUTORIAL: "Hands-on teaching style with practical examples and guided practice opportunities.",
            self.HOW_TO: "Problem-solving approach with clear instructions and actionable steps for readers.",
            self.STEP_BY_STEP: "Sequential instruction breaking complex processes into manageable components.",
            self.EXPLANATORY: "Clarifying complex concepts through examples, analogies, and systematic breakdown.",
            self.PEDAGOGICAL: "Teaching-focused approach using established educational principles and methods.",
            self.DIDACTIC: "Instructive writing designed to teach moral, ethical, or practical lessons.",
            
            # Business & Commercial
            self.BUSINESS: "Professional communication suitable for corporate environments and business relationships.",
            self.CORPORATE: "Formal business language following organizational standards and professional protocols.",
            self.MARKETING: "Persuasive communication designed to influence purchasing decisions and brand perception.",
            self.PERSUASIVE: "Argument-based writing designed to convince readers to accept specific viewpoints or take action.",
            self.SALES_ORIENTED: "Customer-focused language designed to highlight benefits and motivate purchases.",
            self.PROMOTIONAL: "Positive, benefit-focused language designed to generate interest and enthusiasm.",
            self.EXECUTIVE: "High-level business communication with strategic focus and decision-making emphasis.",
            self.CONSULTANT: "Advisory approach with expert analysis, recommendations, and problem-solving focus.",
            
            # Personal & Intimate
            self.PERSONAL: "Individual perspective sharing private thoughts, experiences, and personal insights.",
            self.INTIMATE: "Close, personal communication that creates emotional connection and vulnerability.",
            self.CONFESSIONAL: "Honest, revealing style that shares personal struggles, mistakes, and growth.",
            self.MEMOIR_STYLE: "Personal history narration with reflection on life experiences and their meaning.",
            self.DIARY_STYLE: "Private journal approach with daily observations and personal reflections.",
            self.EPISTOLARY: "Letter-writing format that creates personal communication between characters or with readers.",
            self.REFLECTIVE: "Thoughtful consideration of experiences, ideas, and their deeper implications.",
            self.INTROSPECTIVE: "Internal examination of thoughts, feelings, and motivations with psychological depth.",
            
            # Contemporary & Modern
            self.CONTEMPORARY: "Current cultural references and modern sensibilities reflecting today's world.",
            self.MODERN: "Updated approach to classic themes using current language and contemporary perspectives.",
            self.TRENDY: "Fashion-forward language incorporating current slang, references, and cultural movements.",
            self.SOCIAL_MEDIA: "Brief, engaging format optimized for digital platforms and short attention spans.",
            self.BLOG_STYLE: "Personal online writing with informal tone, regular updates, and interactive elements.",
            self.MILLENNIAL: "Language and references appealing to generation born 1981-1996 with their specific cultural touchstones.",
            self.GEN_Z: "Communication style reflecting digital natives born after 1997 with internet-influenced language.",
            self.INTERNET_NATIVE: "Writing style evolved from online communication with memes, abbreviations, and digital culture.",
            
            # Classical & Traditional
            self.CLASSICAL: "Time-honored literary traditions with formal structure and elevated language.",
            self.TRADITIONAL: "Established literary conventions and formal approaches to storytelling and exposition.",
            self.VICTORIAN: "19th-century British literary style with elaborate prose and moral complexity.",
            self.EDWARDIAN: "Early 20th-century refined style with social awareness and psychological sophistication.",
            self.RENAISSANCE: "Humanistic approach emphasizing individual experience and classical learning.",
            self.BAROQUE: "Elaborate, ornate style with complex structure and rich decorative elements.",
            self.NEOCLASSICAL: "Revival of classical principles emphasizing order, balance, and rational thought.",
            
            # Rhythmic & Stylistic Patterns
            self.RHYTHMIC: "Attention to sound patterns, cadence, and musical qualities in sentence structure.",
            self.MUSICAL: "Prose that emphasizes rhythm, repetition, and sound patterns for auditory appeal.",
            self.FLOWING: "Smooth, continuous movement between ideas with graceful transitions and natural progression.",
            self.STACCATO: "Short, sharp sentences with abrupt rhythm and rapid-fire delivery of information.",
            self.CHOPPY: "Deliberately fragmented style with irregular rhythm and interrupted thought patterns.",
            self.SPARSE: "Minimal language with careful word selection and significant use of white space.",
            self.VERBOSE: "Rich, elaborate language with extensive detail and comprehensive explanation.",
            self.ORNATE: "Decorative, elaborate style with complex sentence structure and sophisticated vocabulary.",
            self.ECONOMICAL: "Efficient use of language with maximum impact from minimum words.",
            
            # Voice & Tone
            self.AUTHORITATIVE: "Confident, expert voice that demonstrates knowledge and commands respect.",
            self.CONFIDENT: "Self-assured tone that expresses certainty and conviction in presented ideas.",
            self.HUMBLE: "Modest, unassuming approach that acknowledges limitations and respects readers.",
            self.WITTY: "Clever, amusing language that entertains through wordplay and intelligent humor.",
            self.SARCASTIC: "Ironic tone that uses contradiction between literal and intended meaning for effect.",
            self.IRONIC: "Subtle contrast between appearance and reality used for humor or emphasis.",
            self.SINCERE: "Genuine, honest communication that expresses authentic thoughts and feelings.",
            self.EARNEST: "Serious, heartfelt approach that demonstrates deep commitment to subject matter.",
            self.PLAYFUL: "Light-hearted, fun approach that engages readers through humor and creativity.",
            self.SERIOUS: "Grave, important tone appropriate for weighty subjects and significant themes.",
            
            # Special Purpose
            self.CHILDREN_FRIENDLY: "Age-appropriate language with simple concepts and engaging, educational content.",
            self.YOUNG_ADULT: "Teen-focused writing addressing adolescent concerns with appropriate complexity.",
            self.THERAPEUTIC: "Healing-focused language designed to provide comfort, understanding, and emotional support.",
            self.INSPIRATIONAL: "Uplifting, motivating language designed to encourage and empower readers.",
            self.MOTIVATIONAL: "Action-oriented writing designed to inspire readers to achieve goals and overcome obstacles.",
            self.PHILOSOPHICAL: "Deep contemplation of existence, meaning, and fundamental questions about life.",
            self.SPIRITUAL: "Focus on matters of soul, faith, and connection to transcendent or divine elements.",
            self.SELF_HELP: "Practical guidance for personal improvement with actionable advice and encouragement."
        }
        return descriptions.get(self, "A distinctive writing approach with its own characteristics and applications.")

    @property
    def complexity_level(self) -> str:
        """Indicates the reading complexity level required."""
        complexity_mapping = {
            # Simple/Accessible
            self.PLAIN_LANGUAGE: "elementary",
            self.CHILDREN_FRIENDLY: "elementary",
            self.CASUAL: "elementary",
            
            # Easy/General
            self.CONVERSATIONAL: "easy",
            self.FRIENDLY: "easy",
            self.INFORMAL: "easy",
            self.APPROACHABLE: "easy",
            self.ACCESSIBLE: "easy",
            self.COLLOQUIAL: "easy",
            self.BLOG_STYLE: "easy",
            self.SOCIAL_MEDIA: "easy",
            
            # Moderate
            self.NARRATIVE: "moderate",
            self.DESCRIPTIVE: "moderate",
            self.CONTEMPORARY: "moderate",
            self.MODERN: "moderate",
            self.BUSINESS: "moderate",
            self.PROFESSIONAL: "moderate",
            self.INSTRUCTIONAL: "moderate",
            self.EDUCATIONAL: "moderate",
            self.JOURNALISTIC: "moderate",
            self.YOUNG_ADULT: "moderate",
            
            # Advanced
            self.LITERARY: "advanced",
            self.ACADEMIC: "advanced",
            self.SCHOLARLY: "advanced",
            self.TECHNICAL: "advanced",
            self.FORMAL: "advanced",
            self.ANALYTICAL: "advanced",
            self.PHILOSOPHICAL: "advanced",
            
            # Expert
            self.SCIENTIFIC: "expert",
            self.RESEARCH_ORIENTED: "expert",
            self.EXPERIMENTAL: "expert",
            self.POSTMODERN: "expert",
            self.STREAM_OF_CONSCIOUSNESS: "expert"
        }
        return complexity_mapping.get(self, "moderate")

    @property
    def target_audience(self) -> str:
        """Primary target audience for this writing style."""
        audience_mapping = {
            # General audiences
            self.CONVERSATIONAL: "general readers",
            self.ACCESSIBLE: "broad audience",
            self.PLAIN_LANGUAGE: "general public",
            
            # Academic audiences  
            self.ACADEMIC: "scholars and researchers",
            self.SCHOLARLY: "academic community",
            self.SCIENTIFIC: "researchers and scientists",
            self.TECHNICAL: "professionals and experts",
            
            # Age-specific
            self.CHILDREN_FRIENDLY: "children and young readers",
            self.YOUNG_ADULT: "teenagers and young adults",
            self.MILLENNIAL: "millennial generation",
            self.GEN_Z: "generation Z readers",
            
            # Professional
            self.BUSINESS: "business professionals",
            self.CORPORATE: "corporate executives",
            self.MARKETING: "consumers and clients",
            
            # Literary
            self.LITERARY: "literary fiction readers",
            self.POETIC: "poetry enthusiasts",
            self.EXPERIMENTAL: "avant-garde readers"
        }
        return audience_mapping.get(self, "general readers")

    @property
    def typical_genres(self) -> List[str]:
        """Genres where this writing style is commonly used."""
        genre_mapping = {
            self.ACADEMIC: ["non-fiction", "textbook", "research"],
            self.LITERARY: ["literary fiction", "contemporary", "drama"],
            self.CONVERSATIONAL: ["memoir", "self-help", "blog", "personal development"],
            self.TECHNICAL: ["manual", "guide", "reference", "textbook"],
            self.NARRATIVE: ["fiction", "memoir", "biography", "historical"],
            self.DESCRIPTIVE: ["travel", "nature writing", "literary fiction"],
            self.SCIENTIFIC: ["science", "research", "academic", "medical"],
            self.BUSINESS: ["business", "professional development", "management"],
            self.JOURNALISTIC: ["non-fiction", "biography", "current events"],
            self.INSTRUCTIONAL: ["how-to", "education", "self-help", "guide"],
            self.HORROR: ["horror", "thriller", "gothic", "supernatural"],
            self.ROMANTIC: ["romance", "women's fiction", "contemporary"],
            self.COMEDIC: ["humor", "comedy", "satire", "entertainment"],
            self.NOIR: ["mystery", "crime", "thriller", "detective"],
            self.GOTHIC: ["horror", "romance", "literary fiction", "historical"],
            self.CHILDREN_FRIENDLY: ["children's books", "middle grade", "educational"],
            self.YOUNG_ADULT: ["young adult", "coming of age", "contemporary"],
            self.PHILOSOPHICAL: ["philosophy", "religion", "spirituality", "literary fiction"]
        }
        return genre_mapping.get(self, ["general fiction", "non-fiction"])

    @classmethod  
    def from_string(cls, style_string: str) -> 'WritingStyle':
        """
        Create WritingStyle from string with restrictive fuzzy matching.
        
        Args:
            style_string: String description of writing style
            
        Returns:
            Matching WritingStyle enum value
            
        Raises:
            ValueError: If no suitable match is found
        """
        if not style_string or not isinstance(style_string, str):
            raise ValueError("Invalid writing style value")
        
        # Clean and normalize input
        cleaned_value = style_string.strip().lower()
        
        # Direct enum value match first
        for style in cls:
            if style.value == cleaned_value:
                return style
        
        # Display name match
        for style in cls:
            if style.display_name.lower() == cleaned_value:
                return style
        
        # Restrictive fuzzy matching with precise synonyms
        fuzzy_mappings = {
            # Academic terms
            "academic": cls.ACADEMIC,
            "scholarly": cls.SCHOLARLY,
            "formal": cls.FORMAL,
            "technical": cls.TECHNICAL,
            "scientific": cls.SCIENTIFIC,
            "research": cls.RESEARCH_ORIENTED,
            "analytical": cls.ANALYTICAL,
            "professional": cls.PROFESSIONAL,
            
            # Literary terms
            "literary": cls.LITERARY,
            "poetic": cls.POETIC,
            "lyrical": cls.LYRICAL,
            "experimental": cls.EXPERIMENTAL,
            "artistic": cls.LITERARY,
            "creative": cls.LITERARY,
            "sophisticated": cls.LITERARY,
            "minimalist": cls.MINIMALIST,
            "modernist": cls.MODERNIST,
            "postmodern": cls.POSTMODERN,
            
            # Conversational terms
            "conversational": cls.CONVERSATIONAL,
            "casual": cls.CASUAL,
            "informal": cls.INFORMAL,
            "friendly": cls.FRIENDLY,
            "approachable": cls.APPROACHABLE,
            "accessible": cls.ACCESSIBLE,
            "simple": cls.PLAIN_LANGUAGE,
            "plain": cls.PLAIN_LANGUAGE,
            "easy": cls.ACCESSIBLE,
            "colloquial": cls.COLLOQUIAL,
            "natural": cls.CONVERSATIONAL,
            
            # Narrative terms
            "narrative": cls.NARRATIVE,
            "descriptive": cls.DESCRIPTIVE,
            "atmospheric": cls.ATMOSPHERIC,
            "cinematic": cls.CINEMATIC,
            "visual": cls.VISUAL,
            "immersive": cls.IMMERSIVE,
            "dramatic": cls.DRAMATIC,
            "storytelling": cls.NARRATIVE,
            "vivid": cls.DESCRIPTIVE,
            
            # Genre-specific terms
            "noir": cls.NOIR,
            "gothic": cls.GOTHIC,
            "romantic": cls.ROMANTIC,
            "epic": cls.EPIC,
            "mythic": cls.MYTHIC,
            "satirical": cls.SATIRICAL,
            "comedic": cls.COMEDIC,
            "funny": cls.COMEDIC,
            "humorous": cls.COMEDIC,
            "tragic": cls.TRAGIC,
            "horror": cls.HORROR,
            "scary": cls.HORROR,
            "suspenseful": cls.SUSPENSEFUL,
            "thriller": cls.SUSPENSEFUL,
            
            # Journalistic terms
            "journalistic": cls.JOURNALISTIC,
            "news": cls.NEWS_STYLE,
            "reportorial": cls.REPORTORIAL,
            "investigative": cls.INVESTIGATIVE,
            "documentary": cls.DOCUMENTARY,
            "objective": cls.OBJECTIVE,
            "factual": cls.FACTUAL,
            "magazine": cls.MAGAZINE_STYLE,
            
            # Educational terms
            "instructional": cls.INSTRUCTIONAL,
            "educational": cls.EDUCATIONAL,
            "tutorial": cls.TUTORIAL,
            "teaching": cls.EDUCATIONAL,
            "pedagogical": cls.PEDAGOGICAL,
            "didactic": cls.DIDACTIC,
            "explanatory": cls.EXPLANATORY,
            
            # Business terms
            "business": cls.BUSINESS,
            "corporate": cls.CORPORATE,
            "marketing": cls.MARKETING,
            "persuasive": cls.PERSUASIVE,
            "sales": cls.SALES_ORIENTED,
            "promotional": cls.PROMOTIONAL,
            "executive": cls.EXECUTIVE,
            "consultant": cls.CONSULTANT,
            
            # Personal terms
            "personal": cls.PERSONAL,
            "intimate": cls.INTIMATE,
            "confessional": cls.CONFESSIONAL,
            "memoir": cls.MEMOIR_STYLE,
            "diary": cls.DIARY_STYLE,
            "reflective": cls.REFLECTIVE,
            "introspective": cls.INTROSPECTIVE,
            
            # Contemporary terms
            "contemporary": cls.CONTEMPORARY,
            "modern": cls.MODERN,
            "trendy": cls.TRENDY,
            "social": cls.SOCIAL_MEDIA,
            "blog": cls.BLOG_STYLE,
            "millennial": cls.MILLENNIAL,
            "internet": cls.INTERNET_NATIVE,
            "digital": cls.SOCIAL_MEDIA,
            
            # Classical terms
            "classical": cls.CLASSICAL,
            "traditional": cls.TRADITIONAL,
            "victorian": cls.VICTORIAN,
            "renaissance": cls.RENAISSANCE,
            "baroque": cls.BAROQUE,
            
            # Rhythmic terms
            "rhythmic": cls.RHYTHMIC,
            "musical": cls.MUSICAL,
            "flowing": cls.FLOWING,
            "smooth": cls.FLOWING,
            "choppy": cls.CHOPPY,
            "sparse": cls.SPARSE,
            "verbose": cls.VERBOSE,
            "ornate": cls.ORNATE,
            "elaborate": cls.ORNATE,
            "economical": cls.ECONOMICAL,
            "concise": cls.ECONOMICAL,
            
            # Voice terms
            "authoritative": cls.AUTHORITATIVE,
            "confident": cls.CONFIDENT,
            "humble": cls.HUMBLE,
            "witty": cls.WITTY,
            "sarcastic": cls.SARCASTIC,
            "ironic": cls.IRONIC,
            "sincere": cls.SINCERE,
            "earnest": cls.EARNEST,
            "playful": cls.PLAYFUL,
            "serious": cls.SERIOUS,
            
            # Special purpose terms
            "children": cls.CHILDREN_FRIENDLY,
            "kids": cls.CHILDREN_FRIENDLY,
            "therapeutic": cls.THERAPEUTIC,
            "healing": cls.THERAPEUTIC,
            "inspirational": cls.INSPIRATIONAL,
            "motivational": cls.MOTIVATIONAL,
            "philosophical": cls.PHILOSOPHICAL,
            "spiritual": cls.SPIRITUAL,
            "religious": cls.SPIRITUAL,
        }
        
        # Check fuzzy mappings with exact matches only
        if cleaned_value in fuzzy_mappings:
            return fuzzy_mappings[cleaned_value]
        
        # Partial word matching - very restrictive
        for style in cls:
            style_words = style.value.split('_')
            input_words = cleaned_value.replace('_', ' ').replace('-', ' ').split()
            
            # Skip if input is too short or has too many words
            if len(cleaned_value) < 4 or len(input_words) > 3:
                continue
            
            # Check for meaningful word overlap
            matched_chars = 0
            total_input_chars = len(cleaned_value.replace(' ', ''))
            
            for input_word in input_words:
                if len(input_word) >= 4:  # Only consider words 4+ characters
                    for style_word in style_words:
                        if input_word == style_word:
                            matched_chars += len(input_word)
                        elif len(input_word) >= 5 and len(style_word) >= 5:
                            # Very restrictive substring matching
                            if (input_word in style_word and len(input_word) >= len(style_word) * 0.8) or \
                               (style_word in input_word and len(style_word) >= len(input_word) * 0.8):
                                matched_chars += min(len(input_word), len(style_word))
            
            # Require very substantial match (at least 80% of input should match)
            if matched_chars > 0 and matched_chars / total_input_chars >= 0.8:
                return style
        
        raise ValueError(f"Invalid writing style: '{style_string}'")

    @classmethod
    def get_academic_styles(cls) -> List['WritingStyle']:
        """Get all academic and scholarly writing styles."""
        return [
            cls.ACADEMIC, cls.SCHOLARLY, cls.SCIENTIFIC, cls.RESEARCH_ORIENTED,
            cls.ANALYTICAL, cls.FORMAL, cls.TECHNICAL, cls.PROFESSIONAL
        ]

    @classmethod
    def get_literary_styles(cls) -> List['WritingStyle']:
        """Get all literary and artistic writing styles."""
        return [
            cls.LITERARY, cls.POETIC, cls.LYRICAL, cls.EXPERIMENTAL,
            cls.STREAM_OF_CONSCIOUSNESS, cls.MODERNIST, cls.POSTMODERN,
            cls.MINIMALIST, cls.PROSE_POETRY
        ]

    @classmethod
    def get_accessible_styles(cls) -> List['WritingStyle']:
        """Get all conversational and accessible writing styles."""
        return [
            cls.CONVERSATIONAL, cls.CASUAL, cls.INFORMAL, cls.FRIENDLY,
            cls.APPROACHABLE, cls.ACCESSIBLE, cls.PLAIN_LANGUAGE, cls.COLLOQUIAL
        ]

    @classmethod
    def get_narrative_styles(cls) -> List['WritingStyle']:
        """Get all narrative and storytelling writing styles."""
        return [
            cls.NARRATIVE, cls.DESCRIPTIVE, cls.ATMOSPHERIC, cls.CINEMATIC,
            cls.VISUAL, cls.IMMERSIVE, cls.EVOCATIVE, cls.DRAMATIC, cls.THEATRICAL
        ]

    @classmethod
    def get_genre_styles(cls) -> List['WritingStyle']:
        """Get all genre-specific writing styles."""
        return [
            cls.NOIR, cls.GOTHIC, cls.ROMANTIC, cls.EPIC, cls.MYTHIC,
            cls.PASTORAL, cls.SATIRICAL, cls.COMEDIC, cls.TRAGIC,
            cls.HORROR, cls.SUSPENSEFUL
        ]

    @classmethod
    def get_business_styles(cls) -> List['WritingStyle']:
        """Get all business and commercial writing styles."""
        return [
            cls.BUSINESS, cls.CORPORATE, cls.MARKETING, cls.PERSUASIVE,
            cls.SALES_ORIENTED, cls.PROMOTIONAL, cls.EXECUTIVE, cls.CONSULTANT
        ]

    @classmethod
    def get_educational_styles(cls) -> List['WritingStyle']:
        """Get all instructional and educational writing styles."""
        return [
            cls.INSTRUCTIONAL, cls.EDUCATIONAL, cls.TUTORIAL, cls.HOW_TO,
            cls.STEP_BY_STEP, cls.EXPLANATORY, cls.PEDAGOGICAL, cls.DIDACTIC
        ]

    @classmethod
    def get_contemporary_styles(cls) -> List['WritingStyle']:
        """Get all contemporary and modern writing styles."""
        return [
            cls.CONTEMPORARY, cls.MODERN, cls.TRENDY, cls.SOCIAL_MEDIA,
            cls.BLOG_STYLE, cls.MILLENNIAL, cls.GEN_Z, cls.INTERNET_NATIVE
        ]

    @classmethod
    def get_classical_styles(cls) -> List['WritingStyle']:
        """Get all classical and traditional writing styles."""
        return [
            cls.CLASSICAL, cls.TRADITIONAL, cls.VICTORIAN, cls.EDWARDIAN,
            cls.RENAISSANCE, cls.BAROQUE, cls.NEOCLASSICAL
        ]

    @classmethod
    def get_styles_by_complexity(cls, complexity: str) -> List['WritingStyle']:
        """Get writing styles filtered by complexity level."""
        complexity_lower = complexity.lower()
        return [style for style in cls if style.complexity_level == complexity_lower]

    @classmethod
    def get_styles_for_genre(cls, genre: str) -> List['WritingStyle']:
        """Get recommended writing styles for a specific genre."""
        genre_lower = genre.lower()
        
        genre_mappings = {
            "romance": [cls.ROMANTIC, cls.INTIMATE, cls.CONVERSATIONAL, cls.DESCRIPTIVE],
            "mystery": [cls.NOIR, cls.SUSPENSEFUL, cls.ATMOSPHERIC, cls.INVESTIGATIVE],
            "horror": [cls.HORROR, cls.GOTHIC, cls.ATMOSPHERIC, cls.SUSPENSEFUL],
            "fantasy": [cls.EPIC, cls.MYTHIC, cls.DESCRIPTIVE, cls.ATMOSPHERIC],
            "science_fiction": [cls.TECHNICAL, cls.DESCRIPTIVE, cls.CINEMATIC],
            "literary": [cls.LITERARY, cls.POETIC, cls.EXPERIMENTAL, cls.INTROSPECTIVE],
            "academic": [cls.ACADEMIC, cls.SCHOLARLY, cls.FORMAL, cls.ANALYTICAL],
            "business": [cls.BUSINESS, cls.PROFESSIONAL, cls.PERSUASIVE, cls.AUTHORITATIVE],
            "self_help": [cls.CONVERSATIONAL, cls.MOTIVATIONAL, cls.INSTRUCTIONAL],
            "biography": [cls.NARRATIVE, cls.PERSONAL, cls.REFLECTIVE, cls.JOURNALISTIC],
            "children": [cls.CHILDREN_FRIENDLY, cls.PLAYFUL, cls.EDUCATIONAL]
        }
        
        # Find matching styles
        for genre_key, styles in genre_mappings.items():
            if genre_key in genre_lower or genre_lower in genre_key:
                return styles
        
        # Default recommendations for unknown genres
        return [cls.CONVERSATIONAL, cls.NARRATIVE, cls.ACCESSIBLE]

    @classmethod
    def get_trending_styles(cls) -> List['WritingStyle']:
        """Get currently trending writing styles."""
        return [
            cls.CONVERSATIONAL, cls.SOCIAL_MEDIA, cls.BLOG_STYLE,
            cls.ACCESSIBLE, cls.PERSONAL, cls.CONTEMPORARY,
            cls.MILLENNIAL, cls.INSPIRATIONAL, cls.THERAPEUTIC
        ]

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"WritingStyle.{self.name}"