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
    def description(self) -> str:
        """Detailed description of the genre for LLM book generation."""
        descriptions = {
            self.ROMANCE: "Focus on romantic relationships and emotional connections between characters, emphasizing character development, emotional growth, and the journey toward love. Stories should feature compelling romantic tension, believable chemistry, and satisfying emotional payoffs. Include realistic dialogue, intimate moments, and relationship obstacles that feel authentic and engaging.",
            
            self.FANTASY: "Create immersive worlds with magic systems, mythical creatures, and supernatural elements. Build rich, detailed fantasy settings with their own rules, cultures, and histories. Incorporate elements like wizards, dragons, magical artifacts, and epic quests. Focus on world-building that feels consistent and lived-in, with magic that has clear limitations and consequences.",
            
            self.MYSTERY: "Craft intricate puzzles and investigative narratives centered around solving crimes or unexplained events. Include well-planted clues, red herrings, and logical deduction. Create compelling detective characters with unique investigative methods. Maintain suspense while playing fair with readers, ensuring all clues needed for the solution are present in the narrative.",
            
            self.THRILLER: "Build intense, fast-paced narratives with constant tension and escalating stakes. Create scenarios where protagonists face imminent danger or time-sensitive threats. Use short, punchy chapters and cliffhangers to maintain momentum. Focus on psychological pressure, chase sequences, and high-stakes conflicts that keep readers on edge.",
            
            self.SCIENCE_FICTION: "Explore futuristic concepts, advanced technology, and scientific possibilities. Create believable future worlds or alternate realities grounded in scientific principles. Incorporate elements like space travel, artificial intelligence, genetic engineering, or time manipulation. Balance technological concepts with human stories and moral implications of scientific advancement.",
            
            self.YOUNG_ADULT: "Write coming-of-age stories featuring teenage protagonists (16-18 years old) facing age-appropriate challenges. Focus on identity formation, first relationships, family dynamics, and finding one's place in the world. Use accessible language while tackling serious themes. Include authentic teen dialogue and contemporary issues relevant to young adult readers.",
            
            self.HISTORICAL_FICTION: "Set narratives in well-researched historical periods, incorporating authentic details about culture, customs, and daily life. Create characters whose actions and motivations align with their historical context while remaining relatable to modern readers. Include accurate historical events, social norms, and period-appropriate language without overwhelming the story.",
            
            self.HORROR: "Evoke fear, dread, and suspense through supernatural or psychological elements. Create atmospheric tension using vivid, unsettling imagery and pacing that builds to frightening climaxes. Focus on psychological horror over gore, using fear of the unknown and characters' vulnerabilities to create genuine scares that linger with readers.",
            
            self.CONTEMPORARY: "Tell realistic stories set in the present day, focusing on current social issues, relationships, and modern life challenges. Create authentic, relatable characters dealing with contemporary problems like career pressures, family dynamics, social media, and modern relationships. Use current language and reference contemporary culture naturally.",
            
            self.PARANORMAL: "Blend supernatural elements with realistic settings and characters. Include creatures like vampires, werewolves, ghosts, or psychic abilities integrated into otherwise normal worlds. Create rules for supernatural elements and explore how they impact character relationships and daily life. Balance supernatural intrigue with emotional storytelling.",
            
            self.DYSTOPIAN: "Create oppressive future societies that serve as warnings about current social, political, or technological trends. Develop totalitarian governments, social control mechanisms, and protagonists who challenge the system. Explore themes of freedom, individuality, and resistance while creating believable societal structures that feel both futuristic and eerily possible.",
            
            self.ADVENTURE: "Craft action-packed journeys with physical challenges, exotic locations, and heroic protagonists. Include elements like treasure hunts, survival scenarios, exploration of unknown territories, and daring escapes. Focus on external conflicts, physical obstacles, and the thrill of discovery while maintaining character development through trials.",
            
            self.CRIME: "Develop intricate criminal plots featuring law enforcement, criminals, or ordinary people caught in criminal situations. Include realistic police procedures, criminal psychology, and legal processes. Create morally complex characters and explore the motivations behind criminal behavior while maintaining authentic procedural elements.",
            
            self.ROMANTASY: "Combine epic fantasy world-building with central romantic relationships. Create magical worlds where the romantic plot is as important as the fantasy elements. Include fantasy creatures, magic systems, and otherworldly settings while developing deep, passionate romantic connections that drive the plot forward.",
            
            self.DARK_ACADEMIA: "Set stories in prestigious academic institutions with gothic, intellectual atmospheres. Include themes of obsessive pursuit of knowledge, secret societies, classical literature, and morally ambiguous characters. Create settings like elite universities or boarding schools with mysterious traditions and intellectual elitism.",
            
            self.COZY_FANTASY: "Write gentle, low-stakes fantasy focusing on community, comfort, and everyday magic. Avoid large-scale conflicts in favor of personal growth, found family, and magical slice-of-life scenarios. Include cozy settings like magical cafes, enchanted libraries, or friendly magical communities where problems are solved through kindness and cooperation.",
            
            self.CLI_FI: "Address climate change and environmental issues through speculative fiction. Create future scenarios dealing with environmental consequences, exploring human adaptation to climate change. Include realistic scientific elements about environmental degradation while focusing on human resilience, community response, and potential solutions.",
            
            self.LITERARY_FICTION: "Emphasize character development, thematic depth, and literary merit over plot-driven narratives. Use sophisticated prose, complex character psychology, and nuanced exploration of human nature. Focus on internal conflicts, social commentary, and artistic expression while maintaining accessibility and emotional resonance.",
            
            self.DRAMA: "Create emotionally intense stories exploring human relationships and personal struggles. Focus on character-driven narratives dealing with family conflicts, personal crises, moral dilemmas, and life-changing events. Emphasize realistic dialogue and authentic emotional responses to challenging situations.",
            
            self.COMING_OF_AGE: "Chronicle protagonists' transition from youth to adulthood through transformative experiences. Include themes of identity formation, loss of innocence, first love, and developing personal values. Show character growth through challenges that force protagonists to mature and understand themselves better.",
            
            self.WESTERN: "Set narratives in the American frontier period (1860s-1890s) featuring cowboys, outlaws, and frontier life. Include authentic details about Old West culture, conflicts between settlers and Native Americans, lawlessness, and the harsh realities of frontier existence. Focus on themes of justice, survival, and civilization versus wilderness.",
            
            self.COMEDY: "Create humorous narratives using wit, satire, absurd situations, and comedic timing. Include funny dialogue, amusing character interactions, and situations that highlight human folly. Balance humor with character development and ensure comedy serves the story rather than overshadowing it.",
            
            self.SATIRE: "Use humor, irony, and exaggeration to criticize societal flaws, institutions, or human behavior. Create sharp, intelligent commentary on contemporary issues while entertaining readers. Include witty observations, clever wordplay, and situations that expose hypocrisy or absurdity in human nature or society.",
            
            self.SELF_HELP: "Provide practical advice, strategies, and insights for personal improvement and life enhancement. Include actionable steps, real-world examples, and evidence-based approaches to common challenges. Focus on empowering readers with tools and knowledge they can immediately apply to improve their lives.",
            
            self.MEMOIR: "Share personal life experiences with honesty, vulnerability, and insight. Include significant life events, personal growth, challenges overcome, and lessons learned. Use authentic voice and emotional truth while crafting narrative structure that engages readers and provides universal insights from personal experiences.",
            
            self.BIOGRAPHY: "Chronicle the life story of notable individuals with thorough research and engaging narrative structure. Include significant achievements, personal struggles, historical context, and the subject's impact on their field or society. Present factual information in compelling storytelling format.",
            
            self.BUSINESS: "Provide insights into business strategy, entrepreneurship, leadership, and professional development. Include case studies, practical frameworks, and actionable advice for business success. Focus on evidence-based approaches, real-world applications, and strategies that readers can implement in their professional lives.",
            
            self.HEALTH: "Offer evidence-based information about physical and mental wellness, medical conditions, and healthy lifestyle choices. Include practical advice, scientific research, and holistic approaches to health. Focus on empowering readers to make informed decisions about their health and wellbeing.",
            
            self.TRUE_CRIME: "Investigate real criminal cases with meticulous research and compelling narrative structure. Include factual details about crimes, investigations, legal proceedings, and the people involved. Balance respect for victims with engaging storytelling while exploring criminal psychology and justice system processes.",
            
            self.TRAVEL: "Provide practical information and inspiring narratives about destinations, cultures, and travel experiences. Include detailed guides, cultural insights, practical tips, and personal travel stories. Help readers plan their own journeys while sharing the transformative power of travel and cultural exploration.",
            
            self.COOKING: "Share recipes, cooking techniques, and food culture with clear instructions and engaging food stories. Include ingredient information, cooking methods, cultural context, and personal connections to food. Make cooking accessible and enjoyable while celebrating culinary traditions and innovation.",
            
            self.HISTORY: "Present historical events, periods, and figures with accurate research and engaging narrative style. Include social, political, and cultural context while making historical information accessible and relevant to contemporary readers. Focus on human stories within historical events.",
            
            self.SCIENCE: "Explain scientific concepts, discoveries, and research with clarity and enthusiasm. Include current scientific understanding, research methodologies, and implications for society. Make complex scientific ideas accessible to general readers while maintaining accuracy and fostering scientific literacy.",
            
            self.TECHNOLOGY: "Explore technological developments, digital trends, and their impact on society. Include practical guides, future predictions, and analysis of how technology shapes human behavior and social structures. Help readers understand and navigate rapidly evolving technological landscapes.",
            
            self.EDUCATION: "Provide learning resources, teaching methodologies, and educational insights for students, educators, and lifelong learners. Include practical strategies, research-based approaches, and tools for effective learning and instruction.",
            
            self.REFERENCE: "Create comprehensive, authoritative resources for quick information lookup and detailed study. Include well-organized information, clear explanations, and practical applications. Focus on accuracy, completeness, and user-friendly organization for easy navigation.",
            
            self.PHILOSOPHY: "Explore fundamental questions about existence, knowledge, values, and human nature through rational inquiry and critical thinking. Include major philosophical traditions, ethical dilemmas, and practical applications of philosophical concepts to contemporary life.",
            
            self.RELIGION: "Examine religious beliefs, practices, and spiritual traditions with respect and scholarly approach. Include theological concepts, religious history, and the role of faith in human experience while remaining accessible to diverse audiences.",
            
            self.POLITICS: "Analyze political systems, governance, and civic engagement with balanced, informative approach. Include current events, political theory, and practical information about democratic participation while maintaining objectivity and encouraging informed citizenship.",
            
            self.PSYCHOLOGY: "Explore human behavior, mental processes, and psychological research with scientific accuracy and practical applications. Include psychological theories, research findings, and insights into human nature that help readers understand themselves and others better.",
            
            self.CHILDREN: "Create age-appropriate stories with engaging characters, simple but meaningful plots, and positive messages. Include themes of friendship, family, learning, and growing up. Use language and situations appropriate for the target age group while providing entertainment and gentle life lessons.",
            
            self.PICTURE_BOOK: "Develop visual storytelling combining text and illustrations for young readers. Include simple, engaging narratives that work with visual elements to tell complete stories. Focus on concepts appropriate for preschool and early elementary ages with repetitive patterns and memorable characters.",
            
            self.POETRY: "Create expressive, rhythmic language that captures emotions, images, and experiences through carefully chosen words and literary devices. Include various poetic forms, themes, and styles while focusing on the musicality and emotional impact of language.",
            
            self.TEXTBOOK: "Provide comprehensive educational content organized for systematic learning and instruction. Include clear explanations, examples, exercises, and assessment tools. Focus on pedagogical effectiveness and accurate, up-to-date information presented in logical sequence.",
            
            self.OTHER: "Create unique narratives that don't fit traditional genre categories but still provide engaging storytelling. Focus on innovative approaches, experimental formats, or genre-blending techniques while maintaining reader engagement and narrative coherence."
        }
        return descriptions.get(self, f"Genre focusing on {self.display_name.lower()} storytelling and themes.")

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

    #CHILDREN BOOKS
    CHILDREN_BOOK = "children_book"

    @property
    def description(self) -> str:
        """Detailed description of the subgenre for LLM book generation."""
        descriptions = {
            # Romance subgenres
            self.CONTEMPORARY_ROMANCE: "Set romantic stories in current times with modern settings, technology, and social situations. Focus on realistic relationship challenges like career conflicts, family dynamics, social media impact, and contemporary dating. Include authentic modern dialogue, current cultural references, and relatable everyday situations that modern readers experience.",
            
            self.HISTORICAL_ROMANCE: "Create passionate love stories set in meticulously researched historical periods, typically before 1950. Include accurate historical details about clothing, customs, social hierarchies, and daily life. Address period-appropriate obstacles to romance like arranged marriages, class differences, or social conventions while maintaining emotional authenticity.",
            
            self.PARANORMAL_ROMANCE: "Blend supernatural elements with romantic relationships, featuring characters like vampires, werewolves, angels, demons, or humans with psychic abilities. Create detailed supernatural world-building with consistent rules while maintaining focus on the romantic relationship. Balance otherworldly elements with emotional intimacy and character development.",
            
            self.ROMANTIC_SUSPENSE: "Combine romantic tension with thriller elements like danger, mystery, or crime. Create scenarios where romance develops amid life-threatening situations, investigations, or high-stakes conflicts. Maintain both romantic and suspenseful pacing, ensuring both elements enhance rather than compete with each other.",
            
            self.DARK_ROMANCE: "Explore intense, morally complex romantic relationships often featuring anti-heroes, taboo themes, or psychologically challenging dynamics. Include elements like obsession, power imbalances, or morally ambiguous characters while maintaining the fundamental romantic arc. Handle sensitive themes with depth and emotional complexity.",
            
            self.ROMANTIC_COMEDY: "Create light-hearted romantic stories emphasizing humor, wit, and amusing situations. Include comedic misunderstandings, funny supporting characters, and situations that highlight the absurdity of love and relationships. Balance humor with genuine romantic development and emotional authenticity.",
            
            self.SPORTS_ROMANCE: "Center romantic stories around athletic characters, sports teams, or competitive environments. Include authentic sports details, team dynamics, and the physical and mental demands of athletic competition. Explore how sports careers impact relationships and use athletic metaphors for romantic development.",
            
            self.BILLIONAIRE_ROMANCE: "Feature wealthy, powerful protagonists dealing with romance amid luxury, corporate intrigue, and high-society expectations. Include authentic details about wealth, business operations, and exclusive lifestyle while exploring how money and power affect romantic relationships. Balance wish-fulfillment with realistic character flaws and growth.",
            
            self.ENEMIES_TO_LOVERS: "Develop romantic relationships between characters who initially dislike, compete with, or oppose each other. Create believable reasons for initial antagonism and realistic progression toward love. Include compelling banter, gradually revealed misconceptions, and authentic emotional transformation from hostility to attraction.",
            
            self.SECOND_CHANCE_ROMANCE: "Tell stories of former lovers who reconnect after separation, exploring themes of forgiveness, growth, and renewed love. Include realistic reasons for initial breakup, personal development during separation, and authentic obstacles to reconciliation. Show how characters have matured and what they've learned from their time apart.",
            
            # Fantasy subgenres
            self.HIGH_FANTASY: "Create epic fantasy worlds completely separate from our reality, featuring complex magic systems, mythical creatures, and detailed world-building. Include multiple races, kingdoms, and cultures with their own languages, customs, and histories. Focus on grand quests, chosen heroes, and battles between good and evil with high stakes and epic scope.",
            
            self.URBAN_FANTASY: "Set fantasy elements within contemporary urban environments, blending magical creatures and supernatural powers with modern city life. Include hidden magical communities existing alongside mundane society, supernatural politics, and protagonists who navigate both worlds. Balance modern technology with ancient magic and folklore.",
            
            self.DARK_FANTASY: "Combine fantasy elements with horror, psychological darkness, or morally ambiguous themes. Include sinister magic, cursed kingdoms, anti-heroes, and exploration of humanity's darker impulses. Create atmospheric, gothic settings where magic comes with terrible costs and heroes face morally complex choices.",
            
            self.EPIC_FANTASY: "Develop vast, sweeping narratives spanning multiple books with world-shaking events, multiple viewpoint characters, and complex political intrigue. Include detailed world-building, extensive character development, and storylines that affect entire civilizations. Focus on grand themes of destiny, power, and the fate of worlds.",
            
            self.PORTAL_FANTASY: "Feature characters who travel from our world to fantastic realms through magical portals, wardrobes, or other transitions. Include fish-out-of-water elements as modern characters adapt to magical worlds. Explore themes of belonging, identity, and choosing between worlds while developing both the familiar and fantastic settings.",
            
            self.FAIRY_TALE_RETELLING: "Reimagine classic fairy tales with fresh perspectives, updated settings, or deeper character development. Include familiar story elements while subverting expectations or exploring themes from different angles. Balance nostalgia for original tales with innovative storytelling and contemporary relevance.",
            
            self.SWORD_AND_SORCERY: "Focus on action-packed adventures featuring warrior protagonists, magical combat, and episodic quests. Include detailed fight scenes, exotic locations, and straightforward good-versus-evil conflicts. Emphasize individual heroism, physical prowess, and immediate adventures over complex political intrigue.",
            
            # Romantasy
            self.ROMANTASY_SUB: "Seamlessly blend epic fantasy world-building with central romantic plotlines where both fantasy adventure and romantic development are equally important. Include detailed magical worlds, fantasy creatures, and epic quests while maintaining focus on passionate romantic relationships that drive the plot forward.",
            
            # Cozy Fantasy
            self.COZY_FANTASY_SUB: "Create gentle, comforting fantasy stories focusing on community, friendship, and everyday magic rather than epic conflicts. Include magical elements like talking animals, helpful spirits, or enchanted objects in domestic settings. Emphasize problem-solving through kindness, cooperation, and the warmth of found family.",
            
            # Mystery subgenres
            self.COZY_MYSTERY: "Develop amateur detective stories set in small communities with minimal violence and emphasis on puzzle-solving over graphic crime. Include quirky local characters, community settings like bookshops or cafes, and protagonists who stumble into mysteries. Focus on intellectual puzzle-solving and character relationships.",
            
            self.POLICE_PROCEDURAL: "Create realistic crime investigations following proper police methods, forensic procedures, and legal processes. Include authentic details about police work, evidence collection, and investigative techniques. Focus on teamwork, methodical investigation, and the professional lives of law enforcement officers.",
            
            self.DETECTIVE_FICTION: "Feature professional or amateur detectives solving complex crimes through observation, deduction, and investigation. Include compelling detective characters with unique methods, interesting cases with multiple suspects, and fair-play clues that allow readers to solve mysteries alongside the detective.",
            
            self.NOIR: "Create dark, cynical crime stories featuring morally ambiguous characters, urban settings, and themes of corruption and moral decay. Include atmospheric descriptions, first-person narration, femme fatales, and protagonists caught in webs of deceit. Emphasize mood and character psychology over puzzle-solving.",
            
            # Thriller subgenres
            self.PSYCHOLOGICAL_THRILLER: "Focus on the mental and emotional states of characters, exploring psychological manipulation, unreliable narrators, and mind games. Include twisted relationships, paranoia, and situations where characters question their own perceptions. Emphasize psychological tension over physical action.",
            
            self.DOMESTIC_THRILLER: "Center suspenseful stories around family relationships, marriages, and household secrets. Include themes of betrayal, hidden identities, and danger within intimate relationships. Focus on how ordinary domestic situations can become threatening and how well we really know those closest to us.",
            
            self.LEGAL_THRILLER: "Combine courtroom drama with suspenseful elements, featuring lawyers, judges, or legal cases with high stakes. Include authentic legal procedures, ethical dilemmas, and cases that threaten characters' careers or lives. Balance legal authenticity with dramatic tension and character development.",
            
            self.TECHNO_THRILLER: "Incorporate advanced technology, cybercrime, or scientific developments into suspenseful plots. Include realistic technical details about computers, weapons, medical advances, or surveillance technology. Explore how technology can be both beneficial and threatening to society and individuals.",
            
            self.SPY_THRILLER: "Feature espionage, international intrigue, and intelligence operations with realistic tradecraft and global political situations. Include authentic spy techniques, international settings, and complex political motivations. Balance action sequences with intellectual strategy and character development.",
            
            self.MEDICAL_THRILLER: "Set suspenseful stories within medical environments, featuring diseases, medical conspiracies, or healthcare professionals facing dangerous situations. Include authentic medical details, hospital settings, and scenarios involving public health threats or medical ethics dilemmas.",
            
            # Science Fiction subgenres
            self.SPACE_OPERA: "Create epic science fiction adventures set across galaxies with space battles, alien civilizations, and grand-scale conflicts. Include detailed space technology, multiple alien species, and storylines spanning star systems. Focus on adventure, heroism, and the wonder of space exploration.",
            
            self.CYBERPUNK: "Set stories in high-tech, dystopian futures focusing on computer hackers, artificial intelligence, and corporate control. Include urban decay, advanced cybernetics, virtual reality, and themes of humanity versus technology. Create dark, neon-lit worlds where technology has transformed society.",
            
            self.DYSTOPIAN_SF: "Develop oppressive future societies serving as warnings about technological, political, or social trends. Include totalitarian governments, surveillance states, and protagonists who challenge systematic oppression. Explore themes of freedom, individuality, and resistance to authoritarian control.",
            
            self.HARD_SF: "Base science fiction elements on rigorous scientific accuracy and plausible technological developments. Include detailed scientific explanations, realistic space travel, and scenarios grounded in current scientific understanding. Focus on how scientific advancement affects human society and individuals.",
            
            self.SOFT_SF: "Emphasize social sciences, character development, and human relationships over hard science and technology. Include speculative societies, psychological studies, and exploration of how social changes affect human behavior. Focus on people rather than technology or scientific concepts.",
            
            self.TIME_TRAVEL: "Feature characters traveling through time with consistent rules for temporal mechanics and consequences of changing history. Include paradoxes, alternate timelines, and exploration of how actions in the past affect the future. Balance time travel concepts with character development and emotional stakes.",
            
            self.POST_APOCALYPTIC: "Set stories after civilization-ending disasters, focusing on survival and rebuilding society. Include realistic survival challenges, community formation, and exploration of human nature under extreme circumstances. Show how people adapt to fundamentally changed world conditions.",
            
            self.ALIEN_CONTACT: "Explore first contact scenarios between humans and extraterrestrial life forms. Include realistic speculation about alien biology, communication challenges, and diplomatic or military responses to contact. Focus on how alien contact would affect human society and individual characters.",
            
            self.BIOPUNK: "Focus on biotechnology, genetic engineering, and biological rather than mechanical technology. Include genetic modification, bioengineering, and societies where biology is the dominant technology. Explore ethical implications of genetic manipulation and biological enhancement.",
            
            self.CLI_FI_SUB: "Address climate change through speculative fiction, exploring future environmental scenarios and human adaptation. Include realistic climate science, environmental consequences, and human responses to environmental challenges. Focus on both problems and potential solutions.",
            
            # Young Adult subgenres
            self.YA_FANTASY: "Create fantasy adventures featuring teenage protagonists discovering magical abilities or entering fantasy worlds. Include age-appropriate themes of identity, belonging, and first love while incorporating fantasy elements. Focus on coming-of-age themes within fantasy settings.",
            
            self.YA_ROMANCE: "Develop romantic stories featuring teenage characters experiencing first love, heartbreak, and relationship challenges. Include authentic teen dialogue, school settings, and age-appropriate romantic development. Focus on emotional growth and learning about healthy relationships.",
            
            self.YA_DYSTOPIAN: "Set stories in oppressive future societies with teenage protagonists challenging the system. Include themes of rebellion, identity formation, and finding one's place in society. Show young people discovering their power to create change in their world.",
            
            self.YA_CONTEMPORARY: "Tell realistic stories about modern teenagers dealing with contemporary issues like family problems, school challenges, social media, and identity formation. Include authentic teen experiences, diverse backgrounds, and current social issues relevant to young adult readers.",
            
            self.YA_THRILLER: "Create suspenseful stories featuring teenage protagonists in dangerous situations. Include age-appropriate threats, school or community settings, and themes of trust, loyalty, and personal courage. Balance thrilling elements with character development and realistic teen experiences.",
            
            self.YA_SCIENCE_FICTION: "Develop science fiction stories with teenage protagonists exploring futuristic concepts. Include themes of technology's impact on young people, identity in changing worlds, and how young characters adapt to or challenge technological or social changes.",
            
            self.YA_PARANORMAL: "Combine supernatural elements with teenage protagonists experiencing paranormal abilities or encounters. Include themes of being different, finding acceptance, and learning to control new abilities. Balance supernatural elements with realistic teen emotional development.",
            
            self.YA_HISTORICAL: "Set coming-of-age stories in historical periods, focusing on how young people navigate historical events and social conditions. Include accurate historical details while exploring universal themes of identity, belonging, and growing up during significant historical moments.",
            
            self.COMING_OF_AGE_SUB: "Focus specifically on the transition from childhood to adulthood through transformative experiences. Include themes of identity formation, moral development, and learning life lessons. Show characters gaining wisdom, independence, and self-understanding through challenges.",
            
            # Horror subgenres
            self.PSYCHOLOGICAL_HORROR: "Create fear through psychological manipulation, mental instability, and characters questioning their own perceptions. Include unreliable narrators, paranoia, and situations where characters' minds become their own worst enemies. Focus on internal terror rather than external threats.",
            
            self.SUPERNATURAL_HORROR: "Feature ghosts, demons, evil spirits, or otherworldly entities threatening characters. Include paranormal investigations, haunted locations, and characters dealing with forces beyond human understanding. Create atmospheric dread and otherworldly threats.",
            
            self.GOTHIC_HORROR: "Develop atmospheric horror using decaying mansions, family curses, and psychological darkness. Include elements like mysterious ancestral homes, tragic family histories, and characters haunted by past sins. Create mood through setting and atmosphere rather than graphic content.",
            
            self.COSMIC_HORROR: "Explore existential dread and humanity's insignificance in the face of incomprehensible cosmic forces. Include ancient entities, forbidden knowledge, and characters discovering terrifying truths about reality. Focus on fear of the unknown and humanity's fragile place in the universe.",
            
            self.BODY_HORROR: "Feature physical transformation, disease, or bodily corruption as sources of horror. Include themes of loss of bodily autonomy, mutation, and disgust. Focus on visceral fear while exploring deeper themes about identity, mortality, and what makes us human.",
            
            self.HAUNTED_HOUSE: "Center horror around specific locations inhabited by ghosts or evil presences. Include detailed descriptions of haunted settings, supernatural manifestations, and characters trapped in dangerous locations. Create atmosphere through environmental storytelling and escalating supernatural events.",
            
            self.ZOMBIE: "Feature reanimated corpses threatening survivors in post-apocalyptic scenarios. Include survival elements, group dynamics under stress, and exploration of what makes us human. Focus on human drama and moral choices during zombie apocalypse scenarios.",
            
            self.VAMPIRE: "Feature vampires as central characters, whether as threats, protagonists, or complex anti-heroes. Include vampire mythology, eternal life themes, and exploration of humanity versus monstrosity. Create compelling vampire characters with depth beyond traditional stereotypes.",
            
            self.SLASHER: "Feature serial killers or masked murderers stalking and killing characters, typically in isolated settings. Include suspenseful cat-and-mouse dynamics, survival themes, and final confrontations between killer and protagonist. Focus on tension and survival rather than graphic violence.",
            
            # Non-Fiction subgenres
            self.MOTIVATIONAL: "Provide inspiration and practical strategies for personal achievement, goal-setting, and overcoming obstacles. Include success stories, actionable advice, and psychological insights about motivation and persistence. Focus on empowering readers to take positive action in their lives.",
            
            self.PERSONAL_FINANCE: "Offer practical advice about money management, investing, budgeting, and building wealth. Include specific strategies, real-world examples, and step-by-step guides for financial improvement. Make complex financial concepts accessible to general readers.",
            
            self.CAREER_DEVELOPMENT: "Provide guidance for professional growth, job searching, skill development, and workplace success. Include industry insights, networking strategies, and practical advice for career advancement. Focus on actionable steps readers can take to improve their professional lives.",
            
            self.RELATIONSHIP_ADVICE: "Offer insights and strategies for improving personal relationships, communication skills, and social connections. Include psychological research, practical exercises, and real-world applications for building stronger relationships with family, friends, and romantic partners.",
            
            self.MINDFULNESS: "Teach meditation, present-moment awareness, and stress reduction techniques based on mindfulness practices. Include practical exercises, scientific research on mindfulness benefits, and applications for daily life. Make contemplative practices accessible to modern readers.",
            
            self.PRODUCTIVITY: "Provide systems and strategies for improving efficiency, time management, and goal achievement. Include practical tools, organizational methods, and techniques for overcoming procrastination and distractions. Focus on sustainable approaches to increased productivity.",
            
            self.ENTREPRENEURSHIP: "Guide readers through starting and running businesses, including business planning, funding, marketing, and growth strategies. Include real entrepreneur stories, practical frameworks, and actionable advice for business success. Address both opportunities and challenges of entrepreneurship.",
            
            self.LEADERSHIP: "Develop leadership skills, management techniques, and strategies for inspiring and guiding others. Include case studies of successful leaders, psychological insights about leadership, and practical applications for various leadership contexts.",
            
            self.MARKETING: "Teach marketing strategies, consumer psychology, and promotional techniques for businesses and personal brands. Include current marketing trends, digital marketing strategies, and practical applications for different industries and business sizes.",
            
            self.BUSINESS_STRATEGY: "Provide frameworks for strategic thinking, competitive analysis, and long-term business planning. Include case studies, strategic models, and practical tools for business decision-making and strategic development.",
            
            self.FITNESS: "Offer exercise programs, training techniques, and physical wellness strategies for improved health and fitness. Include scientific research, practical workout plans, and motivation for maintaining active lifestyles. Make fitness accessible to readers of various fitness levels.",
            
            self.NUTRITION: "Provide evidence-based information about healthy eating, dietary choices, and nutritional science. Include practical meal planning, recipe ideas, and guidance for making informed food choices. Balance scientific accuracy with practical application.",
            
            self.MENTAL_HEALTH: "Address psychological wellness, emotional regulation, and strategies for maintaining good mental health. Include professional insights, self-help techniques, and resources for mental health support. Approach sensitive topics with care and professional accuracy.",
            
            self.ALTERNATIVE_MEDICINE: "Explore complementary and alternative health approaches, including traditional remedies, holistic practices, and integrative medicine. Include research on alternative treatments while maintaining balanced perspective on their effectiveness and limitations.",
            
            self.COOKING_SUB: "Provide recipes, cooking techniques, and culinary knowledge for home cooks. Include ingredient information, step-by-step instructions, and cultural context for dishes. Make cooking accessible and enjoyable while sharing culinary traditions and innovations.",
            
            self.TRAVEL_GUIDE: "Offer comprehensive information about destinations, including practical travel advice, cultural insights, and detailed guides for travelers. Include transportation options, accommodation recommendations, and cultural sensitivity guidelines for respectful travel.",
            
            self.DIY_CRAFTS: "Provide instructions and inspiration for handmade projects, crafting techniques, and creative skills. Include step-by-step tutorials, material lists, and tips for successful project completion. Make crafting accessible to beginners while offering challenges for advanced crafters.",
            
            self.TECHNOLOGY_GUIDE: "Explain technological concepts, provide user guides, and help readers navigate digital tools and trends. Include practical applications, troubleshooting advice, and insights into how technology affects daily life and society.",
            
            self.TRUE_CRIME_SUB: "Investigate real criminal cases with thorough research, compelling narrative, and respectful treatment of victims and their families. Include factual details about crimes, investigations, and legal proceedings while exploring criminal psychology and justice system processes.",
            
            self.CELEBRITY_BIOGRAPHY: "Chronicle the lives of famous individuals, including their achievements, personal struggles, and impact on their fields. Include extensive research, interviews, and balanced perspectives on both public and private aspects of celebrity lives.",
            
            self.HISTORICAL_BIOGRAPHY: "Tell the life stories of historically significant figures with thorough research and engaging narrative style. Include historical context, primary source material, and exploration of how individuals shaped or reflected their historical periods.",
            
            # Children's Books
            self.CHILDREN_BOOK: "Create age-appropriate stories with engaging characters, simple but meaningful plots, and positive messages for young readers. Include themes of friendship, family, learning, and growing up while using language and situations appropriate for the target age group. Focus on entertainment, gentle life lessons, and fostering love of reading."
        }
        return descriptions.get(self, f"Subgenre focusing on {self.display_name.lower()} elements and themes.")

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
            "children_book": cls.CHILDREN_BOOK
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

        GenreType.CHILDREN: {
            SubGenreType.CHILDREN_BOOK,
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