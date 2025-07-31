#!/usr/bin/env python3
"""
Research Prompt Generator for Book Writing - JSON Output Version

This script takes a book summary and book plan to generate research topics
that need to be explored for the book's development.
"""

import json
from typing import Dict, Any, List
from dataclasses import dataclass
from .research_topics_schema import RESEARCH_TOPICS_JSON_SCHEMA, RESEARCH_TOPICS_EXPECTED_OUTPUT

class ResearchPromptGenerator:
    """Generates optimized prompts for research topic identification with JSON output."""
    
    SYSTEM_PROMPT = """You are an expert research consultant and book development strategist. Your task is to analyze a book summary and writing plan to identify specific research topics that need to be explored to create an authentic, engaging, and well-informed book.

## CRITICAL OUTPUT REQUIREMENT
You MUST respond with a valid JSON object following the exact structure provided in the JSON Schema below. Do not include any text before or after the JSON. Do not use markdown code blocks. Return only pure JSON.

## Research Topic Guidelines

1. **Be Specific**: Identify concrete research areas, not generic topics
2. **Prioritize by Impact**: Focus on research that will most enhance the story's authenticity and depth
3. **Consider Audience**: Ensure research supports age-appropriate content and engagement
4. **Balance Depth vs. Breadth**: Include both deep dives and surface-level research as appropriate
5. **Practical Focus**: All research should be actionable and accessible to the author
6. **Cultural Sensitivity**: When dealing with cultural elements, emphasize respectful and accurate representation

## Research Categories to Consider

- **mythology_folklore**: Cultural myths, legends, folklore, and traditional stories
- **historical_context**: Time periods, historical events, social customs, daily life
- **natural_world**: Geography, ecology, animal behavior, natural phenomena  
- **cultural_anthropology**: Social structures, belief systems, customs, traditions
- **science_technology**: Scientific concepts, technological innovations, technical processes
- **psychology_behavior**: Character psychology, human behavior, social dynamics
- **linguistics**: Language patterns, dialects, communication styles
- **arts_crafts**: Traditional arts, crafts, skills, creative practices
- **social_political**: Government systems, political structures, social hierarchies
- **daily_life**: Food, clothing, housing, work, entertainment, family life

## Priority Levels
- **high**: Essential for story authenticity and plot development
- **medium**: Important for richness and depth but not critical for basic story
- **low**: Nice-to-have details that could enhance but aren't necessary

## Research Methods to Consider
- **academic_sources**: Scholarly articles, university research, peer-reviewed studies
- **primary_sources**: Historical documents, firsthand accounts, original texts
- **expert_interviews**: Consultations with specialists, academics, practitioners
- **field_research**: Direct observation, site visits, hands-on experience
- **multimedia_sources**: Documentaries, podcasts, educational videos
- **cultural_sources**: Community resources, cultural centers, traditional practitioners
- **online_databases**: Digital archives, specialized websites, digital libraries
- **books_literature**: Specialized books, reference works, literary sources"""

    RESEARCH_INSTRUCTIONS = """
## Research Topic Generation Instructions

Based on the book summary and writing plan provided, identify 5-12 specific research topics that will be essential for creating an authentic, engaging, and well-informed book. For each topic, provide:

1. **Category**: One of the predefined research categories
2. **Topic**: Specific, focused research area 
3. **Description**: Clear explanation of what needs to be researched and why
4. **Priority**: High, medium, or low based on story impact
5. **Estimated Time**: Realistic hours needed for adequate research
6. **Research Methods**: Most appropriate research approaches for this topic
7. **Key Questions**: 3-5 specific questions the research should answer
8. **Sources Suggested**: 3-5 specific types of sources or resources to consult

Focus on research that will:
- Enhance story authenticity and believability
- Support character development and world-building
- Provide cultural accuracy and sensitivity
- Enable rich, sensory descriptions
- Support plot development and conflict resolution
- Meet the needs and interests of the target audience

Consider the book's genre, setting, characters, themes, and target audience when identifying research needs. Prioritize research that will have the greatest impact on story quality and reader engagement.
"""

    @classmethod
    def generate_prompt(cls, book_summary: str, book_plan: str) -> str:
        """
        Generate a complete prompt for research topic identification.
        
        Args:
            book_summary: BookSummary instance with book details
            book_plan: BookPlan instance with writing plan
            
        Returns:
            Complete formatted prompt string
        """
        # Create summary of book details
        #book_context = cls._create_book_context(book_summary, book_plan)
        
        # Convert to clean JSON for inclusion
        #summary_json = cls._summary_to_dict(book_summary)
        #plan_json = cls._plan_to_dict(book_plan)
        
        # Construct the complete prompt
        complete_prompt = f"""{cls.SYSTEM_PROMPT}

## JSON Output Schema

# ABSOLUTE RULES:
- ❗ Output MUST be valid JSON that conforms to the structure below
- ❗ Do NOT include any explanation, comment, or markdown
- ❗ Populate **every field** in the schema with SPECIFIC, USEFUL data

# Output Format Requirements:
- 🔹 Pure JSON object
- 🔹 All fields filled with meaningful content
- 🔹 NO markdown/code blocks
- 🔹 NO extra commentary

# DO NOT DO:
- ❌ Do not preface with "Here's your JSON:"
- ❌ Do not wrap output in triple backticks
- ❌ Do not include schema again
- ❌ Do not repeat the input data

🛑 Your ONLY job is to produce a JSON object.
✅ Your JSON MUST match the structure and field names EXACTLY.

You MUST respond with a JSON object that follows this exact structure:

```json
{RESEARCH_TOPICS_JSON_SCHEMA}
```

## Here is a correct example output:
```json
{RESEARCH_TOPICS_EXPECTED_OUTPUT}
```

## Book Summary

{book_summary}

## Book Plan Data

{book_plan}


## Research Topic Generation Task

{cls.RESEARCH_INSTRUCTIONS}


Generate the complete research topics list now as a valid JSON object, identifying specific research areas that will enhance this book's authenticity, depth, and engagement. Return ONLY the JSON object with no additional text or formatting.

"""

        return complete_prompt

