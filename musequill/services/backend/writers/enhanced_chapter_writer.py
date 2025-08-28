# enhanced_chapter_writer.py
import os
import re
import unicodedata
from typing import Dict, List, Any, Optional
from uuid import uuid4

from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.writers.book_planning_model import GenericBookPlan
from musequill.services.backend.model.book import BookModelType
from musequill.services.backend.writers.research_model import RefinedResearch
from musequill.services.backend.llm.ollama_client import LLMService
from .context_manager import EnhancedContextManager, create_enhanced_context_manager
from musequill.services.backend.utils import (
    seconds_to_time_string,
    extract_json_from_response
)
# Import the feedback system
from .chapter_feedback import (
    evaluate_chapter_quality_with_feedback,
    create_improvement_prompt
)

def make_enhanced_chapter_prompt(ctx: Dict[str, Any]) -> str:
    """Create an enhanced chapter prompt with rich contextual information."""
    
    book_model: BookModelType = ctx["book_model"]
    chapter_brief: GenericChapterBrief = ctx["chapter_brief"]
    narrative_continuity = ctx.get("narrative_continuity", {})
    
    # Extract key information using proper typed access
    chapter_num = chapter_brief.meta.chapter_number
    chapter_title = chapter_brief.meta.chapter_title
    target_words = chapter_brief.meta.target_words
    
    # Build contextual summary section
    contextual_summary = narrative_continuity.get("contextual_summary", "")
    
    # Build character continuity section
    character_states = narrative_continuity.get("character_states", {})
    character_context = ""
    if character_states:
        character_context = "**Character Continuity:**\n"
        for char_name, char_data in list(character_states.items())[:5]:  # Top 5 characters
            recent_appearances = [entry["chapter"] for entry in char_data["development_arc"][-3:]]
            character_context += f"- {char_name}: {char_data['current_status']}, recent chapters: {recent_appearances}\n"
    
    # Build plot thread continuity section
    active_threads = narrative_continuity.get("active_plot_threads", [])
    thread_context = ""
    if active_threads:
        thread_context = "**Active Plot Threads to Honor:**\n"
        for thread in active_threads[:5]:  # Top 5 threads
            thread_context += f"- {thread['thread']} (since Ch.{thread['introduced_chapter']})\n"
    
    # Build recent chapter progression
    recent_progression = narrative_continuity.get("chapter_progression", [])
    progression_context = ""
    if recent_progression:
        progression_context = "**Recent Chapter Progression:**\n"
        for ch in recent_progression[-3:]:  # Last 3 chapters
            progression_context += f"- Ch.{ch['chapter']}: {ch['title']} - {ch['summary'][:150]}...\n"
    
    # Enhanced research context
    enhanced_research = ctx.get("enhanced_research", {})
    research_context = ""
    if enhanced_research:
        research_context = "**Relevant Research Context:**\n"
        for category, items in enhanced_research.items():
            if items:
                research_context += f"\n*{category.capitalize()}:*\n"
                for item in items[:3]:  # Top 3 per category
                    # Each item is now a string from RefinedResearch
                    research_context += f"- {item[:100]}...\n" if len(item) > 100 else f"- {item}\n"
    
    # Construct the enhanced prompt
    prompt = f"""You are a professional novelist writing Chapter {chapter_num} of a coherent, engaging book.

# MASTER CONTEXT & CONTINUITY
You are writing a continuous story. Each chapter must build naturally on what came before, maintaining character consistency, advancing plot threads, and preserving the narrative voice established in previous chapters.

## Book Overview
- **Title**: {book_model.book.title}
- **Genre**: {book_model.genre.primary.type}
- **Audience**: {book_model.audience.type} ({book_model.audience.age})
- **POV**: {book_model.pov.type}
- **Tone**: {book_model.tone.type}

## Story Continuity Context
{contextual_summary}

{character_context}

{thread_context}

{progression_context}

{research_context}

## Current Chapter Requirements
- **Chapter**: {chapter_num}
- **Title**: {chapter_title}
- **Target Length**: ~{target_words} words
- **Narrative Beats**: {', '.join(chapter_brief.narrative_beats)}
- **Setups to Plant**: {', '.join(chapter_brief.setups)}
- **Payoffs to Deliver**: {', '.join(chapter_brief.payoffs)}

### Scene Structure:
"""

    # Add scene details using proper typed access
    scenes = chapter_brief.scenes
    for i, scene in enumerate(scenes, 1):
        prompt += f"""
**Scene {i}**: {scene.location or 'Unknown location'} ({scene.time or 'Unknown time'})
- Characters: {', '.join(scene.characters_on_stage)}
- Objective: {scene.objective or 'Advance the story'}
- Conflict: {scene.conflict or 'Create tension'}
- Exit: {scene.exit_on or 'Natural transition'}
"""

    prompt += f"""

# CRITICAL WRITING INSTRUCTIONS

## Continuity Imperatives
1. **Character Consistency**: Maintain established character voices, relationships, and development arcs from previous chapters
2. **Plot Thread Advancement**: Progress at least one major plot thread meaningfully
3. **World Consistency**: Honor established rules, settings, and internal logic
4. **Narrative Voice**: Match the established tone, pacing, and style from previous chapters

## Story Progress Requirements
- Make at least ONE irreversible change to the story state (new information revealed, relationship changed, location reached, etc.)
- Connect to at least ONE element from previous chapters
- Set up or pay off at least ONE future story element

## Technical Requirements
- **Length**: {int(target_words*0.9)}-{int(target_words*1.1)} words
- **Format**: Markdown with H1 title, H3 scene breaks
- **POV Rules**: {book_model.pov.type} - {book_model.pov.description}

## Writing Quality Standards
- Show don't tell
- Use concrete, sensory details
- Create vivid, cinematic scenes
- Write dialogue that advances plot and reveals character
- Maintain appropriate pacing for the genre and audience

# OUTPUT FORMAT

Write the complete chapter as markdown, then include a brief analysis block:

```qa
**Story Progress**: [One sentence explaining the irreversible change this chapter makes to the story]
**Character Development**: [Key character growth or change in this chapter]
**Plot Threads Advanced**: [Which major plot threads moved forward]
**Continuity Connections**: [How this chapter connects to previous chapters]
**Setup for Future**: [What this chapter sets up for later chapters]
```

Begin writing the chapter now, keeping all continuity and context requirements in mind."""

    return prompt


