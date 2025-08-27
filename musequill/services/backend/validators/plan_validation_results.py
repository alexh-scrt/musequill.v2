from dataclasses import dataclass
from typing import List, Literal, Optional

@dataclass
class ValidationIssue:
    severity: Literal["error","warn"]   # "error" reduces validity; "warn" reduces score
    code: str                           # machine-friendly
    message: str                        # human-friendly, concise

@dataclass
class ValidationResult:
    is_valid: bool
    score: float                        # 0.0–1.0
    issues: List[ValidationIssue]
    regenerate: bool
    refined_prompt: Optional[str] = None
