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
    BookDNAPromptGenerator
)
from musequill.services.backend.model import (
    BookModelType,
    BookBlueprint,
)
from musequill.services.backend.llm.ollama_client import (
    create_llm_service,
    LLMService
)

from musequill.services.backend.utils import (
    generate_filename,
    seconds_to_time_string,
    extract_json_from_response,
    tick
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
    create_metadata_generator,
    MetadataGenerator,
    MetadataPromptConfig,
)

from musequill.services.backend.integration import (
    create_llm_context_manager
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
    print("BOOK INFORMATION")
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
    
    print(f"\nBook Idea:")
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

    """Main function to handle command line arguments and orchestrate the process."""
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
            
            # Ensure output directory exists
            output_path.parent.mkdir(exist_ok=True)
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

        # BOOK SUMMARY
        logger.info("\n📚 Generating Book Summary...")
        bspg = BookSummaryPromptGenerator()
        book_data = book_model.model_dump()
        prompt = bspg.generate_prompt(book_data)

        output_path.parent.mkdir(exist_ok=True)
        prompt_filename = generate_filename(
            output_path,
            prefix="summary-prompt",
            extension="md"
        )
        # save book summary prompt
        bspg.save_prompt_to_file(prompt, prompt_filename)
        # get prompts stats
        stats = bspg.get_prompt_statistics(book_model.model_dump())
        stats['prompt'] = f'{prompt[:60]+"..." if len(prompt)>60 else prompt}'
        stats['prompt_length'] = len(prompt)
        stats['prompt_file'] = prompt_filename
        prompt_str: str = json.dumps(stats, indent=2)

        logger.info(f"\n📝 Book Summary Prompt:\n{prompt_str}")

        # print("\n" + "="*50)
        # print("PROMPT STATISTICS")
        # print("="*50)
        # for key, value in stats.items():
        #     if isinstance(value, dict):
        #         print(f"{key}:")
        #         for sub_key, sub_value in value.items():
        #             print(f"  {sub_key}: {sub_value}")
        #     else:
        #         print(f"{key}: {value}")


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
        output_path.parent.mkdir(exist_ok=True)
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
        

        # Blueprint Generation
        logger.info("\n📚 Generating Book Blueprint...")
        prompt = BlueprintPromptGenerator.generate_prompt(book_model)
        stats = BlueprintPromptGenerator.get_prompt_statistics(book_model)
        recommended_model_settings = stats.get('recommended_model_settings')
        if recommended_model_settings:
            logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
            # update the llm with the prompt recommended settings
            await llm_service.update_default_parameters(
                temperature=recommended_model_settings.get('temperature', 0.3),
                max_tokens=recommended_model_settings.get('max_tokens', 4000),
                top_p=recommended_model_settings.get('top_p', 0.9)
            )

        logger.info(
            "🤖 Generating book blueprint..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )

        correction:str = ""
        while True:
            try:
                response = await llm_service.generate([prompt + correction])
                if response.get('timelapse', 0):
                    print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
                valid, payload = BlueprintPromptGenerator.validate_json_response(response['response'])
                if valid:
                    break
                logger.error(f"🔴  LLM Response is not valid JSON: {payload}")
                correction = f"""You are to correct the following errors that did not pass the validation on compliance with the TARGET JSON SCHEMA:\n
                        {payload}
                        Your invalid output that you need to correct:\n
                        {response['response']}
                        """
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"🔴  LLM Error: {e}")
                logger.info("🔄  Retrying...")
                await asyncio.sleep(1)

        json_payload = extract_json_from_response(response['response'])
        output_path.parent.mkdir(exist_ok=True)
        response_filename = generate_filename(
            output_path,
            prefix="blueprint-response",
            extension="json"
        )
        with open(response_filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_payload))
        book_blueprint = json.dumps(json_payload, indent=2)
        flag = await ctx_mgr.store(
            book_id=book_id,
            metadata=book_model,
            as_vector=False,
            content_id="book_blueprint",
            content=json.dumps(json_payload),
        )
        if not flag:
            logger.error("🔴 Failed to store book summary")
            sys.exit(1)
        logger.info(f'📝  Book blueprint stored to {ctx_mgr.__class__.__name__}')
        # book_blueprint = ctx_mgr.retrieve(
        #     exact_ids=['book_blueprint'],
        #     filters={
        #         'book_id': book_id
        #     }
        # )

        # Planning
        logger.info("\n📚 Generating Book Planning...")
        pc = PlanningConfig()
        ppg = PlanningPromptGenerator(pc)
        prompt = ppg.generate_planning_prompt(json_payload)
        prompt_filename = generate_filename(
            output_path,
            prefix="plan",
            extension="txt"
        )
        ppg.save_prompt_to_file(prompt, prompt_filename)
        stats = ppg.get_prompt_stats(prompt)
        recommended_model_settings = stats.get('recommended_model_settings')
        # print("\n" + "="*50)
        # print("PROMPT STATISTICS")
        # print("="*50)
        # for key, value in stats.items():
        #     if isinstance(value, dict):
        #         print(f"{key}:")
        #         for sub_key, sub_value in value.items():
        #             print(f"  {sub_key}: {sub_value}")
        #     else:
        #         print(f"{key}: {value}")
        if recommended_model_settings:
            logger.info(f'ℹ️  Using recommended model settings:\n{json.dumps(recommended_model_settings, indent=2)}\n')
            # update the llm with the prompt recommended settings
            await llm_service.update_default_parameters(
                temperature=recommended_model_settings.get('temperature', 1.3),
                max_tokens=recommended_model_settings.get('max_tokens', 5000),
                top_p=recommended_model_settings.get('top_p', 0.5),
                top_k=recommended_model_settings.get('top_k', 40),
                repeat_penalty=recommended_model_settings.get('repeat_penalty', 1.1),
                stop=recommended_model_settings.get("stop"),
            )
        else:
            logger.info("ℹ️  No recommended model settings found, using defaults")
            await llm_service.update_default_parameters(
                temperature=1.3,
                max_tokens=5000,
                top_p=0.5
            )
        logger.info(
            "🤖 Generating book plan..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        plan_filename = generate_filename(
            output_path,
            prefix="plan",
            extension="md"
        )
        with open(plan_filename, 'w', encoding='utf-8') as f:
            f.write(response['response'])

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
        prompt = ResearchPromptGenerator.generate_prompt(book_summary, book_plan)
        await llm_service.update_default_parameters(
            temperature=0.3,
        )

        logger.info(
            "🤖 Generating book research..."
            f"\nℹ️  Prompt:\n\t{prompt[:60] + '...' if len(prompt)>60 else prompt}\n"
        )
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        plan_filename = generate_filename(
            output_path,
            prefix="research",
            extension="json"
        )
        json_payload = extract_json_from_response(response['response'])
        json_str = json.dumps(json_payload)
        with open(plan_filename, 'w', encoding='utf-8') as f:
            f.write(json_str)

        researcher_config = ResearcherConfig()
        researcher = ResearcherAgent(researcher_config)
        research_results = await researcher.execute_research(book_id, ResearchQuery.load_research_queries(json_str))

        research_result_filename = generate_filename(
            output_path,
            prefix="research-result",
            extension="json"
        )
        
        # Extract tavily_answer values for JSON serialization
        def extract_tavily_answers(detailed_results:Dict[str,ResearchResults]):
            extracted_data = {}
            for query_type, result in detailed_results.items():
                tavily_answers = []
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


        # After the deailed research is done, we can now generate the book chapter plan
        stop = time.perf_counter()
        lapse = tick(start, stop)
        print(f'DONE in {lapse}')
    except Exception as e:
        logger.error(f"Error: {e}")

