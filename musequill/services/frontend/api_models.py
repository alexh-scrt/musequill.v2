import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models for API
# ============================================================================

class BookConceptRequest(BaseModel):
    """Request model for initial book concept."""
    concept: str = Field(..., min_length=10, max_length=1000, description="2-3 sentences describing the book idea")
    additional_notes: Optional[str] = Field(None, max_length=500, description="Any additional context or preferences")


class WizardStepRequest(BaseModel):
    """Request model for wizard step processing."""
    session_id: str = Field(..., description="Wizard session ID")
    selection: Optional[str] = Field(None, description="User's selection for current step")
    additional_input: Optional[str] = Field(None, max_length=500, description="Additional user input or context")


class WizardOption(BaseModel):
    """Model for wizard step options."""
    id: str = Field(..., description="Option identifier")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Detailed description")
    recommendation_score: Optional[float] = Field(None, description="LLM recommendation score 0-100")
    market_appeal: Optional[str] = Field(None, description="Commercial appeal indicator")


class WizardStepResponse(BaseModel):
    """Response model for wizard steps."""
    session_id: str
    step_number: int
    step_name: str
    question: str
    options: List[WizardOption]
    llm_reasoning: Optional[str] = None
    can_go_back: bool = False
    is_final_step: bool = False


class WizardSession(BaseModel):
    """Model for wizard session state."""
    session_id: str
    created_at: datetime
    current_step: int
    concept: str
    selections: Dict[str, str] = Field(default_factory=dict)
    additional_inputs: Dict[str, str] = Field(default_factory=dict)
    is_complete: bool = False
    book_summary: Optional[Dict[str, Any]] = None


class StandardResponse(BaseModel):
    """Standard API response format."""
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None