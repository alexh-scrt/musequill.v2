#!/usr/bin/env python3
"""
Blueprint Prompt Generator for Book Writing

This script takes a BookModelType instance and generates an optimized prompt
for Llama 3.3-8B to create a comprehensive book writing blueprint.
"""

import json
from typing import Dict, Any
from musequill.services.backend.model.book import BookModelType


class BlueprintPromptGenerator:
    """Generates optimized prompts for book writing blueprint creation."""
    
    SYSTEM_PROMPT = """You are an expert book writing consultant and publishing strategist. Your task is to create a comprehensive, actionable book writing blueprint based on the provided book template data. You must analyze all elements systematically and provide concrete, step-by-step guidance that transforms the template into a complete writing plan.

## Response Guidelines

1. **Be Specific**: Provide concrete, actionable advice rather than generic writing tips
2. **Use Data**: Reference specific elements from the input template throughout your response
3. **Maintain Coherence**: Ensure all recommendations align with the book's established parameters
4. **Prioritize Commercially**: Focus on market-viable approaches that increase publication success
5. **Structure Clearly**: Use the exact headings and formatting specified
6. **Length Target**: Aim for 1500-2000 words total to provide comprehensive coverage
7. **Practical Focus**: Every recommendation should be implementable by the author

## Critical Success Factors

- Alignment between genre expectations and story execution
- Consistency between writing style and target audience
- Structural integrity based on chosen framework
- Character development that serves the plot type
- World-building that supports rather than overwhelms the story
- Pacing that maintains reader engagement throughout the specified length
- Research integration that enhances rather than interrupts narrative flow"""

    BLUEPRINT_FRAMEWORK = """# BOOK WRITING BLUEPRINT

## Phase 1: Strategic Foundation Analysis

Analyze the template data and establish the strategic foundation:

### Strategic Foundation
- **Commercial Viability**: Assess market potential based on genre/audience combination
- **Target Market**: Define primary and secondary reader demographics  
- **Competitive Positioning**: How this book fits in the current market
- **Unique Value Proposition**: What makes this book distinctive
- **Publishing Path**: Traditional, self-publishing, or hybrid recommendation

## Phase 2: Story Architecture Blueprint

Transform template elements into concrete story structure:

### Core Premise
- **Logline**: One-sentence story summary
- **Central Question**: The main dramatic question driving the narrative
- **Core Conflict**: Primary tension based on conflict type

### Structural Framework  
- **Act Structure**: Break down based on specified structure type
- **Key Plot Points**: Major story beats with approximate word count targets
- **Character Arc Milestones**: Protagonist development stages
- **Pacing Strategy**: How to maintain the specified pace throughout

### Chapter Architecture
- **Estimated Chapter Count**: Based on target length and pacing
- **Average Chapter Length**: Word count per chapter
- **Chapter Function Matrix**: Plot advancement vs. character development balance

## Phase 3: Character Development System

Create detailed character development guidelines:

### Protagonist Blueprint
- **Core Personality Traits**: Based on personality type from template
- **Character Arc Framework**: Beginning → Middle → End transformation
- **Voice and Dialogue Style**: Aligned with writing style and POV
- **Internal Conflict Engine**: Psychological drivers

### Supporting Character Ecosystem
- **Antagonist Profile**: Based on conflict type
- **Ally/Mentor Roles**: Supporting character functions
- **Character Relationship Web**: How characters interact and influence each other

### Narrative Voice Strategy
- **POV Implementation**: Specific techniques for chosen POV
- **Narrative Distance**: Intimacy level with characters
- **Voice Consistency Guidelines**: Maintaining style throughout

## Phase 4: World-Building & Research Framework

Develop setting and research strategy:

### Setting Development
- **World Type Implementation**: Specific to chosen world type
- **Technology Integration**: How the specified era influences the story
- **Cultural and Social Systems**: Based on research requirements
- **Sensory World-Building**: Engaging the five senses

### Research Action Plan
- **Primary Research Areas**: Based on research requirements in template
- **Research Timeline**: When to research during writing process
- **Fact-Checking Systems**: Maintaining accuracy
- **Expert Consultation Needs**: If applicable

### Consistency Management
- **World Bible Creation**: Key elements to track
- **Setting Detail Database**: Organized information storage

## Phase 5: Writing Process Blueprint

Create detailed writing execution plan:

### Pre-Writing Phase (Weeks 1-2)
- **Detailed Outline Creation**: Chapter-by-chapter breakdown
- **Character Profiles Completion**: All major characters
- **World-Building Documentation**: Setting bible
- **Research Completion**: All necessary background work

### Drafting Phase (Weeks 3-X)
- **Daily Writing Targets**: Based on total length and timeline
- **Weekly Milestones**: Progress checkpoints
- **Chapter Writing Order**: Linear vs. non-linear approach
- **Draft Quality Expectations**: First draft standards

### Revision Strategy (Weeks X+1 to X+Y)
- **Macro Revision**: Story structure and character arcs
- **Micro Revision**: Scene-level improvements
- **Line Editing**: Prose quality and style consistency
- **Final Polish**: Grammar, formatting, final touches

### Quality Control Checkpoints
- **25% Review**: Quarter-point assessment
- **50% Review**: Midpoint structural check
- **75% Review**: Three-quarter momentum evaluation
- **Completion Review**: Full draft assessment

## Phase 6: Style & Tone Implementation Guide

Provide specific guidance for maintaining consistency:

### Writing Style Execution
- **Sentence Structure Patterns**: Based on specified style
- **Vocabulary Guidelines**: Appropriate word choices for audience
- **Paragraph Construction**: Pacing and flow techniques
- **Dialogue Implementation**: Character voice differentiation

### Tone Maintenance System
- **Emotional Baseline**: Consistent mood throughout
- **Tonal Shifts**: When and how to vary tone
- **Genre Conventions**: Meeting reader expectations
- **Audience Alignment**: Age-appropriate content and complexity

### Quality Assurance Checklist
- **Style Consistency Markers**: What to check during revision
- **Tone Verification Points**: Ensuring emotional coherence
- **Voice Authentication**: Maintaining narrative authenticity

## Phase 7: Marketing & Publishing Preparation

Prepare for the book's market entry:

### Market Positioning
- **Genre Classification**: Precise category placement
- **Comp Title Analysis**: Similar successful books
- **Target Reader Profile**: Detailed audience description
- **Marketing Hooks**: Key selling points

### Publishing Readiness
- **Manuscript Requirements**: Format and length specifications
- **Query Letter Elements**: For traditional publishing
- **Self-Publishing Checklist**: If going independent route
- **Beta Reader Strategy**: Getting feedback before publication

### Launch Strategy Framework
- **Pre-Launch Timeline**: 6 months before publication
- **Launch Week Tactics**: Release coordination
- **Post-Launch Growth**: Building readership"""

    @classmethod
    def generate_prompt(cls, book_model: BookModelType) -> str:
        """
        Generate a complete prompt for Llama 3.3-8B based on BookModelType.
        
        Args:
            book_model: BookModelType instance containing book template data
            
        Returns:
            Complete formatted prompt string ready for Llama 3.3-8B
        """
        # Extract key template data for context
        template_summary = cls._create_template_summary(book_model)
        
        # Convert to clean JSON for inclusion
        template_json = json.dumps(book_model.dict(), indent=2, ensure_ascii=False)
        
        # Construct the complete prompt
        complete_prompt = f"""{cls.SYSTEM_PROMPT}

## Book Template Summary

{template_summary}

## Blueprint Generation Task

Based on the book template data provided below, create a comprehensive book writing blueprint following the seven-phase framework. Ensure every recommendation is tailored to the specific elements in this template.

{cls.BLUEPRINT_FRAMEWORK}

## Book Template Data

```json
{template_json}
```

Generate the complete book writing blueprint now, addressing each phase systematically and providing specific, actionable guidance based on this template's unique characteristics."""

        return complete_prompt
    
    @classmethod
    def _create_template_summary(cls, book_model: BookModelType) -> str:
        """Create a concise summary of the template for context."""
        return f"""**Book**: "{book_model.book.title}" by {book_model.book.author}
**Genre**: {book_model.genre.primary.type} / {book_model.genre.sub.type}
**Audience**: {book_model.audience.type} (Ages {book_model.audience.age})
**Length**: {book_model.book.length}
**Structure**: {book_model.structure.type}
**Style**: {book_model.writing_style} with {book_model.tone.type} tone
**World**: {book_model.world.type} setting
**Conflict**: {book_model.conflict.type}
**POV**: {book_model.pov.type}
**Research Focus**: {', '.join([r.type for r in book_model.research])}"""

    @classmethod
    def generate_prompt_from_json(cls, json_data: Dict[str, Any]) -> str:
        """
        Generate prompt directly from JSON data.
        
        Args:
            json_data: Dictionary containing book template data
            
        Returns:
            Complete formatted prompt string
        """
        book_model = BookModelType(**json_data)
        return cls.generate_prompt(book_model)
    
    @classmethod
    def save_prompt_to_file(cls, book_model: BookModelType, output_path: str) -> None:
        """
        Generate and save prompt to a file.
        
        Args:
            book_model: BookModelType instance
            output_path: Path where to save the prompt file
        """
        prompt = cls.generate_prompt(book_model)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Blueprint prompt saved to: {output_path}")
    
    @classmethod
    def get_prompt_statistics(cls, book_model: BookModelType) -> Dict[str, Any]:
        """
        Get statistics about the generated prompt.
        
        Args:
            book_model: BookModelType instance
            
        Returns:
            Dictionary with prompt statistics
        """
        prompt = cls.generate_prompt(book_model)
        
        return {
            "total_characters": len(prompt),
            "total_words": len(prompt.split()),
            "estimated_tokens": len(prompt.split()) * 1.3,  # Rough estimate
            "template_complexity_score": cls._calculate_complexity_score(book_model),
            "recommended_model_settings": {
                "temperature": 0.7,
                "max_tokens": 3000,
                "top_p": 0.9
            }
        }
    
    @classmethod
    def _calculate_complexity_score(cls, book_model: BookModelType) -> float:
        """Calculate a complexity score for the template (0.0 to 1.0)."""
        complexity_factors = []
        
        # Genre complexity
        if book_model.world.type in ["high fantasy", "science fiction", "alternate history"]:
            complexity_factors.append(0.8)
        elif book_model.world.type in ["contemporary", "historical"]:
            complexity_factors.append(0.4)
        else:
            complexity_factors.append(0.6)
        
        # Length complexity
        word_count = cls._extract_word_count(book_model.book.length)
        if word_count > 80000:
            complexity_factors.append(0.9)
        elif word_count > 50000:
            complexity_factors.append(0.7)
        else:
            complexity_factors.append(0.5)
        
        # Research complexity
        if len(book_model.research) > 2:
            complexity_factors.append(0.8)
        elif len(book_model.research) > 0:
            complexity_factors.append(0.6)
        else:
            complexity_factors.append(0.3)
        
        return sum(complexity_factors) / len(complexity_factors)
    
    @classmethod
    def _extract_word_count(cls, length_str: str) -> int:
        """Extract approximate word count from length string."""
        length_lower = length_str.lower()
        
        if "40,000-60,000" in length_lower:
            return 50000
        elif "60,000-80,000" in length_lower:
            return 70000
        elif "80,000-100,000" in length_lower:
            return 90000
        elif "novella" in length_lower:
            return 40000
        elif "novel" in length_lower:
            return 80000
        else:
            # Try to extract numbers
            import re
            numbers = re.findall(r'\d+,?\d*', length_str)
            if numbers:
                return int(numbers[0].replace(',', ''))
            return 60000  # Default


def main():
    """Example usage of the BlueprintPromptGenerator."""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Generate book writing blueprint prompts")
    parser.add_argument('--template', '-t', required=True, help='Template name to load')
    parser.add_argument('--output', '-o', help='Output file for the prompt')
    parser.add_argument('--stats', action='store_true', help='Show prompt statistics')
    
    args = parser.parse_args()
    
    # Load template (reusing the logic from main.py)
    template_path = Path("musequill/services/backend/templates") / f"{args.template}.json"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        book_model = BookModelType(**template_data)
        
        # Generate prompt
        prompt = BlueprintPromptGenerator.generate_prompt(book_model)
        
        if args.output:
            BlueprintPromptGenerator.save_prompt_to_file(book_model, args.output)
        else:
            print(prompt)
        
        if args.stats:
            stats = BlueprintPromptGenerator.get_prompt_statistics(book_model)
            print("\n" + "="*50)
            print("PROMPT STATISTICS")
            print("="*50)
            for key, value in stats.items():
                if isinstance(value, dict):
                    print(f"{key}:")
                    for sub_key, sub_value in value.items():
                        print(f"  {sub_key}: {sub_value}")
                else:
                    print(f"{key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()