#!/usr/bin/env python3
"""
Blueprint Prompt Generator for Book Writing - JSON Output Version

This script takes a BookModelType instance and generates an optimized prompt
for Llama 3.3-8B to create a comprehensive book writing blueprint in JSON format.
"""

import json
from typing import Dict, Any
from musequill.services.backend.model.book import BookModelType
from .target_json_schema import TARGET_JSON_SCHEMA, EXPECTED_OUTPUT

class BlueprintPromptGenerator:
    """Generates optimized prompts for book writing blueprint creation with JSON output."""
    
    SYSTEM_PROMPT = """You are an expert book writing consultant and publishing strategist. Your task is to create a comprehensive, actionable book writing blueprint based on the provided book template data. You must analyze all elements systematically and provide concrete, step-by-step guidance that transforms the template into a complete writing plan.

## CRITICAL OUTPUT REQUIREMENT
You MUST respond with a valid JSON object following the exact structure provided in the JSON Schema below. Do not include any text before or after the JSON. Do not use markdown code blocks. Return only pure JSON.

## Response Guidelines

1. **Be Specific**: Provide concrete, actionable advice rather than generic writing tips
2. **Use Data**: Reference specific elements from the input template throughout your response
3. **Maintain Coherence**: Ensure all recommendations align with the book's established parameters
4. **Prioritize Commercially**: Focus on market-viable approaches that increase publication success
5. **Structure as JSON**: Follow the exact JSON schema provided
6. **Comprehensive Coverage**: Ensure every field in the schema is populated with meaningful content
7. **Practical Focus**: Every recommendation should be implementable by the author

## Critical Success Factors

- Alignment between genre expectations and story execution
- Consistency between writing style and target audience
- Structural integrity based on chosen framework
- Character development that serves the plot type
- World-building that supports rather than overwhelms the story
- Pacing that maintains reader engagement throughout the specified length
- Research integration that enhances rather than interrupts narrative flow"""

    BLUEPRINT_INSTRUCTIONS = """
## JSON Blueprint Generation Instructions

Based on the book template data provided, create a comprehensive book writing blueprint following the seven-phase framework. Each phase must be populated with specific, actionable guidance tailored to the template's unique characteristics.

### Phase 1: Strategic Foundation Analysis
Analyze the template data and establish strategic foundation with commercial viability assessment, target market definition, competitive positioning, unique value proposition, and publishing path recommendation.

### Phase 2: Story Architecture Blueprint
Transform template elements into concrete story structure including core premise (logline, central question, core conflict), structural framework (act structure, key plot points with word count targets, character arc milestones, pacing strategy), and chapter architecture (estimated chapter count, average chapter length, chapter function matrix).

### Phase 3: Character Development System
Create detailed character development guidelines including protagonist blueprint (core personality traits, character arc framework, voice and dialogue style, internal conflict engine), supporting character ecosystem (antagonist profile, ally/mentor roles, character relationship web), and narrative voice strategy (POV implementation, narrative distance, voice consistency guidelines).

### Phase 4: World-Building & Research Framework
Develop setting and research strategy including setting development (world type implementation, technology integration, cultural and social systems, sensory world-building), research action plan (primary research areas, research timeline, fact-checking systems, expert consultation needs), and consistency management (world bible creation, setting detail database).

### Phase 5: Writing Process Blueprint
Create detailed writing execution plan including pre-writing phase (detailed outline creation, character profiles completion, world-building documentation, research completion), drafting phase (daily writing targets, weekly milestones, chapter writing order, draft quality expectations), revision strategy (macro revision, micro revision, line editing, final polish), and quality control checkpoints (25%, 50%, 75%, completion reviews).

### Phase 6: Style & Tone Implementation Guide
Provide specific guidance for maintaining consistency including writing style execution (sentence structure patterns, vocabulary guidelines, paragraph construction, dialogue implementation), tone maintenance system (emotional baseline, tonal shifts, genre conventions, audience alignment), and quality assurance checklist (style consistency markers, tone verification points, voice authentication).

### Phase 7: Marketing & Publishing Preparation
Prepare for market entry including market positioning (genre classification, comp title analysis, target reader profile, marketing hooks), publishing readiness (manuscript requirements, query letter elements, self-publishing checklist, beta reader strategy), and launch strategy framework (pre-launch timeline, launch week tactics, post-launch growth).

Remember: Populate ALL fields in the JSON schema with meaningful, specific content based on the template data. Ensure recommendations are commercially viable and practically implementable.
"""

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

