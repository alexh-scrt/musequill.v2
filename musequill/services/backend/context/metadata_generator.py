#!/usr/bin/env python3
"""
MetadataGenerator - LLM-Based Implementation

Generates structured metadata for content using LLM analysis.
Follows the universal metadata schema designed for the book generation pipeline.

Key Features:
- LLM-based content analysis for metadata generation
- Strict JSON schema validation with fallback handling
- Book-specific metadata extraction using actual book model enums
- Configurable prompting strategies for different content types
- Integration with Ollama/local LLM services
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

# Import actual book model enums
try:
    from musequill.models.book.writing_style import WritingStyle
    from musequill.models.book.book_length import BookLength
    from musequill.models.book.genre import GenreType, SubGenreType
    from musequill.models.book.audience import AudienceType
    from musequill.models.book.world import WorldType
    from musequill.models.book.story_structure import StoryStructure
    from musequill.models.book.conflict import ConflictType
    from musequill.models.book.narrative_pov import NarrativePOV
    from musequill.models.book.pacing_style import PacingStyle
    from musequill.models.book.tone_style import ToneStyle
except ImportError as e:
    # Fallback to None - will use string validation
    WritingStyle = None
    BookLength = None
    GenreType = None
    SubGenreType = None
    AudienceType = None
    WorldType = None
    StoryStructure = None
    ConflictType = None
    POVType = None
    PacingStyle = None
    ToneStyle = None


logger = logging.getLogger(__name__)


class ContentTypeHint(Enum):
    """Content type hints for better LLM analysis."""
    RESEARCH = "research"
    CHARACTER = "character" 
    WORLD = "world"
    SCENE = "scene"
    STYLE = "style"
    CHAPTER = "chapter"
    PLAN = "plan"
    UNKNOWN = "unknown"


@dataclass
class MetadataPromptConfig:
    """Configuration for metadata generation prompts."""
    temperature: float = 0.3  # Lower for more consistent JSON
    max_tokens: int = 800     # Enough for complete metadata
    model_name: str = "llama3.3:70b"
    timeout_seconds: int = 30
    retry_attempts: int = 2


class MetadataGenerator(ABC):
    """Abstract interface for metadata generation modules."""
    
    @abstractmethod
    def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """Generate metadata for content using LLM or other methods."""
        pass


class LLMMetadataGenerator(MetadataGenerator):
    """
    LLM-based metadata generator using structured prompting.
    
    Analyzes content and generates metadata following the universal schema.
    Includes validation, error handling, and fallback strategies.
    """
    
    def __init__(self, llm_client, config: Optional[MetadataPromptConfig] = None):
        """
        Initialize with LLM client and configuration.
        
        Args:
            llm_client: LLM service client (e.g., Ollama client)
            config: Configuration for prompting behavior
        """
        self.llm_client = llm_client
        self.config = config or MetadataPromptConfig()
        
        # Universal metadata schema template aligned with actual book models
        self.metadata_schema = {
            "content_type": "research|character|world|scene|style|chapter|plan",
            "content_subtype": "specific_description_string",
            "chapter_relevance": "[list_of_numbers] or 'all'",
            "priority": "essential|important|supporting",
            "quality_score": "0-100",
            "key_concepts": "list_of_up_to_7_key_terms",
            "usage_context": "chapter_writing|planning|reference|background",
            
            # Book model aligned fields (using actual enum values)
            "genre_primary": f"Valid values: {self._get_enum_values(GenreType)}",
            "genre_sub": f"Valid values: {self._get_enum_values(SubGenreType)}",
            "audience_type": f"Valid values: {self._get_enum_values(AudienceType)}",
            "writing_style": f"Valid values: {self._get_enum_values(WritingStyle)}",
            "story_structure": f"Valid values: {self._get_enum_values(StoryStructure)}",
            "world_type": f"Valid values: {self._get_enum_values(WorldType)}",
            "conflict_type": f"Valid values: {self._get_enum_values(ConflictType)}",
            "pov_type": f"Valid values: {self._get_enum_values(NarrativePOV)}",
            "pace_type": f"Valid values: {self._get_enum_values(PacingStyle)}",
            "tone_type": f"Valid values: {self._get_enum_values(ToneStyle)}"
        }
        
        # Content type specific analysis prompts
        self.analysis_prompts = {
            ContentTypeHint.RESEARCH: self._get_research_analysis_prompt(),
            ContentTypeHint.CHARACTER: self._get_character_analysis_prompt(),
            ContentTypeHint.WORLD: self._get_world_analysis_prompt(),
            ContentTypeHint.SCENE: self._get_scene_analysis_prompt(),
            ContentTypeHint.STYLE: self._get_style_analysis_prompt(),
            ContentTypeHint.CHAPTER: self._get_chapter_analysis_prompt(),
            ContentTypeHint.PLAN: self._get_plan_analysis_prompt(),
            ContentTypeHint.UNKNOWN: self._get_general_analysis_prompt()
        }
        
        logger.info(f"LLMMetadataGenerator initialized with model: {self.config.model_name}")
    
    def _get_enum_values(self, enum_class) -> str:
        """Extract values from enum class, handling None case."""
        if enum_class is None:
            return "enum_not_available"
        
        try:
            if hasattr(enum_class, '__members__'):
                return "|".join(enum_class.__members__.keys())
            else:
                # Handle string enums
                return "|".join([item.value for item in enum_class])
        except Exception:
            return "enum_values_unavailable"
    
    def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """
        Generate complete metadata using LLM analysis.
        
        Args:
            content: Raw content to analyze
            content_type: Hint about content type for better analysis
            book_id: Book identifier for context
            
        Returns:
            Complete metadata dictionary following universal schema
        """
        try:
            # Determine content type hint
            content_hint = self._determine_content_hint(content_type, content)
            
            # Generate metadata using LLM
            raw_metadata = self._generate_llm_metadata(content, content_hint, book_id)
            
            # Validate and clean metadata
            validated_metadata = self._validate_and_clean_metadata(raw_metadata)
            
            return validated_metadata
            
        except Exception as e:
            logger.error(f"Metadata generation failed: {e}")
            raise
    
    def _generate_llm_metadata(self, content: str, content_hint: ContentTypeHint, book_id: str) -> Dict[str, Any]:
        """Generate metadata using LLM with structured prompting."""
        
        # Build the analysis prompt
        analysis_prompt = self.analysis_prompts[content_hint]
        
        # Create the complete prompt
        prompt = self._build_metadata_prompt(content, analysis_prompt, book_id)
        
        # Execute LLM call with retries
        for attempt in range(self.config.retry_attempts):
            try:
                response = self._call_llm(prompt)
                parsed_metadata = self._extract_json_from_response(response)
                
                if parsed_metadata:
                    return parsed_metadata
                else:
                    logger.warning(f"No valid JSON in LLM response, attempt {attempt + 1}")
                    
            except Exception as e:
                logger.warning(f"LLM call failed, attempt {attempt + 1}: {e}")
                
                if attempt == self.config.retry_attempts - 1:
                    raise
        
        raise Exception("All LLM metadata generation attempts failed")
    
    def _build_metadata_prompt(self, content: str, analysis_prompt: str, book_id: str) -> str:
        """Build the complete prompt for metadata generation."""
        
        # Truncate content if too long (keep first ~1500 characters for analysis)
        content_sample = content[:1500] + "..." if len(content) > 1500 else content
        
        prompt = f"""You are an expert content analyst for book writing projects. Your task is to analyze the provided content and generate structured metadata in JSON format.

