#!/usr/bin/env python3
"""
Book DNA Generator Prompt Class

This class generates a compressed, essential "DNA" representation of a book project
that can be used as foundational context in all LLM interactions (200-300 tokens).
The DNA captures the unique essence of the book in a format that maintains consistency
across all writing phases while staying within context window limits.
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class BookDNAInputs:
    """
    Container for all information needed to generate accurate Book DNA.
    """
    # Core Book Model Data
    book_model: Dict[str, Any]  # The complete JSON book model
    
    # High-Level Planning Data
    book_blueprint: Dict[str, Any]  # The 7-phase blueprint JSON
    
    # Narrative Elements
    book_summary: str  # Marketing-style summary (MD content)
    
    # Research Context
    research_topics: List[Dict[str, Any]]  # Research areas and priorities
    
    # Unique Identifiers
    book_id: str  # Unique identifier for this book project
    
    # Optional Enhancement Data
    # comprehensive_plan: Optional[str] = None  # Detailed planning document
    # author_preferences: Optional[Dict[str, Any]] = None  # Author-specific preferences
    # market_positioning: Optional[Dict[str, Any]] = None  # Commercial considerations


class BookDNAPromptGenerator:
    """
    Generates compressed Book DNA that captures the essential essence of a book project
    in 200-300 tokens for use as foundational context in all LLM interactions.
    """
    
    # Template for the Book DNA structure
    DNA_TEMPLATE = """
    **BOOK DNA [ID: {book_id}]**
    
    **Core Identity**: "{title}" by {author} - {genre}/{subgenre} for {audience}
    **Narrative Engine**: {plot_type} using {structure} with {conflict} in {world_type}
    **Voice & Style**: {pov} narrator, {writing_style} tone, {pace} pacing
    **Unique Elements**: {unique_hooks}
    **Key Constraints**: {length} | {research_focus} | {publication_goal}
    **Creative DNA**: {story_essence}
    """
    
    SYSTEM_PROMPT = """You are a master book consultant specializing in creating compressed "Book DNA" - 
a 200-300 token essential representation that captures the unique genetic code of a book project.

**CRITICAL OBJECTIVES:**
1. Extract the absolute ESSENCE of this book project
2. Create a genetic fingerprint that maintains consistency across all writing phases
3. Compress complex information into precise, memorable elements
4. Ensure every word adds unique value to the DNA
5. Make it specific enough that no other book would have the same DNA

**DNA REQUIREMENTS:**
- Must be 200-300 tokens (roughly 150-225 words)
- Must capture the book's unique identity and voice
- Must include key constraints that guide all decisions
- Must be memorable and actionable for writers
- Must distinguish this book from all others in the genre

**OUTPUT FORMAT:**
Return ONLY the Book DNA text without explanations or commentary (e.g. 'Here is the Book DNA for' ). 
"""

    def __init__(self):
        """Initialize the Book DNA Generator."""
        self.generated_dnas = {}  # Cache for generated DNAs
    
    @classmethod
    def generate_dna_prompt(cls, inputs: BookDNAInputs) -> str:
        """
        Generate the complete prompt for creating Book DNA.
        
        Args:
            inputs: BookDNAInputs containing all necessary information
            
        Returns:
            Complete formatted prompt string for LLM
        """
        
        # Extract key data elements for prompt context
        context_data = cls._extract_context_data(inputs)
        
        prompt = f"""{cls.SYSTEM_PROMPT}

## BOOK DNA - book essential information

**Book Model Summary:**
{cls._format_book_model_summary(context_data['book_model'])}

**Blueprint Essence:**
{cls._format_blueprint_essence(context_data['blueprint']['blueprint'])}

**Story Positioning:**
{cls._format_story_positioning(context_data)}

**Research & Constraints:**
{cls._format_research_constraints(context_data)}

## DNA GENERATION TASK

Create a Book DNA that captures this project's unique genetic code in 200-300 tokens.
The DNA must be specific enough that any writer could maintain consistency using only this information.

**Focus on:**
- What makes THIS book different from all others
- The emotional and thematic core that drives every decision  
- Key constraints that shape the writing process
- The unique voice/style signature
- Critical world-building or character elements

Generate the Book DNA now:"""

        return prompt
    
    @classmethod
    def _extract_context_data(cls, inputs: BookDNAInputs) -> Dict[str, Any]:
        """Extract and organize context data for prompt generation."""
        
        book_model = inputs.book_model
        blueprint = inputs.book_blueprint
        
        return {
            'book_model': book_model,
            'blueprint': blueprint,
            'book_id': inputs.book_id,
            'summary': inputs.book_summary,
            'research': inputs.research_topics,
        }
    
    @classmethod
    def _format_book_model_summary(cls, book_model: Dict[str, Any]) -> str:
        """Format book model data for prompt context."""
        
        book = book_model.book
        genre = book_model.genre
        audience = book_model.audience
        
        return f"""Title: "{book.title}"
