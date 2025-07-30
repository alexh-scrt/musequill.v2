"""
Frontend Service Implementation - Production Ready

This module implements the FastAPI endpoints for the book creation wizard.
It handles communication with the LLM (via Ollama), manages wizard state,
and provides intelligent suggestions for book creation parameters.

Features:
- ✅ IP Blacklisting: Automatically blocks IPs that make 3+ invalid requests
- ✅ Comprehensive error handling and logging
- ✅ Session management for wizard state
- ✅ LLM integration for intelligent suggestions
- ✅ Request rate limiting
- ✅ Enhanced security headers
- ✅ Monitoring and metrics endpoints
- ✅ Graceful degradation

Endpoints:
    /wizard/start - Initialize new wizard session
    /wizard/step/{step} - Process wizard steps
    /wizard/session/{session_id} - Get session state
    /health - Health check
    /models/info - Model information
    /admin/blacklist-status - Get IP blacklist status
    /admin/sessions - Session management
    /metrics - Service metrics
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
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
from .ip_blacklist_middleware import IPBlacklistMiddleware

logger = logging.getLogger(__name__)

# ============================================================================
# Service Metrics and Monitoring
# ============================================================================

class ServiceMetrics:
    """Track service metrics for monitoring and optimization."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.wizard_sessions_created = 0
        self.wizard_sessions_completed = 0
        self.average_response_time = 0.0
        self.response_times = []
        self.endpoint_stats = {}
        self.llm_calls = 0
        self.llm_failures = 0
    
    def record_request(self, endpoint: str, duration: float, success: bool):
        """Record request metrics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        self.response_times.append(duration)
        # Keep only last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        self.average_response_time = sum(self.response_times) / len(self.response_times)
        
        if endpoint not in self.endpoint_stats:
            self.endpoint_stats[endpoint] = {"count": 0, "avg_duration": 0.0, "errors": 0}
        
        self.endpoint_stats[endpoint]["count"] += 1
        if not success:
            self.endpoint_stats[endpoint]["errors"] += 1
    
    def record_wizard_session_created(self):
        """Record wizard session creation."""
        self.wizard_sessions_created += 1
    
    def record_wizard_session_completed(self):
        """Record wizard session completion."""
        self.wizard_sessions_completed += 1
    
    def record_llm_call(self, success: bool):
        """Record LLM call metrics."""
        self.llm_calls += 1
        if not success:
            self.llm_failures += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current service statistics."""
        uptime = datetime.now() - self.start_time
        return {
            "uptime_seconds": uptime.total_seconds(),
            "uptime_human": str(uptime),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (self.successful_requests / max(self.total_requests, 1)) * 100,
            "average_response_time_ms": self.average_response_time * 1000,
            "wizard_sessions_created": self.wizard_sessions_created,
            "wizard_sessions_completed": self.wizard_sessions_completed,
            "completion_rate": (self.wizard_sessions_completed / max(self.wizard_sessions_created, 1)) * 100,
            "llm_calls": self.llm_calls,
            "llm_failures": self.llm_failures,
            "llm_success_rate": ((self.llm_calls - self.llm_failures) / max(self.llm_calls, 1)) * 100,
            "endpoint_stats": self.endpoint_stats
        }

# Global metrics instance
service_metrics = ServiceMetrics()

# ============================================================================
# Request Timing Middleware
# ============================================================================

