#!/usr/bin/env python3
"""
Chapter Planning Prompt Generator

Generates optimized prompts for creating high-level chapter plans from book artifacts.
Integrates Book DNA, Blueprint, Summary, and Research data to produce comprehensive
chapter-by-chapter planning structures.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import re
from musequill.services.backend.model.book import BookModelType
from musequill.services.backend.model import (
    CHAPTER_PLANNING_SCHEMA, 
    EXAMPLE_CHAPTER_PLAN,
    HighLevelChapterPlan
)
from musequill.services.backend.utils import (
    clean_json_string,
    extract_json_from_response,
    dict_to_markdown
)


@dataclass
class ChapterPlanningInputs:
    """Container for all inputs needed for chapter planning."""
    book_model: BookModelType
    book_dna: str
    blueprint: Dict[str, Any]
    book_summary: str
    research_data: Dict[str, Any]
    book_id: str


class ChapterPlanningPromptGenerator:
    """
    Generates prompts for high-level chapter planning using all available book artifacts.
    """

    SYSTEM_PROMPT = """
You are a meticulous book planner and creative writer.

"""


    PLANNING_INSTRUCTIONS = """
Your task: Produce a complete, commercially viable high-level chapter plan according to BOOK MODEL and BOOK PLAN.
The output you produce will help you in the future tasks to write chapter content - the output should be helpful to you in the future.

"""

    @classmethod
    def generate_prompt(cls, inputs: ChapterPlanningInputs) -> str:
        """
        Generate complete chapter planning prompt from book artifacts.
        
        Args:
            inputs: ChapterPlanningInputs containing all necessary data
            
        Returns:
            Complete formatted prompt string
        """
        from musequill.services.backend.writers import (
            GenericPlan
        )

        output_schema = GenericPlan.model_json_schema()
        book_model = inputs.book_model.to_markdown()
        book_dna = inputs.book_dna
        blueprint = inputs.blueprint
        book_summary = inputs.book_summary
        # formatted_research = "\n\n".join(
        #     f"\t* {k}:\n" + "\n".join(f"\t\t - {x}" for x in (v or []))
        #     for k, v in sorted(inputs.research_data.items())
        # )

        # No fenced code blocks around JSON or schema; models sometimes copy the fences verbatim.
        blueprint_json = json.dumps(blueprint, ensure_ascii=False, indent=2)
        book_plan_md = dict_to_markdown(blueprint, title=inputs.book_model.book.title)
        complete_prompt = f"""{cls.SYSTEM_PROMPT}

{cls.PLANNING_INSTRUCTIONS}

### BOOK MODEL (authoritative data, DO NOT CONTRADICT)
---
{book_model}
---

### BOOK PLAN (authoritative data, DO NOT CONTRADICT)
---
{book_plan_md}
---

### BOOK SUMMARY (authoritative data, DO NOT CONTRADICT)
{book_summary}


### JSON OUTPUT SCHEMA:
{output_schema}

HARD RULES
- Title = "{inputs.book_model.book.title}"; Author = "{inputs.book_model.book.author}"
- Leads = "{inputs.book_model.characters.protagonist}" (no substitutes)
    {"".join([f"\t* {c}\n"  for c in inputs.book_model.characters.protagonists])}
- Genre = "{inputs.book_model.genre.primary.type}"; sub_genre = "{inputs.book_model.genre.sub.type}" only
- Technology = "{inputs.book_model.technology.type}: {inputs.book_model.technology.description}"
- Time Period = "{inputs.book_model.world.type}: {inputs.book_model.world.description}"
- Output exactly one valid JSON object following schema shape
- Only produce JSON output, do not add anything else
- Number of chapters in your output mast match the number of chapters in BOOK PLAN: tread accordingly

Now generate the complete JSON object.
"""

        return complete_prompt

    
    @classmethod
    def _format_book_context(cls, inputs: ChapterPlanningInputs) -> str:
        """Format book model information for context."""
        book = inputs.book_model

        return f"""**Book**: "{book.book.title}" by {book.book.author}
**Genre**: {book.genre.primary.type} / {book.genre.sub.type}
**Audience**: {book.audience.type} (Ages {book.audience.age})
**Length**: {book.book.length}
**Structure**: {book.structure.type}
**Conflict**: {book.conflict.type}
**POV**: {book.pov.type}
**Tone**: {book.tone.type}
**Pace**: {book.pace.type}
**World**: {book.world.type}
**Style**: {book.writing_style}

**Main Characters**: {book.characters.protagonist}

{'\n'.join(
    f"**Protagonist**: {v}"
    for v in book.characters.protagonists
    if isinstance(v, str) and v.strip()
)}

**Story Concept**: {book.book.idea}

