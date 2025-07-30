#!/usr/bin/env python3
"""
Frontend Service Main Entry Point

This is the main entry point for the musequill frontend service that handles
the book creation wizard. It sets up the FastAPI application and starts the server.

Usage:
    python main.py
    
    Or with uvicorn directly:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the Python path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import our frontend application
from musequill.services.frontend.service import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('frontend_service.log')
    ]
)

logger = logging.getLogger(__name__)


def create_frontend_app() -> FastAPI:
    """
    Create and configure the FastAPI application for the frontend service.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Create the main app from service.py
    app = create_app()
    
    # Add CORS middleware for web UI communication
    # This must be added AFTER other middleware for proper order
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8080",
            "http://localhost:3000", 
            "http://127.0.0.1:8080",
            "http://127.0.0.1:3000",
            "https://musequill.ink",
            "http://musequill.ink",
            "https://www.musequill.ink",
            "http://www.musequill.ink",
            "*"  # Allow all origins for development
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Language", 
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-Forwarded-For",
            "X-Real-IP"
        ],
        expose_headers=["*"],
        max_age=86400  # Cache preflight requests for 24 hours
    )
    
    # Modern lifespan events (replaces deprecated on_event)
    from contextlib import asynccontextmanager
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Handle application lifespan events."""
        # Startup
        logger.info("🚀 Musequill Frontend Service starting up...")
        logger.info("📚 Book Creation Wizard ready!")
        logger.info("🌐 CORS configured for musequill.ink and development")
        
        yield
        
        # Shutdown
        logger.info("📚 Musequill Frontend Service shutting down...")
    
    # Note: The actual lifespan will be applied in the enhanced service.py
    
    return app


# Create the app instance
app = create_frontend_app()


async def main():
    """
    Main entry point for running the frontend service.
    """
    try:
        logger.info("Starting Musequill Frontend Service...")
        
        # Configuration
        host = "0.0.0.0"
        port = 8000
        reload = True  # Set to False for production
        
        logger.info(f"Server will start on http://{host}:{port}")
        logger.info("Wizard endpoints will be available at /wizard/")
        logger.info("API documentation available at /docs")
        logger.info("🌐 Accepting CORS requests from musequill.ink")
        
        # Start the server
        config = uvicorn.Config(
            app=app,
            host=host,
            port=port,
            reload=reload,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        await server.serve()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal...")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """
    Entry point when running directly with python main.py
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service failed: {e}")
        sys.exit(1)