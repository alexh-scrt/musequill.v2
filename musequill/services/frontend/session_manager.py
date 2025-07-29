import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


from .api_models import (
    WizardSession,
)

logger = logging.getLogger(__name__)


# ============================================================================
# In-Memory Session Storage (POC)
# ============================================================================

class SessionManager:
    """Simple in-memory session management for POC."""
    
    def __init__(self):
        self.sessions: Dict[str, WizardSession] = {}
    
    def create_session(self, concept: str) -> str:
        """Create new wizard session."""
        session_id = str(uuid.uuid4())
        session = WizardSession(
            session_id=session_id,
            created_at=datetime.now(),
            current_step=1,
            concept=concept
        )
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[WizardSession]:
        """Get session by ID."""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, **updates) -> bool:
        """Update session with new data."""
        if session_id in self.sessions:
            for key, value in updates.items():
                setattr(self.sessions[session_id], key, value)
            return True
        return False