**CRITICAL INSTRUCTIONS:**
- You MUST respond with valid JSON only
- Do NOT include any explanation, commentary, or markdown formatting
- Follow the exact schema provided below
- Analyze the content carefully to determine accurate metadata values

**UNIVERSAL METADATA SCHEMA:**
{json.dumps(self.metadata_schema, indent=2)}

**CONTENT TYPE SPECIFIC ANALYSIS:**
{analysis_prompt}

**BOOK CONTEXT:**
Book ID: {book_id}

**CONTENT TO ANALYZE:**
{content_sample}

**RESPONSE FORMAT:**
Respond with ONLY a valid JSON object that follows the schema exactly. No additional text.

Example response format:
{{
    "content_type": "research",
    "content_subtype": "folklore_mythology",
    "chapter_relevance": [2, 5, 8],
    "priority": "important",
    "quality_score": 85,
    "key_concepts": ["baba_yaga", "slavic_folklore", "trials", "wisdom"],
    "usage_context": "chapter_writing"
}}

Generate the metadata now:"""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Execute LLM call with configured parameters."""
        try:
            # This assumes your LLM client has a generate method
            # Adjust based on your actual LLM client interface
            response = self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout_seconds
            )
            
            # Handle different response formats
            if isinstance(response, dict):
                return response.get('response', response.get('text', str(response)))
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from LLM response, handling various formats."""
        try:
            # Try direct JSON parsing first
            return json.loads(response.strip())
            
        except json.JSONDecodeError:
            # Try to find JSON within the response
            json_patterns = [
                r'\{[\s\S]*\}',  # Find JSON object
                r'```json\s*(\{[\s\S]*?\})\s*```',  # JSON in code blocks
                r'```\s*(\{[\s\S]*?\})\s*```'  # JSON in generic code blocks
            ]
            
            for pattern in json_patterns:
                matches = re.search(pattern, response, re.DOTALL)
                if matches:
                    try:
                        json_str = matches.group(1) if matches.groups() else matches.group(0)
                        return json.loads(json_str.strip())
                    except json.JSONDecodeError:
                        continue
            
            logger.warning("No valid JSON found in LLM response")
            return None
    
    def _validate_and_clean_metadata(self, raw_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata against schema and clean up values using book model enums."""
        
        # Required core fields
        required_fields = [
            "content_type", "content_subtype", "chapter_relevance",
            "priority", "quality_score", "key_concepts", "usage_context"
        ]
        
        # Check all required fields are present
        for field in required_fields:
            if field not in raw_metadata:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate and clean specific fields using book model values
        cleaned_metadata = {}
        
        # content_type validation
        valid_content_types = ["research", "character", "world", "scene", "style", "chapter", "plan"]
        if raw_metadata["content_type"] not in valid_content_types:
            logger.warning(f"Invalid content_type: {raw_metadata['content_type']}, defaulting to 'unknown'")
            cleaned_metadata["content_type"] = "unknown"
        else:
            cleaned_metadata["content_type"] = raw_metadata["content_type"]
        
        # content_subtype - keep as string
        cleaned_metadata["content_subtype"] = str(raw_metadata["content_subtype"])
        
        # chapter_relevance validation
        chapter_rel = raw_metadata["chapter_relevance"]
        if isinstance(chapter_rel, list):
            # Validate list of integers
            cleaned_chapters = []
            for ch in chapter_rel:
                if isinstance(ch, int) and 1 <= ch <= 50:  # Reasonable chapter range
                    cleaned_chapters.append(ch)
            cleaned_metadata["chapter_relevance"] = cleaned_chapters if cleaned_chapters else "all"
        elif isinstance(chapter_rel, str) and chapter_rel.lower() == "all":
            cleaned_metadata["chapter_relevance"] = "all"
        else:
            cleaned_metadata["chapter_relevance"] = "all"
        
        # priority validation
        valid_priorities = ["essential", "important", "supporting"]
        if raw_metadata["priority"] not in valid_priorities:
            cleaned_metadata["priority"] = "supporting"
        else:
            cleaned_metadata["priority"] = raw_metadata["priority"]
        
        # quality_score validation
        try:
            score = float(raw_metadata["quality_score"])
            cleaned_metadata["quality_score"] = max(0, min(100, int(score)))
        except (ValueError, TypeError):
            cleaned_metadata["quality_score"] = 50
        
        # key_concepts validation
        concepts = raw_metadata.get("key_concepts", [])
        if isinstance(concepts, list):
            # Clean and limit to 7 concepts
            clean_concepts = []
            for concept in concepts[:7]:
                if isinstance(concept, str) and concept.strip():
                    clean_concepts.append(concept.strip().lower())
            cleaned_metadata["key_concepts"] = clean_concepts
        else:
            cleaned_metadata["key_concepts"] = ["unspecified"]
        
        # usage_context validation
        valid_contexts = ["chapter_writing", "planning", "reference", "background"]
        if raw_metadata["usage_context"] not in valid_contexts:
            cleaned_metadata["usage_context"] = "reference"
        else:
            cleaned_metadata["usage_context"] = raw_metadata["usage_context"]
        
        # === BOOK MODEL ALIGNED FIELDS (Optional) ===
        
        # genre_primary validation (using actual GenreType enum)
        if "genre_primary" in raw_metadata and GenreType:
            valid_genres = self._get_enum_values_list(GenreType)
            if raw_metadata["genre_primary"] in valid_genres:
                cleaned_metadata["genre_primary"] = raw_metadata["genre_primary"]
        
        # audience_type validation (using actual AudienceType enum)
        if "audience_type" in raw_metadata and AudienceType:
            valid_audiences = self._get_enum_values_list(AudienceType)
            if raw_metadata["audience_type"] in valid_audiences:
                cleaned_metadata["audience_type"] = raw_metadata["audience_type"]
        
        # writing_style validation (using actual WritingStyle enum)
        if "writing_style" in raw_metadata and WritingStyle:
            valid_styles = self._get_enum_values_list(WritingStyle)
            if raw_metadata["writing_style"] in valid_styles:
                cleaned_metadata["writing_style"] = raw_metadata["writing_style"]
        
        # world_type validation (using actual WorldType enum)
        if "world_type" in raw_metadata and WorldType:
            valid_worlds = self._get_enum_values_list(WorldType)
            if raw_metadata["world_type"] in valid_worlds:
                cleaned_metadata["world_type"] = raw_metadata["world_type"]
        
        # conflict_type validation (using actual ConflictType enum)
        if "conflict_type" in raw_metadata and ConflictType:
            valid_conflicts = self._get_enum_values_list(ConflictType)
            if raw_metadata["conflict_type"] in valid_conflicts:
                cleaned_metadata["conflict_type"] = raw_metadata["conflict_type"]
        
        # pov_type validation (using actual POVType enum)
        if "pov_type" in raw_metadata and NarrativePOV:
            valid_povs = self._get_enum_values_list(NarrativePOV)
            if raw_metadata["pov_type"] in valid_povs:
                cleaned_metadata["pov_type"] = raw_metadata["pov_type"]
        
        # pace_type validation (using actual PacingStyle enum)
        if "pace_type" in raw_metadata and PacingStyle:
            valid_paces = self._get_enum_values_list(PacingStyle)
            if raw_metadata["pace_type"] in valid_paces:
                cleaned_metadata["pace_type"] = raw_metadata["pace_type"]
        
        # tone_type validation (using actual ToneStyle enum)
        if "tone_type" in raw_metadata and ToneStyle:
            valid_tones = self._get_enum_values_list(ToneStyle)
            if raw_metadata["tone_type"] in valid_tones:
                cleaned_metadata["tone_type"] = raw_metadata["tone_type"]
        
        # story_structure validation (using actual StoryStructure enum)
        if "story_structure" in raw_metadata and StoryStructure:
            valid_structures = self._get_enum_values_list(StoryStructure)
            if raw_metadata["story_structure"] in valid_structures:
                cleaned_metadata["story_structure"] = raw_metadata["story_structure"]
        
        return cleaned_metadata
    
    def _get_enum_values_list(self, enum_class) -> List[str]:
        """Get list of enum values for validation."""
        if enum_class is None:
            return []
        
        try:
            if hasattr(enum_class, '__members__'):
                return list(enum_class.__members__.keys())
            else:
                # Handle string enums
                return [item.value for item in enum_class]
        except Exception:
            return []
    
    def _determine_content_hint(self, content_type: str, content: str) -> ContentTypeHint:
        """Determine content type hint from type string and content analysis."""
        
        # Direct mapping from content_type string
        type_mapping = {
            "research": ContentTypeHint.RESEARCH,
            "character": ContentTypeHint.CHARACTER,
            "world": ContentTypeHint.WORLD,
            "scene": ContentTypeHint.SCENE,
            "style": ContentTypeHint.STYLE,
            "chapter": ContentTypeHint.CHAPTER,
            "plan": ContentTypeHint.PLAN
        }
        
        if content_type.lower() in type_mapping:
            return type_mapping[content_type.lower()]
        
        # Content-based analysis for unknown types
        content_lower = content.lower()
        
        # Research indicators
        if any(word in content_lower for word in ["folklore", "mythology", "research", "study", "historical"]):
            return ContentTypeHint.RESEARCH
        
        # Character indicators
        if any(word in content_lower for word in ["character", "personality", "dialogue", "motivation"]):
            return ContentTypeHint.CHARACTER
        
        # World-building indicators
        if any(word in content_lower for word in ["world", "setting", "location", "geography", "culture"]):
            return ContentTypeHint.WORLD
        
        # Scene indicators
        if any(word in content_lower for word in ["scene", "action", "description", "transition"]):
            return ContentTypeHint.SCENE
        
        # Planning indicators
        if any(word in content_lower for word in ["plan", "outline", "structure", "phase", "strategy"]):
            return ContentTypeHint.PLAN
        
        # Chapter indicators
        if any(word in content_lower for word in ["chapter", "story", "narrative", "plot"]):
            return ContentTypeHint.CHAPTER
        
        return ContentTypeHint.UNKNOWN
    
    # === CONTENT-SPECIFIC ANALYSIS PROMPTS ===
    
    def _get_research_analysis_prompt(self) -> str:
        return """
For RESEARCH content, focus on:
- Identify specific research topics (folklore, mythology, historical elements)
- Determine which chapters would benefit from this research
- Assess research quality and reliability (quality_score: 0-100)
- Extract key concepts and terminology (max 7 terms)
- Consider usage context (background reference vs active chapter writing)
- If applicable, identify genre alignment (fantasy, historical_fiction, children, etc.)
- Determine writing style implications (academic, narrative, accessible, etc.)
"""
    
    def _get_character_analysis_prompt(self) -> str:
        return """
For CHARACTER content, focus on:
- Identify specific characters mentioned and their roles
- Determine character development stages and growth arcs
- Assess dialogue quality and voice consistency (quality_score: 0-100)
- Extract personality traits and motivations (key_concepts)
- Consider which chapters feature these characters prominently (chapter_relevance)
- Identify POV implications (first_person, third_person_limited, etc.)
- Determine audience alignment (children, young_adult, adult, etc.)
"""
    
    def _get_world_analysis_prompt(self) -> str:
        return """
For WORLD-BUILDING content, focus on:
- Identify world type (fantasy, sci_fi, contemporary, historical, etc.)
- Assess locations, settings, and environmental elements
- Extract magic systems, technology level, and world rules
- Determine cultural and social elements (key_concepts)
- Consider which scenes/chapters need this world information (chapter_relevance)
- Assess complexity level for target audience
- Identify genre implications (fantasy, sci_fi, historical_fiction, etc.)
"""
    
    def _get_scene_analysis_prompt(self) -> str:
        return """
For SCENE content, focus on:
- Identify scene types (action, dialogue, description, transition)
- Assess pacing level (slow, medium, fast) and tension
- Extract structural elements and patterns (key_concepts)
- Determine reusability for similar scenes (usage_context)
- Consider chapter phases where this scene type is needed (chapter_relevance)
- Evaluate writing style (descriptive, cinematic, conversational, etc.)
- Assess quality and effectiveness (quality_score: 0-100)
"""
    
    def _get_style_analysis_prompt(self) -> str:
        return """
For STYLE content, focus on:
- Identify writing style (conversational, literary, accessible, formal, etc.)
- Assess voice consistency and tone (serious, humorous, whimsical, etc.)
- Evaluate age-appropriateness for target audience (children, young_adult, adult)
- Extract dialogue patterns and character speech (key_concepts)
- Determine POV style (first_person, third_person_limited, etc.)
- Consider pace implications (slow, medium, fast)
- Assess style quality and consistency (quality_score: 0-100)
"""
    
    def _get_chapter_analysis_prompt(self) -> str:
        return """
For CHAPTER content, focus on:
- Identify plot progression and story structure elements
- Assess character development within the chapter
- Extract themes and emotional beats (key_concepts)
- Determine chapter's role in overall story structure
- Identify conflict type (person_vs_person, person_vs_supernatural, etc.)
- Consider pacing level (slow, medium, fast) within chapter
- Evaluate world-building elements present
- Assess chapter quality and effectiveness (quality_score: 0-100)
"""
    
    def _get_plan_analysis_prompt(self) -> str:
        return """
For PLANNING content, focus on:
- Identify planning scope (chapter, scene, character, overall story)
- Assess completeness and detail level (quality_score: 0-100)
- Extract structural and organizational elements (key_concepts)
- Determine implementation priority (essential, important, supporting)
- Consider story structure implications (heros_journey, three_act, etc.)
- Identify genre and audience alignment
- Assess dependencies and prerequisites
- Determine usage context (planning, reference, chapter_writing)
"""
    
    def _get_general_analysis_prompt(self) -> str:
        return """
For GENERAL content analysis:
- Analyze content type based on structure and topics
- Identify key themes, concepts, and elements (key_concepts, max 7)
- Assess quality and usefulness for book writing (quality_score: 0-100)
- Determine most appropriate usage context (chapter_writing, planning, reference, background)
- Extract book-specific information (characters, plot, world, genre)
- Identify writing style implications (conversational, literary, accessible, etc.)
- Consider target audience alignment (children, young_adult, adult)
- Determine content priority (essential, important, supporting)
"""