**Research Areas**: {', '.join([r.type for r in book.research])}"""

    @classmethod
    def _format_artifact_context(cls, inputs: ChapterPlanningInputs) -> str:
        """Format all available artifacts for context."""
        
        # Format research summary
        research_summary:str = ""
        if inputs.research_data:
            for k, v in inputs.research_data.items():
                k = re.sub(r"\s+", " ", k.replace("_", " ")).strip().upper()
                research_summary += f"- {k}: {'; '.join(v)}\n"
        
        # Format blueprint summary
        blueprint_summary = "No blueprint available"
        if inputs.blueprint:
            phases = []
            for key in inputs.blueprint['blueprint'].keys():
                if key.startswith('phase_'):
                    phases.append(f"- {key}: Available")
            if phases:
                blueprint_summary = f"7-phase blueprint available:\n" + "\n".join(phases)
        
        return f"""### Book DNA
{inputs.book_dna}

### Book Summary
{inputs.book_summary[:500]}{"..." if len(inputs.book_summary) > 500 else ""}

### Blueprint Status
{blueprint_summary}

### Research Data
{research_summary}"""

    @classmethod
    def _format_schema_context(cls) -> str:
        """Format the JSON schema for the prompt."""
        return json.dumps(CHAPTER_PLANNING_SCHEMA, indent=2, ensure_ascii=False)

    @classmethod
    def create_from_files(cls, 
                         book_model_path: str,
                         book_dna_path: str,
                         blueprint_path: str,
                         summary_path: str,
                         research_path: str,
                         book_id: str) -> str:
        """
        Create chapter planning prompt from file paths.
        
        Args:
            book_model_path: Path to book model JSON
            book_dna_path: Path to book DNA text file
            blueprint_path: Path to blueprint JSON
            summary_path: Path to summary markdown
            research_path: Path to research JSON
            book_id: Unique book identifier
            
        Returns:
            Complete chapter planning prompt
        """
        # Load book model
        with open(book_model_path, 'r', encoding='utf-8') as f:
            book_model_data = json.load(f)
        book_model = BookModelType(**book_model_data)
        
        # Load book DNA
        with open(book_dna_path, 'r', encoding='utf-8') as f:
            book_dna = f.read().strip()
        
        # Load blueprint
        with open(blueprint_path, 'r', encoding='utf-8') as f:
            blueprint = json.load(f)
        
        # Load summary
        with open(summary_path, 'r', encoding='utf-8') as f:
            book_summary = f.read()
        
        # Load research data
        with open(research_path, 'r', encoding='utf-8') as f:
            research_data = json.load(f)
        
        # Create inputs
        inputs = ChapterPlanningInputs(
            book_model=book_model,
            book_dna=book_dna,
            blueprint=blueprint,
            book_summary=book_summary,
            research_data=research_data,
            book_id=book_id
        )
        
        return cls.generate_prompt(inputs)

    @classmethod
    def get_prompt_statistics(cls, inputs: ChapterPlanningInputs) -> Dict[str, Any]:
        """
        Get statistics about the generated prompt.
        
        Args:
            inputs: ChapterPlanningInputs for analysis
            
        Returns:
            Dictionary containing prompt statistics
        """
        prompt = cls.generate_prompt(inputs)
        
        words = prompt.split()
        word_count = len(words)
        estimated_tokens = int(word_count * 1.33)  # Rough estimation
        
        return {
            'prompt_word_count': word_count,
            'estimated_tokens': estimated_tokens,
            'book_title': inputs.book_model.book.title,
            'genre': f"{inputs.book_model.genre.primary.type}/{inputs.book_model.genre.sub.type}",
            'target_length': inputs.book_model.book.length,
            'research_areas': len(inputs.research_data.get('research_areas', [])) if inputs.research_data else 0,
            'has_blueprint': bool(inputs.blueprint),
            'has_book_dna': bool(inputs.book_dna),
            "recommended_model_settings": {
                "temperature": 0.12,
                "top_p": 0.88,
                "top_k": 80,
                "repeat_penalty": 1.07,
                "max_tokens": 25000,
                "seed": 42,
                "response_format": "json"
            }
        }

    @classmethod
    def validate_output(cls, response_text: str) -> Dict[str, Any]:
        """
        Validate LLM response against the expected schema.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Validation results dictionary
        """
        try:
            # Try to parse JSON
            response_json = extract_json_from_response(response_text)
            
            # Try to validate against Pydantic model
            validated_plan = HighLevelChapterPlan(**response_json)
            
            return {
                'is_valid': True,
                'parsed_successfully': True,
                'validation_passed': True,
                'chapter_count': len(validated_plan.chapter_outline),
                'hero_journey_beats': len(validated_plan.hero_journey_beats),
                'research_items': len(validated_plan.research_checklist),
                'themes_count': len(validated_plan.themes),
                'error': None
            }
            
        except json.JSONDecodeError as e:
            return {
                'is_valid': False,
                'parsed_successfully': False,
                'validation_passed': False,
                'error': f"JSON parsing failed: {str(e)}"
            }
        except Exception as e:
            return {
                'is_valid': False,
                'parsed_successfully': True,
                'validation_passed': False,
                'error': f"Schema validation failed: {str(e)}"
            }
