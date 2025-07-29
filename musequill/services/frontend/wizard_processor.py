import logging
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Depends
import sys
from pathlib import Path


# Import our book models
from musequill.models.book.genre import GenreType, SubGenreType, GenreMapping
from musequill.models.book.writing_style import WritingStyle
from musequill.models.book.story_structure import StoryStructure, StructureRecommender
from musequill.models.book.world import WorldType
from musequill.models.book.book_length import BookLength
from musequill.models.book.research import ResearchPlanGenerator

from .api_models import (
    BookConceptRequest,
    WizardStepRequest,
    WizardStepResponse,
    WizardOption,
    WizardSession,
    StandardResponse
)

from .session_manager import SessionManager
from .llm_service import LLMService

logger = logging.getLogger(__name__)


# ============================================================================
# Wizard Step Processors
# ============================================================================

class WizardStepProcessor:
    """Processes individual wizard steps and generates options."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        
        # Define step configuration
        self.steps = {
            1: {"name": "genre_selection", "title": "Genre Selection"},
            2: {"name": "target_audience", "title": "Target Audience"},
            3: {"name": "writing_style", "title": "Writing Style"},
            4: {"name": "book_length", "title": "Book Length"},
            5: {"name": "story_structure", "title": "Story Structure"},
            6: {"name": "world_building", "title": "World Building"},
            7: {"name": "content_preferences", "title": "Content Preferences"},
            8: {"name": "final_summary", "title": "Final Summary"}
        }
    
    async def process_step(self, session: WizardSession, step_number: int, 
                          selection: Optional[str] = None) -> WizardStepResponse:
        """Process a wizard step and return response with options."""
        
        step_config = self.steps.get(step_number)
        if not step_config:
            raise HTTPException(status_code=400, detail="Invalid step number")
        
        # Save selection from previous step
        if selection and step_number > 1:
            prev_step = self.steps[step_number - 1]["name"]
            session.selections[prev_step] = selection
        
        # Get options for current step
        if step_number == 1:
            return await self._process_genre_selection(session)
        elif step_number == 2:
            return await self._process_target_audience(session)
        elif step_number == 3:
            return await self._process_writing_style(session)
        elif step_number == 4:
            return await self._process_book_length(session)
        elif step_number == 5:
            return await self._process_story_structure(session)
        elif step_number == 6:
            return await self._process_world_building(session)
        elif step_number == 7:
            return await self._process_content_preferences(session)
        elif step_number == 8:
            return await self._process_final_summary(session)
        else:
            raise HTTPException(status_code=400, detail="Invalid step")
    
    async def _process_genre_selection(self, session: WizardSession) -> WizardStepResponse:
        """Process genre selection step."""
        # Get high-demand genres for commercial focus
        commercial_genres = [
            GenreType.ROMANCE, GenreType.FANTASY, GenreType.MYSTERY, 
            GenreType.THRILLER, GenreType.ROMANTASY, GenreType.YOUNG_ADULT
        ]
        
        # Convert to options format
        available_options = [
            {
                "id": genre.value,
                "name": genre.display_name,
                "description": f"Commercial appeal: {'High' if genre.is_high_demand else 'Medium'}"
            }
            for genre in commercial_genres
        ]
        
        # Get LLM suggestions
        llm_suggestions = await self.llm_service.suggest_options(
            "Genre Selection", session.concept, session.selections, available_options
        )
        
        # Enhance options with LLM scores
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50,
                market_appeal="High" if GenreType(opt["id"]).is_high_demand else "Medium"
            ))
        
        # Sort by recommendation score
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=1,
            step_name="Genre Selection",
            question="What genre best describes your book concept?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_target_audience(self, session: WizardSession) -> WizardStepResponse:
        """Process target audience selection."""
        # Basic audience options
        available_options = [
            {"id": "adult", "name": "Adult", "description": "Ages 18+ - Full range of themes and complexity"},
            {"id": "young_adult", "name": "Young Adult", "description": "Ages 13-18 - Coming-of-age themes"},
            {"id": "new_adult", "name": "New Adult", "description": "Ages 18-25 - College/early career themes"}
        ]
        
        llm_suggestions = await self.llm_service.suggest_options(
            "Target Audience", session.concept, session.selections, available_options
        )
        
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50
            ))
        
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=2,
            step_name="Target Audience",
            question="Who is your target audience?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_writing_style(self, session: WizardSession) -> WizardStepResponse:
        """Process writing style selection."""
        # Get commercial writing styles
        commercial_styles = [
            WritingStyle.CONVERSATIONAL, WritingStyle.CONTEMPORARY, WritingStyle.ACCESSIBLE,
            WritingStyle.NARRATIVE, WritingStyle.CLASSICAL, WritingStyle.INFORMAL
        ]
        
        # Add genre-specific styles based on previous selection
        selected_genre = session.selections.get("genre_selection")
        if selected_genre == "romance":
            commercial_styles.extend([WritingStyle.ROMANTIC, WritingStyle.CONFESSIONAL])
        elif selected_genre == "fantasy":
            commercial_styles.extend([WritingStyle.EPIC, WritingStyle.ATMOSPHERIC])
        elif selected_genre == "mystery":
            commercial_styles.extend([WritingStyle.SUSPENSEFUL, WritingStyle.NOIR])
        
        available_options = [
            {
                "id": style.value,
                "name": style.display_name if hasattr(style, 'display_name') else style.value.replace('_', ' ').title(),
                "description": f"Suitable for {selected_genre or 'general'} fiction"
            }
            for style in commercial_styles[:6]  # Limit to 6 options
        ]
        
        llm_suggestions = await self.llm_service.suggest_options(
            "Writing Style", session.concept, session.selections, available_options
        )
        
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50
            ))
        
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=3,
            step_name="Writing Style",
            question="What writing style appeals to you?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_book_length(self, session: WizardSession) -> WizardStepResponse:
        """Process book length selection."""
        # Commercial length options
        commercial_lengths = [
            BookLength.SHORT_NOVEL, BookLength.STANDARD_NOVEL, 
            BookLength.LONG_NOVEL, BookLength.NOVELLA
        ]
        
        available_options = [
            {
                "id": length.value,
                "name": length.display_name if hasattr(length, 'display_name') else length.value.replace('_', ' ').title(),
                "description": f"{length.target_words:,} words - {length.publishing_viability} publishing viability" if hasattr(length, 'target_words') else "Standard length"
            }
            for length in commercial_lengths
        ]
        
        llm_suggestions = await self.llm_service.suggest_options(
            "Book Length", session.concept, session.selections, available_options
        )
        
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50
            ))
        
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=4,
            step_name="Book Length",
            question="What length are you targeting?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_story_structure(self, session: WizardSession) -> WizardStepResponse:
        """Process story structure selection."""
        # Commercial structures
        commercial_structures = [
            StoryStructure.THREE_ACT, StoryStructure.HERO_JOURNEY,
            StoryStructure.SAVE_THE_CAT, StoryStructure.ROMANCE_BEAT_SHEET
        ]
        
        available_options = [
            {
                "id": structure.value,
                "name": structure.display_name,
                "description": structure.description if hasattr(structure, 'description') else "Proven narrative structure"
            }
            for structure in commercial_structures
        ]
        
        llm_suggestions = await self.llm_service.suggest_options(
            "Story Structure", session.concept, session.selections, available_options
        )
        
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50
            ))
        
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=5,
            step_name="Story Structure",
            question="Which narrative structure do you prefer?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_world_building(self, session: WizardSession) -> WizardStepResponse:
        """Process world building selection."""
        # Get world types based on genre
        selected_genre = session.selections.get("genre_selection", "")
        
        if "fantasy" in selected_genre.lower():
            world_options = [WorldType.URBAN_FANTASY, WorldType.HIGH_FANTASY, WorldType.SECONDARY_WORLD]
        elif "science" in selected_genre.lower():
            world_options = [WorldType.SCIENCE_FICTION, WorldType.CYBERPUNK, WorldType.SPACE_OPERA]
        else:
            world_options = [WorldType.CONTEMPORARY, WorldType.HISTORICAL, WorldType.ALTERNATE_HISTORY]
        
        available_options = [
            {
                "id": world.value,
                "name": world.display_name if hasattr(world, 'display_name') else world.value.replace('_', ' ').title(),
                "description": "Research complexity: Accurate"
            }
            for world in world_options
        ]
        
        llm_suggestions = await self.llm_service.suggest_options(
            "World Building", session.concept, session.selections, available_options
        )
        
        enhanced_options = []
        for opt in available_options:
            llm_rec = next((r for r in llm_suggestions["recommendations"] if r["option_id"] == opt["id"]), None)
            enhanced_options.append(WizardOption(
                id=opt["id"],
                name=opt["name"],
                description=opt["description"],
                recommendation_score=llm_rec["score"] if llm_rec else 50
            ))
        
        enhanced_options.sort(key=lambda x: x.recommendation_score or 0, reverse=True)
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=6,
            step_name="World Building",
            question="What type of setting interests you?",
            options=enhanced_options,
            llm_reasoning=llm_suggestions.get("general_reasoning"),
            is_final_step=False
        )
    
    async def _process_content_preferences(self, session: WizardSession) -> WizardStepResponse:
        """Process content preferences (free text input)."""
        # This step has no predefined options - it's for free text input
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=7,
            step_name="Content Preferences",
            question="Please specify any content preferences, themes, or restrictions for your book:",
            options=[],  # No predefined options
            llm_reasoning="This is your opportunity to specify content level, themes, or any restrictions.",
            is_final_step=False
        )
    
    async def _process_final_summary(self, session: WizardSession) -> WizardStepResponse:
        """Generate final book summary."""
        # Generate book summary from all selections
        book_summary = {
            "concept": session.concept,
            "genre": session.selections.get("genre_selection"),
            "audience": session.selections.get("target_audience"),
            "writing_style": session.selections.get("writing_style"),
            "length": session.selections.get("book_length"),
            "structure": session.selections.get("story_structure"),
            "world": session.selections.get("world_building"),
            "content_preferences": session.additional_inputs.get("content_preferences", "")
        }
        
        session.book_summary = book_summary
        session.is_complete = True
        
        # Create summary option
        summary_text = f"""
        Book Summary:
        - Genre: {book_summary['genre']}
        - Audience: {book_summary['audience']}
        - Style: {book_summary['writing_style']}
        - Length: {book_summary['length']}
        - Structure: {book_summary['structure']}
        - World: {book_summary['world']}
        """
        
        return WizardStepResponse(
            session_id=session.session_id,
            step_number=8,
            step_name="Final Summary",
            question="Here's your book definition summary:",
            options=[WizardOption(
                id="summary",
                name="Book Summary",
                description=summary_text.strip()
            )],
            llm_reasoning="Your book is now fully defined and ready for creation!",
            is_final_step=True
        )