class SimpleMetadataGenerator(MetadataGenerator):
    """
    Simple metadata generator that creates basic metadata without LLM analysis.
    
    Useful for testing or when LLM analysis is not available.
    """
    
    def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """Generate basic metadata using heuristics."""
        
        # Basic analysis
        word_count = len(content.split())
        
        # Simple quality scoring based on length and structure
        quality_score = 50  # Default
        if word_count > 100:
            quality_score += 10
        if word_count > 500:
            quality_score += 10
        if any(marker in content.lower() for marker in ["#", "**", "```", "-"]):
            quality_score += 10  # Has formatting
        
        # Simple key concept extraction (most frequent meaningful words)
        words = re.findall(r'\b[A-Za-z]{4,}\b', content.lower())
        word_freq = {}
        for word in words:
            if word not in ["that", "with", "have", "this", "will", "from", "they", "been"]:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        key_concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        concepts = [word for word, freq in key_concepts if freq > 1]
        
        return {
            "content_type": content_type if content_type in ["research", "character", "world", "scene", "style", "chapter", "plan"] else "unknown",
            "content_subtype": "basic_analysis",
            "chapter_relevance": "all",
            "priority": "supporting",
            "quality_score": min(100, quality_score),
            "key_concepts": concepts or ["general"],
            "usage_context": "reference"
        }


