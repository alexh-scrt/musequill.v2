# enhanced_feedback_system.py
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Import the proper types
from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.model.book import BookModelType

@dataclass
class ChapterFeedback:
    """Structured feedback for chapter improvement."""
    overall_score: float
    word_count_feedback: str
    structure_feedback: str
    content_feedback: str
    quality_feedback: str
    continuity_feedback: str
    specific_suggestions: List[str]
    strengths: List[str]
    improvement_priority: str  # "high", "medium", "low"

def evaluate_chapter_quality_with_feedback(
    text: str, 
    qa_block: str, 
    chapter_brief: GenericChapterBrief, 
    context: Dict[str, Any],
    word_count: int,
    target_words: int,
    narrative_continuity: Dict[str, Any] = None
) -> Tuple[float, ChapterFeedback]:
    """
    Evaluate chapter quality and provide detailed feedback for improvement.
    Returns (score, feedback_object).
    """
    
    feedback = ChapterFeedback(
        overall_score=0.0,
        word_count_feedback="",
        structure_feedback="",
        content_feedback="",
        quality_feedback="",
        continuity_feedback="",
        specific_suggestions=[],
        strengths=[],
        improvement_priority="low"
    )
    
    score = 0.0
    
    # Word count analysis with feedback (30% of total)
    word_ratio = word_count / target_words
    if 0.9 <= word_ratio <= 1.1:
        score += 0.30
        feedback.word_count_feedback = f"✓ Excellent word count ({word_count} words, {word_ratio:.1%} of target)"
        feedback.strengths.append("Perfect word count targeting")
    elif 0.8 <= word_ratio <= 1.2:
        score += 0.20
        if word_ratio < 0.9:
            feedback.word_count_feedback = f"⚠ Slightly short ({word_count} words, {word_ratio:.1%} of target)"
            feedback.specific_suggestions.append(f"Expand scenes with more sensory details and dialogue to reach {int(target_words * 0.95)}-{target_words} words")
        else:
            feedback.word_count_feedback = f"⚠ Slightly long ({word_count} words, {word_ratio:.1%} of target)" 
            feedback.specific_suggestions.append(f"Trim verbose descriptions and tighten dialogue to reach {target_words}-{int(target_words * 1.05)} words")
    else:
        score += 0.10
        if word_ratio < 0.8:
            feedback.word_count_feedback = f"❌ Too short ({word_count} words, {word_ratio:.1%} of target)"
            feedback.specific_suggestions.append(f"Significantly expand: add character interiority, richer scene descriptions, more dialogue exchanges")
        else:
            feedback.word_count_feedback = f"❌ Too long ({word_count} words, {word_ratio:.1%} of target)"
            feedback.specific_suggestions.append(f"Major trimming needed: remove tangential descriptions, condense dialogue, focus on core scene objectives")

    # Structure analysis with feedback (20% of total)
    structure_issues = []
    structure_strengths = []
    
    title_count = text.count("# ")
    scene_count = text.count("### ")
    
    if title_count >= 1:
        score += 0.10
        structure_strengths.append("Has proper chapter title")
    else:
        structure_issues.append("Missing H1 chapter title")
        feedback.specific_suggestions.append("Add a clear H1 chapter title at the beginning")
    
    if scene_count >= 1:
        score += 0.10
        structure_strengths.append(f"Has {scene_count} scene breaks")
    else:
        structure_issues.append("Missing scene breaks")
        feedback.specific_suggestions.append("Use ### headers to separate distinct scenes or major transitions")
    
    expected_scenes = len(chapter_brief.scenes) if chapter_brief.scenes else 1
    if scene_count < expected_scenes:
        structure_issues.append(f"Expected {expected_scenes} scenes, found {scene_count}")
        feedback.specific_suggestions.append(f"Structure chapter into {expected_scenes} distinct scenes as outlined in the brief")
    
    feedback.structure_feedback = f"Structure: {len(structure_strengths)} strengths, {len(structure_issues)} issues"
    if structure_strengths:
        feedback.strengths.extend(structure_strengths)

    # Content quality analysis (30% of total)
    content_issues = []
    content_strengths = []
    
    if len(text.strip()) > 500:
        score += 0.15
        content_strengths.append("Substantial content length")
    else:
        content_issues.append("Content too brief")
        feedback.specific_suggestions.append("Develop scenes more fully with description, action, and character interaction")
    
    if qa_block:
        score += 0.15
        content_strengths.append("Includes QA analysis block")
    else:
        content_issues.append("Missing QA block")
        feedback.specific_suggestions.append("Include a ```qa block analyzing story progress, character development, and continuity")

    # Dialogue analysis
    dialogue_count = text.count('"')
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    if dialogue_count > 4:  # At least some dialogue
        content_strengths.append("Contains dialogue")
    else:
        content_issues.append("Little or no dialogue")
        feedback.specific_suggestions.append("Add character dialogue to bring scenes to life and advance plot")

    feedback.content_feedback = f"Content: {len(content_strengths)} strengths, {len(content_issues)} issues"
    if content_strengths:
        feedback.strengths.extend(content_strengths)

    # Writing quality indicators (20% of total)
    quality_issues = []
    quality_strengths = []
    
    sentences = text.count('.') + text.count('!') + text.count('?')
    if sentences > 20:
        score += 0.10
        quality_strengths.append(f"Good sentence variety ({sentences} sentences)")
    else:
        quality_issues.append("Too few sentences for chapter length")
        feedback.specific_suggestions.append("Expand with more detailed descriptions and varied sentence structures")
    
    # Check for dialogue
    if dialogue_count > 0:
        score += 0.05
        quality_strengths.append("Contains character dialogue")
    else:
        quality_issues.append("No dialogue present")
    
    # Check for sentence complexity
    comma_count = text.count(',')
    if comma_count > sentences * 0.3:  # Good complexity
        score += 0.05
        quality_strengths.append("Good sentence complexity")
    else:
        quality_issues.append("Sentences too simple")
        feedback.specific_suggestions.append("Use more complex sentence structures with dependent clauses and descriptive phrases")

    feedback.quality_feedback = f"Writing quality: {len(quality_strengths)} strengths, {len(quality_issues)} issues"
    if quality_strengths:
        feedback.strengths.extend(quality_strengths)

    # Continuity analysis (bonus scoring)
    if narrative_continuity:
        continuity_issues = []
        continuity_strengths = []
        
        # Check if chapter references previous elements
        contextual_summary = narrative_continuity.get("contextual_summary", "")
        character_states = narrative_continuity.get("character_states", {})
        active_threads = narrative_continuity.get("active_plot_threads", [])
        
        # Look for character name references
        character_mentions = 0
        for char_name in character_states.keys():
            if char_name.lower() in text.lower():
                character_mentions += 1
        
        if character_mentions > 0:
            continuity_strengths.append(f"References {character_mentions} established characters")
            score += 0.05  # Bonus points
        else:
            continuity_issues.append("No references to established characters")
            feedback.specific_suggestions.append("Include references to characters established in previous chapters")
        
        # Check for plot thread advancement keywords
        thread_advancement = any(
            thread['thread'].lower()[:20] in text.lower() 
            for thread in active_threads[:3]
        )
        
        if thread_advancement:
            continuity_strengths.append("Appears to advance existing plot threads")
            score += 0.05  # Bonus points
        else:
            continuity_issues.append("May not advance established plot threads")
            feedback.specific_suggestions.append("Explicitly advance at least one plot thread from previous chapters")
        
        feedback.continuity_feedback = f"Continuity: {len(continuity_strengths)} strengths, {len(continuity_issues)} issues"
        if continuity_strengths:
            feedback.strengths.extend(continuity_strengths)

    # Overall assessment
    feedback.overall_score = min(score, 1.0)
    
    # Set improvement priority
    if feedback.overall_score >= 0.8:
        feedback.improvement_priority = "low"
    elif feedback.overall_score >= 0.6:
        feedback.improvement_priority = "medium"  
    else:
        feedback.improvement_priority = "high"
    
    # Add priority-specific suggestions
    if feedback.improvement_priority == "high":
        feedback.specific_suggestions.insert(0, "Major revision needed: Focus on structure, content depth, and meeting word count targets")
    elif feedback.improvement_priority == "medium":
        feedback.specific_suggestions.insert(0, "Moderate improvements needed: Polish existing content and address specific gaps")
    
    return feedback.overall_score, feedback

