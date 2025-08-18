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


logger = logging.getLogger(__name__)


class ContentTypeHint(Enum):
    """Content type hints for better LLM analysis."""
    RESEARCH = "research"
    CHARACTER = "character"
    SUMMARY = "summary"
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
            # CORE REQUIRED FIELDS
            "content_type": {
                "values": "research|character|world|scene|style|chapter|plan|summary",
                "description": "Primary classification of content for organizational purposes",
                "required": True
            },
            "content_subtype": {
                "values": "string",
                "description": "Specific subcategory or detailed description of content type",
                "required": True
            },
            "chapter_relevance": {
                "values": "[1, 3, 5] (array of integers) OR \"all\" (string) for entire book",
                "description": "Specific chapter numbers as JSON array, or 'all' string for entire book",
                "required": True
            },
            "priority": {
                "values": "essential|important|supporting",
                "description": "Importance level for book completion - essential=critical, important=helpful, supporting=nice-to-have",
                "required": True
            },
            "quality_score": {
                "values": "0-100",
                "description": "Quality assessment score - higher means more useful/complete/accurate",
                "required": True
            },
            "key_concepts": {
                "values": "[\"term1\", \"term2\", ...] - array of strings, max 7 items",
                "description": "Most important concepts, terms, or themes from this content as a JSON array",
                "required": True
            },
            "usage_context": {
                "values": "chapter_writing|planning|reference|background",
                "description": "How this content should be used - chapter_writing=direct use in chapters, planning=story planning, reference=lookup, background=context",
                "required": True
            },
            
            # OPTIONAL BOOK MODEL FIELDS (include when applicable)
            "genre_primary": {
                "values": f"{self._get_enum_values(GenreType)}",
                "description": "Primary genre classification that this content best fits",
                "required": False
            },
            "genre_sub": {
                "values": f"{self._get_enum_values(SubGenreType)}",
                "description": "Specific subgenre for more precise classification",
                "required": False
            },
            "audience_type": {
                "values": f"{self._get_enum_values(AudienceType)}",
                "description": "Target audience age group and reading level",
                "required": False
            },
            "writing_style": {
                "values": f"{self._get_enum_values(WritingStyle)}",
                "description": "Writing approach and voice style that matches this content",
                "required": False
            },
            "story_structure": {
                "values": f"{self._get_enum_values(StoryStructure)}",
                "description": "Story structure elements or patterns present in this content",
                "required": False
            },
            "world_type": {
                "values": f"{self._get_enum_values(WorldType)}",
                "description": "Type of fictional world or setting framework",
                "required": False
            },
            "conflict_type": {
                "values": f"{self._get_enum_values(ConflictType)}",
                "description": "Primary type of conflict or tension present",
                "required": False
            },
            "pov_type": {
                "values": f"{self._get_enum_values(NarrativePOV)}",
                "description": "Point of view style that matches this content",
                "required": False
            },
            "pace_type": {
                "values": f"{self._get_enum_values(PacingStyle)}",
                "description": "Pacing style or tempo that fits this content",
                "required": False
            },
            "tone_type": {
                "values": f"{self._get_enum_values(ToneStyle)}",
                "description": "Emotional tone or mood that characterizes this content",
                "required": False
            }
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
            ContentTypeHint.SUMMARY: self._get_summary_analysis_prompt(),
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
    
    async def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
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
            raw_metadata = await self._generate_llm_metadata(content, content_hint, book_id)
            
            # Validate and clean metadata
            validated_metadata = self._validate_and_clean_metadata(raw_metadata)
            
            return validated_metadata
            
        except Exception as e:
            logger.error(f"Metadata generation failed: {e}")
            raise
    
    async def _generate_llm_metadata(self, content: str, content_hint: ContentTypeHint, book_id: str) -> Dict[str, Any]:
        """Generate metadata using LLM with structured prompting."""
        
        # Build the analysis prompt
        analysis_prompt = self.analysis_prompts[content_hint]
        
        # Create the complete prompt
        prompt = self._build_metadata_prompt(content, analysis_prompt, book_id)
        
        # Execute LLM call with retries
        for attempt in range(self.config.retry_attempts):
            try:
                response = await self._call_llm(prompt)
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
You must generate a JSON object with these fields. Include ALL required fields and any applicable optional fields.

