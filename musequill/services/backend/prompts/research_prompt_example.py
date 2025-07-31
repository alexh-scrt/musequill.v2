#!/usr/bin/env python3
"""
Example usage of ResearchPromptGenerator with the Joseph Campbell book plan
"""

from .research_prompt_generator import ResearchPromptGenerator, BookSummary, BookPlan

def create_joseph_campbell_example():
    """Create an example using Joseph Campbell's children's fantasy book plan."""
    
    # Extract book summary from the provided plan document
    book_summary = BookSummary(
        title="Joseph Campbell's Children's Fantasy Novel",
        author="Joseph Campbell",
        genre="Children's Fantasy",
        target_audience="Children aged 7-12", 
        plot_summary="A comprehensive children's fantasy story following the hero's journey archetype, featuring rich world-building, character development, and themes appropriate for the target age group.",
        main_characters=["Young protagonist", "Mentor figure", "Supporting characters", "Antagonist"],
        setting="Fantasy world with magical elements",
        themes=["Hero's journey", "Coming of age", "Good vs evil", "Friendship", "Courage", "Self-discovery"]
    )
    
    # Extract book plan elements from the comprehensive plan document
    book_plan = BookPlan(
        phases={
            "foundation_planning": {
                "objectives": "Define project scope, analyze target audience, identify genre conventions",
                "key_elements": ["Project scope", "Target audience analysis", "Genre research", "Success metrics"]
            },
            "structural_blueprint": {
                "objectives": "Develop detailed plot outline, create act/chapter breakdown",
                "key_elements": ["Plot outline", "Act/chapter structure", "Conflict escalation", "Character arcs"]
            },
            "world_design": {
                "objectives": "Create immersive world with geography, history, magic system",
                "key_elements": ["World geography", "Magic system", "Creature design", "Mythology"]
            },
            "character_development": {
                "objectives": "Craft well-developed characters with clear arcs",
                "key_elements": ["Character profiles", "Character arcs", "Motivations", "Conflicts"]
            },
            "revision_strategy": {
                "objectives": "Comprehensive revision plan for manuscript improvement",
                "key_elements": ["Self-editing", "Beta reader feedback", "Professional editing"]
            },
            "publication_roadmap": {
                "objectives": "Prepare for publication and marketing",
                "key_elements": ["Publication options", "Marketing plan", "Promotion strategy"]
            }
        },
        word_count_target=50000,  # Middle of 40,000-60,000 range mentioned in plan
        timeline="Several months with major milestones for draft completion and revision phases",
        key_elements=[
            "Hero's journey structure",
            "Rich world-building", 
            "Age-appropriate themes",
            "Character development",
            "Fantasy elements",
            "Market positioning"
        ]
    )
    
    return book_summary, book_plan

def main():
    """Demonstrate ResearchPromptGenerator usage."""
    
    print("=== RESEARCH PROMPT GENERATOR EXAMPLE ===\n")
    
    # Create the book summary and plan
    book_summary, book_plan = create_joseph_campbell_example()
    
    print("Book Summary:")
    print(f"  Title: {book_summary.title}")
    print(f"  Author: {book_summary.author}")
    print(f"  Genre: {book_summary.genre}")
    print(f"  Target Audience: {book_summary.target_audience}")
    print(f"  Themes: {', '.join(book_summary.themes)}")
    print(f"  Word Count Target: {book_plan.word_count_target:,} words")
    print()
    
    # Generate the research prompt
    print("Generating research prompt...")
    prompt = ResearchPromptGenerator.generate_prompt(book_summary, book_plan)
    
    # Display prompt statistics
    stats = ResearchPromptGenerator.get_prompt_statistics(book_summary, book_plan)
    print("PROMPT STATISTICS:")
    print("=" * 40)
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print()
    
    # Save the prompt to a file
    output_file = "joseph_campbell_research_prompt.txt"
    ResearchPromptGenerator.save_prompt_to_file(book_summary, book_plan, output_file)
    print(f"✅ Research prompt saved to: {output_file}")
    
    # Display a portion of the generated prompt
    print("\nSAMPLE OF GENERATED PROMPT:")
    print("=" * 50)
    print(prompt[:1000] + "..." if len(prompt) > 1000 else prompt)
    print("=" * 50)
    
    # Example of how you would feed this to an LLM and validate response
    print("\nNEXT STEPS:")
    print("1. Feed the generated prompt to your preferred LLM")
    print("2. Receive JSON response with research topics")
    print("3. Validate the response using ResearchPromptGenerator.validate_json_response()")
    print("4. Use the research topics to guide your book research phase")
    
    # Example validation (you would use actual LLM response here)
    example_response = """
    {
      "book_title": "Joseph Campbell's Children's Fantasy Novel",
      "author": "Joseph Campbell",
      "research_topics": [
        {
          "category": "mythology_folklore",
          "topic": "Hero's Journey in Global Mythologies",
          "description": "Study Campbell's monomyth across different cultures",
          "priority": "high",
          "estimated_time_hours": 10,
          "research_methods": ["academic_sources", "primary_sources"],
          "key_questions": ["How does the hero's journey manifest in different cultures?"],
          "sources_suggested": ["The Hero with a Thousand Faces", "Comparative mythology texts"]
        }
      ],
      "total_estimated_research_time": 10,
      "research_timeline": "2 weeks initial research"
    }
    """
    
    is_valid, result = ResearchPromptGenerator.validate_json_response(example_response)
    print(f"\nEXAMPLE VALIDATION:")
    print(f"Valid JSON: {is_valid}")
    if is_valid:
        print("✅ Response structure is valid")
        print(f"Found {len(result['research_topics'])} research topics")
    else:
        print(f"❌ Validation error: {result}")

if __name__ == "__main__":
    main()