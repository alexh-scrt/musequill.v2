from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
import re


class TechnologyLevel(str, Enum):
    """Technology advancement levels for storytelling contexts."""
    
    # Prehistoric and Ancient
    STONE_AGE = "stone_age"
    BRONZE_AGE = "bronze_age"
    IRON_AGE = "iron_age"
    CLASSICAL = "classical"  # Ancient Rome/Greece level
    
    # Historical Periods
    MEDIEVAL = "medieval"
    RENAISSANCE = "renaissance"
    AGE_OF_SAIL = "age_of_sail"  # ~1500-1800s maritime exploration
    ENLIGHTENMENT = "enlightenment"  # ~1650-1800s
    
    # Industrial Revolution Era
    EARLY_INDUSTRIAL = "early_industrial"  # ~1760-1840s
    HIGH_INDUSTRIAL = "high_industrial"  # ~1840-1914
    STEAM_PUNK = "steam_punk"  # Alternative Victorian/Industrial fantasy
    
    # 20th Century
    EARLY_MODERN = "early_modern"  # Early 1900s-1940s
    ATOMIC_AGE = "atomic_age"  # 1940s-1960s
    SPACE_AGE = "space_age"  # 1960s-1990s
    INFORMATION_AGE = "information_age"  # 1990s-2010s
    
    # Contemporary and Near Future
    MODERN = "modern"  # Current day (2020s)
    DIGITAL_AGE = "digital_age"  # Enhanced connectivity, IoT, AI assistants
    NEAR_FUTURE = "near_future"  # 2030s-2050s
    CLIMATE_TECH = "climate_tech"  # Green technology focused future
    
    # Advanced Future
    POST_SCARCITY = "post_scarcity"  # Abundance through technology
    SPACE_FARING = "space_faring"  # Interplanetary civilization
    FAR_FUTURE = "far_future"  # Centuries ahead, advanced AI
    GALACTIC = "galactic"  # Interstellar civilization
    
    # Transcendent/Speculative
    POST_HUMAN = "post_human"  # Beyond current humanity
    SINGULARITY = "singularity"  # Technological singularity achieved
    POST_SINGULARITY = "post_singularity"  # Beyond the singularity
    
    # Hybrid/Alternative
    MIXED = "mixed"  # Multiple levels coexisting
    RETRO_FUTURISM = "retro_futurism"  # Past's vision of future
    DIESELPUNK = "dieselpunk"  # 1920s-1950s aesthetic with advanced tech
    BIOPUNK = "biopunk"  # Biotechnology-focused future
    CYBERPUNK = "cyberpunk"  # High tech, low life
    SOLARPUNK = "solarpunk"  # Optimistic green future
    APOCALYPTIC = "apocalyptic"  # Technology in collapse/regression
    POST_APOCALYPTIC = "post_apocalyptic"  # Rebuilding after collapse

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        """Detailed description of the technology level."""
        descriptions = {
            # Prehistoric and Ancient
            self.STONE_AGE: "Primitive tools made from stone, bone, and wood. Hunter-gatherer societies with basic fire use and simple shelters.",
            self.BRONZE_AGE: "Bronze metallurgy, early writing systems, organized agriculture, and the first cities with complex social hierarchies.",
            self.IRON_AGE: "Iron working technology, advanced agriculture, coined money, and established trade networks across civilizations.",
            self.CLASSICAL: "Advanced engineering, philosophy, literature, and governance. Think Roman aqueducts, Greek democracy, and Chinese innovations.",
            
            # Historical Periods
            self.MEDIEVAL: "Feudal societies with castles, knights, basic medicine, water mills, and early universities. Limited long-distance travel.",
            self.RENAISSANCE: "Scientific revolution, printing press, improved navigation, artistic flowering, and early firearms. Exploration begins.",
            self.AGE_OF_SAIL: "Ocean-going vessels, global trade networks, early colonialism, improved cartography, and maritime empires.",
            self.ENLIGHTENMENT: "Scientific method, early industry, political philosophy, improved medicine, and social reform movements.",
            
            # Industrial Revolution Era
            self.EARLY_INDUSTRIAL: "Steam engines, textile mills, canals, early railroads, and mass production. Rural to urban migration begins.",
            self.HIGH_INDUSTRIAL: "Extensive rail networks, telegraph, steel production, electricity, and large-scale manufacturing.",
            self.STEAM_PUNK: "Alternative history where steam technology advanced beyond historical limits. Airships, mechanical computers, and brass aesthetics.",
            
            # 20th Century
            self.EARLY_MODERN: "Automobiles, aircraft, radio, early cinema, antibiotics, and the beginnings of modern warfare.",
            self.ATOMIC_AGE: "Nuclear technology, early computers, television, jet aircraft, space programs, and Cold War tensions.",
            self.SPACE_AGE: "Moon landings, satellites, personal computers, modern medicine, jet travel, and global communications.",
            self.INFORMATION_AGE: "Internet, mobile phones, digital media, early AI, biotechnology, and global interconnectedness.",
            
            # Contemporary and Near Future
            self.MODERN: "Smartphones, social media, renewable energy, advanced medicine, AI assistants, and climate awareness.",
            self.DIGITAL_AGE: "Ubiquitous connectivity, IoT devices, autonomous vehicles, advanced AI, and digital-first societies.",
            self.NEAR_FUTURE: "Enhanced AI, gene therapy, fusion power, advanced robotics, and early space colonization.",
            self.CLIMATE_TECH: "Carbon capture, renewable dominance, rewilded cities, lab-grown materials, and sustainable abundance.",
            
            # Advanced Future
            self.POST_SCARCITY: "Molecular assemblers, unlimited clean energy, advanced AI managing resources, and material abundance for all.",
            self.SPACE_FARING: "Established colonies on multiple worlds, interplanetary travel, asteroid mining, and orbital habitats.",
            self.FAR_FUTURE: "Advanced AI companions, life extension, terraforming, and the beginning of stellar engineering.",
            self.GALACTIC: "Faster-than-light travel, galactic civilization, mega-structures, and contact with alien intelligence.",
            
            # Transcendent/Speculative
            self.POST_HUMAN: "Consciousness uploading, genetic enhancement beyond recognition, AI-human merger, and transcendence of biological limits.",
            self.SINGULARITY: "The moment of technological singularity where AI surpasses human intelligence and accelerates progress exponentially.",
            self.POST_SINGULARITY: "Post-singularity civilization where the distinction between technology, consciousness, and reality becomes fluid.",
            
            # Hybrid/Alternative
            self.MIXED: "Multiple technology levels coexisting, often due to inequality, cultural differences, or deliberate preservation of older ways.",
            self.RETRO_FUTURISM: "Past eras' optimistic visions of the future, featuring atomic-age aesthetics and yesterday's tomorrow.",
            self.DIESELPUNK: "1920s-1950s aesthetic meets advanced technology. Art deco, diesel engines, and gritty urban futures.",
            self.BIOPUNK: "Biotechnology-dominated future with genetic engineering, bio-computers, living buildings, and organic technology.",
            self.CYBERPUNK: "High technology meets low society. Corporate dominance, cybernetic implants, virtual reality, and urban decay.",
            self.SOLARPUNK: "Optimistic future harmonizing advanced technology with nature. Green cities, sustainable tech, and social equity.",
            self.APOCALYPTIC: "Civilization in collapse with technology failing, infrastructure crumbling, and society breaking down.",
            self.POST_APOCALYPTIC: "Survivors rebuilding with salvaged technology, often mixing advanced remnants with primitive improvisation."
        }
        return descriptions.get(self, f"Technology level: {self.display_name.lower()}")

    @property
    def time_period(self) -> str:
        """Approximate historical time period or future projection."""
        periods = {
            self.STONE_AGE: "~3.3M - 3300 BCE",
            self.BRONZE_AGE: "~3300 - 1200 BCE",
            self.IRON_AGE: "~1200 - 500 BCE",
            self.CLASSICAL: "~500 BCE - 500 CE",
            self.MEDIEVAL: "~500 - 1450 CE",
            self.RENAISSANCE: "~1450 - 1650 CE",
            self.AGE_OF_SAIL: "~1500 - 1800 CE",
            self.ENLIGHTENMENT: "~1650 - 1800 CE",
            self.EARLY_INDUSTRIAL: "~1760 - 1840 CE",
            self.HIGH_INDUSTRIAL: "~1840 - 1914 CE",
            self.STEAM_PUNK: "Alternative 1800s-1900s",
            self.EARLY_MODERN: "~1900 - 1945 CE",
            self.ATOMIC_AGE: "~1945 - 1970 CE",
            self.SPACE_AGE: "~1960 - 1990 CE",
            self.INFORMATION_AGE: "~1990 - 2010 CE",
            self.MODERN: "~2010 - 2030 CE",
            self.DIGITAL_AGE: "~2025 - 2040 CE",
            self.NEAR_FUTURE: "~2030 - 2070 CE",
            self.CLIMATE_TECH: "~2040 - 2080 CE",
            self.POST_SCARCITY: "~2080 - 2150 CE",
            self.SPACE_FARING: "~2100 - 2300 CE",
            self.FAR_FUTURE: "~2200 - 2500 CE",
            self.GALACTIC: "~2500+ CE",
            self.POST_HUMAN: "~2200+ CE",
            self.SINGULARITY: "~2040 - 2100 CE",
            self.POST_SINGULARITY: "Post-2100 CE",
            self.MIXED: "Variable",
            self.RETRO_FUTURISM: "1950s-1970s vision",
            self.DIESELPUNK: "1920s-1950s aesthetic",
            self.BIOPUNK: "~2050+ CE",
            self.CYBERPUNK: "~2030 - 2100 CE",
            self.SOLARPUNK: "~2040+ CE",
            self.APOCALYPTIC: "During collapse",
            self.POST_APOCALYPTIC: "Post-collapse recovery"
        }
        return periods.get(self, "Unknown period")

    @property
    def key_technologies(self) -> List[str]:
        """List of key technologies characteristic of this level."""
        tech_mapping = {
            self.STONE_AGE: ["stone tools", "fire", "basic shelter", "hunting weapons"],
            self.BRONZE_AGE: ["bronze metallurgy", "wheel", "writing", "agriculture", "pottery"],
            self.IRON_AGE: ["iron working", "coinage", "roads", "siege weapons", "trade networks"],
            self.CLASSICAL: ["aqueducts", "concrete", "mechanical clocks", "paper", "advanced mathematics"],
            self.MEDIEVAL: ["water mills", "windmills", "heavy plow", "stirrup", "mechanical clocks"],
            self.RENAISSANCE: ["printing press", "gunpowder", "compass", "telescope", "double-entry bookkeeping"],
            self.AGE_OF_SAIL: ["ocean-going ships", "navigation instruments", "cartography", "cannons", "global trade"],
            self.ENLIGHTENMENT: ["scientific instruments", "improved agriculture", "early manufacturing", "political theory"],
            self.EARLY_INDUSTRIAL: ["steam engine", "textile machinery", "canals", "coal mining", "factory system"],
            self.HIGH_INDUSTRIAL: ["railroads", "telegraph", "steel production", "electricity", "photography"],
            self.STEAM_PUNK: ["advanced steam tech", "airships", "mechanical computers", "pneumatic tubes", "brass engineering"],
            self.EARLY_MODERN: ["automobiles", "aircraft", "radio", "cinema", "assembly lines"],
            self.ATOMIC_AGE: ["nuclear power", "computers", "television", "jet engines", "antibiotics"],
            self.SPACE_AGE: ["rockets", "satellites", "integrated circuits", "lasers", "modern medicine"],
            self.INFORMATION_AGE: ["internet", "personal computers", "mobile phones", "biotechnology", "renewable energy"],
            self.MODERN: ["smartphones", "social media", "AI assistants", "electric vehicles", "renewable energy"],
            self.DIGITAL_AGE: ["IoT", "autonomous vehicles", "advanced AI", "quantum computing", "augmented reality"],
            self.NEAR_FUTURE: ["fusion power", "gene therapy", "neural interfaces", "3D printing", "space colonization"],
            self.CLIMATE_TECH: ["carbon capture", "lab-grown materials", "vertical farming", "atmospheric processors"],
            self.POST_SCARCITY: ["molecular assemblers", "unlimited energy", "resource abundance", "automated production"],
            self.SPACE_FARING: ["interplanetary travel", "space habitats", "asteroid mining", "terraforming"],
            self.FAR_FUTURE: ["stellar engineering", "consciousness transfer", "time manipulation", "dimension travel"],
            self.GALACTIC: ["FTL travel", "galactic networks", "mega-structures", "alien contact"],
            self.POST_HUMAN: ["consciousness uploading", "reality manipulation", "transcendent intelligence"],
            self.SINGULARITY: ["superintelligent AI", "technological acceleration", "exponential progress"],
            self.POST_SINGULARITY: ["incomprehensible technology", "reality as computation", "universal consciousness"],
            self.MIXED: ["varied technology levels", "coexisting eras", "technological diversity"],
            self.RETRO_FUTURISM: ["atomic cars", "flying cars", "robot servants", "atomic aesthetics"],
            self.DIESELPUNK: ["diesel engines", "art deco design", "radio technology", "early plastics"],
            self.BIOPUNK: ["genetic engineering", "bio-computers", "living buildings", "organic technology"],
            self.CYBERPUNK: ["cybernetic implants", "virtual reality", "corporate networks", "street technology"],
            self.SOLARPUNK: ["solar technology", "green architecture", "sustainable design", "social technology"],
            self.APOCALYPTIC: ["failing technology", "resource depletion", "collapsing infrastructure"],
            self.POST_APOCALYPTIC: ["salvaged tech", "improvised solutions", "mixed technology levels"]
        }
        return tech_mapping.get(self, [])

    @property
    def complexity_level(self) -> str:
        """Complexity level for story development."""
        complexity_mapping = {
            self.STONE_AGE: "minimal",
            self.BRONZE_AGE: "low",
            self.IRON_AGE: "low",
            self.CLASSICAL: "moderate",
            self.MEDIEVAL: "moderate",
            self.RENAISSANCE: "moderate",
            self.AGE_OF_SAIL: "moderate",
            self.ENLIGHTENMENT: "moderate",
            self.EARLY_INDUSTRIAL: "moderate",
            self.HIGH_INDUSTRIAL: "moderate",
            self.STEAM_PUNK: "high",
            self.EARLY_MODERN: "moderate",
            self.ATOMIC_AGE: "high",
            self.SPACE_AGE: "high",
            self.INFORMATION_AGE: "high",
            self.MODERN: "moderate",
            self.DIGITAL_AGE: "high",
            self.NEAR_FUTURE: "high",
            self.CLIMATE_TECH: "high",
            self.POST_SCARCITY: "very high",
            self.SPACE_FARING: "very high",
            self.FAR_FUTURE: "very high",
            self.GALACTIC: "extreme",
            self.POST_HUMAN: "extreme",
            self.SINGULARITY: "extreme",
            self.POST_SINGULARITY: "extreme",
            self.MIXED: "variable",
            self.RETRO_FUTURISM: "moderate",
            self.DIESELPUNK: "high",
            self.BIOPUNK: "very high",
            self.CYBERPUNK: "very high",
            self.SOLARPUNK: "high",
            self.APOCALYPTIC: "moderate",
            self.POST_APOCALYPTIC: "high"
        }
        return complexity_mapping.get(self, "unknown")

    @property
    def research_requirements(self) -> List[str]:
        """Areas requiring research for authentic storytelling."""
        research_mapping = {
            self.STONE_AGE: ["archaeology", "anthropology", "survival skills", "prehistoric climate"],
            self.BRONZE_AGE: ["ancient history", "metallurgy", "early civilizations", "archaeology"],
            self.IRON_AGE: ["ancient history", "metallurgy", "classical civilizations", "warfare"],
            self.CLASSICAL: ["classical history", "philosophy", "engineering", "politics", "literature"],
            self.MEDIEVAL: ["medieval history", "feudalism", "medieval warfare", "religion", "daily life"],
            self.RENAISSANCE: ["Renaissance history", "art history", "early science", "exploration", "humanism"],
            self.AGE_OF_SAIL: ["maritime history", "navigation", "colonialism", "naval warfare", "exploration"],
            self.ENLIGHTENMENT: ["intellectual history", "philosophy", "early science", "political theory"],
            self.EARLY_INDUSTRIAL: ["industrial history", "steam technology", "urbanization", "labor movements"],
            self.HIGH_INDUSTRIAL: ["Victorian era", "industrial technology", "social reform", "imperialism"],
            self.STEAM_PUNK: ["Victorian aesthetics", "alternative history", "steam technology", "speculative engineering"],
            self.EARLY_MODERN: ["20th century history", "technology development", "world wars", "social change"],
            self.ATOMIC_AGE: ["nuclear physics", "Cold War history", "space race", "computing history"],
            self.SPACE_AGE: ["space exploration", "computer science", "telecommunications", "modern medicine"],
            self.INFORMATION_AGE: ["internet history", "digital revolution", "biotechnology", "globalization"],
            self.MODERN: ["contemporary technology", "social media", "climate change", "current events"],
            self.DIGITAL_AGE: ["emerging technology", "AI research", "IoT", "cybersecurity", "digital society"],
            self.NEAR_FUTURE: ["technology trends", "futurism", "emerging science", "social forecasting"],
            self.CLIMATE_TECH: ["climate science", "green technology", "sustainability", "environmental policy"],
            self.POST_SCARCITY: ["economics", "nanotechnology", "automation", "social theory"],
            self.SPACE_FARING: ["space colonization", "astronomy", "terraforming", "space psychology"],
            self.FAR_FUTURE: ["speculative science", "futurism", "consciousness studies", "physics"],
            self.GALACTIC: ["astrophysics", "xenobiology", "galactic sociology", "cosmic engineering"],
            self.POST_HUMAN: ["transhumanism", "consciousness studies", "philosophy of mind", "speculative evolution"],
            self.SINGULARITY: ["artificial intelligence", "technological acceleration", "futurism", "philosophy"],
            self.POST_SINGULARITY: ["speculative philosophy", "consciousness studies", "metaphysics", "cosmology"],
            self.MIXED: ["comparative technology", "social stratification", "cultural studies", "economics"],
            self.RETRO_FUTURISM: ["1950s-60s culture", "atomic age aesthetics", "historical futurism"],
            self.DIESELPUNK: ["1920s-50s history", "art deco", "early automotive", "interwar period"],
            self.BIOPUNK: ["biotechnology", "genetic engineering", "bioethics", "synthetic biology"],
            self.CYBERPUNK: ["computer science", "cybernetics", "urban studies", "corporate culture"],
            self.SOLARPUNK: ["sustainability", "green technology", "social ecology", "optimistic futurism"],
            self.APOCALYPTIC: ["disaster studies", "social collapse", "survival psychology", "crisis management"],
            self.POST_APOCALYPTIC: ["survival skills", "rebuilding societies", "scavenging culture", "adaptation"]
        }
        return research_mapping.get(self, [])

    def __str__(self) -> str:
        """String representation returns display name."""
        return self.display_name

    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"TechnologyLevel.{self.name}"

    @classmethod
    def from_string(cls, value: str) -> 'TechnologyLevel':
        """Create TechnologyLevel from string with fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError("Invalid technology level value")
        
        # Clean and normalize input
        cleaned_value = value.strip().lower()
        
        # Direct match first
        for tech_level in cls:
            if tech_level.value == cleaned_value:
                return tech_level
        
        # Display name match
        for tech_level in cls:
            if tech_level.display_name.lower() == cleaned_value:
                return tech_level
        
        # Fuzzy matching with synonyms and common terms
        fuzzy_mappings = {
            # Historical periods
            "stone": cls.STONE_AGE,
            "caveman": cls.STONE_AGE,
            "prehistoric": cls.STONE_AGE,
            "bronze": cls.BRONZE_AGE,
            "iron": cls.IRON_AGE,
            "ancient": cls.CLASSICAL,
            "roman": cls.CLASSICAL,
            "greek": cls.CLASSICAL,
            "middle ages": cls.MEDIEVAL,
            "dark ages": cls.MEDIEVAL,
            "knight": cls.MEDIEVAL,
            "castle": cls.MEDIEVAL,
            "renaissance": cls.RENAISSANCE,
            "sail": cls.AGE_OF_SAIL,
            "sailing": cls.AGE_OF_SAIL,
            "pirate": cls.AGE_OF_SAIL,
            "enlightenment": cls.ENLIGHTENMENT,
            
            # Industrial and modern
            "industrial": cls.HIGH_INDUSTRIAL,
            "victorian": cls.STEAM_PUNK,
            "modern": cls.MODERN,
            "contemporary": cls.MODERN,
            "current": cls.MODERN,
            "today": cls.MODERN,
            "present": cls.MODERN,
            "now": cls.MODERN,
            
            # Future periods
            "future": cls.NEAR_FUTURE,
            "tomorrow": cls.NEAR_FUTURE,
            "sci-fi": cls.FAR_FUTURE,
            "science fiction": cls.FAR_FUTURE,
            "scifi": cls.FAR_FUTURE,
            "space": cls.SPACE_FARING,
            "galactic": cls.GALACTIC,
            "star": cls.GALACTIC,
            "interstellar": cls.GALACTIC,
            
            # Technology themes
            "atomic": cls.ATOMIC_AGE,
            "nuclear": cls.ATOMIC_AGE,
            "digital": cls.DIGITAL_AGE,
            "internet": cls.INFORMATION_AGE,
            "computer": cls.INFORMATION_AGE,
            "cyber": cls.CYBERPUNK,
            "cyberpunk": cls.CYBERPUNK,
            "bio": cls.BIOPUNK,
            "biopunk": cls.BIOPUNK,
            "genetic": cls.BIOPUNK,
            "solar": cls.SOLARPUNK,
            "solarpunk": cls.SOLARPUNK,
            "green": cls.SOLARPUNK,
            "eco": cls.SOLARPUNK,
            "diesel": cls.DIESELPUNK,
            "dieselpunk": cls.DIESELPUNK,
            "retro": cls.RETRO_FUTURISM,
            "vintage": cls.RETRO_FUTURISM,
            "steampunk": cls.STEAM_PUNK,
            
            # Special categories
            "post-apocalyptic": cls.POST_APOCALYPTIC,
            "post apocalyptic": cls.POST_APOCALYPTIC,
            "postapocalyptic": cls.POST_APOCALYPTIC,
            "apocalypse": cls.APOCALYPTIC,
            "end times": cls.APOCALYPTIC,
            "collapse": cls.APOCALYPTIC,
            "mixed": cls.MIXED,
            "multiple": cls.MIXED,
            "varied": cls.MIXED,
            "hybrid": cls.MIXED,
            "singularity": cls.SINGULARITY,
            "posthuman": cls.POST_HUMAN,
            "post-human": cls.POST_HUMAN,
            "transhuman": cls.POST_HUMAN,
            "climate": cls.CLIMATE_TECH,
            "sustainable": cls.CLIMATE_TECH,
            "abundance": cls.POST_SCARCITY,
            "post-scarcity": cls.POST_SCARCITY,
            "postscarcity": cls.POST_SCARCITY,
        }
        
        # Check fuzzy mappings - require more precise matches
        for key, tech_level in fuzzy_mappings.items():
            # Exact match or cleaned_value is a word within the key (for multi-word keys)
            if (key == cleaned_value or 
                (len(key.split()) > 1 and cleaned_value in key.split()) or
                # Allow key to be found in cleaned_value only if it's a substantial part
                (len(key) >= 4 and key in cleaned_value and len(key) >= len(cleaned_value) * 0.6)):
                return tech_level
        
        # Partial word matching - balanced approach  
        for tech_level in cls:
            tech_words = tech_level.value.split('_')
            input_words = cleaned_value.replace('_', ' ').replace('-', ' ').split()
            
            # Check for meaningful word overlap
            matched_chars = 0
            total_input_chars = len(cleaned_value.replace(' ', ''))
            
            # Skip if input is too short or too long compared to tech level value
            if total_input_chars < 3 or total_input_chars > len(tech_level.value) * 2:
                continue
                
            for input_word in input_words:
                if len(input_word) > 2:  # Consider words longer than 2 characters
                    for tech_word in tech_words:
                        if input_word == tech_word:
                            matched_chars += len(input_word)
                        elif len(input_word) >= 4 and input_word in tech_word:
                            matched_chars += len(input_word)
                        elif len(tech_word) >= 4 and tech_word in input_word and len(tech_word) >= 4:
                            matched_chars += len(tech_word)
            
            # Require substantial match (at least 60% of input should match)
            if matched_chars > 0 and matched_chars / total_input_chars >= 0.6:
                return tech_level
        
        raise ValueError(f"Invalid technology level: '{value}'")

    @classmethod
    def get_historical_levels(cls) -> List['TechnologyLevel']:
        """Get technology levels based on real historical periods."""
        return [
            cls.STONE_AGE, cls.BRONZE_AGE, cls.IRON_AGE, cls.CLASSICAL,
            cls.MEDIEVAL, cls.RENAISSANCE, cls.AGE_OF_SAIL, cls.ENLIGHTENMENT,
            cls.EARLY_INDUSTRIAL, cls.HIGH_INDUSTRIAL, cls.EARLY_MODERN,
            cls.ATOMIC_AGE, cls.SPACE_AGE, cls.INFORMATION_AGE, cls.MODERN
        ]

    @classmethod
    def get_future_levels(cls) -> List['TechnologyLevel']:
        """Get speculative future technology levels."""
        return [
            cls.DIGITAL_AGE, cls.NEAR_FUTURE, cls.CLIMATE_TECH, cls.POST_SCARCITY,
            cls.SPACE_FARING, cls.FAR_FUTURE, cls.GALACTIC, cls.POST_HUMAN,
            cls.SINGULARITY, cls.POST_SINGULARITY
        ]

    @classmethod
    def get_alternative_levels(cls) -> List['TechnologyLevel']:
        """Get alternative/speculative technology levels."""
        return [
            cls.STEAM_PUNK, cls.RETRO_FUTURISM, cls.DIESELPUNK, cls.BIOPUNK,
            cls.CYBERPUNK, cls.SOLARPUNK, cls.MIXED, cls.APOCALYPTIC, cls.POST_APOCALYPTIC
        ]

    @classmethod
    def get_by_complexity(cls, complexity: str) -> List['TechnologyLevel']:
        """Get technology levels by complexity rating."""
        complexity_map = {
            "minimal": [],
            "low": [],
            "moderate": [],
            "high": [],
            "very high": [],
            "extreme": [],
            "variable": []
        }
        
        for tech_level in cls:
            level_complexity = tech_level.complexity_level
            if level_complexity in complexity_map:
                complexity_map[level_complexity].append(tech_level)
        
        return complexity_map.get(complexity.lower(), [])

    @classmethod
    def get_research_intensive_levels(cls) -> List['TechnologyLevel']:
        """Get technology levels requiring extensive research."""
        research_intensive = []
        for tech_level in cls:
            if len(tech_level.research_requirements) >= 4:
                research_intensive.append(tech_level)
        return research_intensive

    def get_story_considerations(self) -> Dict[str, List[str]]:
        """Get storytelling considerations for this technology level."""
        return {
            "worldbuilding_focus": self._get_worldbuilding_focus(),
            "common_conflicts": self._get_common_conflicts(),
            "character_concerns": self._get_character_concerns(),
            "plot_opportunities": self._get_plot_opportunities()
        }

    def _get_worldbuilding_focus(self) -> List[str]:
        """Areas to focus on when building worlds at this tech level."""
        focus_areas = {
            self.STONE_AGE: ["survival", "tribal structure", "natural environment", "basic tools"],
            self.MEDIEVAL: ["social hierarchy", "religion", "castles", "rural life", "guilds"],
            self.STEAM_PUNK: ["Victorian aesthetics", "steam technology", "class divide", "industrial cities"],
            self.CYBERPUNK: ["corporate power", "urban decay", "digital worlds", "economic inequality"],
            self.SPACE_FARING: ["space habitats", "interplanetary politics", "resource management", "isolation"],
            self.POST_APOCALYPTIC: ["resource scarcity", "survivor communities", "environmental hazards", "technology salvage"]
        }
        return focus_areas.get(self, ["technology impact", "social structure", "daily life", "power dynamics"])

    def _get_common_conflicts(self) -> List[str]:
        """Common conflict types for this technology level."""
        conflicts = {
            self.STONE_AGE: ["survival vs nature", "tribal warfare", "resource competition"],
            self.MEDIEVAL: ["feudal politics", "religious conflicts", "succession disputes", "external invasions"],
            self.CYBERPUNK: ["corporate espionage", "AI rights", "digital privacy", "class warfare"],
            self.SPACE_FARING: ["colonial independence", "resource rights", "terraforming ethics", "alien contact"],
            self.POST_APOCALYPTIC: ["resource wars", "community conflicts", "technology hoarding", "rebuilding debates"]
        }
        return conflicts.get(self, ["technological ethics", "social change", "power struggles", "resource control"])

    def _get_character_concerns(self) -> List[str]:
        """Typical character concerns for this era."""
        concerns = {
            self.STONE_AGE: ["finding food", "avoiding predators", "tribal acceptance", "seasonal survival"],
            self.MEDIEVAL: ["honor and duty", "religious salvation", "family loyalty", "social status"],
            self.CYBERPUNK: ["identity in digital age", "corporate surveillance", "augmentation choices", "economic survival"],
            self.SPACE_FARING: ["homesickness", "radiation exposure", "colony politics", "cultural preservation"],
            self.POST_APOCALYPTIC: ["finding resources", "protecting loved ones", "moral compromises", "hope vs despair"]
        }
        return concerns.get(self, ["adapting to change", "moral choices", "personal relationships", "future planning"])

    def _get_plot_opportunities(self) -> List[str]:
        """Plot opportunities unique to this technology level."""
        opportunities = {
            self.STONE_AGE: ["discovering fire", "first tool creation", "tribal migrations", "cave paintings"],
            self.MEDIEVAL: ["knightly quests", "political intrigue", "religious pilgrimages", "siege warfare"],
            self.CYBERPUNK: ["corporate heists", "identity theft", "AI awakening", "digital archaeology"],
            self.SPACE_FARING: ["first contact", "terraforming projects", "space piracy", "generation ship drama"],
            self.POST_APOCALYPTIC: ["finding safe haven", "technology recovery", "community building", "uncovering the past"]
        }
        return opportunities.get(self, ["technological discovery", "social upheaval", "exploration", "innovation"])