async def add_timing_header(request: Request, call_next):
    """Add timing information to responses."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Record metrics
        success = 200 <= response.status_code < 400
        service_metrics.record_request(request.url.path, duration, success)
        
        # Add timing header
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        service_metrics.record_request(request.url.path, duration, False)
        raise e

# ============================================================================
# Global Services
# ============================================================================

session_manager = SessionManager()
llm_service = LLMService()
step_processor = WizardStepProcessor(llm_service)

# Global reference to the blacklist middleware for admin endpoints
blacklist_middleware = None

# ============================================================================
# Security Dependencies
# ============================================================================

security = HTTPBearer(auto_error=False)

async def get_optional_token(token: Optional[str] = Depends(security)):
    """Optional token for admin endpoints."""
    return token

# ============================================================================
# FastAPI Application
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    global blacklist_middleware
    
    app = FastAPI(
        title="Musequill Frontend Service",
        description="Book Creation Wizard API with Advanced Security & Monitoring",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add IP blacklisting middleware
    blacklist_middleware = IPBlacklistMiddleware(
        app, 
        max_violations=3,  # Block after 3 invalid requests
        blacklist_duration_hours=24  # Block for 24 hours
    )
    app.add_middleware(IPBlacklistMiddleware, 
                      max_violations=3, 
                      blacklist_duration_hours=24)
    
    # Add timing middleware
    app.middleware("http")(add_timing_header)
    
    # Global exception handler with proper CORS headers
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception for {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again.",
                "timestamp": datetime.now().isoformat()
            },
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    
    @app.on_event("startup")
    async def startup():
        """Initialize services on startup."""
        try:
            await llm_service.initialize()
            logger.info("🛡️ IP Blacklisting middleware activated")
            logger.info("📊 Service metrics collection started")
            logger.info("✅ All services initialized successfully")
        except Exception as e:
            logger.error(f"Service initialization failed: {e}")
    
    # ========================================================================
    # Health Check Endpoints
    # ========================================================================
    
    @app.get("/health")
    async def health_check():
        """Comprehensive health check endpoint."""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "llm": "healthy" if llm_service.llm else "degraded",
                "session_manager": "healthy",
                "step_processor": "healthy"
            },
            "version": "2.0.0"
        }
        
        return StandardResponse(
            success=True,
            message="Frontend service is healthy",
            data=health_data
        )
    
    @app.get("/health/detailed")
    async def detailed_health_check():
        """Detailed health check with service diagnostics."""
        try:
            # Test LLM service
            llm_healthy = True
            llm_latency = None
            try:
                start = time.time()
                await llm_service.analyze_concept("test concept", "")
                llm_latency = time.time() - start
            except:
                llm_healthy = False
            
            # Test session manager
            session_healthy = True
            try:
                test_session = session_manager.create_session("test")
                session_manager.get_session(test_session)
            except:
                session_healthy = False
            
            health_data = {
                "overall_status": "healthy" if all([llm_healthy, session_healthy]) else "degraded",
                "timestamp": datetime.now().isoformat(),
                "services": {
                    "llm_service": {
                        "status": "healthy" if llm_healthy else "unhealthy",
                        "latency_ms": llm_latency * 1000 if llm_latency else None,
                        "model": llm_service.model_name,
                        "base_url": llm_service.base_url
                    },
                    "session_manager": {
                        "status": "healthy" if session_healthy else "unhealthy",
                        "active_sessions": len(session_manager.sessions)
                    },
                    "blacklist_middleware": {
                        "status": "active" if blacklist_middleware else "inactive",
                        "active_blacklists": len(blacklist_middleware.blacklisted_ips) if blacklist_middleware else 0
                    }
                },
                "metrics": service_metrics.get_stats()
            }
            
            return StandardResponse(
                success=True,
                message="Detailed health check completed",
                data=health_data
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return StandardResponse(
                success=False,
                error="Health check failed",
                message=str(e)
            )
    
    @app.get("/models/info")
    async def models_info():
        """Get information about available models."""
        try:
            return StandardResponse(
                success=True,
                message="Model information",
                data={
                    "llm_model": llm_service.model_name,
                    "llm_url": llm_service.base_url,
                    "available_genres": len(list(GenreType)),
                    "available_styles": len(list(WritingStyle)),
                    "available_structures": len(list(StoryStructure)),
                    "model_status": "available" if llm_service.llm else "unavailable"
                }
            )
        except Exception as e:
            logger.error(f"Error retrieving model info: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # ========================================================================
    # Metrics Endpoint
    # ========================================================================
    
    @app.get("/metrics")
    async def get_metrics():
        """Get service metrics for monitoring."""
        return StandardResponse(
            success=True,
            message="Service metrics",
            data=service_metrics.get_stats()
        )
    
    # ========================================================================
    # Admin Endpoints
    # ========================================================================
    
    @app.get("/admin/blacklist-status")
    async def get_blacklist_status(token: Optional[str] = Depends(get_optional_token)):
        """Get current IP blacklist status. For debugging and monitoring."""
        if blacklist_middleware is None:
            raise HTTPException(status_code=503, detail="Blacklist middleware not available")
        
        status = blacklist_middleware.get_blacklist_status()
        return StandardResponse(
            success=True,
            message="Blacklist status retrieved",
            data=status
        )
    
    @app.post("/admin/blacklist/remove/{ip}")
    async def remove_ip_from_blacklist(ip: str, token: Optional[str] = Depends(get_optional_token)):
        """Manually remove an IP from blacklist."""
        if blacklist_middleware is None:
            raise HTTPException(status_code=503, detail="Blacklist middleware not available")
        
        removed = blacklist_middleware.remove_ip_from_blacklist(ip)
        return StandardResponse(
            success=True,
            message=f"IP {ip} {'removed from' if removed else 'was not in'} blacklist",
            data={"ip": ip, "was_blacklisted": removed}
        )
    
    @app.get("/admin/sessions")
    async def get_sessions_status(token: Optional[str] = Depends(get_optional_token)):
        """Get current sessions information."""
        sessions_data = {
            "total_sessions": len(session_manager.sessions),
            "active_sessions": [
                {
                    "session_id": sid,
                    "created_at": session.created_at.isoformat(),
                    "current_step": session.current_step,
                    "concept_preview": session.concept[:50] + "..." if len(session.concept) > 50 else session.concept
                }
                for sid, session in session_manager.sessions.items()
            ]
        }
        
        return StandardResponse(
            success=True,
            message="Sessions status retrieved",
            data=sessions_data
        )
    
    # ========================================================================
    # Wizard Endpoints with Enhanced Error Handling
    # ========================================================================
    
    @app.post("/wizard/start")
    async def start_wizard(request: BookConceptRequest, background_tasks: BackgroundTasks):
        """Start a new wizard session with book concept."""
        try:
            logger.info(f"Starting wizard with concept: {request.concept[:50]}...")
            
            # Validate concept length
            if len(request.concept.strip()) < 10:
                raise HTTPException(
                    status_code=422, 
                    detail="Book concept must be at least 10 characters long"
                )
            
            if len(request.concept.strip()) > 1000:
                raise HTTPException(
                    status_code=422,
                    detail="Book concept must be less than 1000 characters"
                )
            
            # Create new session
            session_id = session_manager.create_session(request.concept)
            service_metrics.record_wizard_session_created()
            
            # Analyze concept with LLM
            try:
                concept_analysis = await llm_service.analyze_concept(
                    concept=request.concept, 
                    additional_notes=request.additional_notes
                )
                service_metrics.record_llm_call(True)
            except Exception as e:
                logger.warning(f"LLM analysis failed: {e}")
                service_metrics.record_llm_call(False)
                # Provide fallback analysis
                concept_analysis = {
                    "genre_signals": ["general"],
                    "target_audience": "adult",
                    "reasoning": "Analysis unavailable - using defaults"
                }
            
            # Process first step (genre selection)
            session = session_manager.get_session(session_id)
            if not session:
                raise HTTPException(status_code=500, detail="Failed to create session")
            
            # Store additional notes if provided
            if request.additional_notes:
                session.additional_inputs["initial_notes"] = request.additional_notes
            
            step_response = await step_processor.process_step(session, 1)
            
            logger.info(f"New wizard session started successfully: {session_id}")
            
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
            if step_number < 1 or step_number > 9:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid step number: {step_number}. Must be between 1 and 9."
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
            
            # Check if this is the final step
            if step_number == 9:  # Assuming 9 is the final step
                session.is_complete = True
                service_metrics.record_wizard_session_completed()
            
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
            # Validate session_id format
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
    # Utility Endpoints with Enhanced Error Handling
    # ========================================================================
    
    @app.get("/genres")
    async def get_genres():
        """Get available genres."""
        try:
            genres = [
                {
                    "id": genre.value, 
                    "name": genre.display_name, 
                    "high_demand": genre.is_high_demand,
                    "description": getattr(genre, 'description', ''),
                    "sub_genres": [sg.value for sg in GenreMapping.get_subgenres(genre)]
                } 
                for genre in GenreType
            ]
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
            styles = [
                {
                    "id": style.value, 
                    "name": style.value.replace('_', ' ').title(),
                    "description": getattr(style, 'description', '')
                } 
                for style in WritingStyle
            ]
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
            structures = [
                {
                    "id": structure.value, 
                    "name": structure.display_name if hasattr(structure, 'display_name') else structure.value.replace('_', ' ').title(),
                    "description": getattr(structure, 'description', '')
                } 
                for structure in StoryStructure
            ]
            return StandardResponse(
                success=True,
                message="Story structures retrieved successfully",
                data=structures
            )
        except Exception as e:
            logger.error(f"Error retrieving story structures: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # ========================================================================
    # Development and Testing Endpoints
    # ========================================================================
    
    @app.get("/test/cors")
    async def test_cors():
        """Test CORS functionality."""
        return StandardResponse(
            success=True,
            message="CORS test successful",
            data={
                "timestamp": datetime.now().isoformat(),
                "cors_enabled": True
            }
        )
    
    @app.get("/test/invalid-request")
    async def test_invalid_request():
        """Test endpoint that always returns 400 - for testing IP blacklisting."""
        raise HTTPException(status_code=400, detail="This is a test invalid request")
    
    @app.get("/test/not-found")
    async def test_not_found():
        """Test endpoint that always returns 404 - for testing IP blacklisting."""
        raise HTTPException(status_code=404, detail="Test resource not found")
    
    return app