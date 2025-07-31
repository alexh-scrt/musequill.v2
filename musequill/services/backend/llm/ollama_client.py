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
    
    def __init__(
        self, 
        model_name: str = "llama3.3:70b", 
        base_url: str = "http://localhost:11434",
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0
    ):
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.llm = None
        
    async def initialize(self):
        """Initialize LLM connection."""
        try:
            # Prepare initialization parameters
            init_params = {
                "model": self.model_name,
                "base_url": self.base_url,
                "temperature": self.temperature,
                "top_p": self.top_p
            }
            
            # Only add max_tokens if it's specified (some models don't support it)
            if self.max_tokens is not None:
                init_params["num_predict"] = self.max_tokens  # Ollama uses 'num_predict' instead of 'max_tokens'
            
            self.llm = OllamaLLM(**init_params)
            logger.info(f"LLM service initialized with model: {self.model_name}, "
                       f"temperature: {self.temperature}, top_p: {self.top_p}, "
                       f"max_tokens: {self.max_tokens}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    async def generate(
        self, 
        prompt: str, 
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate response from LLM with optional parameter overrides.
        
        Args:
            prompt: The input prompt
            temperature: Override temperature for this request
            max_tokens: Override max_tokens for this request  
            top_p: Override top_p for this request
            
        Returns:
            Dict containing response and metadata
        """
        try:
            if not self.llm:
                raise RuntimeError("LLM is not initialized")
            
            # Use per-request parameters if provided, otherwise use instance defaults
            request_temperature = temperature if temperature is not None else self.temperature
            request_max_tokens = max_tokens if max_tokens is not None else self.max_tokens
            request_top_p = top_p if top_p is not None else self.top_p
            
            # For per-request parameter changes, we need to update the LLM instance
            # Note: langchain-ollama might not support dynamic parameter changes
            # In that case, you might need to create a new instance or use the Ollama API directly
            if (request_temperature != self.temperature or 
                request_max_tokens != self.max_tokens or 
                request_top_p != self.top_p):
                
                logger.info(f"Using custom parameters for this request: "
                           f"temperature={request_temperature}, "
                           f"max_tokens={request_max_tokens}, "
                           f"top_p={request_top_p}")
                
                # Create temporary LLM instance with custom parameters
                temp_params = {
                    "model": self.model_name,
                    "base_url": self.base_url,
                    "temperature": request_temperature,
                    "top_p": request_top_p
                }
                
                if request_max_tokens is not None:
                    temp_params["num_predict"] = request_max_tokens
                
                temp_llm = OllamaLLM(**temp_params)
                llm_to_use = temp_llm
            else:
                llm_to_use = self.llm
            
            # Start timing
            start_time = time.perf_counter()
            response = await asyncio.to_thread(llm_to_use.invoke, prompt)
            end_time = time.perf_counter()
            
            # Calculate elapsed time in seconds
            elapsed_time = end_time - start_time
            
            return {
                "response": response,
                "timelapse": elapsed_time,
                "parameters_used": {
                    "temperature": request_temperature,
                    "max_tokens": request_max_tokens,
                    "top_p": request_top_p,
                    "model": self.model_name
                }
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
    
    def update_default_parameters(
        self, 
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None
    ):
        """
        Update the default parameters for future requests.
        This will require re-initialization to take effect.
        
        Args:
            temperature: New default temperature
            max_tokens: New default max_tokens
            top_p: New default top_p
        """
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if top_p is not None:
            self.top_p = top_p
            
        logger.info(f"Updated default parameters: temperature={self.temperature}, "
                   f"max_tokens={self.max_tokens}, top_p={self.top_p}")
        logger.info("Call initialize() again to apply these changes to the LLM instance")
    
    def get_current_parameters(self) -> Dict[str, Any]:
        """Get the current parameter configuration."""
        return {
            "model_name": self.model_name,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "is_initialized": self.llm is not None
        }