# === FACTORY FUNCTION ===

def create_metadata_generator(generator_type: str = "llm", **kwargs) -> MetadataGenerator:
    """
    Factory function to create metadata generator instances.
    
    Args:
        generator_type: Type of generator ("llm" or "simple")
        **kwargs: Additional configuration for the generator
        
    Returns:
        Configured MetadataGenerator instance
    """
    if generator_type == "llm":
        llm_client = kwargs.get("llm_client")
        if not llm_client:
            raise ValueError("llm_client is required for LLM metadata generator")
        
        config = kwargs.get("config", MetadataPromptConfig())
        return LLMMetadataGenerator(llm_client, config)
        
    elif generator_type == "simple":
        return SimpleMetadataGenerator()
    else:
        raise ValueError(f"Unknown generator type: {generator_type}")


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    # Example usage (requires actual LLM client)
    
    # Simple generator example
    simple_gen = create_metadata_generator("simple")
    
    example_content = """
    # Baba Yaga Research Notes
    
    Baba Yaga is a famous figure in Slavic folklore, known for her role as both helper and hindrance. 
    She lives in a hut on chicken legs and tests travelers who seek her wisdom.
    
    **Key Characteristics:**
    - Tests visitors with challenges
    - Rewards the pure of heart
    - Symbol of wisdom through trials
    """
    
    metadata = simple_gen.generate_metadata(example_content, "research", "peter_forest_001")
    print("Generated Metadata:")
    print(json.dumps(metadata, indent=2))