async def book_dna_fn():

    ctx_mgr = await create_llm_context_manager()

    
    start = time.perf_counter()
    config = get_settings()
    with open('musequill/services/backend/outputs/book_model-20250801-202621.json', 'r', encoding='utf-8') as f:
        book_model = json.load(f)
    with open('musequill/services/backend/outputs/blueprint-response-20250801-202936.json', 'r', encoding='utf-8') as f:
        book_blueprint = json.load(f)
    with open('musequill/services/backend/outputs/research-result-20250801-203850.json', 'r', encoding='utf-8') as f:
        research_results = json.load(f)
    with open('musequill/services/backend/outputs/summary-response-20250801-202749.md', 'r', encoding='utf-8') as f:
        book_summary = f.read()

    research_types: List[Dict[str, Any]] = []
    for query in research_results['updated_queries']:
        research_types.append({'type':query['topic']})
    book_id: str = str(uuid4())
    dna_input = BookDNAInputs(**{
        'book_model': book_model,
        'book_blueprint': book_blueprint,
        'research_topics': research_types,
        'book_summary': book_summary,
        'book_id': book_id
    })

    prompt = BookDNAPromptGenerator.generate_dna_prompt(dna_input)
    llm_service = create_llm_service()
    await llm_service.update_default_parameters(
        temperature=1.3,
        max_tokens=800,
        top_k=10,
        top_p=0.9,
        repeat_penalty=1.1
    )
    logger.info("LLM Service initialized successfully")
    response = await llm_service.generate([prompt])
    val_rep = BookDNAPromptGenerator.validate_dna_output(response['response'])
    print(json.dumps(val_rep, indent=2, ensure_ascii=False))
    end = time.perf_counter()
    print(f'done : {tick(start, end)}')

if __name__ == "__main__":
    asyncio.run(main())