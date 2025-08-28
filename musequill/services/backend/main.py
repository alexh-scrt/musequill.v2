#!/usr/bin/env python3
"""
Main script to load and convert JSON templates to BookModelType.

Usage:
    python main.py --template <template_name>
    python main.py -t <template_name>

Example:
    python main.py --template children_fantasy
"""
import asyncio
import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, cast, Iterable, Tuple
import logging
from hashlib import sha256
from uuid import uuid4
import time 

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from musequill.config import (
    Settings,
    get_settings
)

# Import our book model
from musequill.services.backend.model.book import BookModelType
from musequill.services.backend.prompts import (
    BookSummaryPromptGenerator,
    BookSummaryConfig,
    BlueprintPromptGenerator,
    PlanningPromptGenerator,
    PlanningConfig,
    ResearchPromptGenerator,
    generate_validation_prompt,
    BookDNAInputs,
    BookDNAPromptGenerator,
    BookPlanConfig,
    BookPlanPromptGenerator
)
from musequill.services.backend.llm.ollama_client import (
    create_llm_service,
    LLMService
)

from musequill.services.backend.utils import (
    generate_filename,
    seconds_to_time_string,
    extract_json_from_response,
    tick,
    load_chapter_briefs
)

from musequill.services.backend.researcher import (
    ResearcherAgent,
    ResearcherConfig,
    ResearchQuery,
    ResearchResults,
    SearchResult
)

from musequill.services.backend.context import (
    LLMContextManager,
)

from musequill.services.backend.integration import (
    create_llm_context_manager
)

from musequill.services.backend.writers import (
    generate_chapter_plan,
    ValidationPolicy,
    validate_output_generic,
    ValidationError
)

from musequill.services.backend.process_results import (
    extract_research_results_by_category
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend_service.log')
    ]
)

logger = logging.getLogger(__name__)

def load_template(template_name: str) -> Optional[dict]:
    """
    Load a JSON template from the templates directory.
    
    Args:
        template_name: Name of the template file (without .json extension)
        
    Returns:
        Dictionary containing the template data, or None if file not found
    """
    # Construct the path to the template file
    template_path = Path("musequill/services/backend/templates") / f"{template_name}.json"
    
    try:
        if not template_path.exists():
            logger.error(f"Error: Template file '{template_path}' not found.")
            return None
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
            
        logger.info(f"Successfully loaded template: {template_path}")
        return template_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON in template file '{template_path}': {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading template '{template_path}': {e}")
        return None


def convert_to_book_model(template_data: dict) -> Optional[BookModelType]:
    """
    Convert template data to BookModelType instance.
    
    Args:
        template_data: Dictionary containing the template data
        
    Returns:
        BookModelType instance, or None if conversion fails
    """
    try:
        book_model = BookModelType(**template_data)
        logger.info("Successfully converted template to BookModelType")
        return book_model
        
    except Exception as e:
        logger.error(f"Error converting template to BookModelType: {e}")
        return None


def display_book_info(book_model: BookModelType) -> None:
    """
    Display key information from the book model.
    
    Args:
        book_model: BookModelType instance to display
    """
    print("\n" + "="*60)
    print("📖 BOOK INFORMATION 📖")
    print("="*60)
    
    print(f"Title: {book_model.book.title}")
    print(f"Author: {book_model.book.author}")
    print(f"Type: {book_model.book.type}")
    print(f"Length: {book_model.book.length}")
    print(f"Language: {book_model.book.language}")
    
    print(f"\nGenre: {book_model.genre.primary.type} / {book_model.genre.sub.type}")
    print(f"Audience: {book_model.audience.type} (Age: {book_model.audience.age})")
    print(f"Writing Style: {book_model.writing_style}")
    
    print(f"\nStructure: {book_model.structure.type}")
    print(f"Plot Type: {book_model.plot.type}")
    print(f"Conflict: {book_model.conflict.type}")
    print(f"POV: {book_model.pov.type}")
    print(f"Tone: {book_model.tone.type}")
    print(f"Pace: {book_model.pace.type}")
    print(f"World: {book_model.world.type}")
    print(f"Style: {book_model.style.type}")
    
    print(f"\nResearch Areas:")
    for research in book_model.research:
        print(f"  - {research.type}: {research.description}")
    
    print(f"\n📚 Book Idea:")
    # Wrap long text for better readability
    idea_words = book_model.book.idea.split()
    lines = []
    current_line = []
    for word in idea_words:
        if len(' '.join(current_line + [word])) <= 80:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    for line in lines:
        print(f"  {line}")

def save_research_data(data: Dict[str, Any], filename: str):
    """Save research data with ResearchQuery objects to JSON."""
    
    class ResearchEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, '__dict__'):
                return obj.__dict__  # Convert any object with attributes to dict
            elif hasattr(obj, 'value'):  # Handle enums
                return obj.value
            return str(obj)  # Fallback to string
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, cls=ResearchEncoder)

