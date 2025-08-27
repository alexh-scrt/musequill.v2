#!/usr/bin/env python3
"""
Book Summary Prompt Generator for Creative Book Summaries

This script takes book template data (JSON) and generates an optimized prompt
for Ollama with llama3.3:70b to create highly creative, engaging book summaries.
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class BookSummaryConfig:
    """Configuration for book summary generation."""
    target_length: str = "300-500 words"
    creativity_level: str = "high"
    include_themes: bool = True
    include_mythology_elements: bool = True
    target_audience_focus: bool = True


class BookSummaryPromptGenerator:
    """Generates optimized prompts for creative book summary creation."""
    
    SYSTEM_PROMPT = """You are a master storyteller and literary marketing expert specializing in creating captivating book summaries that enchant readers and spark their imagination. Your summaries don't just describe books—they transport readers into the story world and make them desperate to read more.

## CREATIVE EXCELLENCE MANDATE
- Transform mundane plot points into magical, evocative descriptions
- Use sensory language that makes readers feel they're already in the story
- Create emotional hooks that resonate with the target audience
- Weave in mythological and cultural elements naturally
- Build anticipation and wonder without spoiling key plot points
- Match the tone and energy of the book's intended audience

## SUMMARY CRAFTING PRINCIPLES
1. **Hook Immediately**: Open with something that stops readers mid-scroll
2. **Show Don't Tell**: Use vivid scenes instead of generic descriptions
3. **Emotional Resonance**: Connect with universal themes and feelings
4. **Rhythm & Flow**: Create prose that's musical and engaging to read
5. **Mystery & Promise**: Hint at wonders without revealing everything
6. **Authentic Voice**: Match the book's tone and target audience perfectly

## CRITICAL SUCCESS FACTORS
- Every sentence must earn its place and drive interest forward
- Language should sparkle with creativity while remaining accessible
- Cultural/mythological elements should feel integral, not forced
- The summary should feel like a preview of the writing quality inside
- Readers should finish feeling they MUST read this book immediately"""

    SUMMARY_INSTRUCTIONS = """
## Creative Book Summary Generation Instructions

Based on the book template data provided, craft a mesmerizing book summary that captures the essence, magic, and appeal of this story. Your summary should be a literary gem that makes readers fall in love with the book before they've even opened it.

### Core Elements to Weave Together:

**Opening Hook (25-50 words)**
- Start with the most compelling, unique element of the story
- Use active, sensory language that immediately immerses the reader
- Avoid generic opening phrases like "This is a story about..."
- Make the first sentence irresistible

**Character Introduction & World Building (100-150 words)**
- Introduce the protagonist in a way that makes readers care instantly
- Paint the story world with vivid, specific details
- Highlight what makes this fantasy realm unique and magical
- Weave in mythological elements naturally as part of the world

**Conflict & Stakes (75-125 words)**
- Present the central challenge without giving away solutions
- Show why this matters deeply to the protagonist and readers
- Build tension and anticipation
- Hint at the transformative journey ahead

**Thematic Resonance & Promise (50-100 words)**
- Touch on universal themes (courage, growing up, finding yourself)
- Connect with what the target audience craves emotionally
- Promise the kind of reading experience they'll have
- End with something that lingers in their minds

### Style Guidelines:
- **Language Level**: Match the target audience perfectly
- **Tone**: Reflect the book's established tone while adding marketing appeal
- **Pacing**: Create rhythm that pulls readers along
- **Imagery**: Use metaphors and descriptions that spark imagination
- **Cultural Elements**: Integrate mythological aspects as natural story elements

### What Makes This Summary Special:
- Avoid clichéd fantasy summary language
- Focus on emotional journey over plot mechanics
- Use specific, evocative details rather than generic descriptors
- Create a sense of wonder and anticipation
- Make the mythological elements feel fresh and exciting
"""

    @classmethod
    def generate_prompt(cls, book_data: Dict[str, Any], config: Optional[BookSummaryConfig] = None) -> str:
        """
        Generate a complete prompt for llama3.3:70b based on book template data.
        
        Args:
            book_data: Dictionary containing book template data
            config: Optional configuration for summary generation
            
        Returns:
            Complete formatted prompt string optimized for llama3.3:70b
        """
        if config is None:
            config = BookSummaryConfig()
        
        # Extract key information for context
        book_info = book_data.get("book", {})
        genre_info = book_data.get("genre", {})
        audience_info = book_data.get("audience", {})
        world_info = book_data.get("world", {})
        tone_info = book_data.get("tone", {})
        
        # Create contextual summary
        context_summary = cls._create_context_summary(book_data)
        
        # Build mythology context if relevant
        mythology_context = cls._extract_mythology_context(book_data)
        
        # Convert to clean JSON for reference
        clean_json = json.dumps(book_data, indent=2, ensure_ascii=False)
        
        # Construct the complete prompt
        complete_prompt = f"""{cls.SYSTEM_PROMPT}

