from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import re


class GovernmentType(str, Enum):
    """Types of government systems with comprehensive fantasy and real-world options."""
    
    # CLASSICAL GOVERNMENT TYPES
    MONARCHY = "monarchy"
    DEMOCRACY = "democracy"
    REPUBLIC = "republic"
    DICTATORSHIP = "dictatorship"
    OLIGARCHY = "oligarchy"
    THEOCRACY = "theocracy"
    ANARCHY = "anarchy"
    FEUDALISM = "feudalism"
    TRIBALISM = "tribalism"
    EMPIRE = "empire"
    
    # SPECIALIZED GOVERNMENT FORMS
    CITY_STATE = "city_state"
    CONFEDERATION = "confederation"
    FEDERATION = "federation"
    TECHNOCRACY = "technocracy"  # Rule by technical experts
    MERITOCRACY = "meritocracy"  # Rule by merit/ability
    GERONTOCRACY = "gerontocracy"  # Rule by elders
    MILITARY_JUNTA = "military_junta"
    PLUTOCRACY = "plutocracy"  # Rule by the wealthy
    AUTOCRACY = "autocracy"
    TOTALITARIAN = "totalitarian"
    CONSTITUTIONAL_MONARCHY = "constitutional_monarchy"
    PARLIAMENTARY = "parliamentary"
    PRESIDENTIAL = "presidential"
    
    # FANTASY-SPECIFIC GOVERNMENT TYPES
    MAGOCRACY = "magocracy"  # Rule by magic users
    DRUIDOCRACY = "druidocracy"  # Rule by druids/nature priests
    NECROCRACY = "necrocracy"  # Rule by necromancers/undead
    DRACONIC_RULE = "draconic_rule"  # Rule by dragons
    DIVINE_MANDATE = "divine_mandate"  # Direct rule by gods/divine beings
    COUNCIL_OF_RACES = "council_of_races"  # Multi-species government
    GUILD_CONSORTIUM = "guild_consortium"  # Rule by trade guilds
    
    # SCIENCE FICTION GOVERNMENT TYPES
    CORPORATE = "corporate"  # Rule by corporations
    AI_GOVERNANCE = "ai_governance"  # Rule by artificial intelligence
    HIVE_MIND = "hive_mind"  # Collective consciousness rule
    GALACTIC_EMPIRE = "galactic_empire"
    TRADE_FEDERATION = "trade_federation"
    COLONIAL_ADMINISTRATION = "colonial_administration"
    TECHNO_DEMOCRATIC = "techno_democratic"  # Technology-enhanced democracy
    
    # HYBRID/COMPLEX SYSTEMS
    DUAL_MONARCHY = "dual_monarchy"  # Two monarchs sharing power
    ELECTIVE_MONARCHY = "elective_monarchy"
    COUNCIL_REPUBLIC = "council_republic"
    TRIBAL_CONFEDERATION = "tribal_confederation"
    MERCHANT_REPUBLIC = "merchant_republic"
    ECCLESIOCRACY = "ecclesiocracy"  # Church-state hybrid
    
    # TRANSITIONAL/SPECIAL STATES
    PROVISIONAL_GOVERNMENT = "provisional_government"
    REVOLUTIONARY_COUNCIL = "revolutionary_council"
    REGENCY = "regency"
    PROTECTORATE = "protectorate"
    OCCUPIED_TERRITORY = "occupied_territory"
    FAILED_STATE = "failed_state"
    NOMADIC_CHIEFTAINSHIP = "nomadic_chieftainship"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()
    
    @property
    def is_fantasy_specific(self) -> bool:
        """Check if this government type is specific to fantasy settings."""
        fantasy_types = {
            self.MAGOCRACY, self.DRUIDOCRACY, self.NECROCRACY, 
            self.DRACONIC_RULE, self.DIVINE_MANDATE, self.COUNCIL_OF_RACES,
            self.GUILD_CONSORTIUM
        }
        return self in fantasy_types
    
    @property
    def is_sci_fi_specific(self) -> bool:
        """Check if this government type is specific to science fiction settings."""
        sci_fi_types = {
            self.AI_GOVERNANCE, self.HIVE_MIND, self.GALACTIC_EMPIRE,
            self.TRADE_FEDERATION, self.COLONIAL_ADMINISTRATION, 
            self.TECHNO_DEMOCRATIC
        }
        return self in sci_fi_types
    
    @property
    def is_historical(self) -> bool:
        """Check if this government type is primarily historical."""
        historical_types = {
            self.FEUDALISM, self.TRIBALISM, self.EMPIRE, self.CITY_STATE,
            self.CONFEDERATION, self.DUAL_MONARCHY, self.ELECTIVE_MONARCHY,
            self.MERCHANT_REPUBLIC, self.NOMADIC_CHIEFTAINSHIP
        }
        return self in historical_types
    
    @property
    def is_modern(self) -> bool:
        """Check if this government type is common in modern settings."""
        modern_types = {
            self.DEMOCRACY, self.REPUBLIC, self.DICTATORSHIP, 
            self.CONSTITUTIONAL_MONARCHY, self.PARLIAMENTARY, self.PRESIDENTIAL,
            self.FEDERATION, self.MILITARY_JUNTA, self.TOTALITARIAN
        }
        return self in modern_types
    
    @property
    def is_authoritarian(self) -> bool:
        """Check if this government type is typically authoritarian."""
        authoritarian_types = {
            self.DICTATORSHIP, self.AUTOCRACY, self.TOTALITARIAN,
            self.MILITARY_JUNTA, self.NECROCRACY, self.AI_GOVERNANCE,
            self.HIVE_MIND, self.DRACONIC_RULE
        }
        return self in authoritarian_types
    
    @property
    def is_democratic(self) -> bool:
        """Check if this government type involves democratic principles."""
        democratic_types = {
            self.DEMOCRACY, self.REPUBLIC, self.PARLIAMENTARY, 
            self.PRESIDENTIAL, self.FEDERATION, self.COUNCIL_REPUBLIC,
            self.TECHNO_DEMOCRATIC, self.ELECTIVE_MONARCHY
        }
        return self in democratic_types
    
    @property
    def power_structure(self) -> str:
        """Describe the basic power structure of this government type."""
        power_structures = {
            self.MONARCHY: "single hereditary ruler",
            self.DEMOCRACY: "rule by the people",
            self.REPUBLIC: "elected representatives",
            self.DICTATORSHIP: "single absolute ruler",
            self.OLIGARCHY: "rule by few elites",
            self.THEOCRACY: "rule by religious authority",
            self.ANARCHY: "no central authority",
            self.FEUDALISM: "hierarchical land-based system",
            self.TRIBALISM: "clan or tribal leadership",
            self.EMPIRE: "expansive centralized rule",
            self.CITY_STATE: "autonomous city government",
            self.CONFEDERATION: "loose alliance of states",
            self.FEDERATION: "unified states with shared authority",
            self.TECHNOCRACY: "rule by technical experts",
            self.MERITOCRACY: "rule by ability and achievement",
            self.GERONTOCRACY: "rule by elders",
            self.MILITARY_JUNTA: "rule by military officers",
            self.PLUTOCRACY: "rule by the wealthy",
            self.AUTOCRACY: "unlimited power in one person",
            self.TOTALITARIAN: "total state control",
            self.CONSTITUTIONAL_MONARCHY: "monarch limited by constitution",
            self.PARLIAMENTARY: "legislature controls executive",
            self.PRESIDENTIAL: "separate executive and legislative",
            self.MAGOCRACY: "rule by magical practitioners",
            self.DRUIDOCRACY: "rule by nature priests",
            self.NECROCRACY: "rule by undead or death magic users",
            self.DRACONIC_RULE: "rule by dragons or dragon-kin",
            self.DIVINE_MANDATE: "direct divine authority",
            self.COUNCIL_OF_RACES: "multi-species governance",
            self.GUILD_CONSORTIUM: "rule by trade organizations",
            self.CORPORATE: "rule by corporations",
            self.AI_GOVERNANCE: "rule by artificial intelligence",
            self.HIVE_MIND: "collective consciousness authority",
            self.GALACTIC_EMPIRE: "interstellar imperial rule",
            self.TRADE_FEDERATION: "commercial alliance governance",
            self.COLONIAL_ADMINISTRATION: "external territorial control",
            self.TECHNO_DEMOCRATIC: "technology-enhanced democracy",
            self.DUAL_MONARCHY: "shared monarchical power",
            self.ELECTIVE_MONARCHY: "chosen royal authority",
            self.COUNCIL_REPUBLIC: "representative council system",
            self.TRIBAL_CONFEDERATION: "allied tribal groups",
            self.MERCHANT_REPUBLIC: "commercial elite governance",
            self.ECCLESIOCRACY: "integrated church-state rule",
            self.PROVISIONAL_GOVERNMENT: "temporary transitional authority",
            self.REVOLUTIONARY_COUNCIL: "post-revolution leadership",
            self.REGENCY: "rule on behalf of legitimate authority",
            self.PROTECTORATE: "protected dependent state",
            self.OCCUPIED_TERRITORY: "foreign military administration",
            self.FAILED_STATE: "collapsed governmental authority",
            self.NOMADIC_CHIEFTAINSHIP: "mobile tribal leadership"
        }
        return power_structures.get(self, "complex power structure")
    
    @property
    def typical_characteristics(self) -> List[str]:
        """List typical characteristics of this government type."""
        characteristics = {
            self.MONARCHY: ["hereditary succession", "royal court", "nobles", "ceremonial traditions"],
            self.DEMOCRACY: ["elections", "citizen participation", "majority rule", "political parties"],
            self.REPUBLIC: ["elected officials", "separation of powers", "term limits", "constitution"],
            self.DICTATORSHIP: ["absolute power", "suppressed opposition", "propaganda", "secret police"],
            self.OLIGARCHY: ["elite control", "wealth concentration", "limited access", "informal networks"],
            self.THEOCRACY: ["religious law", "clerical hierarchy", "divine authority", "moral codes"],
            self.ANARCHY: ["no central government", "voluntary cooperation", "local autonomy", "mutual aid"],
            self.FEUDALISM: ["land grants", "vassal relationships", "hereditary class", "local lords"],
            self.TRIBALISM: ["kinship bonds", "traditional customs", "elder councils", "oral traditions"],
            self.EMPIRE: ["territorial expansion", "cultural dominance", "tribute systems", "imperial bureaucracy"],
            self.MAGOCRACY: ["magical aptitude required", "spell-based laws", "arcane councils", "magical enforcement"],
            self.CORPORATE: ["profit motive", "shareholder interests", "market competition", "corporate hierarchy"],
            self.AI_GOVERNANCE: ["algorithmic decisions", "data-driven policy", "automated enforcement", "logical optimization"],
            self.TECHNOCRACY: ["expertise-based leadership", "scientific methodology", "efficiency focus", "merit selection"],
            self.HIVE_MIND: ["collective consciousness", "unified purpose", "shared knowledge", "instant communication"]
        }
        return characteristics.get(self, ["complex governance structure", "unique power dynamics"])
    
    @classmethod
    def get_fantasy_types(cls) -> List['GovernmentType']:
        """Get all government types suitable for fantasy settings."""
        return [gov_type for gov_type in cls if gov_type.is_fantasy_specific or gov_type.is_historical]
    
    @classmethod
    def get_sci_fi_types(cls) -> List['GovernmentType']:
        """Get all government types suitable for science fiction settings."""
        return [gov_type for gov_type in cls if gov_type.is_sci_fi_specific or gov_type.is_modern]
    
    @classmethod
    def get_historical_types(cls) -> List['GovernmentType']:
        """Get all government types that are historically based."""
        return [gov_type for gov_type in cls if gov_type.is_historical]
    
    @classmethod
    def get_modern_types(cls) -> List['GovernmentType']:
        """Get all government types common in modern settings."""
        return [gov_type for gov_type in cls if gov_type.is_modern]
    
    @classmethod
    def get_authoritarian_types(cls) -> List['GovernmentType']:
        """Get all authoritarian government types."""
        return [gov_type for gov_type in cls if gov_type.is_authoritarian]
    
    @classmethod
    def get_democratic_types(cls) -> List['GovernmentType']:
        """Get all democratic government types."""
        return [gov_type for gov_type in cls if gov_type.is_democratic]
    
    @classmethod
    def from_string(cls, gov_string: str) -> 'GovernmentType':
        """
        Create GovernmentType from string with restrictive fuzzy matching.
        
        Args:
            gov_string: String description of government type
            
        Returns:
            Matching GovernmentType enum value
            
        Raises:
            ValueError: If no suitable match is found
        """
        if not gov_string or not isinstance(gov_string, str):
            raise ValueError("Invalid government type value")
        
        # Clean and normalize input
        cleaned_value = gov_string.strip().lower()
        
        # Direct enum value match first
        for gov_type in cls:
            if gov_type.value == cleaned_value:
                return gov_type
        
        # Display name match
        for gov_type in cls:
            if gov_type.display_name.lower() == cleaned_value:
                return gov_type
        
        # Restrictive fuzzy matching with precise synonyms
        fuzzy_mappings = {
            # Historical terms
            "king": cls.MONARCHY,
            "queen": cls.MONARCHY,
            "royal": cls.MONARCHY,
            "crown": cls.MONARCHY,
            "throne": cls.MONARCHY,
            "monarch": cls.MONARCHY,
            "feudal": cls.FEUDALISM,
            "medieval": cls.FEUDALISM,
            "lord": cls.FEUDALISM,
            "vassal": cls.FEUDALISM,
            "tribal": cls.TRIBALISM,
            "tribe": cls.TRIBALISM,
            "clan": cls.TRIBALISM,
            "chief": cls.TRIBALISM,
            "imperial": cls.EMPIRE,
            "emperor": cls.EMPIRE,
            "empress": cls.EMPIRE,
            
            # Modern government terms
            "democratic": cls.DEMOCRACY,
            "vote": cls.DEMOCRACY,
            "election": cls.DEMOCRACY,
            "republic": cls.REPUBLIC,
            "representative": cls.REPUBLIC,
            "dictator": cls.DICTATORSHIP,
            "authoritarian": cls.DICTATORSHIP,
            "federal": cls.FEDERATION,
            "federation": cls.FEDERATION,
            "parliament": cls.PARLIAMENTARY,
            "parliamentary": cls.PARLIAMENTARY,
            "president": cls.PRESIDENTIAL,
            "presidential": cls.PRESIDENTIAL,
            
            # Religious government
            "religious": cls.THEOCRACY,
            "priest": cls.THEOCRACY,
            "church": cls.THEOCRACY,
            "divine": cls.THEOCRACY,
            "god": cls.THEOCRACY,
            "druid": cls.DRUIDOCRACY,
            "nature": cls.DRUIDOCRACY,
            "necromancer": cls.NECROCRACY,
            "undead": cls.NECROCRACY,
            
            # Fantasy government
            "magic": cls.MAGOCRACY,
            "magical": cls.MAGOCRACY,
            "wizard": cls.MAGOCRACY,
            "mage": cls.MAGOCRACY,
            "arcane": cls.MAGOCRACY,
            "dragon": cls.DRACONIC_RULE,
            "draconic": cls.DRACONIC_RULE,
            "guild": cls.GUILD_CONSORTIUM,
            "guilds": cls.GUILD_CONSORTIUM,
            
            # Sci-fi government
            "corporate": cls.CORPORATE,
            "corporation": cls.CORPORATE,
            "company": cls.CORPORATE,
            "business": cls.CORPORATE,
            "ai": cls.AI_GOVERNANCE,
            "artificial": cls.AI_GOVERNANCE,
            "computer": cls.AI_GOVERNANCE,
            "algorithm": cls.AI_GOVERNANCE,
            "hive": cls.HIVE_MIND,
            "collective": cls.HIVE_MIND,
            "galactic": cls.GALACTIC_EMPIRE,
            "space": cls.GALACTIC_EMPIRE,
            "interstellar": cls.GALACTIC_EMPIRE,
            
            # Power structures
            "oligarch": cls.OLIGARCHY,
            "oligarchy": cls.OLIGARCHY,
            "elite": cls.OLIGARCHY,
            "military": cls.MILITARY_JUNTA,
            "junta": cls.MILITARY_JUNTA,
            "general": cls.MILITARY_JUNTA,
            "wealthy": cls.PLUTOCRACY,
            "rich": cls.PLUTOCRACY,
            "plutocrat": cls.PLUTOCRACY,
            "expert": cls.TECHNOCRACY,
            "technocrat": cls.TECHNOCRACY,
            "scientist": cls.TECHNOCRACY,
            "technical": cls.TECHNOCRACY,
            "merit": cls.MERITOCRACY,
            "ability": cls.MERITOCRACY,
            "skill": cls.MERITOCRACY,
            "elder": cls.GERONTOCRACY,
            "elders": cls.GERONTOCRACY,
            "anarch": cls.ANARCHY,
            "anarchist": cls.ANARCHY,
            "chaos": cls.ANARCHY,
            
            # Special states
            "provisional": cls.PROVISIONAL_GOVERNMENT,
            "temporary": cls.PROVISIONAL_GOVERNMENT,
            "interim": cls.PROVISIONAL_GOVERNMENT,
            "revolution": cls.REVOLUTIONARY_COUNCIL,
            "revolutionary": cls.REVOLUTIONARY_COUNCIL,
            "rebel": cls.REVOLUTIONARY_COUNCIL,
            "regent": cls.REGENCY,
            "regency": cls.REGENCY,
            "protectorate": cls.PROTECTORATE,
            "protected": cls.PROTECTORATE,
            "occupied": cls.OCCUPIED_TERRITORY,
            "occupation": cls.OCCUPIED_TERRITORY,
            "failed": cls.FAILED_STATE,
            "collapse": cls.FAILED_STATE,
            "collapsed": cls.FAILED_STATE,
        }
        
        # Check fuzzy mappings with exact matches only
        if cleaned_value in fuzzy_mappings:
            return fuzzy_mappings[cleaned_value]
        
        # Partial word matching - very restrictive
        for gov_type in cls:
            gov_words = gov_type.value.split('_')
            input_words = cleaned_value.replace('_', ' ').replace('-', ' ').split()
            
            # Skip if input is too short or has too many words
            if len(cleaned_value) < 4 or len(input_words) > 3:
                continue
            
            # Check for meaningful word overlap
            matched_chars = 0
            total_input_chars = len(cleaned_value.replace(' ', ''))
            
            for input_word in input_words:
                if len(input_word) >= 4:  # Only consider words 4+ characters
                    for gov_word in gov_words:
                        if input_word == gov_word:
                            matched_chars += len(input_word)
                        elif len(input_word) >= 5 and len(gov_word) >= 5:
                            # Very restrictive substring matching
                            if (input_word in gov_word and len(input_word) >= len(gov_word) * 0.8) or \
                               (gov_word in input_word and len(gov_word) >= len(input_word) * 0.8):
                                matched_chars += min(len(input_word), len(gov_word))
            
            # Require very substantial match (at least 80% of input should match)
            if matched_chars > 0 and matched_chars / total_input_chars >= 0.8:
                return gov_type
        
        raise ValueError(f"Invalid government type: '{gov_string}'")
    
    def __str__(self) -> str:
        """String representation using display name."""
        return self.display_name
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"GovernmentType.{self.name}"