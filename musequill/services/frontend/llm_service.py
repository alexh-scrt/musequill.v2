import asyncio
import logging
from typing import Dict, List, Optional, Any

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import langchain and ollama
from langchain_ollama import OllamaLLM
from langchain.schema import BaseMessage, HumanMessage, SystemMessage


logger = logging.getLogger(__name__)

# ============================================================================
# LLM Service Integration
# ============================================================================

class LLMService:
    """Service for LLM communication via Ollama."""
    
    def __init__(self, model_name: str = "llama3.1", base_url: str = "http://localhost:11434"):
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
    
    async def analyze_concept(self, concept: str) -> Dict[str, Any]:
        """Analyze initial book concept and extract key elements."""
        prompt = f"""
        Analyze this book concept and extract key elements:
        
        Concept: "{concept}"
        
        Please identify:
        1. Primary genre signals (fantasy, romance, mystery, etc.)
        2. Target audience indicators (adult, young adult, children)
        3. Setting type (contemporary, historical, fantasy world, etc.)
        4. Tone and style indicators (dark, humorous, serious, etc.)
        5. Story complexity level (simple, moderate, complex)
        
        Respond in JSON format with these fields:
        {{
            "genre_signals": ["list", "of", "detected", "genres"],
            "audience_signals": ["target", "audience", "indicators"],
            "setting_signals": ["setting", "type", "indicators"],
            "tone_signals": ["tone", "indicators"],
            "complexity": "simple/moderate/complex"
        }}
        """
        
        try:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            # Parse JSON response (basic parsing for POC)
            import json
            # Extract JSON from response if it's wrapped in text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return {"genre_signals": ["general"], "audience_signals": ["adult"], 
                       "setting_signals": ["contemporary"], "tone_signals": ["neutral"], 
                       "complexity": "moderate"}
        except Exception as e:
            logger.error(f"Error analyzing concept: {e}")
            return {"genre_signals": ["general"], "audience_signals": ["adult"], 
                   "setting_signals": ["contemporary"], "tone_signals": ["neutral"], 
                   "complexity": "moderate"}
    
    async def suggest_options(self, step_name: str, concept: str, previous_selections: Dict[str, str], 
                            available_options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get LLM suggestions for wizard step options."""
        
        # Format previous selections
        selections_text = "\n".join([f"- {k}: {v}" for k, v in previous_selections.items()])
        
        # Format available options
        options_text = "\n".join([f"- {opt['id']}: {opt['name']} - {opt.get('description', '')}" 
                                 for opt in available_options])
        
        prompt = f"""
        You are helping a user create a commercially successful book. 
        
        Book concept: "{concept}"
        
        Previous selections:
        {selections_text}
        
        Current step: {step_name}
        Available options:
        {options_text}
        
        Please:
        1. Recommend the top 3-4 most suitable options for commercial success
        2. Provide a brief reasoning for each recommendation
        3. Score each recommended option from 0-100 based on commercial potential
        
        Focus on market appeal, genre consistency, and commercial viability.
        
        Respond in JSON format:
        {{
            "recommendations": [
                {{
                    "option_id": "option_identifier",
                    "score": 85,
                    "reasoning": "Brief explanation of why this works commercially"
                }}
            ],
            "general_reasoning": "Overall reasoning for these recommendations"
        }}
        """
        
        try:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            import json
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback - return top 3 options with default scores
                return {
                    "recommendations": [
                        {"option_id": opt["id"], "score": 80, "reasoning": "Good commercial option"}
                        for opt in available_options[:3]
                    ],
                    "general_reasoning": "These options offer good commercial potential."
                }
        except Exception as e:
            logger.error(f"Error getting LLM suggestions: {e}")
            # Return fallback recommendations
            return {
                "recommendations": [
                    {"option_id": opt["id"], "score": 70, "reasoning": "Recommended option"}
                    for opt in available_options[:3]
                ],
                "general_reasoning": "Standard commercial recommendations."
            }

