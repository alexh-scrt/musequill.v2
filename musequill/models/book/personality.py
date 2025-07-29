from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union
import re


class PersonalityTrait(str, Enum):
    """Common personality traits for character development."""
    # Positive Traits
    BRAVE = "brave"
    LOYAL = "loyal"
    INTELLIGENT = "intelligent"
    COMPASSIONATE = "compassionate"
    DETERMINED = "determined"
    HONEST = "honest"
    CREATIVE = "creative"
    PATIENT = "patient"
    OPTIMISTIC = "optimistic"
    HUMBLE = "humble"
    GENEROUS = "generous"
    WISE = "wise"
    CHARISMATIC = "charismatic"
    RELIABLE = "reliable"
    EMPATHETIC = "empathetic"
    
    # Negative Traits  
    ARROGANT = "arrogant"
    SELFISH = "selfish"
    IMPULSIVE = "impulsive"
    STUBBORN = "stubborn"
    JEALOUS = "jealous"
    COWARDLY = "cowardly"
    DISHONEST = "dishonest"
    CRUEL = "cruel"
    LAZY = "lazy"
    PESSIMISTIC = "pessimistic"
    GREEDY = "greedy"
    MANIPULATIVE = "manipulative"
    VINDICTIVE = "vindictive"
    RECKLESS = "reckless"
    PARANOID = "paranoid"
    
    # Neutral/Complex Traits
    AMBITIOUS = "ambitious"
    INDEPENDENT = "independent"
    MYSTERIOUS = "mysterious"
    ECCENTRIC = "eccentric"
    PRAGMATIC = "pragmatic"
    CAUTIOUS = "cautious"
    ANALYTICAL = "analytical"
    SPONTANEOUS = "spontaneous"
    COMPETITIVE = "competitive"
    INTROVERTED = "introverted"
    EXTROVERTED = "extroverted"

    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        return self.value.replace("_", " ").title()

    @property
    def description(self) -> str:
        """Detailed description of the personality trait."""
        descriptions = {
            # Positive Traits
            self.BRAVE: "Shows courage in the face of danger, difficulty, or pain, willing to confront fears and take risks for what's right.",
            self.LOYAL: "Demonstrates unwavering faithfulness and allegiance to friends, family, principles, or causes, even in difficult circumstances.",
            self.INTELLIGENT: "Possesses keen mental faculties, quick understanding, and the ability to learn, reason, and solve problems effectively.",
            self.COMPASSIONATE: "Shows deep empathy and concern for others' suffering, actively seeking to help and alleviate pain or hardship.",
            self.DETERMINED: "Displays firmness of purpose and resolute persistence in pursuing goals despite obstacles or setbacks.",
            self.HONEST: "Consistently tells the truth and acts with integrity, being genuine and transparent in dealings with others.",
            self.CREATIVE: "Shows original thinking and imagination, able to generate novel ideas and innovative solutions to problems.",
            self.PATIENT: "Demonstrates the ability to wait calmly, tolerate delay or frustration without becoming annoyed or anxious.",
            self.OPTIMISTIC: "Maintains a positive outlook and hopeful attitude, expecting good outcomes and seeing opportunities in challenges.",
            self.HUMBLE: "Shows modesty and lack of arrogance, recognizing personal limitations and treating others with respect regardless of status.",
            self.GENEROUS: "Freely gives time, money, help, or kindness to others without expecting anything in return.",
            self.WISE: "Possesses deep understanding, good judgment, and the ability to make sound decisions based on experience and knowledge.",
            self.CHARISMATIC: "Has a compelling charm and natural ability to attract, influence, and inspire others through personal magnetism.",
            self.RELIABLE: "Consistently dependable and trustworthy, can be counted on to fulfill commitments and responsibilities.",
            self.EMPATHETIC: "Understands and shares the feelings of others, able to see situations from different perspectives with emotional intelligence.",
            
            # Negative Traits
            self.ARROGANT: "Displays excessive pride and self-importance, often looking down on others and overestimating personal abilities.",
            self.SELFISH: "Primarily concerned with personal interests and needs, often at the expense of others' well-being or feelings.",
            self.IMPULSIVE: "Acts quickly without thinking through consequences, often making hasty decisions based on immediate emotions or desires.",
            self.STUBBORN: "Refuses to change opinions or course of action despite good reasons to do so, being inflexibly set in ways.",
            self.JEALOUS: "Experiences resentment and envy toward others' advantages, success, or relationships, often leading to bitter feelings.",
            self.COWARDLY: "Lacks courage and bravery, tends to avoid danger or difficult situations, often abandoning others in times of need.",
            self.DISHONEST: "Frequently lies, deceives, or acts with duplicity, cannot be trusted to tell the truth or act with integrity.",
            self.CRUEL: "Takes pleasure in causing pain or suffering to others, showing callous disregard for others' feelings or welfare.",
            self.LAZY: "Avoids work or effort, preferring ease and inactivity, often failing to fulfill responsibilities or reach potential.",
            self.PESSIMISTIC: "Consistently expects the worst outcomes, focuses on negative aspects of situations, and maintains a gloomy outlook.",
            self.GREEDY: "Has an excessive desire for wealth, material possessions, or power, often at the expense of ethical considerations.",
            self.MANIPULATIVE: "Uses cunning and deceit to influence or control others for personal gain, often exploiting emotional vulnerabilities.",
            self.VINDICTIVE: "Seeks revenge and retribution, holding grudges and actively trying to harm those who have wronged them.",
            self.RECKLESS: "Acts without considering consequences or safety, taking dangerous risks that endanger self and others.",
            self.PARANOID: "Exhibits irrational suspicion and distrust of others, often believing in conspiracy theories or persecution.",
            
            # Neutral/Complex Traits
            self.AMBITIOUS: "Strongly desires success, achievement, or advancement, willing to work hard but may sometimes prioritize goals over relationships.",
            self.INDEPENDENT: "Values self-reliance and autonomy, prefers to make own decisions and may resist help or advice from others.",
            self.MYSTERIOUS: "Keeps personal thoughts and feelings private, often appearing enigmatic and hard to understand or predict.",
            self.ECCENTRIC: "Displays unconventional or quirky behavior and thinking patterns that deviate from social norms in harmless ways.",
            self.PRAGMATIC: "Takes a practical, realistic approach to situations, focusing on what works rather than idealistic principles.",
            self.CAUTIOUS: "Carefully considers risks and potential problems before acting, preferring safety and security over bold ventures.",
            self.ANALYTICAL: "Approaches problems systematically, breaking down complex issues into components for logical examination and solution.",
            self.SPONTANEOUS: "Acts on impulse and embraces unplanned activities, preferring flexibility and excitement over routine and structure.",
            self.COMPETITIVE: "Strives to win and excel in comparison to others, driven by the desire to be the best in chosen endeavors.",
            self.INTROVERTED: "Gains energy from solitude and internal reflection, preferring smaller groups and deep conversations over large social gatherings.",
            self.EXTROVERTED: "Gains energy from social interaction and external stimulation, enjoying large groups and being the center of attention.",
        }
        return descriptions.get(self, f"Character trait: {self.display_name.lower()}")

    @property
    def trait_type(self) -> str:
        """Category of trait (positive, negative, or complex)."""
        positive_traits = {
            self.BRAVE, self.LOYAL, self.INTELLIGENT, self.COMPASSIONATE, self.DETERMINED,
            self.HONEST, self.CREATIVE, self.PATIENT, self.OPTIMISTIC, self.HUMBLE,
            self.GENEROUS, self.WISE, self.CHARISMATIC, self.RELIABLE, self.EMPATHETIC
        }
        negative_traits = {
            self.ARROGANT, self.SELFISH, self.IMPULSIVE, self.STUBBORN, self.JEALOUS,
            self.COWARDLY, self.DISHONEST, self.CRUEL, self.LAZY, self.PESSIMISTIC,
            self.GREEDY, self.MANIPULATIVE, self.VINDICTIVE, self.RECKLESS, self.PARANOID
        }
        
        if self in positive_traits:
            return "positive"
        elif self in negative_traits:
            return "negative"
        else:
            return "complex"

    @property
    def opposite_trait(self) -> Optional['PersonalityTrait']:
        """The opposite or contrasting trait, if one exists."""
        opposites = {
            self.BRAVE: self.COWARDLY,
            self.COWARDLY: self.BRAVE,
            self.OPTIMISTIC: self.PESSIMISTIC,
            self.PESSIMISTIC: self.OPTIMISTIC,
            self.HONEST: self.DISHONEST,
            self.DISHONEST: self.HONEST,
            self.GENEROUS: self.SELFISH,
            self.SELFISH: self.GENEROUS,
            self.HUMBLE: self.ARROGANT,
            self.ARROGANT: self.HUMBLE,
            self.PATIENT: self.IMPULSIVE,
            self.IMPULSIVE: self.PATIENT,
            self.COMPASSIONATE: self.CRUEL,
            self.CRUEL: self.COMPASSIONATE,
            self.DETERMINED: self.LAZY,
            self.LAZY: self.DETERMINED,
            self.INTROVERTED: self.EXTROVERTED,
            self.EXTROVERTED: self.INTROVERTED,
            self.CAUTIOUS: self.RECKLESS,
            self.RECKLESS: self.CAUTIOUS,
        }
        return opposites.get(self)

    @classmethod
    def from_string(cls, value: str) -> 'PersonalityTrait':
        """Create PersonalityTrait from string with fuzzy matching."""
        value_lower = value.lower().strip()
        
        # Direct value matching
        try:
            return cls(value_lower)
        except ValueError:
            pass
        
        # Fuzzy matching with synonyms
        mappings = {
            # Positive trait synonyms
            "courageous": cls.BRAVE,
            "fearless": cls.BRAVE,
            "heroic": cls.BRAVE,
            "faithful": cls.LOYAL,
            "devoted": cls.LOYAL,
            "trustworthy": cls.LOYAL,
            "smart": cls.INTELLIGENT,
            "brilliant": cls.INTELLIGENT,
            "clever": cls.INTELLIGENT,
            "caring": cls.COMPASSIONATE,
            "kind": cls.COMPASSIONATE,
            "sympathetic": cls.COMPASSIONATE,
            "persistent": cls.DETERMINED,
            "resolute": cls.DETERMINED,
            "steadfast": cls.DETERMINED,
            "truthful": cls.HONEST,
            "sincere": cls.HONEST,
            "genuine": cls.HONEST,
            "artistic": cls.CREATIVE,
            "imaginative": cls.CREATIVE,
            "innovative": cls.CREATIVE,
            "tolerant": cls.PATIENT,
            "calm": cls.PATIENT,
            "positive": cls.OPTIMISTIC,
            "hopeful": cls.OPTIMISTIC,
            "modest": cls.HUMBLE,
            "unassuming": cls.HUMBLE,
            "giving": cls.GENEROUS,
            "charitable": cls.GENEROUS,
            "knowledgeable": cls.WISE,
            "insightful": cls.WISE,
            "magnetic": cls.CHARISMATIC,
            "charming": cls.CHARISMATIC,
            "dependable": cls.RELIABLE,
            "understanding": cls.EMPATHETIC,
            
            # Negative trait synonyms  
            "proud": cls.ARROGANT,
            "conceited": cls.ARROGANT,
            "egotistical": cls.ARROGANT,
            "self-centered": cls.SELFISH,
            "narcissistic": cls.SELFISH,
            "hasty": cls.IMPULSIVE,
            "rash": cls.IMPULSIVE,
            "obstinate": cls.STUBBORN,
            "headstrong": cls.STUBBORN,
            "envious": cls.JEALOUS,
            "coward": cls.COWARDLY,
            "timid": cls.COWARDLY,
            "deceitful": cls.DISHONEST,
            "false": cls.DISHONEST,
            "mean": cls.CRUEL,
            "heartless": cls.CRUEL,
            "idle": cls.LAZY,
            "slothful": cls.LAZY,
            "negative": cls.PESSIMISTIC,
            "gloomy": cls.PESSIMISTIC,
            "avaricious": cls.GREEDY,
            "scheming": cls.MANIPULATIVE,
            "controlling": cls.MANIPULATIVE,
            "vengeful": cls.VINDICTIVE,
            "careless": cls.RECKLESS,
            "suspicious": cls.PARANOID,
            
            # Complex trait synonyms
            "driven": cls.AMBITIOUS,
            "goal-oriented": cls.AMBITIOUS,
            "self-reliant": cls.INDEPENDENT,
            "autonomous": cls.INDEPENDENT,
            "enigmatic": cls.MYSTERIOUS,
            "secretive": cls.MYSTERIOUS,
            "quirky": cls.ECCENTRIC,
            "unconventional": cls.ECCENTRIC,
            "practical": cls.PRAGMATIC,
            "realistic": cls.PRAGMATIC,
            "careful": cls.CAUTIOUS,
            "logical": cls.ANALYTICAL,
            "systematic": cls.ANALYTICAL,
            "impulsive": cls.SPONTANEOUS,
            "free-spirited": cls.SPONTANEOUS,
            "driven to win": cls.COMPETITIVE,
            "shy": cls.INTROVERTED,
            "reserved": cls.INTROVERTED,
            "outgoing": cls.EXTROVERTED,
            "social": cls.EXTROVERTED,
        }
        
        # Sort by length for better matching
        sorted_mappings = sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True)
        
        for keyword, trait in sorted_mappings:
            if keyword in value_lower:
                return trait
        
        raise ValueError(f"Unknown personality trait: {value}")

    @classmethod
    def get_positive_traits(cls) -> List['PersonalityTrait']:
        """Get all positive personality traits."""
        return [trait for trait in cls if trait.trait_type == "positive"]

    @classmethod
    def get_negative_traits(cls) -> List['PersonalityTrait']:
        """Get all negative personality traits."""
        return [trait for trait in cls if trait.trait_type == "negative"]

    @classmethod
    def get_complex_traits(cls) -> List['PersonalityTrait']:
        """Get all complex/neutral personality traits."""
        return [trait for trait in cls if trait.trait_type == "complex"]

    @classmethod
    def get_contrasting_pairs(cls) -> List[Tuple['PersonalityTrait', 'PersonalityTrait']]:
        """Get pairs of contrasting traits."""
        pairs = []
        processed = set()
        
        for trait in cls:
            if trait not in processed and trait.opposite_trait:
                pairs.append((trait, trait.opposite_trait))
                processed.add(trait)
                processed.add(trait.opposite_trait)
        
        return pairs

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"PersonalityTrait.{self.name}"