async def main():
    logger.info("🚀  Starting backend service...")
    logger.info("🏗️  Loading configuration...")
    config = get_settings()
    start = time.perf_counter()
    logger.info(f"✅  Loaded configuration: {config.model_dump_json(indent=2)}")
    parser = argparse.ArgumentParser(
        description="Load and convert JSON templates to BookModelType",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --template children_fantasy
  python main.py -t adventure_story
  python main.py --template mystery_novel
        """
    )
    
    parser.add_argument(
        '--template', '-t',
        type=str,
        required=True,
        help='Name of the template file (without .json extension)'
    )
    
    parser.add_argument(
        '--output', '-o',
        action='store_true',
        help='Write products to output (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--stats', 
        action='store_true',
        help='Show statistics'
    )

    
    args = parser.parse_args()
    
    if args.verbose:
        logger.info(f"🏗️  Loading template: {args.template}")
        logger.info(f"Template path: musequill/services/backend/templates/{args.template}.json")
    
    # Load the template
    template_data = load_template(args.template)
    if template_data is None:
        sys.exit(1)
    
    # Convert to BookModelType
    book_model = convert_to_book_model(template_data)
    if book_model is None:
        sys.exit(1)
    
    # Display book information
    display_book_info(book_model)

    book_id = str(uuid4())
    logger.info(f'🆕  New book id: {book_id}')

    # Save to output file if specified
    if args.output:
        try:
            output_path = Path('musequill/services/backend/outputs')
            output_path.mkdir(parents=True, exist_ok=True)
            book_model_filename = generate_filename(
                output_path,
                prefix="book_model",
                extension="json"
            )
            with open(book_model_filename, 'w', encoding='utf-8') as f:
                json.dump(book_model.model_dump(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"\nBook model saved to: {output_path}")
            
        except Exception as e:
            logger.info(f"Error saving to output file '{args.output}': {e}")
            sys.exit(1)
    
    logger.info(f"\n✅ Successfully processed template: {args.template}")

    try:
        logger.info('Creating LLM Context Manager...')
        ctx_mgr:LLMContextManager = await create_llm_context_manager()
        logger.info("✅ LLM Context Manager initialized")

        recommended_model_settings: Optional[dict] = None
        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/outputs')
        output_path.mkdir(parents=True, exist_ok=True)

        # BOOK SUMMARY
        logger.info("\n📚 Generating Book Summary...")
        bspg = BookSummaryPromptGenerator()
        book_data = book_model.model_dump()
        prompt = bspg.generate_prompt(book_data)

        prompt_filename = generate_filename(
            output_path,
            prefix="summary-prompt",
            extension="md"
        )
        # save book summary prompt
        bspg.save_prompt_to_file(prompt, prompt_filename)
        # get prompts stats
        stats = bspg.get_prompt_statistics(prompt, book_model.model_dump())
        stats['prompt'] = f'{prompt[:60]+"..." if len(prompt)>60 else prompt}'
        stats['prompt_length'] = len(prompt)
        stats['prompt_file'] = prompt_filename
        prompt_str: str = json.dumps(stats, indent=2)

        logger.info(f"\n📝 Book Summary Prompt:\n{prompt_str}")

        recommended_model_settings = stats.get('recommended_model_settings')
        if recommended_model_settings:
            logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
            # update the llm with the prompt recommended settings
            await llm_service.update_default_parameters(
                temperature=recommended_model_settings.get('temperature', 0.7),
                max_tokens=recommended_model_settings.get('max_tokens', 5000),
                top_p=recommended_model_settings.get('top_p', 0.5),
                top_k=recommended_model_settings.get('top_k', 40),
                repeat_penalty=recommended_model_settings.get('repeat_penalty', 1.1),
                stop=recommended_model_settings.get("stop")
            )
        else:
            logger.info("ℹ️  No recommended model settings found, using defaults")
            # prompt stats not available - use default
            await llm_service.update_default_parameters(
                temperature=0.7,
                max_tokens=5000,
                top_p=0.5,
                top_k=40,
                repeat_penalty=1.1,
                stop=None
            )
        # generate book summary response
        logger.info("🤖 Generating book summary...")
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        # save book summary
        response_filename = generate_filename(
            output_path,
            prefix="summary-response",
            extension="md"
        )
        with open(response_filename, 'w', encoding='utf-8') as f:
            f.write(response['response'])

        book_summary = response['response']
        flag = await ctx_mgr.store(
            book_id=book_id,
            as_vector=False, # Redis in-mem store
            metadata=book_model,
            content_id="book_summary",
            content=response['response'],
        )
        if not flag:
            logger.error("🔴  Failed to store book summary")
            sys.exit(1)
        logger.info(f'📝  Book summary stored to {ctx_mgr.__class__.__name__}')
        

        # # Blueprint Generation
        # logger.info("\n📚 Generating Book Blueprint...")
        # prompt = BlueprintPromptGenerator.generate_prompt(book_model)
        # stats = BlueprintPromptGenerator.get_prompt_statistics(book_model)
        # recommended_model_settings = stats.get('recommended_model_settings')
        # if recommended_model_settings:
        #     logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
        #     # update the llm with the prompt recommended settings
        #     await llm_service.update_default_parameters(
        #         temperature=recommended_model_settings.get('temperature', 0.3),
        #         max_tokens=recommended_model_settings.get('max_tokens', 4000),
        #         top_p=recommended_model_settings.get('top_p', 0.9)
        #     )
        # response_filename = generate_filename(
        #     output_path,
        #     prefix="blueprint-prompt",
        #     extension="md"
        # )
        # with open(response_filename, 'w', encoding='utf-8') as f:
        #     f.write(prompt)

        # logger.info(
        #     "🤖 Generating book blueprint..."
        #     f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        # )

        correction:str = ""
        #while True:
        #    try:
        #         response = await llm_service.generate([prompt + correction])
        #         if response.get('timelapse', 0):
        #             print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        #         valid, payload = BlueprintPromptGenerator.validate_json_response(response['response'])
        #         if valid:
        #             break
        #         logger.error(f"🔴  LLM Response is not valid JSON: {payload}")
        #         correction = f"""You are to correct the following errors that did not pass the validation on compliance with the TARGET JSON SCHEMA:\n
        #                 {payload}
        #                 Your invalid output that you need to correct:\n
        #                 {response['response']}
        #                 """
        #         await asyncio.sleep(5)
        #     except Exception as e:
        #         logger.error(f"🔴  LLM Error: {e}")
        #         logger.info("🔄  Retrying...")
        #         await asyncio.sleep(1)

        # json_payload = extract_json_from_response(response['response'])
        # response_filename = generate_filename(
        #     output_path,
        #     prefix="blueprint-response",
        #     extension="json"
        # )
        # with open(response_filename, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(json_payload))
        # book_blueprint = json.dumps(json_payload, indent=2)
        # flag = await ctx_mgr.store(
        #     book_id=book_id,
        #     metadata=book_model,
        #     as_vector=False,
        #     content_id="book_blueprint",
        #     content=json.dumps(json_payload),
        # )
        # if not flag:
        #     logger.error("🔴 Failed to store book summary")
        #     sys.exit(1)
        # logger.info(f'📝  Book blueprint stored to {ctx_mgr.__class__.__name__}')

        # Planning
        logger.info("\n📚 Generating Book Planning...")
        generator = BookPlanPromptGenerator(BookPlanConfig(
            include_examples=True,
            detail_level="comprehensive",
        ))

        prompt = generator.generate_BookPlan_prompt(book_model, book_summary)
        # send `prompt` to your LLM with the recommended settings:
        stats = generator.get_prompt_stats(prompt, payload={
            # optional: if you already compute a staged payload elsewhere, pass it in
            "phase1": {"genre": f"{book_model.genre.primary.type}", "audience": f"{book_model.audience.type}", "length": book_model.book.length},
            "phase2": {"structure": book_model.structure.type},
            "phase3": {"world": book_model.world.description, "technology": book_model.technology.description},
            "phase4": {"characters": {"protagonists": book_model.characters.protagonists}},
            "research": [{"context": r.context, "type": r.type} for r in book_model.research]
        })

        generator.save_prompt_to_file(prompt, generate_filename(
            output_path,
            prefix="plan-prompt",
            extension="md"
        ))
        recommended_model_settings = stats.get('recommended_model_settings')
        if recommended_model_settings:
            logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
            # update the llm with the prompt recommended settings
            await llm_service.update_default_parameters(**recommended_model_settings)

        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        with open(
            generate_filename(
                output_path,
                prefix="plan-response",
                extension="json"
        ), 'w', encoding='utf-8') as f:
            json.dump(json.loads(response['response']), f, indent=2, ensure_ascii=False)





        # pc = PlanningConfig()
        # ppg = PlanningPromptGenerator(pc)
        # prompt = ppg.generate_planning_prompt(json_payload)
        # prompt_filename = generate_filename(
        #     output_path,
        #     prefix="plan",
        #     extension="txt"
        # )
        # ppg.save_prompt_to_file(prompt, prompt_filename)
        # stats = ppg.get_prompt_stats(prompt)
        # recommended_model_settings = stats.get('recommended_model_settings')
        # if recommended_model_settings:
        #     logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
        #     # update the llm with the prompt recommended settings
        #     await llm_service.update_default_parameters(
        #         temperature=recommended_model_settings.get('temperature', 1.3),
        #         max_tokens=recommended_model_settings.get('max_tokens', 5000),
        #         top_p=recommended_model_settings.get('top_p', 0.5),
        #         top_k=recommended_model_settings.get('top_k', 40),
        #         repeat_penalty=recommended_model_settings.get('repeat_penalty', 1.1),
        #         stop=recommended_model_settings.get("stop"),
        #     )
        # else:
        #     logger.info("ℹ️  No recommended model settings found, using defaults")
        #     await llm_service.update_default_parameters(
        #         temperature=1.3,
        #         max_tokens=5000,
        #         top_p=0.5
        #     )
        # logger.info(
        #     "🤖 Generating book plan..."
        #     f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        # )
        # response = await llm_service.generate([prompt])
        # if response.get('timelapse', 0):
        #     print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        # plan_filename = generate_filename(
        #     output_path,
        #     prefix="plan",
        #     extension="md"
        # )
        # with open(plan_filename, 'w', encoding='utf-8') as f:
        #     f.write(response['response'])

        book_plan = response['response']
        flag = await ctx_mgr.store(
            book_id=book_id,
            metadata=book_model,
            as_vector=False,
            content_id="book_plan",
            content=book_plan,
        )
        if not flag:
            logger.error("🔴 Failed to store book plan")
            sys.exit(1)
        logger.info(f'📝  Book plan stored to {ctx_mgr.__class__.__name__}')

        # Research
        logger.info("\n📚 Generating Book Research...")
        book_plan_json:Dict[str, Any] = json.loads(book_plan)
        prompt = ResearchPromptGenerator.generate_prompt(book_model, book_summary, book_plan_json)
        await llm_service.update_default_parameters(
            temperature=0.1,
            max_tokens=5000,
            top_p=0.5
        )

        logger.info(
            "🤖 Generating book research..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        json_payload = extract_json_from_response(response['response'])
        json_str = json.dumps(json_payload)
        with open(generate_filename(
            output_path,
            prefix="research-query",
            extension="json"
        ), 'w', encoding='utf-8') as f:
            json.dump(json_payload, f, indent=2, ensure_ascii=False)

        researcher_config = ResearcherConfig()
        researcher = ResearcherAgent(researcher_config)
        research_results = await researcher.execute_research(book_id, ResearchQuery.load_research_queries(json_str))

        research_result_filename = generate_filename(
            output_path,
            prefix="research-result",
            extension="json"
        )
        
        # Extract tavily_answer values for JSON serialization
        def extract_tavily_answers(detailed_results:Dict[str, List[ResearchResults]]):
            extracted_data = {}
            for query_type, result_list in detailed_results.items():
                tavily_answers = []
                for result in result_list:
                    for sr in cast(Iterable[SearchResult], result.search_results):
                        tavily_answers.append(f'{sr.title}: {sr.content}')
                extracted_data[query_type] = tavily_answers
            return extracted_data
        
        research_tavily_data = extract_tavily_answers(research_results.get('detailed_results', {}))
        save_research_data(research_tavily_data, research_result_filename)
        
        flag = await ctx_mgr.store(
            book_id=book_id,
            metadata=book_model,
            as_vector=False,
            content_id="research_results",
            content=json.dumps(research_tavily_data),
        )
        if not flag:
            logger.error("🔴 Failed to store book research")
            sys.exit(1)
        logger.info(f'📝  Research results stored to {ctx_mgr.__class__.__name__}')

        research_types: list[tuple[str, str]] = [
            (k, v[0]) for k, v in research_tavily_data.items() if v
        ]
        # Book DNA
        logger.info("\n📚 Generating Book DNA...")

        dna_input = BookDNAInputs(**{
            'book_model': book_model,
            'book_blueprint': json.loads(book_blueprint),
            'research_topics': research_types,
            'book_summary': book_summary,
            'book_id': book_id
        })

        prompt = BookDNAPromptGenerator.generate_dna_prompt(dna_input)
        await llm_service.update_default_parameters(
            temperature=1.3,
            max_tokens=800,
            top_k=10,
            top_p=0.9,
            repeat_penalty=1.1
        )

        logger.info(
            "🤖 Generating book dna..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        book_dna = response['response']
        flag = await ctx_mgr.store(
            book_id=book_id,
            metadata=book_model,
            as_vector=False,
            content_id="book_dna",
            content=book_dna
        )
        if not flag:
            logger.error("🔴 Failed to store book dna")
            sys.exit(1)
        logger.info(f'📝  Book DNA stored to {ctx_mgr.__class__.__name__}')

        book_dna_filename = generate_filename(
            output_path,
            prefix="book-dna",
            extension="md"
        )
        with open(book_dna_filename, 'w', encoding='utf-8') as f:
            f.write(book_dna)

        # Chapter Planning
        logger.info("\n📚 Generating Book Chapter Planning...")
        # Chapter Planning Generation
        chapter_plan = await generate_chapter_plan(
            ctx_mgr=ctx_mgr,
            llm_service=llm_service,
            book_model=book_model,
            book_id=book_id,
            output_path=output_path,
            book_dna=book_dna,  # From previous step
            blueprint=json.loads(book_blueprint),   # From blueprint generation step
            book_summary=book_summary,    # From summary generation step
            research_data=research_tavily_data   # From research generation step
        )
        
        if chapter_plan:
            logger.info("✅ Chapter planning completed successfully")
            
            # Parse the chapter plan for further use
            try:
                chapter_plan_data = json.loads(chapter_plan)
                
                # Display some key information
                project_info = chapter_plan_data.get('project', {})
                chapter_outline = chapter_plan_data.get('chapter_outline', [])
                themes = chapter_plan_data.get('themes', [])
                
                logger.info(f"📖 Title: {project_info.get('title', 'Unknown')}")
                logger.info(f"👤 Author: {project_info.get('author', 'Unknown')}")
                logger.info(f"📊 Chapters planned: {len(chapter_outline)}")
                logger.info(f"🎯 Core themes: {len(themes)}")
                
                if themes:
                    logger.info("📝 Themes identified:")
                    for i, theme in enumerate(themes[:3], 1):  # Show first 3 themes
                        logger.info(f"   {i}. {theme}")
                
                # Show first few chapters
                if chapter_outline:
                    logger.info("\n📋 First few chapters:")
                    for chapter in chapter_outline[:3]:  # Show first 3 chapters
                        ch_num = chapter.get('ch', '?')
                        title = chapter.get('title', 'Untitled')
                        goal = chapter.get('external_goal', 'No goal specified')
                        logger.info(f"   Ch{ch_num}: {title} - {goal}")
                
            except json.JSONDecodeError:
                logger.error("❌ Could not parse chapter plan JSON for display")
        
        else:
            logger.error("❌ Chapter planning failed")
            # You might want to continue with other steps or exit here


        stop = time.perf_counter()
        lapse = tick(start, stop)
        print(f'DONE in {lapse}')
    except Exception as e:
        logger.error(f"Error: {e}")

async def book_research():
    try:
        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        book_id = str(uuid4())
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan_json = json.load(f)
        with open(output_path.joinpath('book_model.json')) as f:
            book_model:BookModelType = json.load(f)
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read

        logger.info("\n📚 Generating Book Research...")
        prompt = ResearchPromptGenerator.generate_prompt(book_model, book_summary, book_plan_json)
        await llm_service.update_default_parameters(
            temperature=0.1,
            max_tokens=5000,
            top_p=0.5
        )

        logger.info(
            "🤖 Generating book research..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        json_payload = extract_json_from_response(response['response'])
        json_str = json.dumps(json_payload)
        with open(generate_filename(
            output_path,
            prefix="research-query",
            extension="json"
        ), 'w', encoding='utf-8') as f:
            json.dump(json_payload, f, indent=2, ensure_ascii=False)

        researcher_config = ResearcherConfig()
        researcher = ResearcherAgent(researcher_config)
        research_results = await researcher.execute_research(book_id, ResearchQuery.load_research_queries(json_str))

        research_result_filename = generate_filename(
            output_path,
            prefix="research-result",
            extension="json"
        )
        save_research_data(research_results, research_result_filename)

    except Exception as e:
        logger.error(f"Error: {e}")

async def process_results():
    try:
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        with open(output_path.joinpath('research-result.json')) as f:
            research_result_json = json.load(f)
        refined_research_results = extract_research_results_by_category(research_result_json)
        with open(generate_filename(
            output_path,
            prefix="refined-research-result",
            extension="json"
        ), 'w', encoding='utf-8') as f:
            json.dump(refined_research_results, f, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Error: {e}")

async def generate_book_dna():

    try:
        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        book_id = str(uuid4())
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan = json.load(f)
        with open(output_path.joinpath('book_model.json')) as f:
            book_model:BookModelType = json.load(f)
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read()
        with open(output_path.joinpath('refined-research-results.json')) as f:
            research_results = json.load(f)

        # Book DNA
        logger.info("\n📚 Generating Book DNA...")

        dna_input = BookDNAInputs(**{
            'book_model': book_model,
            'book_blueprint': book_plan,
            'research_topics': research_results,
            'book_summary': book_summary,
            'book_id': book_id
        })

        prompt = BookDNAPromptGenerator.generate_dna_prompt(dna_input)
        await llm_service.update_default_parameters(
            temperature=1.3,
            max_tokens=800,
            top_k=10,
            top_p=0.9,
            repeat_penalty=1.1
        )
        with open(generate_filename(
            output_path,
            prefix="book-dna-prompt",
            extension="md"
        ), 'w', encoding='utf-8') as f:
            f.write(prompt)

        logger.info(
            "🤖 Generating book dna..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        book_dna = response['response']

        book_dna_filename = generate_filename(
            output_path,
            prefix="book-dna",
            extension="md"
        )
        with open(book_dna_filename, 'w', encoding='utf-8') as f:
            f.write(book_dna)
    except Exception as e:
        logger.error(f"Error: {e}")

async def chapter_plan():
    try:

        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        book_id = str(uuid4())
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan = json.load(f)
        with open(output_path.joinpath('book_model.json')) as f:
            book_model:BookModelType = BookModelType(**json.load(f))
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read()
        with open(output_path.joinpath('book-dna.md')) as f:
            book_dna = f.read()
        with open(output_path.joinpath('refined-research-results.json')) as f:
            research_results = json.load(f)

        # Chapter Planning
        logger.info("\n📚 Generating Book Chapter Planning...")
        # Chapter Planning Generation
        from musequill.services.backend.writers.chapter_planning_model import GenericPlan
        chapter_plan: Optional[GenericPlan] = await generate_chapter_plan(
            ctx_mgr=None,
            llm_service=llm_service,
            book_model=book_model,
            book_id=book_id,
            output_path=output_path,
            book_dna=book_dna,  # From previous step
            blueprint=book_plan,   # From blueprint generation step
            book_summary=book_summary,    # From summary generation step
            research_data=research_results   # From research generation step
        )
        
        if chapter_plan:
            logger.info("✅ Chapter planning completed successfully")
                # Save validated JSON
            payload = chapter_plan.model_dump_json(indent=2, exclude_none=True)
            with open(generate_filename(str(output_path), prefix="chapter-plan-response", extension="json"), 'w', encoding='utf-8') as f:
                # Pretty print the JSON for readability
                f.write(payload)

    except Exception as e:
        logger.error(f"Error: {e}")

async def chapter_briefs():
    try:
        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        book_id = str(uuid4())
        from musequill.services.backend.writers.chapter_planning_model import GenericPlan
        from musequill.services.backend.writers.book_planning_model import GenericBookPlan
        with open(output_path.joinpath('chapter-plan.json')) as f:
            chapter_plan:GenericPlan = GenericPlan(**json.load(f))
        with open(output_path.joinpath('book_model.json')) as f:
            book_model:BookModelType = BookModelType(**json.load(f))
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan:GenericBookPlan = GenericBookPlan(**json.load(f))
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read()
        with open(output_path.joinpath('book-dna.md')) as f:
            book_dna = f.read()
        with open(output_path.joinpath('refined-research-results.json')) as f:
            research_results = json.load(f)

        from musequill.services.backend.writers.chapter_briefs import make_all_chapter_briefs_from_plan

        briefs = make_all_chapter_briefs_from_plan(
            book_model=book_model,
            book_plan=book_plan,
            chapter_plan=chapter_plan,
            book_summary=book_summary
        )
        for chapter in briefs:
            with open(generate_filename(
                output_path,
                prefix=f"chapter-{chapter['meta']['chapter_number']}-brief",
                extension="json"
            ), 'w', encoding='utf-8') as f:
                json.dump(chapter, f, indent=2, ensure_ascii=False),

    except Exception as e:
        logger.error(f"Error: {e}")

async def writer():
    from musequill.services.backend.writers.chapter_writer import write_all_chapters_with_qc
    try:
        llm_service:LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        book_id = str(uuid4())

        from musequill.services.backend.writers.chapter_planning_model import GenericPlan
        from musequill.services.backend.writers.book_planning_model import GenericBookPlan
        from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
        from musequill.services.backend.utils import coerce_to_model
        from musequill.services.backend.writers.research_model import RefinedResearch
        with open(output_path.joinpath('chapter-plan.json')) as f:
            chapter_plan:GenericPlan = GenericPlan(**json.load(f))
        with open(output_path.joinpath('book_model.json')) as f:
            book_model:BookModelType = BookModelType(**json.load(f))
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan:GenericBookPlan = GenericBookPlan(**json.load(f))
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read()
        with open(output_path.joinpath('book-dna.md')) as f:
            book_dna = f.read()
        with open(output_path.joinpath('refined-research-results.json')) as f:
            research_dict = json.load(f)

        briefs_dict = load_chapter_briefs(output_path)
        briefs: List[GenericChapterBrief] = [
            coerce_to_model(payload, GenericChapterBrief) for _, payload in briefs_dict.items()
        ]

        research = RefinedResearch.from_json_dict(research_dict)

        results = await write_all_chapters_with_qc(
            book_model=book_model,
            book_plan=book_plan,
            chapter_briefs=briefs,          # output from your chapter planner
            book_summary=book_summary,
            research_corpus=research,
            llm=llm_service,
            out_dir="manuscript"
        )


    except Exception as e:
        logger.error(f"Error: {e}")

# enhanced_main.py - Replace your existing writer() function

import asyncio
import json
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Any

# Import your existing modules
from musequill.services.backend.writers.chapter_planning_model import GenericPlan
from musequill.services.backend.writers.book_planning_model import GenericBookPlan
from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.utils import coerce_to_model
from musequill.services.backend.writers.research_model import RefinedResearch
from musequill.services.backend.model import BookModelType
from musequill.services.backend.llm.ollama_client import LLMService, create_llm_service
from musequill.services.backend.utils.loader import load_chapter_briefs

# Import the enhanced chapter writer
from musequill.services.backend.writers.enhanced_chapter_writer import enhanced_write_all_chapters_with_qc

import logging
logger = logging.getLogger(__name__)


async def enhanced_writer():
    """Enhanced writer function with improved context management for coherent chapters."""
    
    try:
        print("🚀 Starting Enhanced Book Writer with Context Memory")
        
        # Initialize LLM service
        llm_service: LLMService = create_llm_service()
        output_path = Path('musequill/services/backend/samples')
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate unique book ID for this run
        book_id = str(uuid4())
        print(f"📚 Book ID: {book_id}")
        
        print("📂 Loading planning artifacts...")
        
        # Load all the planning artifacts
        with open(output_path.joinpath('chapter-plan.json')) as f:
            chapter_plan: GenericPlan = GenericPlan(**json.load(f))
            
        with open(output_path.joinpath('book_model.json')) as f:
            book_model: BookModelType = BookModelType(**json.load(f))
            
        with open(output_path.joinpath('book_plan.json')) as f:
            book_plan: GenericBookPlan = GenericBookPlan(**json.load(f))
            
        with open(output_path.joinpath('book_summary.md')) as f:
            book_summary = f.read()
            
        with open(output_path.joinpath('book-dna.md')) as f:
            book_dna = f.read()
            
        with open(output_path.joinpath('refined-research-results.json')) as f:
            research_dict = json.load(f)
        
        # Load chapter briefs
        briefs_dict = load_chapter_briefs(output_path)
        briefs: List[GenericChapterBrief] = [
            coerce_to_model(payload, GenericChapterBrief) 
            for _, payload in briefs_dict.items()
        ]
        
        # Convert research to proper format
        research = RefinedResearch.from_json_dict(research_dict)
        
        print(f"📋 Loaded {len(briefs)} chapter briefs")
        print(f"🔬 Loaded research corpus with {len(research_dict.get('figures', []))} figures, "
              f"{len(research_dict.get('locales', []))} locations, {len(research_dict.get('topics', []))} topics")
        
        # Enhanced context information
        print("🧠 Initializing Enhanced Context System...")
        print("   ✓ Narrative state tracking")
        print("   ✓ Character development continuity") 
        print("   ✓ Plot thread management")
        print("   ✓ Cross-chapter relationship tracking")
        
        # Prepare output directory
        manuscript_dir = "manuscript"
        Path(manuscript_dir).mkdir(parents=True, exist_ok=True)
        
        print("✍️ Beginning enhanced chapter generation...")
        print("=" * 60)
        
        # Write all chapters with enhanced context management
        results = await enhanced_write_all_chapters_with_qc(
            book_model=book_model,
            book_plan=book_plan,
            chapter_briefs=briefs,
            book_summary=book_summary,
            research_corpus=research,  # This will be converted internally
            llm=llm_service,
            out_dir=manuscript_dir,
            book_id=book_id
        )
        
        print("=" * 60)
        print("📊 Generation Summary:")
        print(f"✅ Successfully generated {len(results)} chapters")
        
        # Calculate statistics
        total_words = sum(r["metadata"]["word_count"] for r in results)
        avg_quality = sum(r["quality_score"] for r in results) / len(results)
        
        print(f"📝 Total words: {total_words:,}")
        print(f"📈 Average quality score: {avg_quality:.2f}/1.0")
        print(f"🎯 Average words per chapter: {total_words // len(results):,}")
        
        # Quality breakdown
        high_quality = sum(1 for r in results if r["quality_score"] >= 0.8)
        medium_quality = sum(1 for r in results if 0.6 <= r["quality_score"] < 0.8)
        low_quality = sum(1 for r in results if r["quality_score"] < 0.6)
        
        print(f"🏆 Quality distribution:")
        print(f"   High (≥0.8): {high_quality} chapters")
        print(f"   Medium (0.6-0.8): {medium_quality} chapters") 
        print(f"   Low (<0.6): {low_quality} chapters")
        
        # Save generation report
        report = {
            "book_id": book_id,
            "generation_timestamp": str(Path().absolute()),
            "total_chapters": len(results),
            "total_words": total_words,
            "average_quality_score": avg_quality,
            "quality_distribution": {
                "high": high_quality,
                "medium": medium_quality, 
                "low": low_quality
            },
            "chapters": [
                {
                    "number": r["metadata"]["chapter_number"],
                    "title": r["metadata"]["chapter_title"],
                    "word_count": r["metadata"]["word_count"],
                    "quality_score": r["quality_score"],
                    "attempts": r["metadata"]["attempts"]
                }
                for r in results
            ]
        }
        
        report_path = Path(manuscript_dir) / f"generation_report_{book_id}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Generation report saved to: {report_path}")
        
        # Context coherence analysis
        print("\n🔗 Context Coherence Analysis:")
        context_manager_state = Path(manuscript_dir) / f"narrative_state_{book_id}.json"
        if context_manager_state.exists():
            with open(context_manager_state, 'r') as f:
                narrative_data = json.load(f)
                
            print(f"   Character states tracked: {len(narrative_data.get('character_states', {}))}")
            print(f"   Plot threads tracked: {len(narrative_data.get('plot_threads', []))}")
            print(f"   Chapter summaries stored: {len(narrative_data.get('chapter_summaries', []))}")
        
        print("🎉 Enhanced book generation completed successfully!")
        print(f"📁 Manuscript saved in: {Path(manuscript_dir).absolute()}")
        
        return results
        
    except Exception as e:
        logger.error(f"Enhanced writer failed: {e}")
        print(f"❌ Error during enhanced generation: {e}")
        raise


if __name__ == "__main__":
    # Run the enhanced writer
    asyncio.run(enhanced_writer())
    
    # Uncomment to run single chapter test instead:
    # asyncio.run(test_enhanced_writer_single_chapter())