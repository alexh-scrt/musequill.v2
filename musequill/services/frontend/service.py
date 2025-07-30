"""
Frontend Service Implementation

This module implements the FastAPI endpoints for the book creation wizard.
It handles communication with the LLM (via Ollama), manages wizard state,
and provides intelligent suggestions for book creation parameters.

Endpoints:
    /wizard/start - Initialize new wizard session
    /wizard/step/{step} - Process wizard steps
    /wizard/session/{session_id} - Get session state
    /health - Health check
    /models/info - Model information
"""

import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


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
from .wizard_processor import WizardStepProcessor

logger = logging.getLogger(__name__)


# ============================================================================
# Global Services
# ============================================================================

session_manager = SessionManager()
llm_service = LLMService()
step_processor = WizardStepProcessor(llm_service)


# ============================================================================
# FastAPI Application
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Musequill Frontend Service",
        description="Book Creation Wizard API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    @app.on_event("startup")
    async def startup():
        """Initialize services on startup."""
        await llm_service.initialize()
    
    # ========================================================================
    # Health Check Endpoints
    # ========================================================================
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return StandardResponse(
            success=True,
            message="Frontend service is healthy",
            data={"status": "ok", "timestamp": datetime.now().isoformat()}
        )
    
    @app.get("/models/info")
    async def models_info():
        """Get information about available models."""
        return StandardResponse(
            success=True,
            message="Model information",
            data={
                "llm_model": llm_service.model_name,
                "llm_url": llm_service.base_url,
                "available_genres": len(list(GenreType)),
                "available_styles": len(list(WritingStyle)),
                "available_structures": len(list(StoryStructure))
            }
        )
    
    # ========================================================================
    # Wizard Endpoints
    # ========================================================================
    
    @app.post("/wizard/start")
    async def start_wizard(request: BookConceptRequest):
        """Start a new wizard session with book concept."""
        try:
            # Create new session
            session_id = session_manager.create_session(request.concept)
            
            # Analyze concept with LLM
            concept_analysis = await llm_service.analyze_concept(concept=request.concept, additional_notes=request.additional_notes)
            
            # Process first step (genre selection)
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(status_code=500, detail="Failed to create session")
            
            # Store additional notes if provided
            if request.additional_notes:
                session.additional_inputs["initial_notes"] = request.additional_notes
            
            step_response = await step_processor.process_step(session, 1)
            
            return StandardResponse(
                success=True,
                message="Wizard session started successfully",
                data={
                    "session_id": session_id,
                    "concept_analysis": concept_analysis,
                    "first_step": step_response.dict()
                }
            )
            
        except Exception as e:
            logger.error(f"Error starting wizard: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/wizard/step/{step_number}")
    async def process_wizard_step(step_number: int, request: WizardStepRequest):
        """Process a wizard step."""
        try:
            # Get session
            session = session_manager.get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            # Store additional input if provided
            if request.additional_input:
                step_name = step_processor.steps.get(step_number - 1, {}).get("name", f"step_{step_number - 1}")
                session.additional_inputs[step_name] = request.additional_input
            
            # Update current step
            session.current_step = step_number
            
            # Process step
            step_response = await step_processor.process_step(session, step_number, request.selection)
            
            return StandardResponse(
                success=True,
                message=f"Step {step_number} processed successfully",
                data=step_response.dict()
            )
            
        except Exception as e:
            logger.error(f"Error processing step {step_number}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/wizard/session/{session_id}")
    async def get_wizard_session(session_id: str):
        """Get current wizard session state."""
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return StandardResponse(
            success=True,
            message="Session retrieved successfully",
            data=session.dict()
        )
    
    # ========================================================================
    # Utility Endpoints
    # ========================================================================
    
    @app.get("/genres")
    async def get_genres():
        """Get available genres."""
        genres = [{"id": genre.value, "name": genre.display_name, "high_demand": genre.is_high_demand} 
                 for genre in GenreType]
        return StandardResponse(
            success=True,
            message="Genres retrieved successfully",
            data=genres
        )
    
    @app.get("/writing-styles")
    async def get_writing_styles():
        """Get available writing styles."""
        styles = [{"id": style.value, "name": style.value.replace('_', ' ').title()} 
                 for style in WritingStyle]
        return StandardResponse(
            success=True,
            message="Writing styles retrieved successfully",
            data=styles
        )
    
    @app.get("/story-structures")
    async def get_story_structures():
        """Get available story structures."""
        structures = [{"id": structure.value, "name": structure.display_name} 
                     for structure in StoryStructure]
        return StandardResponse(
            success=True,
            message="Story structures retrieved successfully",
            data=structures
        )
    
    return app