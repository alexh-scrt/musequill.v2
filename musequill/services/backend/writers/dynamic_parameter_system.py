# dynamic_parameter_system.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class DynamicParams:
    """Dynamic parameters that adjust based on context and performance."""
    max_context_tokens: int = 1500
    quality_threshold: float = 0.85
    max_text_for_continuity: int = 8000
    max_text_for_summary: int = 4000
    max_generation_tokens: Optional[int] = None
    temperature_base: float = 0.8
    temperature_revision: float = 0.7

class ParameterAdaptationManager:
    """Manages dynamic parameter adjustment based on context and performance."""
    
    def __init__(self):
        self.chapter_performance_history = []
        self.token_usage_history = []
        
    def calculate_dynamic_params(
        self,
        chapter_brief,
        target_chapter: int,
        narrative_state_size: int = 0,
        previous_attempts: List[Dict] = None,
        book_complexity: str = "medium"  # low, medium, high
    ) -> DynamicParams:
        """Calculate dynamic parameters based on context and history."""
        
        params = DynamicParams()
        
        # Adjust context tokens based on chapter complexity
        chapter_complexity = self._assess_chapter_complexity(chapter_brief)
        
        if chapter_complexity == "high":
            params.max_context_tokens = 2000
            params.quality_threshold = 0.82  # Slightly lower for complex chapters
            params.max_text_for_continuity = 12000
            params.max_generation_tokens = 4000
        elif chapter_complexity == "low":
            params.max_context_tokens = 1000
            params.quality_threshold = 0.88  # Higher for simple chapters
            params.max_text_for_continuity = 6000
            params.max_generation_tokens = 2000
        else:  # medium
            params.max_context_tokens = 1500
            params.quality_threshold = 0.85
            params.max_text_for_continuity = 8000
            params.max_generation_tokens = 3000
        
        # Adjust based on narrative state size (more context needed for later chapters)
        if narrative_state_size > 1000:  # Rich narrative history
            params.max_context_tokens = min(params.max_context_tokens + 500, 2500)
        
        # Adjust based on previous attempts
        if previous_attempts:
            failed_attempts = len([a for a in previous_attempts if a.get('score', 0) < 0.8])
            if failed_attempts >= 2:
                # Lower threshold and increase context for struggling chapters
                params.quality_threshold -= 0.05
                params.max_context_tokens += 300
                params.temperature_base += 0.1  # More creative
        
        # Adjust for book complexity
        if book_complexity == "high":
            params.max_context_tokens = min(params.max_context_tokens + 300, 2500)
            params.quality_threshold -= 0.03
        
        return params
    
    def _assess_chapter_complexity(self, chapter_brief) -> str:
        """Assess chapter complexity based on the chapter brief."""
        complexity_score = 0
        
        # Count scenes
        if hasattr(chapter_brief, 'scenes') and chapter_brief.scenes:
            scene_count = len(chapter_brief.scenes)
            if scene_count >= 3:
                complexity_score += 2
            elif scene_count >= 2:
                complexity_score += 1
        
        # Count characters
        characters = set()
        if hasattr(chapter_brief, 'scenes') and chapter_brief.scenes:
            for scene in chapter_brief.scenes:
                if hasattr(scene, 'characters_on_stage') and scene.characters_on_stage:
                    for char_entry in scene.characters_on_stage:
                        if '&' in char_entry:
                            characters.update([c.strip() for c in char_entry.split('&')])
                        else:
                            characters.add(char_entry.strip())
        
        if len(characters) >= 4:
            complexity_score += 2
        elif len(characters) >= 3:
            complexity_score += 1
        
        # Count narrative beats
        beat_count = 0
        if hasattr(chapter_brief, 'narrative_beats'):
            beat_count += len(chapter_brief.narrative_beats)
        if hasattr(chapter_brief, 'chapter_specific_beats'):
            beat_count += len(chapter_brief.chapter_specific_beats)
        
        if beat_count >= 5:
            complexity_score += 2
        elif beat_count >= 3:
            complexity_score += 1
        
        # Check for dialogue requirements
        if hasattr(chapter_brief, 'dialogue_cues') and chapter_brief.dialogue_cues:
            if len(chapter_brief.dialogue_cues) >= 3:
                complexity_score += 1
        
        # Check for motifs and themes
        if hasattr(chapter_brief, 'motifs') and chapter_brief.motifs:
            if len(chapter_brief.motifs) >= 3:
                complexity_score += 1
        
        # Determine complexity level
        if complexity_score >= 6:
            return "high"
        elif complexity_score <= 2:
            return "low"
        else:
            return "medium"
    
    def adjust_generation_params(
        self, 
        llm_service, 
        params: DynamicParams, 
        attempt_number: int = 1,
        previous_response_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """Adjust LLM generation parameters dynamically."""
        
        generation_params = {
            "temperature": params.temperature_base,
            "top_p": 0.95,
            "top_k": 50
        }
        
        # Set max tokens if specified
        if params.max_generation_tokens:
            generation_params["max_tokens"] = params.max_generation_tokens
        
        # Adjust for revision attempts
        if attempt_number > 1:
            generation_params["temperature"] = params.temperature_revision + (attempt_number - 1) * 0.05
            generation_params["top_p"] = 0.9
            generation_params["top_k"] = 40
        
        # Adjust if previous response was too short
        if previous_response_length and previous_response_length < 1000:
            generation_params["temperature"] += 0.1
            if params.max_generation_tokens:
                generation_params["max_tokens"] = int(params.max_generation_tokens * 1.2)
        
        # Adjust if previous response was too long
        if previous_response_length and previous_response_length > 5000:
            generation_params["temperature"] -= 0.1
            if params.max_generation_tokens:
                generation_params["max_tokens"] = int(params.max_generation_tokens * 0.8)
        
        return generation_params
    
    def record_chapter_performance(
        self, 
        chapter_number: int, 
        attempts: int, 
        final_score: float, 
        word_count: int,
        response_length: int
    ):
        """Record chapter performance for future parameter adjustments."""
        self.chapter_performance_history.append({
            "chapter": chapter_number,
            "attempts": attempts,
            "score": final_score,
            "word_count": word_count,
            "response_length": response_length
        })
        
        # Keep only recent history
        if len(self.chapter_performance_history) > 10:
            self.chapter_performance_history = self.chapter_performance_history[-10:]
    
    def get_adaptive_context_length(
        self,
        target_chapter: int,
        narrative_state_size: int,
        base_max_tokens: int = 1500
    ) -> int:
        """Get adaptive context length based on story progression."""
        
        # Later chapters need more context
        chapter_multiplier = min(1.0 + (target_chapter - 1) * 0.05, 1.5)
        
        # Rich narrative history needs more context
        history_multiplier = min(1.0 + (narrative_state_size / 1000) * 0.1, 1.3)
        
        # Performance history suggests adjustment
        performance_multiplier = 1.0
        if self.chapter_performance_history:
            recent_scores = [p["score"] for p in self.chapter_performance_history[-3:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            if avg_score < 0.8:
                performance_multiplier = 1.2  # More context for struggling generation
        
        adaptive_length = int(
            base_max_tokens * chapter_multiplier * history_multiplier * performance_multiplier
        )
        
        return min(adaptive_length, 2500)  # Cap at reasonable limit


# Integration functions for the enhanced chapter writer

def integrate_dynamic_params_with_enhanced_writer():
    """Example of how to integrate dynamic parameters with the enhanced writer."""
    
    # This would be added to the enhanced_write_chapter_with_qc function
    example_integration = '''
    # At the beginning of enhanced_write_chapter_with_qc:
    param_manager = ParameterAdaptationManager()
    
    # Calculate dynamic parameters
    narrative_state_size = len(str(context_manager.narrative_state.chapter_summaries))
    dynamic_params = param_manager.calculate_dynamic_params(
        chapter_brief=chapter_brief,
        target_chapter=target_chapter,
        narrative_state_size=narrative_state_size,
        previous_attempts=[]  # Would track from previous calls
    )
    
    # Adjust context building
    contextual_summary = context_manager.narrative_state.get_contextual_summary(
        target_chapter, max_tokens=dynamic_params.max_context_tokens
    )
    
    # Use dynamic quality threshold
    quality_threshold = dynamic_params.quality_threshold
    
    # In the generation loop:
    for attempt in range(max_retries):
        generation_params = param_manager.adjust_generation_params(
            llm, dynamic_params, attempt + 1, 
            previous_response_length=len(best_text) if best_text else None
        )
        
        await llm.update_default_parameters(**generation_params)
        
        # ... rest of generation logic
        
        # Check against dynamic threshold
        if score >= quality_threshold:
            break
    
    # Record performance for future adjustments
    param_manager.record_chapter_performance(
        target_chapter, attempts, best_score, 
        count_words(best_text), len(best_text)
    )
    '''
    
    return example_integration


# Utility functions for parameter optimization

def optimize_for_short_responses(
    current_params: Dict[str, Any],
    response_length: int,
    target_length: int
) -> Dict[str, Any]:
    """Optimize parameters when responses are too short."""
    
    optimized = current_params.copy()
    
    if response_length < target_length * 0.7:  # Significantly short
        optimized["temperature"] = min(optimized.get("temperature", 0.8) + 0.15, 1.2)
        optimized["max_tokens"] = int(optimized.get("max_tokens", 3000) * 1.3)
        optimized["top_p"] = min(optimized.get("top_p", 0.95) + 0.05, 1.0)
    
    return optimized

def optimize_for_long_responses(
    current_params: Dict[str, Any],
    response_length: int,
    target_length: int
) -> Dict[str, Any]:
    """Optimize parameters when responses are too long."""
    
    optimized = current_params.copy()
    
    if response_length > target_length * 1.5:  # Significantly long
        optimized["temperature"] = max(optimized.get("temperature", 0.8) - 0.1, 0.3)
        optimized["max_tokens"] = int(optimized.get("max_tokens", 3000) * 0.8)
        optimized["top_k"] = max(optimized.get("top_k", 50) - 10, 20)
    
    return optimized