{self._format_schema_for_prompt()}

**CONTENT TYPE SPECIFIC ANALYSIS:**
{analysis_prompt}

**BOOK CONTEXT:**
Book ID: {book_id}

**CONTENT TO ANALYZE:**
{content_sample}

**RESPONSE FORMAT:**
Respond with ONLY a valid JSON object that follows the schema exactly. No additional text.

**COMPLETE BOOK-LEVEL METADATA EXAMPLES:**

**Example 1 - Children's Fantasy Adventure:**
{{
    "content_type": "plan",
    "content_subtype": "complete_book_outline",
    "chapter_relevance": "all",
    "priority": "essential",
    "quality_score": 92,
    "key_concepts": ["magical_forest", "talking_animals", "friendship", "courage", "environmental_protection", "self_discovery", "adventure"],
    "usage_context": "planning",
    "genre_primary": "fantasy",
    "genre_sub": "children_fantasy",
    "audience_type": "children",
    "writing_style": "accessible",
    "story_structure": "heros_journey",
    "world_type": "fantasy",
    "conflict_type": "person_vs_supernatural",
    "pov_type": "third_person_limited",
    "pace_type": "medium",
    "tone_type": "whimsical"
}}

**Example 2 - Young Adult Contemporary Drama:**
{{
    "content_type": "character",
    "content_subtype": "protagonist_development_arc",
    "chapter_relevance": [1, 3, 5, 7, 9, 12, 15],
    "priority": "essential",
    "quality_score": 88,
    "key_concepts": ["identity_crisis", "family_secrets", "coming_of_age", "social_pressure", "authentic_self"],
    "usage_context": "chapter_writing",
    "genre_primary": "contemporary_fiction",
    "audience_type": "young_adult",
    "writing_style": "conversational",
    "story_structure": "three_act",
    "world_type": "contemporary",
    "conflict_type": "person_vs_society",
    "pov_type": "first_person",
    "pace_type": "medium",
    "tone_type": "serious"
}}

**CRITICAL REQUIREMENTS:**
- Always include ALL 7 required core fields: content_type, content_subtype, chapter_relevance, priority, quality_score, key_concepts, usage_context
- Add optional book model fields when applicable to the content
- Use lists for key_concepts (max 7 items), chapter_relevance (when specific chapters), and any multi-value fields
- Ensure chapter_relevance is either "all" for book-wide content or [list of chapter numbers]
- Quality_score must be 0-100 integer
- All enum values must match exactly (case-sensitive)