#     @classmethod
#     def _create_book_context(cls, book_summary: BookSummary, book_plan: BookPlan) -> str:
#         """Create a concise context summary."""
#         return f"""**Book**: "{book_summary.title}" by {book_summary.author}
# **Genre**: {book_summary.genre}
# **Target Audience**: {book_summary.target_audience}
# **Setting**: {book_summary.setting}
# **Main Characters**: {', '.join(book_summary.main_characters)}
# **Key Themes**: {', '.join(book_summary.themes)}
# **Word Count Target**: {book_plan.word_count_target:,} words
# **Timeline**: {book_plan.timeline}"""

#     @classmethod
#     def _summary_to_dict(cls, book_summary: BookSummary) -> Dict[str, Any]:
#         """Convert BookSummary to dictionary."""
#         return {
#             "title": book_summary.title,
#             "author": book_summary.author,
#             "genre": book_summary.genre,
#             "target_audience": book_summary.target_audience,
#             "plot_summary": book_summary.plot_summary,
#             "main_characters": book_summary.main_characters,
#             "setting": book_summary.setting,
#             "themes": book_summary.themes
#         }

#     @classmethod
#     def _plan_to_dict(cls, book_plan: BookPlan) -> Dict[str, Any]:
#         """Convert BookPlan to dictionary."""
#         return {
#             "phases": book_plan.phases,
#             "word_count_target": book_plan.word_count_target,
#             "timeline": book_plan.timeline,
#             "key_elements": book_plan.key_elements
#         }

    # @classmethod
    # def generate_prompt_from_dicts(cls, book_summary_dict: Dict[str, Any], book_plan_dict: Dict[str, Any]) -> str:
    #     """
    #     Generate prompt directly from dictionary data.
        
    #     Args:
    #         book_summary_dict: Dictionary containing book summary data
    #         book_plan_dict: Dictionary containing book plan data
            
    #     Returns:
    #         Complete formatted prompt string
    #     """
    #     book_summary = BookSummary(**book_summary_dict)
    #     book_plan = BookPlan(**book_plan_dict)
    #     return cls.generate_prompt(book_summary, book_plan)

    @classmethod
    def save_prompt_to_file(cls, prompt: str, output_path: str) -> None:
        """
        Generate and save prompt to a file.
        
        Args:
            book_summary: BookSummary instance
            book_plan: BookPlan instance  
            output_path: Path where to save the prompt file
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Research prompt saved to: {output_path}")

    @classmethod
    def validate_json_response(cls, response: str) -> tuple[bool, Any]:
        """
        Validate LLM response conforms to expected JSON schema.
        
        Args:
            response: The LLM response string
            
        Returns:
            Tuple of (is_valid, parsed_json_or_error_message)
        """
        try:
            # Try to parse the JSON
            parsed_json = json.loads(response.strip())
            
            # Basic structure validation
            required_keys = ["book_title", "author", "research_topics", "total_estimated_research_time", "research_timeline"]
            
            # Check top-level structure
            for key in required_keys:
                if key not in parsed_json:
                    return False, f"Missing required key: {key}"
            
            # Check research_topics is array
            if not isinstance(parsed_json.get("research_topics"), list):
                return False, "research_topics must be an array"
            
            # Check each research topic has required fields
            required_topic_fields = ["category", "topic", "description", "priority", "estimated_time_hours", "research_methods", "key_questions", "sources_suggested"]
            
            for i, topic in enumerate(parsed_json.get("research_topics", [])):
                for field in required_topic_fields:
                    if field not in topic:
                        return False, f"Missing field '{field}' in research topic {i+1}"
            
            return True, parsed_json
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    # @classmethod
    # def get_prompt_statistics(cls, book_summary: BookSummary, book_plan: BookPlan) -> Dict[str, Any]:
    #     """
    #     Get statistics about the generated prompt.
        
    #     Args:
    #         book_summary: BookSummary instance
    #         book_plan: BookPlan instance
            
    #     Returns:
    #         Dictionary with prompt statistics
    #     """
    #     prompt = cls.generate_prompt(book_summary, book_plan)
        
    #     return {
    #         "total_characters": len(prompt),
    #         "total_words": len(prompt.split()),
    #         "estimated_tokens": len(prompt.split()) * 1.3,  # Rough estimate
    #         "book_complexity_score": cls._calculate_complexity_score(book_summary, book_plan),
    #         "recommended_model_settings": {
    #             "temperature": 0.2,  # Lower temperature for structured JSON output
    #             "max_tokens": 3000,  # Adequate for research topics list
    #             "top_p": 0.8
    #         }
    #     }

    # @classmethod  
    # def _calculate_complexity_score(cls, book_summary: BookSummary, book_plan: BookPlan) -> float:
    #     """Calculate a complexity score for the book (0.0 to 1.0)."""
    #     score = 0.0
        
    #     # Genre complexity
    #     complex_genres = ['fantasy', 'historical', 'science fiction', 'mystery']
    #     if any(genre in book_summary.genre.lower() for genre in complex_genres):
    #         score += 0.3
            
    #     # Setting complexity  
    #     if 'historical' in book_summary.setting.lower() or 'mythological' in book_summary.setting.lower():
    #         score += 0.2
            
    #     # Theme complexity
    #     complex_themes = ['mythology', 'cultural', 'historical', 'spiritual', 'philosophical']
    #     theme_complexity = sum(1 for theme in book_summary.themes if any(ct in theme.lower() for ct in complex_themes))
    #     score += min(theme_complexity * 0.1, 0.3)
        
    #     # Word count complexity
    #     if book_plan.word_count_target > 60000:
    #         score += 0.2
            
    #     return min(score, 1.0)


