#!/usr/bin/env python3
"""
ContentParser - Implementation with Concrete Parsers

Provides content parsing capabilities for different formats used in the book generation pipeline.
Includes parsers for JSON, Markdown, and plain text with format normalization.

Key Features:
- Abstract interface for pluggable parsing strategies
- JSON parser for structured book data (models, blueprints, research)
- Markdown parser for narrative content (summaries, plans, chapters)
- Text parser for simple content normalization
- Configurable parsing options for different use cases
- References actual book model enums for consistency
"""

import json
import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Import actual book model enums for consistency
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
    from musequill.models.book.research import ResearchType
    from musequill.models.book.technology import TechnologyLevel
    from musequill.models.book.personality import PersonalityTrait
    from musequill.models.book.plot import PlotType
except ImportError as e:
    logging.warning(f"Could not import book model enums: {e}")
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
    PaceType = None
    ToneType = None
    ResearchType = None
    TechnologyType = None
    PersonalityType = None
    PlotType = None


logger = logging.getLogger(__name__)


@dataclass
class ParsedContent:
    """Container for parsed content with metadata about parsing."""
    content: str
    original_format: str
    parsed_format: str
    parsing_notes: List[str]
    metadata_extracted: Dict[str, Any]


class ContentParser(ABC):
    """Abstract interface for content parsing modules."""
    
    @abstractmethod
    def parse_content(self, raw_content: str, content_format: str) -> str:
        """
        Parse and normalize content from various formats.
        
        Args:
            raw_content: Original content string
            content_format: Format type (json|markdown|text)
            
        Returns:
            Parsed and normalized content string
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, raw_content: str, content_format: str) -> Dict[str, Any]:
        """
        Extract structured metadata from content if available.
        
        Args:
            raw_content: Original content string
            content_format: Format type
            
        Returns:
            Dictionary of extracted metadata
        """
        pass


class BookContentParser(ContentParser):
    """
    Concrete implementation for parsing book-related content.
    
    Handles JSON (book models, blueprints), Markdown (summaries, plans), 
    and text content used in the book generation pipeline.
    """
    
    def __init__(self, preserve_structure: bool = True, extract_key_concepts: bool = True):
        """
        Initialize parser with configuration options.
        
        Args:
            preserve_structure: Whether to maintain formatting structure in output
            extract_key_concepts: Whether to extract key concepts for metadata
        """
        self.preserve_structure = preserve_structure
        self.extract_key_concepts = extract_key_concepts
        
        # Patterns for content analysis
        self.markdown_patterns = {
            'headers': re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE),
            'bold': re.compile(r'\*\*(.+?)\*\*'),
            'italic': re.compile(r'\*(.+?)\*'),
            'code_blocks': re.compile(r'```[\s\S]*?```'),
            'inline_code': re.compile(r'`([^`]+)`'),
            'links': re.compile(r'\[([^\]]+)\]\([^\)]+\)'),
            'lists': re.compile(r'^[\s]*[-\*\+]\s+(.+)$', re.MULTILINE)
        }
        
        logger.info(f"BookContentParser initialized (preserve_structure={preserve_structure})")
    
    def _get_enum_values_list(self, enum_class) -> List[str]:
        """Get list of enum values for validation and detection."""
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
    
    def _detect_enum_value_in_text(self, text: str, enum_class, case_sensitive: bool = False) -> Optional[str]:
        """Detect if any enum values appear in the text."""
        if enum_class is None:
            return None
        
        enum_values = self._get_enum_values_list(enum_class)
        text_to_search = text if case_sensitive else text.lower()
        
        for value in enum_values:
            search_value = value if case_sensitive else value.lower()
            if search_value in text_to_search:
                return value
        
        return None
    
    def parse_content(self, raw_content: str, content_format: str) -> str:
        """
        Parse content based on detected format.
        
        Args:
            raw_content: Original content string
            content_format: Format type (json|markdown|text)
            
        Returns:
            Parsed and normalized content string
        """
        try:
            if content_format == "json":
                return self._parse_json_content(raw_content)
            elif content_format == "markdown":
                return self._parse_markdown_content(raw_content)
            else:
                return self._parse_text_content(raw_content)
                
        except Exception as e:
            logger.warning(f"Parsing failed for format {content_format}: {e}")
            return self._parse_text_content(raw_content)  # Fallback to text parsing
    
    def extract_metadata(self, raw_content: str, content_format: str) -> Dict[str, Any]:
        """
        Extract metadata from content based on format.
        
        Args:
            raw_content: Original content string
            content_format: Format type
            
        Returns:
            Dictionary of extracted metadata
        """
        metadata = {
            "word_count": len(raw_content.split()),
            "character_count": len(raw_content),
            "format": content_format
        }
        
        try:
            if content_format == "json":
                metadata.update(self._extract_json_metadata(raw_content))
            elif content_format == "markdown":
                metadata.update(self._extract_markdown_metadata(raw_content))
            else:
                metadata.update(self._extract_text_metadata(raw_content))
                
        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")
        
        return metadata
    
    # === JSON PARSING ===
    
    def _parse_json_content(self, raw_content: str) -> str:
        """Parse JSON content into readable text format."""
        try:
            data = json.loads(raw_content.strip())
            return self._json_to_readable_text(data)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON content: {e}")
            return raw_content
    
    def _json_to_readable_text(self, data: Any, prefix: str = "") -> str:
        """Convert JSON structure to readable text format."""
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._json_to_readable_text(value, prefix + "  "))
                else:
                    lines.append(f"{prefix}{key}: {value}")
            return "\n".join(lines)
        
        elif isinstance(data, list):
            lines = []
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}Item {i+1}:")
                    lines.append(self._json_to_readable_text(item, prefix + "  "))
                else:
                    lines.append(f"{prefix}- {item}")
            return "\n".join(lines)
        
        else:
            return str(data)
    
    def _extract_json_metadata(self, raw_content: str) -> Dict[str, Any]:
        """Extract metadata from JSON content using actual book model enums."""
        metadata = {}
        
        try:
            data = json.loads(raw_content.strip())
            
            # Extract common book-related fields
            if isinstance(data, dict):
                # Book model fields
                if "book" in data:
                    book_data = data["book"]
                    metadata["title"] = book_data.get("title")
                    metadata["author"] = book_data.get("author")
                    metadata["length"] = book_data.get("length")
                    
                    # Detect book length category using actual BookLength enum
                    if "length" in book_data and BookLength:
                        detected_length = self._detect_book_length_category(book_data["length"])
                        if detected_length:
                            metadata["book_length_category"] = detected_length
                
                # Genre information using actual GenreType enum
                if "genre" in data:
                    genre_data = data["genre"]
                    if "primary" in genre_data:
                        primary_type = genre_data["primary"].get("type")
                        if primary_type and GenreType:
                            # Validate against actual enum
                            valid_genres = self._get_enum_values_list(GenreType)
                            if primary_type.upper() in [g.upper() for g in valid_genres]:
                                metadata["primary_genre"] = primary_type
                    
                    if "sub" in genre_data:
                        sub_type = genre_data["sub"].get("type")
                        if sub_type and SubGenreType:
                            # Validate against actual enum
                            valid_subgenres = self._get_enum_values_list(SubGenreType)
                            if sub_type.upper() in [s.upper() for s in valid_subgenres]:
                                metadata["sub_genre"] = sub_type
                
                # Audience information using actual AudienceType enum
                if "audience" in data:
                    audience_data = data["audience"]
                    audience_type = audience_data.get("type")
                    if audience_type and AudienceType:
                        valid_audiences = self._get_enum_values_list(AudienceType)
                        if audience_type.upper() in [a.upper() for a in valid_audiences]:
                            metadata["target_audience"] = audience_type
                    metadata["age_range"] = audience_data.get("age")
                
                # Writing style using actual WritingStyle enum
                if "writing_style" in data:
                    style = data["writing_style"]
                    if WritingStyle:
                        valid_styles = self._get_enum_values_list(WritingStyle)
                        if style.upper() in [s.upper() for s in valid_styles]:
                            metadata["writing_style"] = style
                
                # Story structure using actual StoryStructure enum
                if "structure" in data:
                    structure_data = data["structure"]
                    structure_type = structure_data.get("type")
                    if structure_type and StoryStructure:
                        valid_structures = self._get_enum_values_list(StoryStructure)
                        if structure_type.upper() in [s.upper() for s in valid_structures]:
                            metadata["story_structure"] = structure_type
                
                # World type using actual WorldType enum
                if "world" in data:
                    world_data = data["world"]
                    world_type = world_data.get("type")
                    if world_type and WorldType:
                        valid_worlds = self._get_enum_values_list(WorldType)
                        if world_type.upper() in [w.upper() for w in valid_worlds]:
                            metadata["world_type"] = world_type
                
                # Conflict type using actual ConflictType enum
                if "conflict" in data:
                    conflict_data = data["conflict"]
                    conflict_type = conflict_data.get("type")
                    if conflict_type and ConflictType:
                        valid_conflicts = self._get_enum_values_list(ConflictType)
                        if conflict_type.upper() in [c.upper() for c in valid_conflicts]:
                            metadata["conflict_type"] = conflict_type
                
                # POV type using actual POVType enum
                if "pov" in data:
                    pov_data = data["pov"]
                    pov_type = pov_data.get("type")
                    if pov_type and NarrativePOV:
                        valid_povs = self._get_enum_values_list(NarrativePOV)
                        if pov_type.upper() in [p.upper() for p in valid_povs]:
                            metadata["pov_type"] = pov_type
                
                # Pace type using actual PaceType enum
                if "pace" in data:
                    pace_data = data["pace"]
                    pace_type = pace_data.get("type")
                    if pace_type and PacingStyle:
                        valid_paces = self._get_enum_values_list(PacingStyle)
                        if pace_type.upper() in [p.upper() for p in valid_paces]:
                            metadata["pace_type"] = pace_type
                
                # Tone type using actual ToneType enum
                if "tone" in data:
                    tone_data = data["tone"]
                    tone_type = tone_data.get("type")
                    if tone_type and ToneStyle:
                        valid_tones = self._get_enum_values_list(ToneStyle)
                        if tone_type.upper() in [t.upper() for t in valid_tones]:
                            metadata["tone_type"] = tone_type
                
                # Research topics using actual ResearchType enum
                if "research" in data:
                    research_data = data["research"]
                    if isinstance(research_data, list) and ResearchType:
                        valid_research_types = self._get_enum_values_list(ResearchType)
                        research_topics = []
                        for r in research_data:
                            if isinstance(r, dict) and "type" in r:
                                r_type = r["type"]
                                if r_type.upper() in [rt.upper() for rt in valid_research_types]:
                                    research_topics.append(r_type)
                        if research_topics:
                            metadata["research_topics"] = research_topics
                
                # Chapter information (for blueprints)
                if any(key.startswith("phase") for key in data.keys()):
                    metadata["content_subtype"] = "blueprint"
                    metadata["phases"] = list(data.keys())
                
        except Exception as e:
            logger.warning(f"JSON metadata extraction failed: {e}")
        
        return metadata
    
    def _detect_book_length_category(self, length_str: str) -> Optional[str]:
        """Detect book length category from length string using actual BookLength enum."""
        if not BookLength or not length_str:
            return None
        
        # Extract word count numbers from string like "40,000-60,000 words"
        numbers = re.findall(r'[\d,]+', length_str.replace(',', ''))
        if not numbers:
            return None
        
        try:
            # Use the first number as representative word count
            word_count = int(numbers[0])
            
            # Match against actual BookLength enum values and their word count ranges
            # This would need to be implemented based on your BookLength enum structure
            # For now, return the detected pattern
            for length_type in self._get_enum_values_list(BookLength):
                # This is a simplified detection - you might want to implement
                # proper word count range checking based on your BookLength enum
                if length_type.lower() in length_str.lower():
                    return length_type
            
            # Simple word count based detection
            if word_count < 1000:
                return "flash_fiction" if "FLASH_FICTION" in self._get_enum_values_list(BookLength) else None
            elif word_count < 7500:
                return "short_story" if "SHORT_STORY" in self._get_enum_values_list(BookLength) else None
            elif word_count < 40000:
                return "novella" if "NOVELLA" in self._get_enum_values_list(BookLength) else None
            elif word_count < 90000:
                return "standard_novel" if "STANDARD_NOVEL" in self._get_enum_values_list(BookLength) else None
            else:
                return "long_novel" if "LONG_NOVEL" in self._get_enum_values_list(BookLength) else None
                
        except (ValueError, IndexError):
            return None
    
    # === MARKDOWN PARSING ===
    
    def _parse_markdown_content(self, raw_content: str) -> str:
        """Parse Markdown content with optional structure preservation."""
        if not self.preserve_structure:
            return self._strip_markdown_formatting(raw_content)
        else:
            return self._normalize_markdown_structure(raw_content)
    
    def _strip_markdown_formatting(self, content: str) -> str:
        """Remove all Markdown formatting, keeping only text content."""
        # Remove code blocks first
        content = self.markdown_patterns['code_blocks'].sub('', content)
        
        # Remove headers (keep text)
        content = self.markdown_patterns['headers'].sub(r'\1', content)
        
        # Remove bold/italic formatting
        content = self.markdown_patterns['bold'].sub(r'\1', content)
        content = self.markdown_patterns['italic'].sub(r'\1', content)
        
        # Remove inline code
        content = self.markdown_patterns['inline_code'].sub(r'\1', content)
        
        # Remove links (keep text)
        content = self.markdown_patterns['links'].sub(r'\1', content)
        
        # Clean up lists
        content = self.markdown_patterns['lists'].sub(r'\1', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        return content.strip()
    
    def _normalize_markdown_structure(self, content: str) -> str:
        """Normalize Markdown structure while preserving readability."""
        lines = content.split('\n')
        normalized_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                normalized_lines.append('')
                continue
            
            # Convert headers to structured format
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2)
                normalized_lines.append(f"{'  ' * (level-1)}SECTION: {text}")
                continue
            
            # Convert list items
            list_match = re.match(r'^[\s]*[-\*\+]\s+(.+)$', line)
            if list_match:
                normalized_lines.append(f"- {list_match.group(1)}")
                continue
            
            # Regular text
            normalized_lines.append(line)
        
        return '\n'.join(normalized_lines)
    
    def _extract_markdown_metadata(self, raw_content: str) -> Dict[str, Any]:
        """Extract metadata from Markdown content using actual book model enums."""
        metadata = {}
        
        # Extract headers
        headers = self.markdown_patterns['headers'].findall(raw_content)
        if headers:
            metadata["headers"] = headers
            metadata["section_count"] = len(headers)
            
            # Try to detect content type from headers using book model context
            header_text = ' '.join(headers).lower()
            
            # Detect content subtype based on headers and book model knowledge
            if any(word in header_text for word in ['chapter', 'scene', 'character']):
                metadata["content_subtype"] = "narrative"
            elif any(word in header_text for word in ['plan', 'outline', 'strategy']):
                metadata["content_subtype"] = "planning"
            elif any(word in header_text for word in ['research', 'folklore', 'mythology']):
                metadata["content_subtype"] = "research"
            
            # Detect book model elements in headers
            self._detect_book_elements_in_text(header_text, metadata)
        
        # Extract key concepts if enabled
        if self.extract_key_concepts:
            concepts = self._extract_key_concepts_from_text(raw_content)
            if concepts:
                metadata["key_concepts"] = concepts[:7]  # Limit to 7 as per schema
        
        # Count structural elements
        metadata["bold_phrases"] = len(self.markdown_patterns['bold'].findall(raw_content))
        metadata["italic_phrases"] = len(self.markdown_patterns['italic'].findall(raw_content))
        metadata["code_blocks"] = len(self.markdown_patterns['code_blocks'].findall(raw_content))
        metadata["links"] = len(self.markdown_patterns['links'].findall(raw_content))
        
        # Estimate reading complexity aligned with book model audience types
        sentences = re.split(r'[.!?]+', raw_content)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Use actual AudienceType enum to determine complexity alignment
        if avg_sentence_length < 10:
            metadata["complexity_level"] = "simple"
            # Suggest this aligns with children's content
            if AudienceType and "CHILDREN" in self._get_enum_values_list(AudienceType):
                metadata["suggested_audience"] = "children"
        elif avg_sentence_length < 20:
            metadata["complexity_level"] = "moderate"
            # Suggest this aligns with young adult content
            if AudienceType and "YOUNG_ADULT" in self._get_enum_values_list(AudienceType):
                metadata["suggested_audience"] = "young_adult"
        else:
            metadata["complexity_level"] = "complex"
            # Suggest this aligns with adult content
            if AudienceType and "ADULT" in self._get_enum_values_list(AudienceType):
                metadata["suggested_audience"] = "adult"
        
        # Detect book model elements in the full content
        self._detect_book_elements_in_text(raw_content.lower(), metadata)
        
        return metadata
    
    def _detect_book_elements_in_text(self, text: str, metadata: Dict[str, Any]) -> None:
        """Detect book model elements in text and add to metadata."""
        
        # Detect writing style elements
        if WritingStyle:
            detected_style = self._detect_enum_value_in_text(text, WritingStyle)
            if detected_style:
                metadata["detected_writing_style"] = detected_style
        
        # Detect world type elements
        if WorldType:
            detected_world = self._detect_enum_value_in_text(text, WorldType)
            if detected_world:
                metadata["detected_world_type"] = detected_world
        
        # Detect conflict type elements
        if ConflictType:
            detected_conflict = self._detect_enum_value_in_text(text, ConflictType)
            if detected_conflict:
                metadata["detected_conflict_type"] = detected_conflict
        
        # Detect tone elements
        if ToneStyle:
            detected_tone = self._detect_enum_value_in_text(text, ToneStyle)
            if detected_tone:
                metadata["detected_tone_type"] = detected_tone
        
        # Detect pace indicators
        if PacingStyle:
            # Check for pace-related keywords
            pace_keywords = {
                "slow": ["slow", "leisurely", "gradual", "gentle"],
                "medium": ["steady", "moderate", "balanced"],
                "fast": ["fast", "rapid", "quick", "intense", "urgent"]
            }
            
            for pace_type in self._get_enum_values_list(PacingStyle):
                pace_lower = pace_type.lower()
                if pace_lower in pace_keywords:
                    if any(keyword in text for keyword in pace_keywords[pace_lower]):
                        metadata["detected_pace_type"] = pace_type
                        break
    
    # === TEXT PARSING ===
    
    def _parse_text_content(self, raw_content: str) -> str:
        """Parse plain text content with basic normalization."""
        # Basic text cleaning
        content = raw_content.strip()
        
        # Normalize whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Multiple newlines to double
        content = re.sub(r'[ \t]+', ' ', content)  # Multiple spaces to single
        
        # Remove common formatting artifacts
        content = re.sub(r'^\s*[-=]{3,}\s*$', '', content, flags=re.MULTILINE)  # Separator lines
        
        return content
    
    def _extract_text_metadata(self, raw_content: str) -> Dict[str, Any]:
        """Extract metadata from plain text content using book model awareness."""
        metadata = {}
        
        # Basic text statistics
        sentences = re.split(r'[.!?]+', raw_content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        metadata["sentence_count"] = len(sentences)
        metadata["paragraph_count"] = len([p for p in raw_content.split('\n\n') if p.strip()])
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            metadata["avg_sentence_length"] = round(avg_sentence_length, 1)
            
            # Estimate complexity aligned with book model audience types
            if avg_sentence_length < 8:
                metadata["complexity_level"] = "simple"
                if AudienceType and "CHILDREN" in self._get_enum_values_list(AudienceType):
                    metadata["suggested_audience"] = "children"
            elif avg_sentence_length < 15:
                metadata["complexity_level"] = "moderate"
                if AudienceType and "YOUNG_ADULT" in self._get_enum_values_list(AudienceType):
                    metadata["suggested_audience"] = "young_adult"
            else:
                metadata["complexity_level"] = "complex"
                if AudienceType and "ADULT" in self._get_enum_values_list(AudienceType):
                    metadata["suggested_audience"] = "adult"
        
        # Extract key concepts if enabled
        if self.extract_key_concepts:
            concepts = self._extract_key_concepts_from_text(raw_content)
            if concepts:
                metadata["key_concepts"] = concepts[:7]
        
        # Detect book model elements in text
        self._detect_book_elements_in_text(raw_content.lower(), metadata)
        
        return metadata
    
    # === UTILITY METHODS ===
    
    def _extract_key_concepts_from_text(self, text: str) -> List[str]:
        """Extract key concepts/terms from text using simple heuristics."""
        # Remove markdown formatting for better concept extraction
        clean_text = self._strip_markdown_formatting(text)
        
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'our', 'their', 'what', 'which', 'who', 'when',
            'where', 'why', 'how', 'not', 'no', 'yes', 'all', 'some', 'any', 'each', 'every'
        }
        
        # Extract words, prioritizing capitalized terms and longer words
        words = re.findall(r'\b[A-Za-z]+\b', clean_text)
        
        # Count word frequencies, giving bonus to capitalized words
        word_scores = {}
        for word in words:
            word_lower = word.lower()
            if word_lower not in stop_words and len(word) > 2:
                score = 1
                if word[0].isupper() and len(word) > 3:  # Capitalized words get bonus
                    score = 2
                if len(word) > 6:  # Longer words get bonus
                    score += 1
                
                word_scores[word_lower] = word_scores.get(word_lower, 0) + score
        
        # Return top concepts sorted by score
        sorted_concepts = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, score in sorted_concepts[:10]]  # Top 10 concepts


class SimpleContentParser(ContentParser):
    """
    Simple content parser that performs minimal processing.
    
    Useful for cases where you want to preserve content exactly as-is
    or when dealing with already processed content.
    """
    
    def parse_content(self, raw_content: str, content_format: str) -> str:
        """Return content with minimal normalization."""
        return raw_content.strip()
    
    def extract_metadata(self, raw_content: str, content_format: str) -> Dict[str, Any]:
        """Extract only basic metadata."""
        return {
            "word_count": len(raw_content.split()),
            "character_count": len(raw_content),
            "format": content_format
        }


# === FACTORY FUNCTION ===

def create_content_parser(parser_type: str = "book", **kwargs) -> ContentParser:
    """
    Factory function to create content parser instances.
    
    Args:
        parser_type: Type of parser ("book" or "simple")
        **kwargs: Additional configuration for the parser
        
    Returns:
        Configured ContentParser instance
    """
    if parser_type == "book":
        return BookContentParser(**kwargs)
    elif parser_type == "simple":
        return SimpleContentParser()
    else:
        raise ValueError(f"Unknown parser type: {parser_type}")


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    # Example usage of the content parser
    
    # Create parser
    parser = create_content_parser("book", preserve_structure=True, extract_key_concepts=True)
    
    # Example JSON content (book model)
    json_content = '''
    {
        "book": {
            "title": "The Enchanted Forest of Peter",
            "author": "Joseph Campbell", 
            "length": "40,000-60,000 words"
        },
        "genre": {
            "primary": {"type": "children"},
            "sub": {"type": "fantasy"}
        },
        "audience": {"type": "children", "age": "7-12"}
    }
    '''
    
    # Example Markdown content
    markdown_content = '''
    # Chapter Planning for Peter's Adventure
    
    ## Character Development
    - **Peter**: Curious bunny who grows in courage
    - *Baba Yaga*: Wise but testing mentor figure
    
    ## Key Scenes  
    1. Forest entrance - wonder and trepidation
    2. First encounter with magical creatures
    3. Meeting Baba Yaga - the crucial test
    
    The story should maintain a **whimsical tone** while exploring themes of `courage` and `self-discovery`.
    '''
    
    # Parse and extract metadata
    print("=== JSON PARSING ===")
    parsed_json = parser.parse_content(json_content, "json")
    json_metadata = parser.extract_metadata(json_content, "json")
    print("Parsed JSON:")
    print(parsed_json[:200] + "...")
    print(f"Metadata: {json_metadata}")
    
    print("\n=== MARKDOWN PARSING ===")
    parsed_md = parser.parse_content(markdown_content, "markdown") 
    md_metadata = parser.extract_metadata(markdown_content, "markdown")
    print("Parsed Markdown:")
    print(parsed_md[:200] + "...")
    print(f"Metadata: {md_metadata}")