from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
import json
from datetime import datetime


class ResearchType(str, Enum):
    """Types of research needed for book generation."""
    
    # Core research types
    HISTORICAL = "historical"
    SCIENTIFIC = "scientific"
    TECHNICAL = "technical"
    CULTURAL = "cultural"
    GEOGRAPHICAL = "geographical"
    LINGUISTIC = "linguistic"
    
    # Professional domains
    PROFESSIONAL = "professional"
    LEGAL = "legal"
    MEDICAL = "medical"
    PSYCHOLOGICAL = "psychological"
    SOCIOLOGICAL = "sociological"
    ECONOMIC = "economic"
    POLITICAL = "political"
    MILITARY = "military"
    
    # Cultural & creative
    RELIGIOUS = "religious"
    ARTISTIC = "artistic"
    ARCHITECTURAL = "architectural"
    CULINARY = "culinary"
    FASHION = "fashion"
    SPORTS = "sports"
    
    # Extended research types for comprehensive coverage
    BIOGRAPHICAL = "biographical"
    MYTHOLOGICAL = "mythological"
    FOLKLORE = "folklore"
    TECHNOLOGICAL = "technological"
    ENVIRONMENTAL = "environmental"
    EDUCATIONAL = "educational"
    PHILOSOPHICAL = "philosophical"
    SUPERNATURAL = "supernatural"
    CRIME_INVESTIGATION = "crime_investigation"
    BUSINESS = "business"
    TRAVEL = "travel"
    MUSIC = "music"
    LITERATURE = "literature"
    ENTERTAINMENT = "entertainment"
    MEDIA = "media"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            self.HISTORICAL: "Historical Research",
            self.SCIENTIFIC: "Scientific Research", 
            self.TECHNICAL: "Technical Research",
            self.CULTURAL: "Cultural Research",
            self.GEOGRAPHICAL: "Geographical Research",
            self.LINGUISTIC: "Linguistic Research",
            self.PROFESSIONAL: "Professional Research",
            self.LEGAL: "Legal Research",
            self.MEDICAL: "Medical Research",
            self.PSYCHOLOGICAL: "Psychological Research",
            self.SOCIOLOGICAL: "Sociological Research",
            self.ECONOMIC: "Economic Research",
            self.POLITICAL: "Political Research",
            self.MILITARY: "Military Research",
            self.RELIGIOUS: "Religious Research",
            self.ARTISTIC: "Artistic Research",
            self.ARCHITECTURAL: "Architectural Research",
            self.CULINARY: "Culinary Research",
            self.FASHION: "Fashion Research",
            self.SPORTS: "Sports Research",
            self.BIOGRAPHICAL: "Biographical Research",
            self.MYTHOLOGICAL: "Mythological Research",
            self.FOLKLORE: "Folklore Research",
            self.TECHNOLOGICAL: "Technological Research",
            self.ENVIRONMENTAL: "Environmental Research",
            self.EDUCATIONAL: "Educational Research",
            self.PHILOSOPHICAL: "Philosophical Research",
            self.SUPERNATURAL: "Supernatural Research",
            self.CRIME_INVESTIGATION: "Crime Investigation Research",
            self.BUSINESS: "Business Research",
            self.TRAVEL: "Travel Research",
            self.MUSIC: "Music Research",
            self.LITERATURE: "Literature Research",
            self.ENTERTAINMENT: "Entertainment Research",
            self.MEDIA: "Media Research",
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Detailed description of the research type."""
        descriptions = {
            self.HISTORICAL: "Research into historical events, periods, figures, and contexts",
            self.SCIENTIFIC: "Research into scientific principles, theories, discoveries, and methodologies",
            self.TECHNICAL: "Research into technical processes, procedures, and specialized knowledge",
            self.CULTURAL: "Research into cultural practices, traditions, customs, and social norms",
            self.GEOGRAPHICAL: "Research into locations, places, geographical features, and settings",
            self.LINGUISTIC: "Research into languages, dialects, communication, and translation",
            self.PROFESSIONAL: "Research into specific professions, careers, and workplace dynamics",
            self.LEGAL: "Research into legal systems, laws, procedures, and judicial processes",
            self.MEDICAL: "Research into medical conditions, treatments, procedures, and healthcare",
            self.PSYCHOLOGICAL: "Research into mental processes, behavior, and psychological conditions",
            self.SOCIOLOGICAL: "Research into social structures, relationships, and group dynamics",
            self.ECONOMIC: "Research into economic systems, markets, financial concepts, and business",
            self.POLITICAL: "Research into political systems, governance, and policy matters",
            self.MILITARY: "Research into military operations, history, equipment, and strategy",
            self.RELIGIOUS: "Research into religious beliefs, practices, institutions, and history",
            self.ARTISTIC: "Research into art forms, artistic movements, and creative processes",
            self.ARCHITECTURAL: "Research into building design, construction, and architectural styles",
            self.CULINARY: "Research into food, cooking, cuisine, and culinary traditions",
            self.FASHION: "Research into clothing, style, fashion trends, and textile history",
            self.SPORTS: "Research into sports, athletics, games, and recreational activities",
            self.BIOGRAPHICAL: "Research into specific individuals, their lives, and achievements",
            self.MYTHOLOGICAL: "Research into myths, legends, and mythological systems",
            self.FOLKLORE: "Research into folk tales, traditional stories, and cultural narratives",
            self.TECHNOLOGICAL: "Research into technology, innovations, and technological systems",
            self.ENVIRONMENTAL: "Research into environmental issues, ecology, and natural systems",
            self.EDUCATIONAL: "Research into education systems, learning, and academic institutions",
            self.PHILOSOPHICAL: "Research into philosophical concepts, ethics, and abstract thinking",
            self.SUPERNATURAL: "Research into supernatural concepts, paranormal phenomena, and magic",
            self.CRIME_INVESTIGATION: "Research into criminal procedures, forensics, and law enforcement",
            self.BUSINESS: "Research into business practices, industries, and commercial operations",
            self.TRAVEL: "Research into travel, tourism, transportation, and destinations",
            self.MUSIC: "Research into musical styles, instruments, composition, and music history",
            self.LITERATURE: "Research into literary works, authors, and literary movements",
            self.ENTERTAINMENT: "Research into entertainment industry, media, and popular culture",
            self.MEDIA: "Research into media systems, journalism, and information dissemination",
        }
        return descriptions.get(self, "")
    
    @property
    def complexity_level(self) -> str:
        """Complexity level for research and AI integration."""
        easy = {
            self.TRAVEL, self.CULINARY, self.SPORTS, self.ENTERTAINMENT,
            self.FASHION, self.MUSIC, self.ARTISTIC
        }
        medium = {
            self.CULTURAL, self.GEOGRAPHICAL, self.HISTORICAL, self.BIOGRAPHICAL,
            self.FOLKLORE, self.BUSINESS, self.EDUCATIONAL, self.LITERATURE
        }
        hard = {
            self.SCIENTIFIC, self.TECHNICAL, self.PROFESSIONAL, self.PSYCHOLOGICAL,
            self.SOCIOLOGICAL, self.ECONOMIC, self.POLITICAL, self.RELIGIOUS,
            self.PHILOSOPHICAL, self.ENVIRONMENTAL, self.MEDIA
        }
        very_hard = {
            self.LEGAL, self.MEDICAL, self.MILITARY, self.TECHNOLOGICAL,
            self.CRIME_INVESTIGATION, self.SUPERNATURAL, self.MYTHOLOGICAL,
            self.LINGUISTIC, self.ARCHITECTURAL
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
    def typical_sources(self) -> List[str]:
        """Typical sources for this type of research."""
        source_map = {
            self.HISTORICAL: ["academic papers", "historical documents", "museums", "archives", "textbooks"],
            self.SCIENTIFIC: ["peer-reviewed journals", "research papers", "scientific databases", "expert interviews"],
            self.TECHNICAL: ["technical manuals", "industry publications", "expert forums", "documentation"],
            self.CULTURAL: ["ethnographic studies", "cultural institutions", "travel guides", "local sources"],
            self.GEOGRAPHICAL: ["maps", "travel guides", "geographical surveys", "satellite imagery", "local guides"],
            self.LINGUISTIC: ["dictionaries", "language resources", "linguistic databases", "native speakers"],
            self.PROFESSIONAL: ["industry publications", "professional associations", "career guides", "interviews"],
            self.LEGAL: ["legal databases", "court records", "law journals", "legal experts", "statutes"],
            self.MEDICAL: ["medical journals", "clinical studies", "medical textbooks", "healthcare professionals"],
            self.PSYCHOLOGICAL: ["psychology journals", "case studies", "research papers", "clinical data"],
            self.SOCIOLOGICAL: ["sociological studies", "demographic data", "social research", "surveys"],
            self.ECONOMIC: ["economic reports", "financial data", "market research", "economic journals"],
            self.POLITICAL: ["government sources", "political science journals", "policy documents", "news"],
            self.MILITARY: ["military history", "defense publications", "strategic studies", "veteran accounts"],
            self.RELIGIOUS: ["religious texts", "theological studies", "religious institutions", "scholars"],
            self.ARTISTIC: ["art history books", "museums", "artist biographies", "art criticism", "galleries"],
            self.ARCHITECTURAL: ["architectural history", "building records", "architectural journals", "blueprints"],
            self.CULINARY: ["cookbooks", "culinary history", "food blogs", "chef interviews", "recipes"],
            self.FASHION: ["fashion magazines", "fashion history", "designer interviews", "style guides"],
            self.SPORTS: ["sports statistics", "athlete biographies", "sports journalism", "rule books"],
        }
        return source_map.get(self, ["general sources", "online databases", "expert interviews"])
    
    @property
    def ai_research_difficulty(self) -> str:
        """How difficult this research type is for AI to conduct."""
        easy = {
            self.TRAVEL, self.CULINARY, self.SPORTS, self.ENTERTAINMENT,
            self.FASHION, self.MUSIC, self.GEOGRAPHICAL, self.ARTISTIC
        }
        medium = {
            self.CULTURAL, self.HISTORICAL, self.BIOGRAPHICAL, self.FOLKLORE,
            self.BUSINESS, self.EDUCATIONAL, self.LITERATURE, self.MEDIA
        }
        hard = {
            self.SCIENTIFIC, self.TECHNICAL, self.PROFESSIONAL, self.PSYCHOLOGICAL,
            self.SOCIOLOGICAL, self.ECONOMIC, self.POLITICAL, self.RELIGIOUS,
            self.PHILOSOPHICAL, self.ENVIRONMENTAL
        }
        very_hard = {
            self.LEGAL, self.MEDICAL, self.MILITARY, self.TECHNOLOGICAL,
            self.CRIME_INVESTIGATION, self.SUPERNATURAL, self.MYTHOLOGICAL,
            self.LINGUISTIC, self.ARCHITECTURAL
        }
        
        if self in easy:
            return "easy"
        elif self in medium:
            return "medium"
        elif self in hard:
            return "hard"
        else:
            return "very_hard"
    
    @classmethod
    def from_string(cls, value: str) -> 'ResearchType':
        """Create ResearchType from string with fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid research type value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for research_type in cls:
            if research_type.value == normalized_value:
                return research_type
        
        # Fuzzy matching
        fuzzy_matches = {
            "history": cls.HISTORICAL,
            "science": cls.SCIENTIFIC,
            "tech": cls.TECHNICAL,
            "culture": cls.CULTURAL,
            "geography": cls.GEOGRAPHICAL,
            "language": cls.LINGUISTIC,
            "profession": cls.PROFESSIONAL,
            "law": cls.LEGAL,
            "medicine": cls.MEDICAL,
            "psychology": cls.PSYCHOLOGICAL,
            "sociology": cls.SOCIOLOGICAL,
            "economics": cls.ECONOMIC,
            "politics": cls.POLITICAL,
            "military": cls.MILITARY,
            "religion": cls.RELIGIOUS,
            "art": cls.ARTISTIC,
            "architecture": cls.ARCHITECTURAL,
            "cooking": cls.CULINARY,
            "food": cls.CULINARY,
            "style": cls.FASHION,
            "athletics": cls.SPORTS,
            "biography": cls.BIOGRAPHICAL,
            "myth": cls.MYTHOLOGICAL,
            "legend": cls.FOLKLORE,
            "technology": cls.TECHNOLOGICAL,
            "environment": cls.ENVIRONMENTAL,
            "education": cls.EDUCATIONAL,
            "philosophy": cls.PHILOSOPHICAL,
            "paranormal": cls.SUPERNATURAL,
            "magic": cls.SUPERNATURAL,
            "detective": cls.CRIME_INVESTIGATION,
            "forensics": cls.CRIME_INVESTIGATION,
            "business": cls.BUSINESS,
            "journey": cls.TRAVEL,
            "music": cls.MUSIC,
            "books": cls.LITERATURE,
            "entertainment": cls.ENTERTAINMENT,
            "journalism": cls.MEDIA,
        }
        
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, research_type in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return research_type
        
        # Check if the normalized value contains any research type as a substring
        for research_type in cls:
            if research_type.value in normalized_value or normalized_value in research_type.value:
                return research_type
        
        available_types = [rt.value for rt in cls]
        raise ValueError(
            f"Unknown research type: '{value}'. "
            f"Available types include: {', '.join(sorted(available_types[:10]))}..."
        )
    
    @classmethod
    def get_types_for_genre(cls, genre: str) -> List['ResearchType']:
        """Get recommended research types for a specific genre."""
        genre_lower = genre.lower()
        
        # Genre-specific research type mappings
        genre_mappings = {
            "fantasy": [cls.MYTHOLOGICAL, cls.FOLKLORE, cls.HISTORICAL, cls.LINGUISTIC, 
                       cls.CULTURAL, cls.MILITARY, cls.SUPERNATURAL, cls.GEOGRAPHICAL],
            "science_fiction": [cls.SCIENTIFIC, cls.TECHNOLOGICAL, cls.ENVIRONMENTAL, 
                               cls.PHILOSOPHICAL, cls.POLITICAL, cls.MILITARY],
            "historical_fiction": [cls.HISTORICAL, cls.CULTURAL, cls.GEOGRAPHICAL, 
                                  cls.POLITICAL, cls.MILITARY, cls.LINGUISTIC],
            "mystery": [cls.CRIME_INVESTIGATION, cls.LEGAL, cls.PROFESSIONAL, 
                       cls.PSYCHOLOGICAL, cls.TECHNICAL],
            "thriller": [cls.CRIME_INVESTIGATION, cls.LEGAL, cls.MILITARY, cls.POLITICAL, 
                        cls.TECHNICAL, cls.PROFESSIONAL],
            "romance": [cls.CULTURAL, cls.PSYCHOLOGICAL, cls.PROFESSIONAL, cls.TRAVEL, 
                       cls.FASHION, cls.CULINARY],
            "horror": [cls.SUPERNATURAL, cls.PSYCHOLOGICAL, cls.MEDICAL, cls.HISTORICAL, 
                      cls.FOLKLORE, cls.RELIGIOUS],
            "young_adult": [cls.EDUCATIONAL, cls.PSYCHOLOGICAL, cls.CULTURAL, cls.SPORTS, 
                           cls.ENTERTAINMENT, cls.TRAVEL],
            "literary_fiction": [cls.PSYCHOLOGICAL, cls.SOCIOLOGICAL, cls.PHILOSOPHICAL, 
                                cls.CULTURAL, cls.POLITICAL],
            "non_fiction": [cls.HISTORICAL, cls.SCIENTIFIC, cls.BIOGRAPHICAL, cls.PROFESSIONAL, 
                           cls.EDUCATIONAL, cls.BUSINESS],
            "memoir": [cls.BIOGRAPHICAL, cls.HISTORICAL, cls.CULTURAL, cls.PROFESSIONAL],
            "biography": [cls.BIOGRAPHICAL, cls.HISTORICAL, cls.PROFESSIONAL, cls.CULTURAL],
            "business": [cls.BUSINESS, cls.ECONOMIC, cls.PROFESSIONAL, cls.TECHNICAL],
            "self_help": [cls.PSYCHOLOGICAL, cls.PROFESSIONAL, cls.EDUCATIONAL, cls.BUSINESS],
            "travel": [cls.TRAVEL, cls.GEOGRAPHICAL, cls.CULTURAL, cls.HISTORICAL, cls.CULINARY],
            "cookbook": [cls.CULINARY, cls.CULTURAL, cls.HISTORICAL],
        }
        
        # Find matching research types
        recommended = set()
        for genre_key, research_types in genre_mappings.items():
            if genre_key in genre_lower:
                recommended.update(research_types)
        
        # If no specific mapping found, return general types
        if not recommended:
            recommended = {cls.CULTURAL, cls.HISTORICAL, cls.GEOGRAPHICAL, cls.PROFESSIONAL}
        
        return sorted(list(recommended), key=lambda x: x.display_name)
    
    @classmethod
    def get_ai_friendly_types(cls) -> List['ResearchType']:
        """Get research types that are easier for AI to conduct."""
        return [rt for rt in cls if rt.ai_research_difficulty in ["easy", "medium"]]
    
    @classmethod
    def get_types_by_complexity(cls, complexity: str) -> List['ResearchType']:
        """Get research types by complexity level."""
        return [rt for rt in cls if rt.complexity_level == complexity.lower()]
    
    def __str__(self) -> str:
        return self.display_name


