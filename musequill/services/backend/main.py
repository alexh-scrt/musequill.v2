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
from typing import Optional
import logging

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import our book model
from musequill.services.backend.model.book import BookModelType
from musequill.services.backend.prompts import (
    BlueprintPromptGenerator
)
from musequill.services.backend.llm.ollama_client import LLMService
from musequill.services.backend.utils import (
    generate_filename,
    seconds_to_time_string
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


async def main():
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
        logger.info(f"Loading template: {args.template}")
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
                json.dump(book_model.dict(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"\nBook model saved to: {output_path}")
            
        except Exception as e:
            logger.info(f"Error saving to output file '{args.output}': {e}")
            sys.exit(1)
    
    logger.info(f"\n✅ Successfully processed template: {args.template}")

    try:
        prompt = BlueprintPromptGenerator.generate_prompt(book_model)
        
        if args.output:
            output_path.parent.mkdir(exist_ok=True)
            prompt_filename = generate_filename(
                output_path,
                prefix="blueprint",
                extension="txt"
            )
            BlueprintPromptGenerator.save_prompt_to_file(book_model, prompt_filename)
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
        logger.error(f"Error: {e}")

    try:
        llm_service = LLMService(model_name="llama3.3:70b")
        await llm_service.initialize()
        logger.info("LLM Service initialized successfully")
        response = await llm_service.generate([prompt])
        if response.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(response['timelapse'])}")
        if args.output:
            output_path.parent.mkdir(exist_ok=True)
            response_filename = generate_filename(
                output_path,
                prefix="blueprint-response",
                extension="md"
            )
            with open(response_filename, 'w', encoding='utf-8') as f:
                f.write(response['response'])

        print(response)
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())