## How It Begins:

{book_info['bootstrap']}        

## Book Context Summary

{context_summary}

## Summary Generation Task

{cls.SUMMARY_INSTRUCTIONS}

### Target Summary Specifications:
- **Length**: {config.target_length}
- **Creativity Level**: {config.creativity_level}
- **Target Audience**: {audience_info.get('type', 'general')} ({audience_info.get('age', 'all ages')})
- **Tone to Match**: {tone_info.get('type', 'engaging')} - {tone_info.get('description', 'captivating and appropriate')}
- **World Type**: {world_info.get('type', 'fantasy')} - {world_info.get('description', 'magical and immersive')}

### Special Focus Areas:
{"\n".join([f'\t* {i["type"]} - {i["description"]}' for i in book_data['research']])}

## Complete Book Template Data

{clean_json}

---

## YOUR TASK

Create a captivating, creative book summary that makes readers desperate to read "The Enchanted Forest of Peter." Your summary should be a perfect blend of marketing appeal and literary artistry.

**Remember:**
- Every word should sparkle with creativity
- Make the Slavic mythology feel fresh and exciting
- Connect emotionally with children and parents who might read together
- Build anticipation without spoiling the magic
- Let your creativity flow while staying true to the book's essence

Write the most compelling book summary you can imagine - one that would make this book impossible to ignore on a bookshelf or in an online store.

Generate your creative book summary now:"""

        return complete_prompt
    
    @classmethod
    def _create_context_summary(cls, book_data: Dict[str, Any]) -> str:
        """Create a concise summary of the book context."""
        book = book_data.get("book", {})
        genre = book_data.get("genre", {})
        audience = book_data.get("audience", {})
        structure = book_data.get("structure", {})
        conflict = book_data.get("conflict", {})
        world = book_data.get("world", {})
        
        return f"""**Title**: "{book.get('title', 'Unknown')}" by {book.get('author', 'Unknown')}
**Core Concept**: {book.get('idea', 'A magical adventure story')}
**How It Begins**: {book.get('bootstrap', 'A typical beginning for the genre')}
**Genre**: {genre.get('primary', {}).get('type', 'fantasy')} / {genre.get('sub', {}).get('type', 'children')}
**Target Audience**: {audience.get('type', 'children')} (Ages: {audience.get('age', '7-12')})
**Length**: {book.get('length', '40,000-60,000 words')} - {book.get('type', 'novelle')}
**Story Structure**: {structure.get('type', 'Hero\'s Journey')}
**Central Conflict**: {conflict.get('type', 'character vs supernatural')}
**World Setting**: {world.get('type', 'high fantasy')} - {world.get('description', 'magical realm')}
**Language**: {book.get('language', 'English')}"""

    @classmethod
    def _extract_mythology_context(cls, book_data: Dict[str, Any]) -> str:
        """Extract and highlight mythological elements."""
        book_idea = book_data.get("book", {}).get("idea", "")
        research = book_data.get("research", [])
        
        mythology_elements = []
        if "Baba Yaga" in book_idea:
            mythology_elements.append("Baba Yaga (the witch of the iron teeth)")
        if "Leshy" in book_idea:
            mythology_elements.append("Leshy (forest guardian spirit)")
        if "Domovoi" in book_idea:
            mythology_elements.append("Domovoi (household protective spirit)")
        if "Rusalka" in book_idea:
            mythology_elements.append("Rusalka (water spirit/mermaid)")
        
        folklore_research = any(r.get("type") == "folklore" for r in research)
        
        if mythology_elements or folklore_research:
            return f"""
## Mythological & Cultural Context

**Slavic Mythology Elements**: {', '.join(mythology_elements) if mythology_elements else 'Rich folklore tradition'}
**Cultural Research**: {"Folklore and traditional stories integrated" if folklore_research else "Cultural authenticity emphasized"}

