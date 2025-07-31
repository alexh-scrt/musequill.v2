import asyncio
import logging
from typing import Dict, List, Optional, Any
import json
import time
# Import langchain and ollama
from langchain_ollama import OllamaLLM
from langchain.schema import BaseMessage, HumanMessage, SystemMessage


logger = logging.getLogger(__name__)

# ============================================================================
# LLM Service Integration
# ============================================================================

class LLMService:
    """Service for LLM communication via Ollama."""
    
    def __init__(self, model_name: str = "llama3.3:70b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        
    async def initialize(self):
        """Initialize LLM connection."""
        try:
            self.llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.3  # Lower temperature for more consistent suggestions
            )
            logger.info(f"LLM service initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    async def generate(self, prompt: str) -> Dict[str, Any]:
        try:
            if not self.llm:
                raise RuntimeError("LLM is not initialized")
            
            # Start timing
            start_time = time.perf_counter()
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            end_time = time.perf_counter()
            
            # Calculate elapsed time in seconds
            elapsed_time = end_time - start_time
            
            return {
                "response": response,
                "timelapse": elapsed_time
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in concept analysis: {e}")
            return {
                "error": f"Invalid response: {e}"
            }
        except Exception as e:
            logger.error(f"Error in concept analysis: {e}")
            return {
                "error": str(e)
            }