async def enhanced_write_chapter_with_qc(
    llm: LLMService,
    context_manager: EnhancedContextManager,
    book_model: BookModelType,
    book_summary: str,
    constraints: Dict[str, Any],
    research_corpus: RefinedResearch,
    chapter_brief: GenericChapterBrief,
    target_chapter: int,
    banned_ngrams: List[str] = None,
    max_retries: int = 3,
    prior_chapter_text: Optional[str] = None,
    prior_chapter_summary: Optional[str] = None
) -> Dict[str, Any]:
    """Enhanced chapter writing with feedback-driven improvement loop."""
    
    # Build enhanced context
    enhanced_context = context_manager.build_enhanced_context_pack(
        book_model=book_model,
        book_summary=book_summary,
        constraints=constraints,
        research_corpus=research_corpus,
        chapter_brief=chapter_brief,
        target_chapter=target_chapter,
        prior_chapter_text=prior_chapter_text,
        prior_chapter_summary=prior_chapter_summary
    )
    
    attempts = 0
    best_text = ""
    best_score = 0
    best_feedback = None
    feedback_history = []
    
    # Initial generation
    attempts += 1
    try:
        initial_prompt = make_enhanced_chapter_prompt(enhanced_context)
        
        # Generate with moderate creativity
        temp = 0.8
        await llm.update_default_parameters(**{
            "temperature": temp,
            "top_p": 0.95,
            "top_k": 50
        })
        
        res = await llm.generate(initial_prompt)
        if res.get('timelapse', 0):
            print(f"⏱️  LLM Response Time: {seconds_to_time_string(res['timelapse'])}")
        
        text, qa_block = extract_qa_block(res['response'])
        word_count = count_words(text)
        target_words = chapter_brief.meta.target_words
        
        # Get detailed feedback
        score, feedback = evaluate_chapter_quality_with_feedback(
            text, qa_block, chapter_brief, enhanced_context, 
            word_count, target_words, enhanced_context.get("narrative_continuity")
        )
        
        best_text = text
        best_score = score
        best_feedback = feedback
        feedback_history.append(feedback)
        
        print(f"  Initial attempt: Score {score:.2f}, Priority: {feedback.improvement_priority}")
        
        # If initial attempt is good enough, we're done
        if score >= 0.85:
            print(f"  ✓ Chapter meets quality threshold on first attempt")
        else:
            print(f"  → Needs improvement, beginning feedback loop...")
            
            # Improvement loop with feedback
            while attempts < max_retries and best_score < 0.85:
                attempts += 1
                
                try:
                    # Create improvement prompt based on feedback
                    improvement_prompt = create_improvement_prompt(
                        best_text, best_feedback, enhanced_context, attempts
                    )
                    
                    # Adjust generation parameters for revision
                    revision_temp = 0.7 + (attempts - 1) * 0.05  # Slightly less creative for revisions
                    await llm.update_default_parameters(**{
                        "temperature": revision_temp,
                        "top_p": 0.9,
                        "top_k": 40
                    })
                    
                    res = await llm.generate(improvement_prompt)
                    if res.get('timelapse', 0):
                        print(f"⏱️  Revision Time: {seconds_to_time_string(res['timelapse'])}")
                    
                    revised_text, revised_qa = extract_qa_block(res['response'])
                    revised_word_count = count_words(revised_text)
                    
                    # Evaluate revision
                    revised_score, revised_feedback = evaluate_chapter_quality_with_feedback(
                        revised_text, revised_qa, chapter_brief, enhanced_context,
                        revised_word_count, target_words, enhanced_context.get("narrative_continuity")
                    )
                    
                    print(f"  Revision {attempts-1}: Score {revised_score:.2f} (was {best_score:.2f})")
                    
                    # Keep the better version
                    if revised_score > best_score:
                        best_text = revised_text
                        best_score = revised_score
                        best_feedback = revised_feedback
                        print(f"    ✓ Improvement accepted")
                    else:
                        print(f"    → No improvement, keeping previous version")
                    
                    feedback_history.append(revised_feedback)
                    
                    # Break if we reach quality threshold
                    if best_score >= 0.85:
                        print(f"  ✓ Chapter meets quality threshold after {attempts-1} revisions")
                        break
                        
                except Exception as e:
                    print(f"    ❌ Revision attempt {attempts} failed: {e}")
                    continue
    
    except Exception as e:
        print(f"❌ Initial generation failed: {e}")
        raise RuntimeError(f"Failed to generate chapter: {e}")
    
    if not best_text:
        raise RuntimeError(f"Failed to generate chapter after {max_retries} attempts")
    
    # Extract continuity information for state updates
    continuity_data = await extract_continuity_advanced(best_text, chapter_brief, llm)
    
    # Create chapter metadata
    chapter_meta = {
        "chapter_number": target_chapter,
        "chapter_title": chapter_brief.meta.chapter_title,
        "word_count": count_words(best_text),
        "summary": await generate_chapter_summary(best_text, chapter_brief, llm),
        "quality_score": best_score,
        "attempts": attempts,
        "final_feedback": best_feedback.__dict__ if best_feedback else {},
        "improvement_history": [f.__dict__ for f in feedback_history]
    }
    
    # Update narrative state
    context_manager.update_after_chapter_completion(
        best_text, chapter_meta, continuity_data
    )
    
    return {
        "chapter_md": best_text,
        "metadata": chapter_meta,
        "continuity": continuity_data,
        "context_used": enhanced_context,
        "quality_score": best_score,
        "feedback": best_feedback
    }