@dataclass
class ResearchRequirement:
    """A specific research requirement for book generation."""
    research_type: ResearchType
    topic: str
    description: str = ""
    priority: str = "medium"  # low, medium, high, critical
    estimated_time: int = 30  # minutes
    sources_needed: List[str] = field(default_factory=list)
    specific_questions: List[str] = field(default_factory=list)
    context: str = ""
    
    def __post_init__(self):
        """Initialize default sources if none provided."""
        if not self.sources_needed:
            self.sources_needed = self.research_type.typical_sources
    
    @property
    def complexity_score(self) -> int:
        """Calculate complexity score (1-10) based on various factors."""
        base_score = {
            "easy": 2,
            "medium": 4,
            "hard": 7,
            "very_hard": 9
        }.get(self.research_type.complexity_level, 5)
        
        # Adjust based on priority
        priority_modifier = {
            "low": -1,
            "medium": 0,
            "high": 1,
            "critical": 2
        }.get(self.priority, 0)
        
        # Adjust based on number of specific questions
        question_modifier = min(len(self.specific_questions) // 3, 2)
        
        return max(1, min(10, base_score + priority_modifier + question_modifier))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "research_type": self.research_type.value,
            "topic": self.topic,
            "description": self.description,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "sources_needed": self.sources_needed,
            "specific_questions": self.specific_questions,
            "context": self.context,
            "complexity_score": self.complexity_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ResearchRequirement':
        """Create from dictionary."""
        research_type = ResearchType(data["research_type"])
        return cls(
            research_type=research_type,
            topic=data["topic"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            estimated_time=data.get("estimated_time", 30),
            sources_needed=data.get("sources_needed", []),
            specific_questions=data.get("specific_questions", []),
            context=data.get("context", "")
        )


@dataclass
class ResearchPlan:
    """A comprehensive research plan for a book project."""
    book_title: str
    genre: str
    target_audience: str
    requirements: List[ResearchRequirement] = field(default_factory=list)
    total_estimated_time: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_requirement(self, requirement: ResearchRequirement) -> None:
        """Add a research requirement to the plan."""
        self.requirements.append(requirement)
        self._update_total_time()
    
    def remove_requirement(self, index: int) -> None:
        """Remove a research requirement by index."""
        if 0 <= index < len(self.requirements):
            self.requirements.pop(index)
            self._update_total_time()
    
    def _update_total_time(self) -> None:
        """Update total estimated time."""
        self.total_estimated_time = sum(req.estimated_time for req in self.requirements)
    
    @property
    def research_types_summary(self) -> Dict[ResearchType, int]:
        """Get summary of research types and their counts."""
        summary = {}
        for req in self.requirements:
            summary[req.research_type] = summary.get(req.research_type, 0) + 1
        return summary
    
    @property
    def priority_breakdown(self) -> Dict[str, int]:
        """Get breakdown by priority levels."""
        breakdown = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for req in self.requirements:
            breakdown[req.priority] += 1
        return breakdown
    
    @property
    def complexity_breakdown(self) -> Dict[str, int]:
        """Get breakdown by complexity levels."""
        breakdown = {"easy": 0, "medium": 0, "hard": 0, "very_hard": 0}
        for req in self.requirements:
            breakdown[req.research_type.complexity_level] += 1
        return breakdown
    
    def get_requirements_by_priority(self, priority: str) -> List[ResearchRequirement]:
        """Get requirements filtered by priority."""
        return [req for req in self.requirements if req.priority == priority]
    
    def get_requirements_by_type(self, research_type: ResearchType) -> List[ResearchRequirement]:
        """Get requirements filtered by research type."""
        return [req for req in self.requirements if req.research_type == research_type]
    
    def sort_by_priority(self) -> None:
        """Sort requirements by priority (critical first)."""
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        self.requirements.sort(key=lambda x: priority_order.get(x.priority, 2))
    
    def sort_by_complexity(self, ascending: bool = True) -> None:
        """Sort requirements by complexity."""
        self.requirements.sort(
            key=lambda x: x.complexity_score, 
            reverse=not ascending
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "book_title": self.book_title,
            "genre": self.genre,
            "target_audience": self.target_audience,
            "requirements": [req.to_dict() for req in self.requirements],
            "total_estimated_time": self.total_estimated_time,
            "created_at": self.created_at.isoformat(),
            "research_types_summary": {rt.value: count for rt, count in self.research_types_summary.items()},
            "priority_breakdown": self.priority_breakdown,
            "complexity_breakdown": self.complexity_breakdown
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ResearchPlan':
        """Create from dictionary."""
        plan = cls(
            book_title=data["book_title"],
            genre=data["genre"],
            target_audience=data["target_audience"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
        
        for req_data in data["requirements"]:
            requirement = ResearchRequirement.from_dict(req_data)
            plan.add_requirement(requirement)
        
        return plan
    
    def export_to_json(self) -> str:
        """Export plan to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    @classmethod
    def import_from_json(cls, json_str: str) -> 'ResearchPlan':
        """Import plan from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


class ResearchPlanGenerator:
    """Generates research plans based on book parameters."""
    
    @classmethod
    def generate_plan(cls,
                     book_title: str,
                     genre: str,
                     target_audience: str = "adult",
                     complexity_preference: str = "medium",
                     num_research_topics: int = 5,
                     include_ai_friendly_only: bool = False) -> ResearchPlan:
        """
        Generate a research plan for a book.
        
        Args:
            book_title: Title of the book
            genre: Genre of the book
            target_audience: Target audience
            complexity_preference: Preferred complexity level
            num_research_topics: Number of research topics to include
            include_ai_friendly_only: Whether to include only AI-friendly research types
            
        Returns:
            ResearchPlan with generated requirements
        """
        plan = ResearchPlan(
            book_title=book_title,
            genre=genre,
            target_audience=target_audience
        )
        
        # Get recommended research types for the genre
        genre_types = ResearchType.get_types_for_genre(genre)
        
        # Filter for AI-friendly if requested
        if include_ai_friendly_only:
            ai_friendly = set(ResearchType.get_ai_friendly_types())
            genre_types = [rt for rt in genre_types if rt in ai_friendly]
        
        # Filter by complexity preference if specified
        if complexity_preference != "any":
            complexity_types = set(ResearchType.get_types_by_complexity(complexity_preference))
            genre_types = [rt for rt in genre_types if rt in complexity_types]
        
        # Ensure we have enough types
        if len(genre_types) < num_research_topics:
            # Add general types if we don't have enough genre-specific ones
            all_types = list(ResearchType)
            if include_ai_friendly_only:
                all_types = ResearchType.get_ai_friendly_types()
            
            # Add types not already in genre_types
            additional_types = [rt for rt in all_types if rt not in genre_types]
            genre_types.extend(additional_types[:num_research_topics - len(genre_types)])
        
        # Generate requirements for the selected types
        selected_types = genre_types[:num_research_topics]
        
        for research_type in selected_types:
            requirement = cls._generate_requirement_for_type(
                research_type, genre, book_title, target_audience
            )
            plan.add_requirement(requirement)
        
        return plan
    
    @classmethod
    def _generate_requirement_for_type(cls,
                                     research_type: ResearchType,
                                     genre: str,
                                     book_title: str,
                                     target_audience: str) -> ResearchRequirement:
        """Generate a specific requirement for a research type."""
        # Generate topic based on research type and genre
        topic = cls._generate_topic(research_type, genre, book_title)
        
        # Generate description
        description = cls._generate_description(research_type, genre, topic)
        
        # Determine priority based on research type and genre
        priority = cls._determine_priority(research_type, genre)
        
        # Estimate time based on complexity
        estimated_time = cls._estimate_time(research_type, priority)
        
        # Generate specific questions
        questions = cls._generate_questions(research_type, genre, topic)
        
        return ResearchRequirement(
            research_type=research_type,
            topic=topic,
            description=description,
            priority=priority,
            estimated_time=estimated_time,
            specific_questions=questions,
            context=f"Research needed for {genre} book: '{book_title}' targeting {target_audience} audience"
        )
    
    @classmethod
    def _generate_topic(cls, research_type: ResearchType, genre: str, book_title: str) -> str:
        """Generate a specific topic for the research type."""
        genre_lower = genre.lower()
        
        # Topic templates based on research type and genre
        topic_templates = {
            ResearchType.HISTORICAL: {
                "fantasy": "Medieval period customs and daily life",
                "historical_fiction": "Specific historical period and events",
                "default": "Historical context and background"
            },
            ResearchType.CULTURAL: {
                "fantasy": "Cultural traditions and social structures",
                "romance": "Dating customs and relationship traditions",
                "default": "Cultural background and social norms"
            },
            ResearchType.GEOGRAPHICAL: {
                "fantasy": "Geography and world-building locations",
                "travel": "Specific travel destinations and features",
                "default": "Setting locations and geographical features"
            },
            ResearchType.PROFESSIONAL: {
                "mystery": "Police procedures and detective work",
                "medical": "Medical profession and healthcare",
                "default": "Professional practices and workplace culture"
            },
            ResearchType.CRIME_INVESTIGATION: {
                "mystery": "Criminal investigation procedures",
                "thriller": "Forensic science and police methods",
                "default": "Crime investigation and legal procedures"
            },
            ResearchType.SUPERNATURAL: {
                "fantasy": "Magic systems and supernatural elements",
                "horror": "Supernatural phenomena and folklore",
                "default": "Supernatural concepts and paranormal elements"
            }
        }
        
        template_dict = topic_templates.get(research_type, {"default": f"{research_type.display_name} research"})
        
        # Find matching genre template or use default
        topic = None
        for genre_key, topic_template in template_dict.items():
            if genre_key == "default":
                continue
            if genre_key in genre_lower:
                topic = topic_template
                break
        
        if not topic:
            topic = template_dict.get("default", f"{research_type.display_name} for the story")
        
        return topic
    
    @classmethod
    def _generate_description(cls, research_type: ResearchType, genre: str, topic: str) -> str:
        """Generate a description for the research requirement."""
        return f"Research {topic} to ensure accuracy and authenticity in the {genre} narrative. {research_type.description}"
    
    @classmethod
    def _determine_priority(cls, research_type: ResearchType, genre: str) -> str:
        """Determine priority based on research type and genre relevance."""
        genre_lower = genre.lower()
        
        # High priority mappings
        high_priority_mappings = {
            "fantasy": [ResearchType.MYTHOLOGICAL, ResearchType.HISTORICAL, ResearchType.SUPERNATURAL],
            "science_fiction": [ResearchType.SCIENTIFIC, ResearchType.TECHNOLOGICAL],
            "mystery": [ResearchType.CRIME_INVESTIGATION, ResearchType.LEGAL],
            "historical_fiction": [ResearchType.HISTORICAL, ResearchType.CULTURAL],
            "medical": [ResearchType.MEDICAL, ResearchType.PROFESSIONAL],
            "legal": [ResearchType.LEGAL, ResearchType.PROFESSIONAL]
        }
        
        # Check if this research type is high priority for the genre
        for genre_key, high_priority_types in high_priority_mappings.items():
            if genre_key in genre_lower and research_type in high_priority_types:
                return "high"
        
        # Default to medium priority
        return "medium"
    
    @classmethod
    def _estimate_time(cls, research_type: ResearchType, priority: str) -> int:
        """Estimate research time in minutes."""
        base_times = {
            "easy": 20,
            "medium": 35,
            "hard": 60,
            "very_hard": 90
        }
        
        base_time = base_times.get(research_type.complexity_level, 35)
        
        # Adjust based on priority
        priority_multipliers = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.3,
            "critical": 1.5
        }
        
        multiplier = priority_multipliers.get(priority, 1.0)
        return int(base_time * multiplier)
    
    @classmethod
    def _generate_questions(cls, research_type: ResearchType, genre: str, topic: str) -> List[str]:
        """Generate specific research questions."""
        # Base questions for each research type
        base_questions = {
            ResearchType.HISTORICAL: [
                "What were the key events of this period?",
                "What was daily life like for ordinary people?",
                "What were the social and political structures?"
            ],
            ResearchType.CULTURAL: [
                "What are the important cultural traditions?",
                "How do social relationships function?",
                "What are the key values and beliefs?"
            ],
            ResearchType.PROFESSIONAL: [
                "What are the typical daily responsibilities?",
                "What training and qualifications are required?",
                "What are the common challenges and conflicts?"
            ],
            ResearchType.GEOGRAPHICAL: [
                "What are the key geographical features?",
                "What is the climate and environment like?",
                "How do people travel and navigate?"
            ],
            ResearchType.CRIME_INVESTIGATION: [
                "What are standard investigation procedures?",
                "What forensic techniques are commonly used?",
                "How does the legal process work?"
            ]
        }
        
        # Get base questions or generate generic ones
        questions = base_questions.get(research_type, [
            f"What are the key aspects of {topic}?",
            f"How does {topic} relate to the story?",
            f"What details are important for authenticity?"
        ])
        
        return questions[:3]  # Limit to 3 questions


# Example usage and testing
if __name__ == "__main__":
    print("=== MuseQuill Research System Demo ===\n")
    
    # Test ResearchType enum
    print("1. Research Type Examples:")
    test_types = [ResearchType.HISTORICAL, ResearchType.SUPERNATURAL, ResearchType.CRIME_INVESTIGATION]
    for rt in test_types:
        print(f"  • {rt.display_name}")
        print(f"    Complexity: {rt.complexity_level}")
        print(f"    AI Difficulty: {rt.ai_research_difficulty}")
        print(f"    Sources: {', '.join(rt.typical_sources[:3])}...")
        print()
    
    # Test from_string functionality
    print("2. String Conversion Examples:")
    test_strings = ["history", "crime investigation", "supernatural", "cooking"]
    for test_str in test_strings:
        try:
            rt = ResearchType.from_string(test_str)
            print(f"  '{test_str}' -> {rt.display_name}")
        except ValueError as e:
            print(f"  '{test_str}' -> ERROR: {e}")
    
    # Test genre recommendations
    print("\n3. Genre-based Research Recommendations:")
    test_genres = ["fantasy", "mystery", "historical_fiction"]
    for genre in test_genres:
        types = ResearchType.get_types_for_genre(genre)
        print(f"  {genre.title()}: {', '.join([rt.display_name for rt in types[:4]])}...")
    
    # Test research plan generation
    print("\n4. Generated Research Plan:")
    plan = ResearchPlanGenerator.generate_plan(
        book_title="The Crystal Prophecy",
        genre="fantasy",
        target_audience="young_adult",
        num_research_topics=4,
        include_ai_friendly_only=True
    )
    
    print(f"  Book: {plan.book_title}")
    print(f"  Genre: {plan.genre}")
    print(f"  Total estimated time: {plan.total_estimated_time} minutes")
    print(f"  Requirements ({len(plan.requirements)}):")
    
    for i, req in enumerate(plan.requirements, 1):
        print(f"    {i}. {req.research_type.display_name}")
        print(f"       Topic: {req.topic}")
        print(f"       Priority: {req.priority} | Time: {req.estimated_time}min")
        print(f"       Questions: {len(req.specific_questions)} questions")
        print()
    
    # Test plan summaries
    print("5. Plan Analysis:")
    print(f"  Priority breakdown: {plan.priority_breakdown}")
    print(f"  Complexity breakdown: {plan.complexity_breakdown}")
    
    # Test JSON export/import
    print("\n6. JSON Export/Import Test:")
    json_export = plan.export_to_json()
    imported_plan = ResearchPlan.import_from_json(json_export)
    print(f"  Export successful: {len(json_export)} characters")
    print(f"  Import successful: {imported_plan.book_title} ({len(imported_plan.requirements)} requirements)")
    
    print("\n=== Demo Complete ===")