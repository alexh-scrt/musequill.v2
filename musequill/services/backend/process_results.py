from difflib import SequenceMatcher

def is_similar_content(text1: str, text2: str, threshold: float = 0.8) -> bool:
    """
    Check if two texts are similar based on their first 100 characters.
    
    Args:
        text1: First text to compare
        text2: Second text to compare  
        threshold: Similarity threshold (0.0-1.0), default 0.8
        
    Returns:
        True if texts are similar, False otherwise
    """
    if not text1 or not text2:
        return False
    
    # Compare first 100 characters
    sample1 = text1[:100].strip().lower()
    sample2 = text2[:100].strip().lower()
    
    # Use SequenceMatcher to calculate similarity ratio
    similarity = SequenceMatcher(None, sample1, sample2).ratio()
    return similarity >= threshold

def extract_research_results_by_category(research_results):
    """
    Extract tavily_answer values from research results organized by category.
    Filters out duplicate or highly similar answers based on content similarity.
    
    Args:
        research_results: Dict containing research results with 'detailed_results' key
        
    Returns:
        Dict mapping category names to lists of unique tavily_answer strings
        Example: {
            "medical": ["answer1", "answer2", ...],
            "finance": ["answer1", "answer2", ...],
            ...
        }
    """
    if not isinstance(research_results, dict) or 'detailed_results' not in research_results:
        return {}
    
    detailed_results = research_results['detailed_results']
    if not isinstance(detailed_results, dict):
        return {}
    
    category_answers = {}
    
    for category, category_data in detailed_results.items():
        answers = []
        
        if isinstance(category_data, list):
            for item in category_data:
                if isinstance(item, dict) and 'search_results' in item:
                    search_results = item['search_results']
                    if isinstance(search_results, list):
                        for result in search_results:
                            if isinstance(result, dict) and 'tavily_answer' in result:
                                tavily_answer = result['tavily_answer']
                                if tavily_answer and isinstance(tavily_answer, str):
                                    # Check if this answer is similar to any existing answer
                                    is_duplicate = any(
                                        is_similar_content(tavily_answer, existing_answer)
                                        for existing_answer in answers
                                    )
                                    if not is_duplicate:
                                        answers.append(tavily_answer)
        
        category_answers[category] = answers
    
    return category_answers