# def main():
#     """Example usage of the ResearchPromptGenerator."""
    
#     # Example book summary
#     book_summary = BookSummary(
#         title="The Enchanted Forest of Peter",
#         author="Joseph Campbell",
#         genre="Children's Fantasy",
#         target_audience="Children aged 7-12",
#         plot_summary="A brave bunny ventures beyond his meadow into a magical forest filled with Slavic mythological creatures, facing challenges that test his courage and wit before returning home transformed.",
#         main_characters=["Peter the Bunny", "Forest Spirits", "Mythological Creatures"],
#         setting="Magical forest inspired by Slavic folklore",
#         themes=["Courage", "Growth", "Cultural mythology", "Nature connection"]
#     )
    
#     # Example book plan
#     book_plan = BookPlan(
#         phases={
#             "foundation": "Genre analysis and audience research",
#             "structure": "Plot outline and character development", 
#             "world_building": "Forest setting and creature design",
#             "research": "Slavic folklore and natural world study",
#             "writing": "Draft creation and revision",
#             "publication": "Editing and publishing preparation"
#         },
#         word_count_target=45000,
#         timeline="6-month project with 2 weeks initial research",
#         key_elements=["Slavic mythology", "Animal protagonist", "Coming-of-age journey", "Magical realism"]
#     )
    
#     # Generate prompt
#     prompt = ResearchPromptGenerator.generate_prompt(book_summary, book_plan)
    
#     print("Generated Research Prompt:")
#     print("=" * 50)
#     print(prompt)
    
#     # Get statistics
#     stats = ResearchPromptGenerator.get_prompt_statistics(book_summary, book_plan)
#     print("\n" + "=" * 50) 
#     print("PROMPT STATISTICS")
#     print("=" * 50)
#     for key, value in stats.items():
#         if isinstance(value, dict):
#             print(f"{key}:")
#             for sub_key, sub_value in value.items():
#                 print(f"  {sub_key}: {sub_value}")
#         else:
#             print(f"{key}: {value}")


# if __name__ == "__main__":
#     main()