Generate the metadata now following these examples:"""
        
        return prompt
    
    def _format_schema_for_prompt(self) -> str:
        """Format the metadata schema for clear LLM instructions."""
        formatted_fields = []
        
        for field_name, field_info in self.metadata_schema.items():
            required_text = "**REQUIRED**" if field_info["required"] else "*optional*"
            
            # Add special formatting for list fields
            list_indicator = ""
            if field_name == "key_concepts":
                list_indicator = " (LIST of up to 7 strings)"
            elif field_name == "chapter_relevance":
                list_indicator = " (LIST of integers or 'all')"
            
            formatted_fields.append(
                f"  \"{field_name}\"{list_indicator}: {required_text}\n"
                f"    - Values: {field_info['values']}\n"
                f"    - Purpose: {field_info['description']}"
            )
        
        return "\n\n".join(formatted_fields)
    
    async def _call_llm(self, prompt: str) -> str:
        """Execute LLM call with configured parameters."""
        try:
            # This assumes your LLM client has a generate method
            # Adjust based on your actual LLM client interface
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
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
        """
        Validate metadata against schema and clean up values using book model enums.
        
        Enhanced validation features:
        - Field existence checks with .get() for all fields
        - Robust list handling for key_concepts and chapter_relevance
        - Support for comma-separated strings converted to lists
        - Single-value field cleaning for enum fields (handles accidental lists)
        - Required field validation with fallback defaults
        - Type coercion and range validation for numeric fields
        """
        
        # Identify required fields from schema
        required_fields = [field for field, info in self.metadata_schema.items() if info["required"]]
        
        # Check all required fields are present
        missing_fields = [field for field in required_fields if field not in raw_metadata]
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}. Using defaults.")
        
        # === CORE REQUIRED FIELD VALIDATION ===
        cleaned_metadata = {}
        
        # content_type validation
        valid_content_types = ["summary", "research", "character", "world", "scene", "style", "chapter", "plan"]
        content_type = raw_metadata.get("content_type", "unknown")
        if str(content_type).lower() not in valid_content_types:
            logger.warning(f"Invalid content_type: {content_type}, defaulting to 'unknown'")
            cleaned_metadata["content_type"] = "unknown"
        else:
            cleaned_metadata["content_type"] = str(content_type).lower()
        
        # content_subtype - keep as string
        cleaned_metadata["content_subtype"] = str(raw_metadata.get("content_subtype", "unspecified"))
        
        # chapter_relevance validation (handles lists, strings, and mixed formats)
        chapter_rel = raw_metadata.get("chapter_relevance", "all")
        
        if isinstance(chapter_rel, list):
            # Validate list of integers or strings
            cleaned_chapters = []
            for ch in chapter_rel:
                if isinstance(ch, int) and 1 <= ch <= 50:  # Reasonable chapter range
                    cleaned_chapters.append(ch)
                elif isinstance(ch, str):
                    # Handle string representations of numbers or special values
                    if ch.lower() in ['all', 'entire_book', 'whole_book']:
                        cleaned_metadata["chapter_relevance"] = "all"
                        break
                    try:
                        ch_num = int(ch)
                        if 1 <= ch_num <= 50:
                            cleaned_chapters.append(ch_num)
                    except ValueError:
                        continue  # Skip invalid chapter references
            
            # Only set list if we didn't already set "all" and have valid chapters
            if "chapter_relevance" not in cleaned_metadata:
                if cleaned_chapters:
                    cleaned_metadata["chapter_relevance"] = sorted(list(set(cleaned_chapters)))  # Remove duplicates and sort
                else:
                    cleaned_metadata["chapter_relevance"] = "all"
                    
        elif isinstance(chapter_rel, str):
            if chapter_rel.lower() in ["all", "entire_book", "whole_book"]:
                cleaned_metadata["chapter_relevance"] = "all"
            else:
                # Try to parse comma-separated chapter numbers
                try:
                    chapters = [int(ch.strip()) for ch in chapter_rel.split(',') if ch.strip().isdigit()]
                    valid_chapters = [ch for ch in chapters if 1 <= ch <= 50]
                    if valid_chapters:
                        cleaned_metadata["chapter_relevance"] = sorted(list(set(valid_chapters)))
                    else:
                        cleaned_metadata["chapter_relevance"] = "all"
                except:
                    cleaned_metadata["chapter_relevance"] = "all"
        elif isinstance(chapter_rel, int) and 1 <= chapter_rel <= 50:
            cleaned_metadata["chapter_relevance"] = [chapter_rel]
        else:
            cleaned_metadata["chapter_relevance"] = "all"
        
        # priority validation
        valid_priorities = ["essential", "important", "supporting"]
        priority = raw_metadata.get("priority", "important")
        if priority not in valid_priorities:
            cleaned_metadata["priority"] = "important"
        else:
            cleaned_metadata["priority"] = priority
        
        # quality_score validation
        try:
            score = float(raw_metadata.get("quality_score", 50))
            cleaned_metadata["quality_score"] = max(0, min(100, int(score)))
        except (ValueError, TypeError):
            cleaned_metadata["quality_score"] = 50
        
        # key_concepts validation (handles lists, strings, and mixed formats)
        concepts = raw_metadata.get("key_concepts", [])
        clean_concepts = []
        
        if isinstance(concepts, list):
            # Handle list of concepts
            for concept in concepts[:7]:  # Limit to 7 concepts max
                if isinstance(concept, str) and concept.strip():
                    clean_concepts.append(concept.strip().lower())
                elif concept is not None:  # Handle non-string types
                    clean_concepts.append(str(concept).strip().lower())
        elif isinstance(concepts, str):
            # Handle comma-separated string of concepts
            concept_parts = [c.strip().lower() for c in concepts.split(',') if c.strip()]
            clean_concepts.extend(concept_parts[:7])
        
        # Ensure we have at least one concept
        if not clean_concepts:
            clean_concepts = ["general"]
        
        cleaned_metadata["key_concepts"] = clean_concepts
        
        # usage_context validation
        valid_contexts = ["chapter_writing", "planning", "reference", "background"]
        usage_context = raw_metadata.get("usage_context", "reference")
        if usage_context not in valid_contexts:
            cleaned_metadata["usage_context"] = "reference"
        else:
            cleaned_metadata["usage_context"] = usage_context
        
        # === BOOK MODEL ALIGNED FIELDS (Optional) ===
        
        # === OPTIONAL BOOK MODEL FIELDS (only include when applicable) ===
        
        # genre_primary validation (using actual GenreType enum)
        if "genre_primary" in raw_metadata or "genre" in raw_metadata:
            if GenreType:
                valid_genres = self._get_enum_values_list(GenreType)
                genre_value = raw_metadata.get("genre_primary", raw_metadata.get("genre", ""))
                cleaned_genre = self._clean_single_value_field(genre_value, valid_genres)
                if cleaned_genre != "unspecified":
                    cleaned_metadata["genre_primary"] = cleaned_genre
        
        # genre_sub validation (using actual SubGenreType enum)
        if "genre_sub" in raw_metadata:
            if SubGenreType:
                valid_subgenres = self._get_enum_values_list(SubGenreType)
                subgenre_value = raw_metadata["genre_sub"]
                cleaned_subgenre = self._clean_single_value_field(subgenre_value, valid_subgenres)
                if cleaned_subgenre != "unspecified":
                    cleaned_metadata["genre_sub"] = cleaned_subgenre
        
        # audience_type validation (using actual AudienceType enum)
        if "audience_type" in raw_metadata:
            if AudienceType:
                valid_audiences = self._get_enum_values_list(AudienceType)
                audience_value = raw_metadata["audience_type"]
                cleaned_audience = self._clean_single_value_field(audience_value, valid_audiences)
                if cleaned_audience != "unspecified":
                    cleaned_metadata["audience_type"] = cleaned_audience
        
        # writing_style validation (using actual WritingStyle enum)
        if "writing_style" in raw_metadata:
            if WritingStyle:
                valid_styles = self._get_enum_values_list(WritingStyle)
                style_value = raw_metadata["writing_style"]
                cleaned_style = self._clean_single_value_field(style_value, valid_styles)
                if cleaned_style != "unspecified":
                    cleaned_metadata["writing_style"] = cleaned_style
        
        # world_type validation (using actual WorldType enum)
        if "world_type" in raw_metadata or "world_building" in raw_metadata:
            if WorldType:
                valid_worlds = self._get_enum_values_list(WorldType)
                world_type = raw_metadata.get("world_type", raw_metadata.get("world_building", ""))
                if world_type in valid_worlds:
                    cleaned_metadata["world_type"] = world_type
        
        # conflict_type validation (using actual ConflictType enum)
        if "conflict_type" in raw_metadata:
            if ConflictType:
                valid_conflicts = self._get_enum_values_list(ConflictType)
                conflict_type = raw_metadata["conflict_type"]
                if conflict_type in valid_conflicts:
                    cleaned_metadata["conflict_type"] = conflict_type
        
        # pov_type validation (using actual NarrativePOV enum)
        if "pov_type" in raw_metadata:
            if NarrativePOV:
                valid_povs = self._get_enum_values_list(NarrativePOV)
                pov_type = raw_metadata["pov_type"]
                if pov_type in valid_povs:
                    cleaned_metadata["pov_type"] = pov_type
        
        # pace_type validation (using actual PacingStyle enum)
        if "pace_type" in raw_metadata:
            if PacingStyle:
                valid_paces = self._get_enum_values_list(PacingStyle)
                pace_type = raw_metadata["pace_type"]
                if pace_type in valid_paces:
                    cleaned_metadata["pace_type"] = pace_type
        
        # tone_type validation (using actual ToneStyle enum)
        if "tone_type" in raw_metadata:
            if ToneStyle:
                valid_tones = self._get_enum_values_list(ToneStyle)
                tone_type = raw_metadata["tone_type"]
                if tone_type in valid_tones:
                    cleaned_metadata["tone_type"] = tone_type
        
        # story_structure validation (using actual StoryStructure enum)
        if "story_structure" in raw_metadata or "story_structure_elements" in raw_metadata:
            if StoryStructure:
                valid_structures = self._get_enum_values_list(StoryStructure)
                story_structure = raw_metadata.get("story_structure", raw_metadata.get("story_structure_elements", ""))
                if story_structure in valid_structures:
                    cleaned_metadata["story_structure"] = story_structure
        
        # Final validation - ensure all required fields are present
        for field_name, field_info in self.metadata_schema.items():
            if field_info["required"] and field_name not in cleaned_metadata:
                # Provide defaults for missing required fields
                defaults = {
                    "content_type": "unknown",
                    "content_subtype": "unspecified",
                    "chapter_relevance": "all",
                    "priority": "important",
                    "quality_score": 50,
                    "key_concepts": ["general"],
                    "usage_context": "reference"
                }
                cleaned_metadata[field_name] = defaults.get(field_name, "unknown")
                logger.warning(f"Missing required field '{field_name}', using default: {cleaned_metadata[field_name]}")
        
        return cleaned_metadata
    
    def _clean_single_value_field(self, raw_value: Any, valid_values: List[str], default: str = "unspecified") -> str:
        """Clean a single-value field that might come as a list or other format."""
        if isinstance(raw_value, list) and raw_value:
            # If it's a list, take the first valid value
            for value in raw_value:
                if isinstance(value, str) and value in valid_values:
                    return value
            return default
        elif isinstance(raw_value, str) and raw_value in valid_values:
            return raw_value
        else:
            return default
    
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
            "plan": ContentTypeHint.PLAN,
            "summary": ContentTypeHint.SUMMARY
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
    def _get_summary_analysis_prompt(self) -> str:
        return """
For SUMMARY content, focus on:
- Identify summary scope (chapter, section, character arc, plot thread)
- Assess completeness and accuracy of key plot points (quality_score: 0-100)
- Extract main story elements and narrative beats (key_concepts)
- Determine which chapters or sections this summary covers (chapter_relevance)
- Consider summary purpose (quick reference, continuity check, progress tracking)
- Identify story structure elements (inciting incident, climax, resolution, etc.)
- Assess usefulness for maintaining story consistency (usage_context)
- Determine if summary captures character development and world-building elements
"""

class SimpleMetadataGenerator(MetadataGenerator):
    """
    Simple metadata generator that creates basic metadata without LLM analysis.
    
    Useful for testing or when LLM analysis is not available.
    """
    
    def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """Generate basic metadata using heuristics."""
        # Note: book_id not used in simple generator but kept for interface compatibility
        
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