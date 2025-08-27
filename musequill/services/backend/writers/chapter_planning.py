
from typing import Dict, Any, Optional
from pathlib import Path
import logging
import json
import asyncio
from musequill.services.backend.model import BookModelType
from musequill.services.backend.llm import LLMService
from musequill.services.backend.context import LLMContextManager
from musequill.services.backend.prompts import (
    ChapterPlanningInputs,
    ChapterPlanningPromptGenerator
)
from musequill.services.backend.utils import (
    generate_filename,
    seconds_to_time_string
)
from musequill.services.backend.writers.chapter_planning_model import GenericPlan

from musequill.services.backend.utils.payloads import extract_json_from_response

from musequill.services.backend.validators import (
    PlanBaselines,
    validate_plan_against_baselines,
    ValidationResult,
    ValidationIssue
)

logger = logging.getLogger(__name__)

async def generate_chapter_plan(
    ctx_mgr: LLMContextManager,
    llm_service: LLMService,
    book_model: BookModelType,
    book_id: str,
    output_path: Path,
    book_dna: str,
    blueprint: Dict[str, Any],
    book_summary: str,
    research_data: Dict[str, Any]
) -> Optional[GenericPlan]:
    """
    Generate high-level chapter plan using all available artifacts.
    
    Args:
        ctx_mgr: Context manager for storage
        llm_service: LLM service for generation
        book_model: Book model data
        book_id: Unique book identifier
        output_path: Output directory path
        book_dna: Generated book DNA string
        blueprint: Generated blueprint data
        book_summary: Generated book summary
        research_data: Generated research data
        
    Returns:
        Generated chapter plan JSON string
    """
    
    logger.info("\n📋 Generating High-Level Chapter Plan...")
    

    # Create inputs for chapter planning
    planning_inputs = ChapterPlanningInputs(
        book_model=book_model,
        book_dna=book_dna,
        blueprint=blueprint,
        book_summary=book_summary,
        research_data=research_data,
        book_id=book_id
    )
    
    # Generate prompt
    prompt = ChapterPlanningPromptGenerator.generate_prompt(planning_inputs)
    
    with open(generate_filename(output_path, prefix="chapter-plan-prompt", extension="md"), 'w', encoding='utf-8') as f:
        f.write(prompt)

    # Get prompt statistics and configure LLM
    stats = ChapterPlanningPromptGenerator.get_prompt_statistics(planning_inputs)
    logger.info(f"📊 Chapter Planning Prompt Stats: {stats['prompt_word_count']} words, ~{stats['estimated_tokens']} tokens")
    
    recommended_settings = stats.get('recommended_model_settings', {})
    if recommended_settings:
        logger.info("🔧 Applying recommended model settings for chapter planning...")
        try:
            await llm_service.update_default_parameters(
                **recommended_settings
            )
        except Exception as e:
            logger.error(f"🔴 Failed to update LLM parameters: {e}")
            logger.info("🔄 Using default parameters...")

    chapter_plan: Optional[GenericPlan] = None
    # Generate chapter plan
    while True:
        
        logger.info("🤖 Generating chapter plan...")
        response = await llm_service.generate([prompt])
        
        if response.get('timelapse', 0):
            logger.info(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        
        # Save raw response
        response_filename = generate_filename(
            output_path,
            prefix="chapter-plan-response-raw",
            extension="json"
        )
        raw_response = extract_json_from_response(response['response'])
        with open(response_filename, 'w', encoding='utf-8') as f:
            json.dump(raw_response, f, indent=2, ensure_ascii=False)

        try:
            chapter_plan = GenericPlan(**raw_response)
            baselines = PlanBaselines(
                title=book_model.book.title,
                author=book_model.book.author,
                allowed_genres={book_model.genre.primary.type,book_model.genre.sub.type},
                disallowed_genres={"Thriller","Sci-Fi","Fantasy","Journalism"},
                required_entities={"Noah Bennett","Dr. Ava Kline"},
                forbidden_terms={"spaceship","dragon","time portal"},
                min_characters=2,
                min_chapters=12,
                min_beats=6,
                preferred_theme_keywords={"self-honesty","obligation"},
                preferred_setting_keywords={"New York","NYC","Manhattan"},
                max_logline_chars=280,
                require_empty_fields={}  # add paths -> [] if you extend the model with such fields
            )

            result = validate_plan_against_baselines(chapter_plan.model_dump(), baselines)

            if not result.is_valid or result.regenerate:
                # Feed result.refined_prompt back to your LLM along with the original artifacts
                print(result.score, [f"{i.severity}:{i.code}" for i in result.issues])
                prompt = result.refined_prompt
                continue
            else:
                print("Plan accepted. Score:", result.score)
                break

        except Exception as e:
            logger.error(f"🔴 Failed to parse chapter plan: {e}")
            logger.info("🔄 Retrying...")
            await asyncio.sleep(1)
            continue

    logger.info("✅ Chapter plan validation passed")
            
    return chapter_plan
    