Author: {book.author}
Genre: {genre.primary.type}: {genre.primary.description}
Sub-genre: {genre.sub.type}: {genre.sub.description}
Audience: {audience.type} (Ages: {audience.age})
Length: {book.length}
Core Idea: {book.idea}"""
    
    @classmethod
    def _get_from_blueprint(cls, blueprint: Dict[str, Any], phase: str, default: str = 'Not specified') -> str:
        """Retrieve data from blueprint for the given phase."""
        for value in blueprint.values():
            if isinstance(value, dict):
                for k, v in value.items():
                    if k == phase:
                        return v if v is not None else default

    @classmethod
    def _get_blueprint_essence(cls, blueprint: Dict[str, Any]) -> str:
        """Retrieve blueprint data for the essence."""
        blueprint_essence:str = ''
        for value in blueprint.values():
            if isinstance(value, dict):
                for k, v in value.items():
                    k = re.sub(r"\s+", " ", k.replace("_", " ")).strip().upper()
                    blueprint_essence += f'{k}: {v}\n'
        return blueprint_essence

    @classmethod
    def _format_blueprint_essence(cls, blueprint: Dict[str, Any]) -> str:
        """Format blueprint data for prompt context according to the new 7-phase structure."""
        return cls._get_blueprint_essence(blueprint)
    
    @classmethod
    def _format_story_positioning(cls, context_data: Dict[str, Any]) -> str:
        """Format story positioning information."""
        
        book_model = context_data['book_model']
        summary = context_data['summary']  # First 300 chars
        
        return f"""Story World: {book_model.world}. {book_model.world.description}
Writing Style: {book_model.writing_style}
POV: {book_model.pov}. {book_model.pov.description}
Tone: {book_model.tone.type}. {book_model.tone.description}
Pace: {book_model.pace.type}, {book_model.pace.description}

Story Essence: {summary}"""
    
    @classmethod
    def _format_research_constraints(cls, context_data: Dict[str, Any]) -> str:
        """Format research and constraint information."""
        
        research = context_data['research']
        book_model = context_data['book_model']
        research_topics = [v[0] for v in research]
        research_context = [v[1] for v in research if v[1]]
        return f"""Primary Research: {', '.join(research_topics)}