**Summary Writing Note**: These mythological elements should feel like natural parts of an exciting adventure, not educational content. Make them mysterious, wonderful, and slightly dangerous in child-appropriate ways."""
        
        return ""
    
    @classmethod
    def generate_prompt_from_json_file(cls, json_file_path: str, config: Optional[BookSummaryConfig] = None) -> str:
        """
        Generate prompt from a JSON file.
        
        Args:
            json_file_path: Path to JSON file containing book template data
            config: Optional configuration for summary generation
            
        Returns:
            Complete formatted prompt string
        """
        with open(json_file_path, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        return cls.generate_prompt(book_data, config)
    
    @classmethod
    def save_prompt_to_file(cls, prompt:str, output_filename: str, config: Optional[BookSummaryConfig] = None) -> None:
        """
        Generate and save prompt to a file.
        
        Args:
            book_data: Dictionary containing book template data
            output_path: Path where to save the prompt file
            config: Optional configuration for summary generation
        """
        file_path = Path(output_filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Book summary prompt saved to: {file_path}")
    
    @classmethod
    def get_prompt_statistics(cls, prompt:str, book_data: Dict[str, Any], config: Optional[BookSummaryConfig] = None) -> Dict[str, Any]:
        """
        Get statistics about the generated prompt.
        
        Args:
            book_data: Dictionary containing book template data
            config: Optional configuration
            
        Returns:
            Dictionary with prompt statistics and recommendations
        """
        
        # Calculate complexity based on book elements
        complexity_score = cls._calculate_complexity_score(book_data)
        
        return {
            "total_characters": len(prompt),
            "total_words": len(prompt.split()),
            "estimated_tokens": int(len(prompt.split()) * 1.3),  # Rough estimate for llama
            "book_complexity_score": complexity_score,
            "recommended_model_settings": {
                "temperature": 1.3,  # Higher for creativity
                "top_k": 45,
                "top_p": 0.9,
                "repeat_penalty": 1.2,
                "max_tokens": 1000,  # Enough for detailed summary
                "stop": ["</summary>"],
            },
            "optimization_notes": [
                "High temperature for creative language",
                "Moderate top_p to maintain coherence",
                "Stop tokens prevent over-generation",
                f"Complexity level: {'High' if complexity_score > 0.7 else 'Medium' if complexity_score > 0.4 else 'Low'}"
            ]
        }
    
    @classmethod
    def _calculate_complexity_score(cls, book_data: Dict[str, Any]) -> float:
        """Calculate complexity score based on book elements (0.0 to 1.0)."""
        score = 0.0
        
        # Base complexity from genre and audience
        genre_type = book_data.get("genre", {}).get("primary", {}).get("type", "")
        if genre_type == "children":
            score += 0.3  # Children's books have moderate complexity
        
        # World building complexity
        world_type = book_data.get("world", {}).get("type", "")
        if world_type == "high fantasy":
            score += 0.3
        
        # Mythology integration
        book_idea = book_data.get("book", {}).get("idea", "")
        mythology_count = sum(1 for creature in ["Baba Yaga", "Leshy", "Domovoi", "Rusalka"] if creature in book_idea)
        score += min(mythology_count * 0.1, 0.3)
        
        # Research requirements
        research = book_data.get("research", [])
        if any(r.get("type") == "folklore" for r in research):
            score += 0.1
        
        return min(score, 1.0)


def main():
    """Example usage of the BookSummaryPromptGenerator."""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Generate creative book summary prompts for Ollama llama3.3:70b")
    parser.add_argument('--json', '-j', required=True, help='JSON file with book template data')
    parser.add_argument('--output', '-o', help='Output file for the prompt')
    parser.add_argument('--stats', action='store_true', help='Show prompt statistics')
    parser.add_argument('--length', default="300-500 words", help='Target summary length')
    parser.add_argument('--creativity', default="high", choices=["low", "medium", "high"], help='Creativity level')
    
    args = parser.parse_args()
    
    try:
        # Create configuration
        config = BookSummaryConfig(
            target_length=args.length,
            creativity_level=args.creativity,
            include_themes=True,
            include_mythology_elements=True,
            target_audience_focus=True
        )
        
        # Load and process JSON data
        with open(args.json, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        # Generate prompt
        if args.output:
            BookSummaryPromptGenerator.save_prompt_to_file(book_data, args.output, config)
        else:
            prompt = BookSummaryPromptGenerator.generate_prompt(book_data, config)
            print(prompt)
        
        if args.stats:
            stats = BookSummaryPromptGenerator.get_prompt_statistics(book_data, config)
            print("\n" + "="*60)
            print("BOOK SUMMARY PROMPT STATISTICS")
            print("="*60)
            for key, value in stats.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")
                elif isinstance(value, list):
                    print(f"{key}:")
                    for item in value:
                        print(f"  • {item}")
                else:
                    print(f"{key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()