async def enhanced_write_all_chapters_with_qc(
    *,
    book_model: BookModelType,
    book_plan: GenericBookPlan,
    chapter_briefs: List[GenericChapterBrief],
    book_summary: str,
    research_corpus: RefinedResearch,
    llm: LLMService,
    out_dir: str = "manuscript",
    book_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Write all chapters with enhanced context management."""
    
    if not book_id:
        book_id = str(uuid4())
    
    # Initialize enhanced context manager
    context_manager = create_enhanced_context_manager(book_id, out_dir)
    
    os.makedirs(out_dir, exist_ok=True)
    results: List[Dict[str, Any]] = []
    
    banned_ngrams = []  # Could be loaded from config
    
    for brief in sorted(chapter_briefs, key=lambda b: b.meta.chapter_number):
        chapter_num = brief.meta.chapter_number
        
        print(f"Writing Chapter {chapter_num}: {brief.meta.chapter_title}")
        
        # Get previous chapter text for immediate continuity
        prev_chapter_text = None
        if results:
            prev_chapter_text = results[-1]["chapter_md"]
        
        # Write chapter with enhanced context and feedback loop
        chapter_result = await enhanced_write_chapter_with_qc(
            llm=llm,
            context_manager=context_manager,
            book_model=book_model,
            book_summary=book_summary,
            constraints=getattr(book_plan, 'constraints', None) or {},
            research_corpus=research_corpus,
            chapter_brief=brief,
            target_chapter=chapter_num,
            banned_ngrams=banned_ngrams,
            max_retries=3,
            prior_chapter_text=prev_chapter_text
        )
        
        results.append(chapter_result)
        
        # Save chapter to file
        save_markdown_chapter(
            chapter_result["chapter_md"], 
            brief, 
            out_dir
        )
        
        print(f"✓ Chapter {chapter_num} completed (Quality: {chapter_result['quality_score']:.2f})")
    
    return results


# Helper functions

def extract_qa_block(text: str) -> tuple[str, str]:
    """Extract QA block from generated text."""
    
    # Look for ```qa block
    qa_pattern = r'```qa\s*(.*?)\s*```'
    match = re.search(qa_pattern, text, re.DOTALL)
    
    if match:
        qa_block = match.group(1).strip()
        chapter_text = text[:match.start()].strip()
        return chapter_text, qa_block
    
    return text.strip(), ""


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def evaluate_chapter_quality(
    text: str, 
    qa_block: str, 
    chapter_brief: GenericChapterBrief, 
    context: Dict[str, Any],
    word_count: int,
    target_words: int
) -> float:
    """Evaluate chapter quality (0.0 to 1.0)."""
    
    score = 0.0
    
    # Word count scoring (30% of total)
    word_ratio = word_count / target_words
    if 0.9 <= word_ratio <= 1.1:
        score += 0.30
    elif 0.8 <= word_ratio <= 1.2:
        score += 0.20
    elif 0.7 <= word_ratio <= 1.3:
        score += 0.10
    
    # Structure scoring (20% of total)
    if text.count("# ") >= 1:  # Has title
        score += 0.10
    if text.count("### ") >= 1:  # Has scene breaks
        score += 0.10
    
    # Content scoring (30% of total)
    if len(text.strip()) > 500:  # Substantial content
        score += 0.15
    if qa_block:  # Has QA block
        score += 0.15
    
    # Basic quality indicators (20% of total)
    sentences = text.count('.') + text.count('!') + text.count('?')
    if sentences > 20:  # Reasonable sentence count
        score += 0.10
    
    # Check for dialogue
    if '"' in text:
        score += 0.05
    
    # Check for variety in sentence structure
    if text.count(',') > sentences * 0.5:  # Complex sentences
        score += 0.05
    
    return min(score, 1.0)

async def extract_continuity_advanced(text: str, chapter_brief: GenericChapterBrief, llm: LLMService) -> Dict[str, Any]:
    """Extract detailed continuity information from chapter."""
    
    prompt = f"""Extract key continuity elements from this chapter for story tracking.

Chapter {chapter_brief.meta.chapter_number}: {chapter_brief.meta.chapter_title}

Chapter Text:
{text[:8000]}  # Truncate for prompt length

Extract and return as JSON:
{{
    "characters_introduced": ["list of new character names"],
    "characters_developed": ["list of characters who changed/grew"],
    "plot_threads_advanced": ["list of plot threads that moved forward"],
    "new_plot_threads": ["list of new plot threads introduced"],
    "world_changes": ["list of changes to the world/setting"],
    "relationships_changed": ["list of relationship changes"],
    "key_events": ["list of major events that happened"],
    "foreshadowing_planted": ["list of foreshadowing elements"],
    "callbacks_to_earlier": ["list of callbacks to previous chapters"]
}}

Return only valid JSON."""
    
    try:
        response = await llm.generate(prompt, temperature=0.3)
        return extract_json_from_response(response['response'])
    except Exception:
        return {
            "characters_introduced": [],
            "characters_developed": [],
            "plot_threads_advanced": [],
            "new_plot_threads": [],
            "world_changes": [],
            "relationships_changed": [],
            "key_events": [],
            "foreshadowing_planted": [],
            "callbacks_to_earlier": []
        }


async def generate_chapter_summary(text: str, chapter_brief: GenericChapterBrief, llm: LLMService) -> str:
    """Generate a concise chapter summary."""
    
    prompt = f"""Write a concise 2-3 sentence summary of this chapter that captures the key events and character development:

Chapter {chapter_brief.meta.chapter_number}: {chapter_brief.meta.chapter_title}

{text[:4000]}...

Summary:"""
    
    try:
        response = await llm.generate(prompt, temperature=0.3, top_p=0.9)
        return response['response'].strip()
    except:
        return f"Chapter {chapter_brief.meta.chapter_number} summary unavailable"


def save_markdown_chapter(text: str, brief: GenericChapterBrief, out_dir: str) -> str:
    """Save chapter as markdown file."""
    
    os.makedirs(out_dir, exist_ok=True)
    ch = brief.meta.chapter_number
    title = brief.meta.chapter_title
    
    # Slugify title for filename
    slug_title = unicodedata.normalize("NFKD", title)
    slug_title = slug_title.encode("ascii", "ignore").decode("ascii")
    slug_title = re.sub(r"[^\w\s-]", "", slug_title).strip().lower()
    slug_title = re.sub(r"[-\s]+", "-", slug_title) or "chapter"
    
    fname = f"{ch:02d}-{slug_title}.md"
    path = os.path.join(out_dir, fname)
    
    # Ensure chapter has proper header
    if not text.strip().lower().startswith("# chapter"):
        header = f"# Chapter {ch}: {title}\n\n"
        content = header + text.lstrip()
    else:
        content = text
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return path