"""
Frontend Service Implementation

This module implements the FastAPI endpoints for the book creation wizard.
It handles communication with the LLM (via Ollama), manages wizard state,
and provides intelligent suggestions for book creation parameters.

Features:
- IP Blacklisting: Automatically blocks IPs that make 3+ invalid requests
- Comprehensive error handling and logging
- Session management for wizard state
- LLM integration for intelligent suggestions

Endpoints:
    /wizard/start - Initialize new wizard session
    /wizard/step/{step} - Process wizard steps
    /wizard/session/{session_id} - Get session state
    /health - Health check
    /models/info - Model information
    /admin/blacklist-status - Get IP blacklist status (admin only)
"""

import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request
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

# Import the IP blacklisting middleware
from .ip_blacklist_middleware import IPBlacklistMiddleware

logger = logging.getLogger(__name__)


# ============================================================================
# Global Services
# ============================================================================

session_manager = SessionManager()
llm_service = LLMService()
step_processor = WizardStepProcessor(llm_service)

# Global reference to the blacklist middleware for admin endpoints
blacklist_middleware = None


# ============================================================================
# FastAPI Application
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    global blacklist_middleware
    
    app = FastAPI(
        title="Musequill Frontend Service",
        description="Book Creation Wizard API with IP Blacklisting",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add IP blacklisting middleware
    blacklist_middleware = IPBlacklistMiddleware(
        app, 
        max_violations=3,  # Block after 3 invalid requests
        blacklist_duration_hours=24  # Block for 24 hours
    )
    app.add_middleware(type(blacklist_middleware), **blacklist_middleware.__dict__)
    
    @app.on_event("startup")
    async def startup():
        """Initialize services on startup."""
        await llm_service.initialize()
        logger.info("🛡️ IP Blacklisting middleware activated")
    
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
    # Admin Endpoints
    # ========================================================================
    
    @app.get("/admin/blacklist-status")
    async def get_blacklist_status():
        """Get current IP blacklist status. For debugging and monitoring."""
        if blacklist_middleware is None:
            raise HTTPException(status_code=503, detail="Blacklist middleware not available")
        
        status = blacklist_middleware.get_blacklist_status()
        return StandardResponse(
            success=True,
            message="Blacklist status retrieved",
            data=status
        )
    
    # ========================================================================
    # Wizard Endpoints
    # ========================================================================
    
    @app.post("/wizard/start")
    async def start_wizard(request: BookConceptRequest):
        """Start a new wizard session with book concept."""
        try:
            # Validate concept length (this will trigger 422 if invalid)
            if len(request.concept.strip()) < 10:
                raise HTTPException(
                    status_code=422, 
                    detail="Book concept must be at least 10 characters long"
                )
            
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
            
            logger.info(f"New wizard session started: {session_id}")
            
            return StandardResponse(
                success=True,
                message="Wizard session started successfully",
                data={
                    "session_id": session_id,
                    "concept_analysis": concept_analysis,
                    "first_step": step_response.dict()
                }
            )
            
        except HTTPException:
            # Re-raise HTTP exceptions (will be caught by middleware for blacklisting)
            raise
        except Exception as e:
            logger.error(f"Error starting wizard: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/wizard/step/{step_number}")
    async def process_wizard_step(step_number: int, request: WizardStepRequest):
        """Process a wizard step."""
        try:
            # Validate step number
            if step_number < 1 or step_number > 8:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid step number: {step_number}. Must be between 1 and 8."
                )
            
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
            
            logger.info(f"Processed step {step_number} for session {request.session_id}")
            
            return StandardResponse(
                success=True,
                message=f"Step {step_number} processed successfully",
                data=step_response.dict()
            )
            
        except HTTPException:
            # Re-raise HTTP exceptions (will be caught by middleware for blacklisting)
            raise
        except Exception as e:
            logger.error(f"Error processing step {step_number}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/wizard/session/{session_id}")
    async def get_wizard_session(session_id: str):
        """Get current wizard session state."""
        try:
            # Validate session_id format (basic validation)
            if not session_id or len(session_id) < 10:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid session ID format"
                )
            
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return StandardResponse(
                success=True,
                message="Session retrieved successfully",
                data=session.dict()
            )
            
        except HTTPException:
            # Re-raise HTTP exceptions (will be caught by middleware for blacklisting)
            raise
        except Exception as e:
            logger.error(f"Error retrieving session {session_id}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # ========================================================================
    # Utility Endpoints
    # ========================================================================
    
    @app.get("/genres")
    async def get_genres():
        """Get available genres."""
        try:
            genres = [{"id": genre.value, "name": genre.display_name, "high_demand": genre.is_high_demand} 
                     for genre in GenreType]
            return StandardResponse(
                success=True,
                message="Genres retrieved successfully",
                data=genres
            )
        except Exception as e:
            logger.error(f"Error retrieving genres: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/writing-styles")
    async def get_writing_styles():
        """Get available writing styles."""
        try:
            styles = [{"id": style.value, "name": style.value.replace('_', ' ').title()} 
                     for style in WritingStyle]
            return StandardResponse(
                success=True,
                message="Writing styles retrieved successfully",
                data=styles
            )
        except Exception as e:
            logger.error(f"Error retrieving writing styles: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/story-structures")
    async def get_story_structures():
        """Get available story structures."""
        try:
            structures = [{"id": structure.value, "name": structure.value.replace('_', ' ').title()} 
                         for structure in StoryStructure]
            return StandardResponse(
                success=True,
                message="Story structures retrieved successfully",
                data=structures
            )
        except Exception as e:
            logger.error(f"Error retrieving story structures: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # ========================================================================
    # Error Handler for Testing Blacklisting (Development Only)
    # ========================================================================
    
    @app.get("/test/invalid-request")
    async def test_invalid_request():
        """Test endpoint that always returns 400 - for testing IP blacklisting."""
        raise HTTPException(status_code=400, detail="This is a test invalid request")
    
    @app.get("/test/not-found")
    async def test_not_found():
        """Test endpoint that always returns 404 - for testing IP blacklisting."""
        raise HTTPException(status_code=404, detail="Test resource not found")
    
    return app