Technology Level: {book_model.technology.type}. {book_model.technology.description}
Research Context: {', '.join(research_context)}
Length Constraint: {book_model.book.length}"""
    
    @classmethod
    def _identify_unique_elements(cls, context_data: Dict[str, Any]) -> str:
        """Identify unique differentiating elements."""
        
        book_model = context_data['book_model']
        blueprint = context_data['blueprint']
        
        # Extract unique elements that set this book apart
        unique_elements = []
        
        # Character elements
        characters = blueprint.get('phase2', {}).get('supporting_characters', [])
        if characters:
            unique_elements.append(f"Features characters: {', '.join(characters[:3])}")
        
        # World elements
        world_desc = book_model.world.description
        if 'magic' in world_desc.lower():
            unique_elements.append("Magic system integration")
        
        # Plot elements
        plot_twists = blueprint.get('phase4', {}).get('plot_twists', [])
        if plot_twists:
            unique_elements.append(f"Key plot elements: {', '.join(plot_twists)}")
        
        # Research focus
        research_focus = book_model.research
        research_topics = [v[0] for v in research_focus]
        if research_topics:
            unique_elements.append(f"Research-driven: {', '.join(research_topics)}")
        
        return '\n'.join(unique_elements) if unique_elements else "Standard genre conventions"
    
    @classmethod
    def create_dna_from_files(cls, 
                             book_model_path: str,
                             blueprint_path: str, 
                             summary_path: str,
                             research_path: str,
                             book_id: str) -> str:
        """
        Create Book DNA prompt from file paths.
        
        Args:
            book_model_path: Path to book model JSON file
            blueprint_path: Path to blueprint JSON file
            summary_path: Path to summary markdown file
            research_path: Path to research JSON file
            book_id: Unique identifier for this book
            
        Returns:
            Complete DNA generation prompt
        """
        
        # Load book model
        with open(book_model_path, 'r', encoding='utf-8') as f:
            book_model = json.load(f)
        
        # Load blueprint
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)
        
        # Load summary
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary = f.read()
        
        # Load research
        with open(research_path, 'r', encoding='utf-8') as f:
            research_data = json.load(f)
            research_topics = research_data.get('updated_queries', [])

        # Create inputs
        inputs = BookDNAInputs(
            book_model=book_model,
            book_blueprint=blueprint,
            book_summary=summary,
            research_topics=research_topics,
            book_id=book_id
        )
        
        return cls.generate_dna_prompt(inputs)
    
    @classmethod
    def validate_dna_output(cls, dna_text: str) -> Dict[str, Any]:
        """
        Validate that generated DNA meets requirements.
        
        Args:
            dna_text: The generated DNA text
            
        Returns:
            Validation results
        """
        
        words = dna_text.split()
        word_count = len(words)
        
        # Rough token estimation (1 token ≈ 0.75 words)
        estimated_tokens = int(word_count * 1.33)
        
        validation = {
            'word_count': word_count,
            'estimated_tokens': estimated_tokens,
            'target_range': (200, 300),
            'in_range': 200 <= estimated_tokens <= 700,
            'has_book_id': 'BOOK DNA' in dna_text and 'ID:' in dna_text,
            'has_essential_elements': any(keyword in dna_text.lower() for keyword in 
                                        ['title', 'author', 'genre', 'audience', 'protagonist']),
            'density_score': cls._calculate_information_density(dna_text)
        }
        
        validation['is_valid'] = (
            validation['in_range'] and 
            validation['has_essential_elements'] and
            validation['density_score'] > 0.7
        )
        
        return validation
    
    @classmethod
    def _calculate_information_density(cls, text: str) -> float:
        """Calculate information density score (0.0 to 1.0)."""
        
        # Look for key information markers
        info_markers = [
            'genre', 'audience', 'structure', 'conflict', 'world',
            'pov', 'style', 'pace', 'length', 'research', 'unique',
            'protagonist', 'antagonist', 'supporting characters', 'plot twists',
            'cultures', 'magic', 'magic system', 'technology', 'research-driven'
        ]
        
        found_markers = sum(1 for marker in info_markers if marker.lower() in text.lower())
        density = found_markers / len(info_markers)
        
        return min(density, 1.0)
    
    def generate_and_cache_dna(self, inputs: BookDNAInputs) -> str:
        """
        Generate DNA prompt and cache it for reuse.
        
        Args:
            inputs: BookDNAInputs containing all necessary information
            
        Returns:
            Generated DNA prompt
        """
        
        cache_key = inputs.book_id
        
        if cache_key not in self.generated_dnas:
            self.generated_dnas[cache_key] = self.generate_dna_prompt(inputs)
        
        return self.generated_dnas[cache_key]
    
    def get_cached_dna(self, book_id: str) -> Optional[str]:
        """Get cached DNA for a book ID."""
        return self.generated_dnas.get(book_id)
    
    def clear_cache(self) -> None:
        """Clear the DNA cache."""
        self.generated_dnas.clear()


# # Example usage and testing
# if __name__ == "__main__":
#     # Example of how to use the BookDNAGenerator
    
#     # Create sample inputs (you would load these from your actual files)
#     sample_inputs = BookDNAInputs(
#         book_model={
#             "book": {
#                 "title": "The Enchanted Forest of Peter",
#                 "author": "Joseph Campbell",
#                 "idea": "A brave bunny ventures into an enchanted forest...",
#                 "length": "40,000-60,000 words"
#             },
#             "genre": {
#                 "primary": {"type": "children"},
#                 "sub": {"type": "fantasy"}
#             },
#             "audience": {"type": "children", "age": "7-12"},
#             "writing_style": "conversational",
#             "world": {"type": "high fantasy"},
#             "pov": {"type": "third person objective"}
#         },
#         book_blueprint={
#             "phase2": {
#                 "plot_structure": "Hero's Journey",
#                 "main_character": "Peter the bunny",
#                 "conflict_type": "Person vs Supernatural"
#             }
#         },
#         book_summary="A whimsical tale of Peter the bunny...",
#         research_topics=[{"type": "folklore"}, {"type": "mythology"}],
#         book_id="peter_forest_001"
#     )
    
#     # Generate DNA prompt
#     generator = BookDNAPromptGenerator()
#     dna_prompt = generator.generate_dna_prompt(sample_inputs)
    
#     print("Generated Book DNA Prompt:")
#     print("=" * 50)
#     print(dna_prompt)
    
#     # Example validation of hypothetical DNA output
#     sample_dna = """**BOOK DNA [ID: peter_forest_001]**
    
#     **Core Identity**: "The Enchanted Forest of Peter" by Joseph Campbell - children/fantasy for ages 7-12
#     **Narrative Engine**: Hero's Journey with Person vs Supernatural in high fantasy world
#     **Voice & Style**: Third person objective, conversational tone, fast pacing
#     **Unique Elements**: Slavic mythology creatures (Baba Yaga, Leshy, Rusalka), folklore-driven
#     **Key Constraints**: 40,000-60,000 words | folklore research | children's market
#     **Creative DNA**: Brave curious bunny learns courage/kindness through mythical encounters"""
    
#     validation = BookDNAPromptGenerator.validate_dna_output(sample_dna)
#     print("\nValidation Results:")
#     print("=" * 50)
#     for key, value in validation.items():
#         print(f"{key}: {value}")