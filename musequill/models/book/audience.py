from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
import json


class AudienceType(str, Enum):
    """Comprehensive target audience types for book generation."""
    
    # General Audiences
    GENERAL_READERS = "general_readers"
    MAINSTREAM_AUDIENCE = "mainstream_audience"
    CASUAL_READERS = "casual_readers"
    AVID_READERS = "avid_readers"
    
    # Age-Based Audiences
    CHILDREN = "children"
    MIDDLE_GRADE = "middle_grade"
    YOUNG_ADULT = "young_adult"
    NEW_ADULT = "new_adult"
    ADULT = "adult"
    MATURE_ADULT = "mature_adult"
    SENIORS = "seniors"
    
    # Genre-Specific Audiences
    GENRE_FANS = "genre_fans"
    FANTASY_READERS = "fantasy_readers"
    SCI_FI_FANS = "sci_fi_fans"
    MYSTERY_LOVERS = "mystery_lovers"
    ROMANCE_READERS = "romance_readers"
    HORROR_FANS = "horror_fans"
    LITERARY_FICTION_READERS = "literary_fiction_readers"
    NON_FICTION_READERS = "non_fiction_readers"
    
    # Professional & Career Audiences
    PROFESSIONALS = "professionals"
    BUSINESS_PROFESSIONALS = "business_professionals"
    HEALTHCARE_WORKERS = "healthcare_workers"
    EDUCATORS = "educators"
    LAWYERS = "lawyers"
    ENGINEERS = "engineers"
    MARKETERS = "marketers"
    CONSULTANTS = "consultants"
    MANAGERS = "managers"
    EXECUTIVES = "executives"
    ENTREPRENEURS = "entrepreneurs"
    
    # Academic & Educational Audiences
    ACADEMICS = "academics"
    RESEARCHERS = "researchers"
    SCHOLARS = "scholars"
    STUDENTS = "students"
    GRADUATE_STUDENTS = "graduate_students"
    UNDERGRADUATE_STUDENTS = "undergraduate_students"
    LIFELONG_LEARNERS = "lifelong_learners"
    
    # Skill Level Audiences
    BEGINNERS = "beginners"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERTS = "experts"
    HOBBYISTS = "hobbyists"
    ENTHUSIASTS = "enthusiasts"
    
    # Creative & Technical Audiences
    CREATIVES = "creatives"
    ARTISTS = "artists"
    WRITERS = "writers"
    DESIGNERS = "designers"
    MUSICIANS = "musicians"
    FILMMAKERS = "filmmakers"
    TECHNICAL_AUDIENCE = "technical_audience"
    DEVELOPERS = "developers"
    DATA_SCIENTISTS = "data_scientists"
    
    # Lifestyle & Interest Audiences
    PARENTS = "parents"
    NEW_PARENTS = "new_parents"
    WORKING_PARENTS = "working_parents"
    FITNESS_ENTHUSIASTS = "fitness_enthusiasts"
    HEALTH_CONSCIOUS = "health_conscious"
    SPIRITUAL_SEEKERS = "spiritual_seekers"
    SELF_IMPROVEMENT = "self_improvement"
    TRAVEL_ENTHUSIASTS = "travel_enthusiasts"
    FOOD_LOVERS = "food_lovers"
    
    # Niche & Specialized Audiences
    COLLECTORS = "collectors"
    GAMERS = "gamers"
    INVESTORS = "investors"
    RETIREES = "retirees"
    MILITARY = "military"
    VETERANS = "veterans"
    IMMIGRANTS = "immigrants"
    CAREGIVERS = "caregivers"
    ACTIVISTS = "activists"
    
    # Reading Behavior Audiences
    COMMUTERS = "commuters"
    BEDTIME_READERS = "bedtime_readers"
    AUDIOBOOK_LISTENERS = "audiobook_listeners"
    QUICK_READERS = "quick_readers"
    SLOW_READERS = "slow_readers"
    RE_READERS = "re_readers"

    # Gender & Demographics  
    WOMEN = "women"
    MEN = "men"
    ADULTS = "adults"

    # Family & Social Groups
    FAMILIES = "families"
    TEENS = "teens"

    # Lifestyle Categories
    ADVENTURERS = "adventurers"
    LIFESTYLE_READERS = "lifestyle_readers"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            # General Audiences
            self.GENERAL_READERS: "General Readers",
            self.MAINSTREAM_AUDIENCE: "Mainstream Audience",
            self.CASUAL_READERS: "Casual Readers",
            self.AVID_READERS: "Avid Readers",
            
            # Age-Based Audiences
            self.CHILDREN: "Children",
            self.MIDDLE_GRADE: "Middle Grade Readers",
            self.YOUNG_ADULT: "Young Adult Readers",
            self.NEW_ADULT: "New Adult Readers",
            self.ADULT: "Adult Readers",
            self.MATURE_ADULT: "Mature Adult Readers",
            self.SENIORS: "Senior Readers",
            
            # Genre-Specific Audiences
            self.GENRE_FANS: "Genre Fans",
            self.FANTASY_READERS: "Fantasy Readers",
            self.SCI_FI_FANS: "Science Fiction Fans",
            self.MYSTERY_LOVERS: "Mystery Lovers",
            self.ROMANCE_READERS: "Romance Readers",
            self.HORROR_FANS: "Horror Fans",
            self.LITERARY_FICTION_READERS: "Literary Fiction Readers",
            self.NON_FICTION_READERS: "Non-Fiction Readers",
            
            # Professional & Career Audiences
            self.PROFESSIONALS: "Professionals",
            self.BUSINESS_PROFESSIONALS: "Business Professionals",
            self.HEALTHCARE_WORKERS: "Healthcare Workers",
            self.EDUCATORS: "Educators",
            self.LAWYERS: "Lawyers",
            self.ENGINEERS: "Engineers",
            self.MARKETERS: "Marketers",
            self.CONSULTANTS: "Consultants",
            self.MANAGERS: "Managers",
            self.EXECUTIVES: "Executives",
            self.ENTREPRENEURS: "Entrepreneurs",
            
            # Academic & Educational Audiences
            self.ACADEMICS: "Academics",
            self.RESEARCHERS: "Researchers",
            self.SCHOLARS: "Scholars",
            self.STUDENTS: "Students",
            self.GRADUATE_STUDENTS: "Graduate Students",
            self.UNDERGRADUATE_STUDENTS: "Undergraduate Students",
            self.LIFELONG_LEARNERS: "Lifelong Learners",
            
            # Skill Level Audiences
            self.BEGINNERS: "Beginners",
            self.INTERMEDIATE: "Intermediate Level",
            self.ADVANCED: "Advanced Level",
            self.EXPERTS: "Experts",
            self.HOBBYISTS: "Hobbyists",
            self.ENTHUSIASTS: "Enthusiasts",
            
            # Creative & Technical Audiences
            self.CREATIVES: "Creative Professionals",
            self.ARTISTS: "Artists",
            self.WRITERS: "Writers",
            self.DESIGNERS: "Designers",
            self.MUSICIANS: "Musicians",
            self.FILMMAKERS: "Filmmakers",
            self.TECHNICAL_AUDIENCE: "Technical Audience",
            self.DEVELOPERS: "Software Developers",
            self.DATA_SCIENTISTS: "Data Scientists",
            
            # Lifestyle & Interest Audiences
            self.PARENTS: "Parents",
            self.NEW_PARENTS: "New Parents",
            self.WORKING_PARENTS: "Working Parents",
            self.FITNESS_ENTHUSIASTS: "Fitness Enthusiasts",
            self.HEALTH_CONSCIOUS: "Health-Conscious Readers",
            self.SPIRITUAL_SEEKERS: "Spiritual Seekers",
            self.SELF_IMPROVEMENT: "Self-Improvement Seekers",
            self.TRAVEL_ENTHUSIASTS: "Travel Enthusiasts",
            self.FOOD_LOVERS: "Food Lovers",
            
            # Niche & Specialized Audiences
            self.COLLECTORS: "Collectors",
            self.GAMERS: "Gamers",
            self.INVESTORS: "Investors",
            self.RETIREES: "Retirees",
            self.MILITARY: "Military Personnel",
            self.VETERANS: "Veterans",
            self.IMMIGRANTS: "Immigrants",
            self.CAREGIVERS: "Caregivers",
            self.ACTIVISTS: "Activists",
            
            # Reading Behavior Audiences
            self.COMMUTERS: "Commuters",
            self.BEDTIME_READERS: "Bedtime Readers",
            self.AUDIOBOOK_LISTENERS: "Audiobook Listeners",
            self.QUICK_READERS: "Quick Readers",
            self.SLOW_READERS: "Thoughtful Readers",
            self.RE_READERS: "Re-Readers",

            # ---
            self.WOMEN: "Women Readers",
            self.MEN: "Men Readers", 
            self.FAMILIES: "Families",
            self.TEENS: "Teen Readers",
            self.ADVENTURERS: "Adventure Seekers",
            self.LIFESTYLE_READERS: "Lifestyle Readers",
            self.ADULTS: "Adults"
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Detailed description of the audience type."""
        descriptions = {
            # General Audiences
            self.GENERAL_READERS: "Broad audience of readers who enjoy various genres and don't have specific preferences, seeking accessible and engaging content across different topics and styles.",
            self.MAINSTREAM_AUDIENCE: "Mass market readers who prefer popular, widely-appealing content that reflects current trends, bestseller appeal, and broad cultural relevance.",
            self.CASUAL_READERS: "Occasional readers who read for relaxation and entertainment, preferring easy-to-follow stories with straightforward narratives and familiar themes.",
            self.AVID_READERS: "Voracious readers who consume books regularly, appreciate literary quality, and are open to complex narratives, diverse genres, and challenging content.",
            
            # Age-Based Audiences
            self.CHILDREN: "Young readers typically aged 5-12 who enjoy age-appropriate stories with simple language, engaging illustrations, and themes relevant to childhood experiences.",
            self.MIDDLE_GRADE: "Readers aged 8-12 who are developing independent reading skills and enjoy adventure stories, friendship themes, and coming-of-age narratives with relatable protagonists.",
            self.YOUNG_ADULT: "Teenage readers aged 13-18 who connect with stories about identity, relationships, social issues, and the transition to adulthood, often featuring teenage protagonists.",
            self.NEW_ADULT: "Readers aged 18-25 experiencing life transitions like college, first jobs, and serious relationships, seeking stories about independence and adult decision-making.",
            self.ADULT: "Mature readers aged 25+ who appreciate complex narratives, diverse themes, sophisticated character development, and stories reflecting adult experiences and responsibilities.",
            self.MATURE_ADULT: "Experienced readers aged 40+ who value depth, nuance, and reflection in their reading, often drawn to literary fiction, historical narratives, and contemplative themes.",
            self.SENIORS: "Older readers aged 65+ who may prefer larger print, familiar themes, nostalgic elements, and stories that reflect their life experiences and wisdom.",
            
            # Genre-Specific Audiences
            self.GENRE_FANS: "Dedicated readers who have strong preferences for specific genres and deeply understand genre conventions, tropes, and expect high-quality execution within their preferred categories.",
            self.FANTASY_READERS: "Fans of fantasy literature who enjoy magical worlds, mythical creatures, epic quests, and complex world-building with detailed magic systems and heroic journeys.",
            self.SCI_FI_FANS: "Science fiction enthusiasts who appreciate futuristic concepts, technological speculation, space exploration, and stories that explore the implications of scientific advancement.",
            self.MYSTERY_LOVERS: "Readers who enjoy puzzles, detective work, crime-solving, and the intellectual challenge of following clues and unraveling complex plots and mysteries.",
            self.ROMANCE_READERS: "Fans of romantic fiction who seek emotional connection, relationship development, and stories centered on love, attraction, and romantic fulfillment.",
            self.HORROR_FANS: "Readers who enjoy being frightened and appreciate supernatural elements, psychological thriller aspects, and stories designed to create fear, suspense, and unease.",
            self.LITERARY_FICTION_READERS: "Sophisticated readers who value artistic expression, complex themes, experimental narrative techniques, and books that are recognized for their literary merit.",
            self.NON_FICTION_READERS: "Readers who prefer factual content, real-world information, educational material, and books that provide practical knowledge or explore true events and experiences.",
            
            # Professional & Career Audiences
            self.PROFESSIONALS: "Working individuals seeking content relevant to their careers, professional development, industry insights, and skills enhancement for workplace success.",
            self.BUSINESS_PROFESSIONALS: "Corporate workers, managers, and business owners interested in leadership, strategy, management techniques, and business insights for career advancement.",
            self.HEALTHCARE_WORKERS: "Medical professionals including doctors, nurses, and healthcare staff seeking medical knowledge, patient care insights, and healthcare industry information.",
            self.EDUCATORS: "Teachers, professors, and educational professionals looking for teaching resources, educational theory, classroom management, and academic content.",
            self.LAWYERS: "Legal professionals seeking legal knowledge, case studies, legal theory, professional development, and insights into the legal system and practice.",
            self.ENGINEERS: "Technical professionals interested in engineering principles, technological innovation, problem-solving methodologies, and technical skill development.",
            self.MARKETERS: "Marketing professionals seeking insights into consumer behavior, advertising strategies, brand development, and digital marketing techniques.",
            self.CONSULTANTS: "Advisory professionals looking for industry expertise, client management strategies, analytical frameworks, and professional development resources.",
            self.MANAGERS: "Supervisory professionals seeking leadership skills, team management techniques, organizational behavior insights, and management best practices.",
            self.EXECUTIVES: "Senior leadership professionals interested in strategic thinking, corporate governance, executive decision-making, and high-level business insights.",
            self.ENTREPRENEURS: "Business founders and startup professionals seeking guidance on business creation, innovation, risk management, and entrepreneurial success strategies.",
            
            # Academic & Educational Audiences
            self.ACADEMICS: "University professors, researchers, and scholars engaged in academic pursuits who value rigorous analysis, peer-reviewed insights, and scholarly discourse.",
            self.RESEARCHERS: "Individuals conducting formal research who need access to methodologies, data analysis techniques, research findings, and academic resources.",
            self.SCHOLARS: "Learned individuals pursuing deep knowledge in specific fields who appreciate scholarly work, historical analysis, and intellectual exploration.",
            self.STUDENTS: "Learners at various educational levels seeking knowledge, study resources, educational content, and materials that support their academic goals.",
            self.GRADUATE_STUDENTS: "Advanced students pursuing master's or doctoral degrees who need specialized knowledge, research skills, and academic expertise in their field of study.",
            self.UNDERGRADUATE_STUDENTS: "College students seeking foundational knowledge, study skills, career guidance, and educational content relevant to their major and future goals.",
            self.LIFELONG_LEARNERS: "Individuals committed to continuous education and personal growth who actively seek new knowledge, skills, and understanding throughout their lives.",
            
            # Skill Level Audiences
            self.BEGINNERS: "Newcomers to a subject who need foundational knowledge, step-by-step guidance, basic concepts, and accessible introductions to new topics or skills.",
            self.INTERMEDIATE: "Readers with some background knowledge who seek to build upon existing skills, explore more complex concepts, and advance their understanding.",
            self.ADVANCED: "Experienced individuals who want sophisticated content, complex analysis, nuanced understanding, and advanced techniques in their areas of interest.",
            self.EXPERTS: "Highly knowledgeable professionals who seek cutting-edge insights, expert-level analysis, and advanced concepts at the forefront of their field.",
            self.HOBBYISTS: "Individuals pursuing interests as recreational activities who want practical guidance, inspiration, and enjoyable content related to their hobbies.",
            self.ENTHUSIASTS: "Passionate individuals deeply interested in specific topics who seek comprehensive information, insider knowledge, and detailed exploration of their interests.",
            
            # Creative & Technical Audiences
            self.CREATIVES: "Artists, designers, and creative professionals seeking inspiration, creative techniques, artistic insights, and guidance for creative expression and professional development.",
            self.ARTISTS: "Visual artists, painters, sculptors, and other fine artists looking for artistic techniques, creative inspiration, art history, and professional guidance.",
            self.WRITERS: "Authors, journalists, and writing professionals seeking writing techniques, storytelling methods, publishing insights, and creative inspiration for their craft.",
            self.DESIGNERS: "Graphic designers, web designers, and design professionals interested in design principles, creative processes, and visual communication techniques.",
            self.MUSICIANS: "Musical artists, composers, and music professionals seeking musical knowledge, performance techniques, music theory, and industry insights.",
            self.FILMMAKERS: "Directors, producers, and film professionals interested in filmmaking techniques, storytelling for screen, industry insights, and cinematic arts.",
            self.TECHNICAL_AUDIENCE: "Technology professionals and technically-minded individuals who appreciate detailed technical information, precise specifications, and technical accuracy.",
            self.DEVELOPERS: "Software developers and programmers seeking coding techniques, programming languages, software development methodologies, and technical skills.",
            self.DATA_SCIENTISTS: "Analytics professionals working with data who need statistical methods, data analysis techniques, machine learning insights, and quantitative approaches.",
            
            # Lifestyle & Interest Audiences
            self.PARENTS: "Mothers and fathers seeking parenting advice, child development insights, family management strategies, and guidance for raising children successfully.",
            self.NEW_PARENTS: "First-time parents or those with very young children who need practical guidance, reassurance, and foundational parenting knowledge.",
            self.WORKING_PARENTS: "Parents balancing career and family responsibilities who seek advice on time management, work-life balance, and managing multiple commitments.",
            self.FITNESS_ENTHUSIASTS: "Individuals passionate about physical fitness who seek exercise techniques, nutrition guidance, health optimization, and athletic performance improvement.",
            self.HEALTH_CONSCIOUS: "Readers focused on wellness and healthy living who want information about nutrition, preventive health, mental wellness, and lifestyle optimization.",
            self.SPIRITUAL_SEEKERS: "Individuals exploring spirituality, personal growth, and meaning who seek guidance on spiritual practices, personal development, and life purpose.",
            self.SELF_IMPROVEMENT: "Readers committed to personal development who want practical strategies for self-improvement, goal achievement, and personal transformation.",
            self.TRAVEL_ENTHUSIASTS: "People passionate about travel who seek destination guides, travel tips, cultural insights, and inspiration for exploring the world.",
            self.FOOD_LOVERS: "Culinary enthusiasts who enjoy cooking, dining, and food culture, seeking recipes, cooking techniques, food history, and culinary inspiration.",
            
            # Niche & Specialized Audiences
            self.COLLECTORS: "Individuals who collect items as a hobby or investment who seek specialized knowledge about collectibles, market trends, and collecting strategies.",
            self.GAMERS: "Video game enthusiasts and tabletop gamers who enjoy gaming culture, game design insights, strategy guides, and gaming-related content.",
            self.INVESTORS: "Individuals interested in financial markets who seek investment strategies, market analysis, financial planning, and wealth-building guidance.",
            self.RETIREES: "Retired individuals who have time for reading and may be interested in life reflection, leisure activities, health maintenance, and post-career pursuits.",
            self.MILITARY: "Active military personnel who may be interested in military history, leadership, tactical knowledge, and stories relevant to military experience.",
            self.VETERANS: "Former military personnel who may connect with stories about military experience, transition to civilian life, and veteran-specific issues.",
            self.IMMIGRANTS: "Individuals who have moved to new countries who may seek guidance on cultural adaptation, language learning, and navigating new societies.",
            self.CAREGIVERS: "Individuals caring for family members or working in care professions who need guidance on caregiving, emotional support, and care management.",
            self.ACTIVISTS: "Individuals engaged in social causes who seek information about social change, advocacy strategies, and movements for social justice.",
            
            # Reading Behavior Audiences
            self.COMMUTERS: "Readers who primarily read during travel time and prefer content suitable for interrupted reading, audiobooks, or easily digestible segments.",
            self.BEDTIME_READERS: "Individuals who read before sleep and may prefer calming content, shorter chapters, or material that aids relaxation rather than high excitement.",
            self.AUDIOBOOK_LISTENERS: "Readers who prefer listening to books and appreciate content that works well in audio format with good narration and clear storytelling.",
            self.QUICK_READERS: "Fast readers who consume books rapidly and appreciate engaging plots, efficient storytelling, and content that maintains quick pacing.",
            self.SLOW_READERS: "Deliberate readers who prefer to savor content, appreciate detailed descriptions, complex language, and books that reward careful reading.",
            self.RE_READERS: "Readers who enjoy revisiting favorite books and appreciate content with layers of meaning, details that reward multiple readings, and timeless appeal.",


            self.WOMEN: "Female readers who may be drawn to books with strong female characters, relationship themes, emotional depth, and stories that reflect women's experiences and perspectives.",
            self.MEN: "Male readers who may prefer action-oriented stories, adventure narratives, technical content, or books that explore themes and experiences that resonate with masculine perspectives.",
            self.FAMILIES: "Family units looking for content suitable for shared reading, family activities, educational materials, or books that bring family members together across different age groups.",
            self.TEENS: "Teenage readers aged 13-18 who are navigating adolescence and seek stories about identity, peer relationships, independence, and the challenges of growing up in contemporary society.",
            self.ADVENTURERS: "Readers who seek excitement, exploration, and adventure in their reading, drawn to travel narratives, outdoor activities, extreme sports, and stories of courage and discovery.",
            self.LIFESTYLE_READERS: "Readers interested in lifestyle content including home design, personal style, wellness trends, social media culture, and contemporary living approaches and philosophies.",
            self.ADULTS: "Mature readers aged 25+ who appreciate complex narratives, diverse themes, sophisticated character development, and stories reflecting adult experiences and responsibilities.",
        }
        return descriptions.get(self, f"Target audience: {self.display_name.lower()}")
    
    @property
    def age_range(self) -> Optional[str]:
        """Typical age range for this audience type."""
        age_ranges = {
            self.CHILDREN: "5-12",
            self.MIDDLE_GRADE: "8-12", 
            self.YOUNG_ADULT: "13-18",
            self.NEW_ADULT: "18-25",
            self.ADULT: "25-65",
            self.MATURE_ADULT: "40-75",
            self.SENIORS: "65+",
            self.UNDERGRADUATE_STUDENTS: "18-22",
            self.GRADUATE_STUDENTS: "22-35",
            self.NEW_PARENTS: "25-40",
            self.WORKING_PARENTS: "25-50",
            self.RETIREES: "60+",
        }
        return age_ranges.get(self, None)
    
    @property
    def reading_level(self) -> str:
        """Expected reading comprehension level."""
        levels = {
            # Basic level
            self.CHILDREN: "elementary",
            self.CASUAL_READERS: "basic",
            self.BEDTIME_READERS: "basic",
            
            # Intermediate level
            self.MIDDLE_GRADE: "intermediate",
            self.YOUNG_ADULT: "intermediate", 
            self.GENERAL_READERS: "intermediate",
            self.MAINSTREAM_AUDIENCE: "intermediate",
            self.BEGINNERS: "intermediate",
            self.HOBBYISTS: "intermediate",
            self.COMMUTERS: "intermediate",
            
            # Advanced level
            self.NEW_ADULT: "advanced",
            self.ADULT: "advanced",
            self.PROFESSIONALS: "advanced",
            self.STUDENTS: "advanced",
            self.GENRE_FANS: "advanced",
            self.AVID_READERS: "advanced",
            self.INTERMEDIATE: "advanced",
            self.ENTHUSIASTS: "advanced",
            
            # Expert level
            self.ACADEMICS: "expert",
            self.RESEARCHERS: "expert",
            self.SCHOLARS: "expert",
            self.EXPERTS: "expert",
            self.TECHNICAL_AUDIENCE: "expert",
            self.LITERARY_FICTION_READERS: "expert",
            self.GRADUATE_STUDENTS: "expert",
            self.ADVANCED: "expert",
        }
        return levels.get(self, "intermediate")
    
    @property
    def typical_reading_time(self) -> str:
        """Typical reading session duration for this audience."""
        reading_times = {
            self.CHILDREN: "15-30 minutes",
            self.MIDDLE_GRADE: "30-45 minutes",
            self.CASUAL_READERS: "30-60 minutes",
            self.COMMUTERS: "20-45 minutes",
            self.BEDTIME_READERS: "30-60 minutes",
            self.QUICK_READERS: "60-120 minutes",
            self.AVID_READERS: "90-180 minutes",
            self.ACADEMICS: "60-240 minutes",
            self.STUDENTS: "45-90 minutes",
            self.PROFESSIONALS: "30-60 minutes",
            self.RETIREES: "60-180 minutes",
        }
        return reading_times.get(self, "45-90 minutes")
    
    @property
    def preferred_content_length(self) -> str:
        """Preferred book length for this audience."""
        length_preferences = {
            self.CHILDREN: "short (under 50 pages)",
            self.MIDDLE_GRADE: "short to medium (50-200 pages)",
            self.YOUNG_ADULT: "medium (200-400 pages)",
            self.CASUAL_READERS: "medium (200-350 pages)",
            self.COMMUTERS: "medium (250-400 pages)",
            self.AVID_READERS: "any length",
            self.ACADEMICS: "long (300+ pages)",
            self.PROFESSIONALS: "medium (200-350 pages)",
            self.TECHNICAL_AUDIENCE: "comprehensive (400+ pages)",
            self.QUICK_READERS: "any length",
            self.SLOW_READERS: "medium to long (250-500 pages)",
        }
        return length_preferences.get(self, "medium (200-400 pages)")
    
    @property
    def content_complexity_preference(self) -> str:
        """Preferred complexity level of content."""
        complexity_map = {
            self.CHILDREN: "simple",
            self.MIDDLE_GRADE: "simple", 
            self.CASUAL_READERS: "moderate",
            self.GENERAL_READERS: "moderate",
            self.MAINSTREAM_AUDIENCE: "moderate",
            self.YOUNG_ADULT: "moderate",
            self.BEGINNERS: "simple",
            self.INTERMEDIATE: "moderate",
            self.ADVANCED: "complex",
            self.EXPERTS: "complex",
            self.ACADEMICS: "complex",
            self.LITERARY_FICTION_READERS: "complex",
            self.TECHNICAL_AUDIENCE: "complex",
            self.PROFESSIONALS: "moderate to complex",
        }
        return complexity_map.get(self, "moderate")
    
    @property
    def marketing_channels(self) -> List[str]:
        """Effective marketing channels for reaching this audience."""
        channels = {
            self.CHILDREN: ["parent blogs", "school libraries", "children's bookstores", "family magazines"],
            self.YOUNG_ADULT: ["social media", "BookTok", "YA book blogs", "school libraries", "teen magazines"],
            self.GENRE_FANS: ["genre-specific forums", "convention marketing", "specialized bookstores", "genre magazines"],
            self.PROFESSIONALS: ["LinkedIn", "industry publications", "professional associations", "business magazines"],
            self.ACADEMICS: ["academic journals", "university bookstores", "scholarly conferences", "research networks"],
            self.ENTREPRENEURS: ["business podcasts", "startup communities", "LinkedIn", "business conferences"],
            self.PARENTS: ["parenting blogs", "family magazines", "parent social groups", "school networks"],
            self.FITNESS_ENTHUSIASTS: ["fitness magazines", "gym partnerships", "health blogs", "wellness expos"],
            self.TECHNICAL_AUDIENCE: ["tech blogs", "developer communities", "technical conferences", "professional networks"],
            self.SENIORS: ["library programs", "senior centers", "traditional media", "word-of-mouth"],
        }
        return channels.get(self, ["social media", "online bookstores", "book blogs", "traditional media"])
    
    @classmethod
    def from_string(cls, value: str) -> 'AudienceType':
        """Create AudienceType from string with fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid audience type value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for audience in cls:
            if audience.value == normalized_value:
                return audience
        
        # Fuzzy matching
        fuzzy_matches = {
            # General variations
            "general": cls.GENERAL_READERS,
            "mainstream": cls.MAINSTREAM_AUDIENCE,
            "casual": cls.CASUAL_READERS,
            "avid": cls.AVID_READERS,
            
            # Age variations
            "kids": cls.CHILDREN,
            "child": cls.CHILDREN,
            "mg": cls.MIDDLE_GRADE,
            "ya": cls.YOUNG_ADULT,
            "teen": cls.YOUNG_ADULT,
            "teenager": cls.YOUNG_ADULT,
            "na": cls.NEW_ADULT,
            "adults": cls.ADULT,
            "mature": cls.MATURE_ADULT,
            "seniors": cls.SENIORS,
            "elderly": cls.SENIORS,
            
            # Genre variations
            "fantasy": cls.FANTASY_READERS,
            "sci_fi": cls.SCI_FI_FANS,
            "science_fiction": cls.SCI_FI_FANS,
            "mystery": cls.MYSTERY_LOVERS,
            "romance": cls.ROMANCE_READERS,
            "horror": cls.HORROR_FANS,
            "literary": cls.LITERARY_FICTION_READERS,
            "nonfiction": cls.NON_FICTION_READERS,
            "non_fiction": cls.NON_FICTION_READERS,
            
            # Professional variations
            "business": cls.BUSINESS_PROFESSIONALS,
            "healthcare": cls.HEALTHCARE_WORKERS,
            "medical": cls.HEALTHCARE_WORKERS,
            "teachers": cls.EDUCATORS,
            "education": cls.EDUCATORS,
            "legal": cls.LAWYERS,
            "engineering": cls.ENGINEERS,
            "marketing": cls.MARKETERS,
            "management": cls.MANAGERS,
            "executive": cls.EXECUTIVES,
            "entrepreneur": cls.ENTREPRENEURS,
            
            # Academic variations
            "academic": cls.ACADEMICS,
            "researcher": cls.RESEARCHERS,
            "scholar": cls.SCHOLARS,
            "student": cls.STUDENTS,
            "grad": cls.GRADUATE_STUDENTS,
            "undergrad": cls.UNDERGRADUATE_STUDENTS,
            "learner": cls.LIFELONG_LEARNERS,
            
            # Skill variations
            "beginner": cls.BEGINNERS,
            "novice": cls.BEGINNERS,
            "expert": cls.EXPERTS,
            "hobbyist": cls.HOBBYISTS,
            "hobby": cls.HOBBYISTS,
            
            # Creative variations
            "creative": cls.CREATIVES,
            "artist": cls.ARTISTS,
            "writer": cls.WRITERS,
            "designer": cls.DESIGNERS,
            "musician": cls.MUSICIANS,
            "filmmaker": cls.FILMMAKERS,
            "technical": cls.TECHNICAL_AUDIENCE,
            "developer": cls.DEVELOPERS,
            "programmer": cls.DEVELOPERS,
            "data": cls.DATA_SCIENTISTS,
            
            # Lifestyle variations
            "parent": cls.PARENTS,
            "mom": cls.PARENTS,
            "dad": cls.PARENTS,
            "fitness": cls.FITNESS_ENTHUSIASTS,
            "health": cls.HEALTH_CONSCIOUS,
            "spiritual": cls.SPIRITUAL_SEEKERS,
            "improvement": cls.SELF_IMPROVEMENT,
            "travel": cls.TRAVEL_ENTHUSIASTS,
            "food": cls.FOOD_LOVERS,
            "cooking": cls.FOOD_LOVERS,
            
            # Specialized variations
            "gamer": cls.GAMERS,
            "investor": cls.INVESTORS,
            "retired": cls.RETIREES,
            "veteran": cls.VETERANS,
            "caregiver": cls.CAREGIVERS,
            
            # Reading behavior variations
            "commuter": cls.COMMUTERS,
            "audiobook": cls.AUDIOBOOK_LISTENERS,
            "audio": cls.AUDIOBOOK_LISTENERS,
            "quick": cls.QUICK_READERS,
            "fast": cls.QUICK_READERS,
            "slow": cls.SLOW_READERS,

            # ---
            "women": cls.WOMEN,
            "female": cls.WOMEN,
            "men": cls.MEN,
            "male": cls.MEN,
            "families": cls.FAMILIES,
            "family": cls.FAMILIES,
            "teens": cls.TEENS,
            "teenage": cls.TEENS,
            "adventure": cls.ADVENTURERS,
            "adventurer": cls.ADVENTURERS,
            "lifestyle": cls.LIFESTYLE_READERS,
        }
        
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, audience in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return audience
        
        # Check if the normalized value contains any audience as a substring
        for audience in cls:
            if audience.value in normalized_value or normalized_value in audience.value:
                return audience
        
        available_audiences = [a.value for a in cls]
        raise ValueError(
            f"Unknown audience type: '{value}'. "
            f"Available types include: {', '.join(sorted(available_audiences[:10]))}..."
        )
    
    @classmethod
    def get_audiences_for_genre(cls, genre: str) -> List['AudienceType']:
        """Get recommended audience types for a specific genre."""
        genre_lower = genre.lower()
        
        genre_mappings = {
            "fantasy": [
                cls.FANTASY_READERS, cls.GENRE_FANS, cls.YOUNG_ADULT, 
                cls.AVID_READERS, cls.GENERAL_READERS
            ],
            "science_fiction": [
                cls.SCI_FI_FANS, cls.GENRE_FANS, cls.TECHNICAL_AUDIENCE,
                cls.ADULTS, cls.AVID_READERS
            ],
            "romance": [
                cls.ROMANCE_READERS, cls.GENRE_FANS, cls.WOMEN,
                cls.NEW_ADULT, cls.ADULT
            ],
            "mystery": [
                cls.MYSTERY_LOVERS, cls.GENRE_FANS, cls.MATURE_ADULT,
                cls.AVID_READERS, cls.GENERAL_READERS
            ],
            "horror": [
                cls.HORROR_FANS, cls.GENRE_FANS, cls.YOUNG_ADULT,
                cls.ADULT, cls.AVID_READERS
            ],
            "young_adult": [
                cls.YOUNG_ADULT, cls.NEW_ADULT, cls.MIDDLE_GRADE,
                cls.TEENS, cls.GENERAL_READERS
            ],
            "children": [
                cls.CHILDREN, cls.MIDDLE_GRADE, cls.PARENTS,
                cls.EDUCATORS, cls.FAMILIES
            ],
            "business": [
                cls.BUSINESS_PROFESSIONALS, cls.ENTREPRENEURS, cls.MANAGERS,
                cls.EXECUTIVES, cls.PROFESSIONALS
            ],
            "self_help": [
                cls.SELF_IMPROVEMENT, cls.GENERAL_READERS, cls.PROFESSIONALS,
                cls.LIFELONG_LEARNERS, cls.ADULTS
            ],
            "biography": [
                cls.GENERAL_READERS, cls.AVID_READERS, cls.MATURE_ADULT,
                cls.NON_FICTION_READERS, cls.ACADEMICS
            ],
            "history": [
                cls.ACADEMICS, cls.SCHOLARS, cls.NON_FICTION_READERS,
                cls.MATURE_ADULT, cls.AVID_READERS
            ],
            "health": [
                cls.HEALTH_CONSCIOUS, cls.FITNESS_ENTHUSIASTS, cls.HEALTHCARE_WORKERS,
                cls.GENERAL_READERS, cls.PROFESSIONALS
            ],
            "cooking": [
                cls.FOOD_LOVERS, cls.HOBBYISTS, cls.GENERAL_READERS,
                cls.FAMILIES, cls.PROFESSIONALS
            ],
            "travel": [
                cls.TRAVEL_ENTHUSIASTS, cls.GENERAL_READERS, cls.ADVENTURERS,
                cls.LIFESTYLE_READERS, cls.AVID_READERS
            ],
            "technical": [
                cls.TECHNICAL_AUDIENCE, cls.DEVELOPERS, cls.ENGINEERS,
                cls.PROFESSIONALS, cls.EXPERTS
            ],
            "literary_fiction": [
                cls.LITERARY_FICTION_READERS, cls.ACADEMICS, cls.AVID_READERS,
                cls.MATURE_ADULT, cls.SCHOLARS
            ]
        }
        
        # Find matching audiences
        recommended = set()
        for genre_key, audiences in genre_mappings.items():
            if genre_key in genre_lower:
                recommended.update(audiences)
        
        # If no specific mapping found, return general audiences
        if not recommended:
            recommended = {cls.GENERAL_READERS, cls.MAINSTREAM_AUDIENCE, cls.ADULT}
        
        return sorted(list(recommended), key=lambda x: x.display_name)
    
    @classmethod
    def get_audiences_by_age(cls, age_group: str) -> List['AudienceType']:
        """Get audience types for a specific age group."""
        age_group_lower = age_group.lower()
        
        age_mappings = {
            "children": [cls.CHILDREN, cls.MIDDLE_GRADE],
            "teens": [cls.YOUNG_ADULT, cls.MIDDLE_GRADE],
            "young_adults": [cls.NEW_ADULT, cls.YOUNG_ADULT],
            "adults": [cls.ADULT, cls.PROFESSIONALS, cls.PARENTS],
            "seniors": [cls.SENIORS, cls.MATURE_ADULT, cls.RETIREES],
        }
        
        return age_mappings.get(age_group_lower, [cls.GENERAL_READERS])
    
    @classmethod
    def get_professional_audiences(cls) -> List['AudienceType']:
        """Get all professional/career-focused audience types."""
        return [
            cls.PROFESSIONALS, cls.BUSINESS_PROFESSIONALS, cls.HEALTHCARE_WORKERS,
            cls.EDUCATORS, cls.LAWYERS, cls.ENGINEERS, cls.MARKETERS,
            cls.CONSULTANTS, cls.MANAGERS, cls.EXECUTIVES, cls.ENTREPRENEURS
        ]
    
    @classmethod
    def get_creative_audiences(cls) -> List['AudienceType']:
        """Get all creative-focused audience types."""
        return [
            cls.CREATIVES, cls.ARTISTS, cls.WRITERS, cls.DESIGNERS,
            cls.MUSICIANS, cls.FILMMAKERS
        ]
    
    @classmethod
    def get_academic_audiences(cls) -> List['AudienceType']:
        """Get all academic/educational audience types."""
        return [
            cls.ACADEMICS, cls.RESEARCHERS, cls.SCHOLARS, cls.STUDENTS,
            cls.GRADUATE_STUDENTS, cls.UNDERGRADUATE_STUDENTS, cls.LIFELONG_LEARNERS
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage and testing
if __name__ == "__main__":
    print("=== MuseQuill Audience Type System Demo ===\n")
    
    # Test AudienceType enum
    print("1. Audience Type Examples:")
    test_audiences = [
        AudienceType.YOUNG_ADULT, AudienceType.BUSINESS_PROFESSIONALS, 
        AudienceType.FANTASY_READERS, AudienceType.ACADEMICS
    ]
    
    for audience in test_audiences:
        print(f"  • {audience.display_name}")
        print(f"    Age Range: {audience.age_range or 'Not specified'}")
        print(f"    Reading Level: {audience.reading_level}")
        print(f"    Content Complexity: {audience.content_complexity_preference}")
        print(f"    Preferred Length: {audience.preferred_content_length}")
        print(f"    Description: {audience.description[:100]}...")
        print()
    
    # Test string conversion
    print("2. String Conversion Examples:")
    test_strings = ["ya", "business", "fantasy readers", "academics", "parents"]
    for test_str in test_strings:
        try:
            audience = AudienceType.from_string(test_str)
            print(f"  '{test_str}' -> {audience.display_name}")
        except ValueError as e:
            print(f"  '{test_str}' -> ERROR: {e}")
    
    # Test genre recommendations
    print("\n3. Genre-based Audience Recommendations:")
    test_genres = ["fantasy", "business", "young_adult", "technical"]
    for genre in test_genres:
        audiences = AudienceType.get_audiences_for_genre(genre)
        print(f"  {genre.title()}: {', '.join([a.display_name for a in audiences[:4]])}...")
    
    # Test category groupings
    print("\n4. Audience Categories:")
    
    print("  Professional Audiences:")
    for audience in AudienceType.get_professional_audiences()[:5]:
        print(f"    - {audience.display_name}")
    
    print("  Creative Audiences:")
    for audience in AudienceType.get_creative_audiences():
        print(f"    - {audience.display_name}")
    
    print("  Academic Audiences:")
    for audience in AudienceType.get_academic_audiences()[:5]:
        print(f"    - {audience.display_name}")
    
    print("\n=== Demo Complete ===")