def create_improvement_prompt(
    original_text: str,
    feedback: ChapterFeedback,
    enhanced_context: Dict[str, Any],
    attempt_number: int
) -> str:
    """Create a focused improvement prompt based on feedback."""
    
    chapter_brief: GenericChapterBrief = enhanced_context["chapter_brief"]
    narrative_continuity = enhanced_context.get("narrative_continuity", {})
    
    chapter_num = chapter_brief.meta.chapter_number
    chapter_title = chapter_brief.meta.chapter_title
    target_words = chapter_brief.meta.target_words
    
    # Build feedback summary
    feedback_summary = f"""
## Quality Assessment (Attempt {attempt_number})
**Overall Score**: {feedback.overall_score:.2f}/1.0 ({feedback.improvement_priority.upper()} priority)

**Current Issues to Address**:
{chr(10).join(f"- {suggestion}" for suggestion in feedback.specific_suggestions[:5])}

**Strengths to Maintain**:
{chr(10).join(f"- {strength}" for strength in feedback.strengths[:3]) if feedback.strengths else "- Focus on building fundamental chapter quality"}

**Detailed Feedback**:
- {feedback.word_count_feedback}
- {feedback.structure_feedback}  
- {feedback.content_feedback}
- {feedback.quality_feedback}
- {feedback.continuity_feedback}
"""

    # Build continuity context
    continuity_context = ""
    if narrative_continuity:
        contextual_summary = narrative_continuity.get("contextual_summary", "")
        character_states = narrative_continuity.get("character_states", {})
        active_threads = narrative_continuity.get("active_plot_threads", [])
        
        if contextual_summary:
            continuity_context += f"\n**Story Context to Honor**:\n{contextual_summary}\n"
        
        if character_states:
            continuity_context += f"\n**Established Characters to Reference**:\n"
            for char_name in list(character_states.keys())[:3]:
                continuity_context += f"- {char_name}\n"
        
        if active_threads:
            continuity_context += f"\n**Plot Threads to Advance**:\n"
            for thread in active_threads[:3]:
                continuity_context += f"- {thread['thread']}\n"

    improvement_prompt = f"""You are revising Chapter {chapter_num} based on specific feedback. Your goal is to address the identified issues while maintaining the chapter's strengths.

{feedback_summary}

## Original Chapter to Improve:
{original_text}

## Context for Revision:
**Chapter Requirements**: 
- Title: {chapter_title}
- Target: {target_words} words ({int(target_words*0.9)}-{int(target_words*1.1)} acceptable)
- Scenes: {len(chapter_brief.scenes)} planned scenes
- Beats: {', '.join(chapter_brief.narrative_beats)}

{continuity_context}

## Revision Instructions:

### Primary Focus (Based on Feedback Priority: {feedback.improvement_priority.upper()}):
"""

    # Add priority-specific instructions
    if feedback.improvement_priority == "high":
        improvement_prompt += """
1. **Structure**: Ensure proper H1 title and H3 scene breaks
2. **Length**: Meet the target word count through scene expansion
3. **Content**: Add substantial dialogue and character interaction
4. **Continuity**: Reference established characters and advance plot threads
"""
    elif feedback.improvement_priority == "medium":
        improvement_prompt += """
1. **Polish**: Refine existing content for better flow and impact
2. **Depth**: Add more sensory details and character interiority  
3. **Dialogue**: Enhance character voices and dialogue purpose
4. **Connections**: Strengthen ties to previous chapters
"""
    else:  # low priority
        improvement_prompt += """
1. **Refinement**: Minor adjustments to improve quality
2. **Enhancement**: Add vivid details where needed
3. **Flow**: Ensure smooth scene transitions
4. **Voice**: Maintain consistent narrative tone
"""

    improvement_prompt += f"""

### Specific Actions Required:
{chr(10).join(f"- {suggestion}" for suggestion in feedback.specific_suggestions)}

### Quality Standards:
- Use concrete, sensory details
- Write dialogue that advances plot and reveals character  
- Show don't tell
- Maintain consistent POV and tone
- Create vivid, cinematic scenes

## Output Requirements:
1. Provide the complete revised chapter in Markdown format
2. Include the ```qa analysis block
3. Address ALL feedback points listed above
4. Maintain narrative consistency with previous chapters

Begin the revision now, focusing especially on the {feedback.improvement_priority} priority issues identified:"""

    return improvement_prompt