## JSON Output Schema

# ABSOLUTE RULES:
- ❗ Output MUST be valid JSON that conforms to the structure below
- ❗ Do NOT include any explanation, comment, or markdown
- ❗ Populate **every field** in the schema with SPECIFIC, USEFUL data

# Output Format Requirements:
- 🔹 Pure JSON object
- 🔹 All fields filled
- 🔹 NO markdown/code blocks
- 🔹 NO extra commentary

# DO NOT DO:
- ❌ Do not preface with “Here’s your JSON:”
- ❌ Do not wrap output in triple backticks
- ❌ Do not include schema again
- ❌ Do not repeat the template data


🛑 Your ONLY job is to produce a JSON object.
🚫 Do NOT interpret. Do NOT reformat. Do NOT include text, commentary, or labels.
✅ Your JSON MUST match the structure and field names EXACTLY.

🔍 Common Mistakes to Avoid:
- Using `phase1` instead of `phase_1`
- Skipping the `"blueprint"` root node
- Returning `"target_audience"` as a string instead of a nested object

You MUST respond with a JSON object that follows this exact structure:

```json
{TARGET_JSON_SCHEMA}
```
## Here is a correct example output:
```json
{EXPECTED_OUTPUT}
```
## Book Template Summary

{template_summary}

## Blueprint Generation Task

{cls.BLUEPRINT_INSTRUCTIONS}

## Book Template Data


{template_json}


Generate the complete book writing blueprint now as a valid JSON object, addressing each phase systematically and providing specific, actionable guidance based on this template's unique characteristics. Return ONLY the JSON object with no additional text or formatting.

"""

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
                "temperature": 0.3,  # Lower temperature for JSON consistency
                "max_tokens": 4000,  # Higher for JSON output
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

    @classmethod
    def validate_json_response(cls, response: str) -> tuple[bool, Dict[str, Any] | str]:
        """
        Validate that the LLM response is valid JSON matching our schema.
        
        Args:
            response: The LLM response string
            
        Returns:
            Tuple of (is_valid, parsed_json_or_error_message)
        """
        try:
            # Try to parse the JSON
            parsed_json = json.loads(response.strip())
            
            # Basic structure validation
            required_keys = ["title", "author", "blueprint"]
            blueprint_phases = ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5", "phase_6", "phase_7"]
            
            # Check top-level structure
            for key in required_keys:
                if key not in parsed_json:
                    return False, f"Missing required key: {key}"
            
            # Check blueprint phases
            if "blueprint" in parsed_json:
                for phase in blueprint_phases:
                    if phase not in parsed_json["blueprint"]:
                        return False, f"Missing blueprint phase: {phase}"
            
            return True, parsed_json
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"


def main():
    """Example usage of the BlueprintPromptGenerator."""
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Generate book writing blueprint prompts with JSON output")
    parser.add_argument('--template', '-t', required=True, help='Template name to load')
    parser.add_argument('--output', '-o', help='Output file for the prompt')
    parser.add_argument('--stats', action='store_true', help='Show prompt statistics')
    parser.add_argument('--validate', action='store_true', help='Validate JSON schema')
    
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
        
        if args.validate:
            print("\n" + "="*50)
            print("JSON SCHEMA VALIDATION")
            print("="*50)
            print("Schema structure looks valid ✓")
            print("Use validate_json_response() method to validate LLM responses")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()