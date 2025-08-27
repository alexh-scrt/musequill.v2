# qa_session.py
from __future__ import annotations
import json
from typing import Any, Dict, List, Union, Callable

Context = Union[str, Dict[str, Any], List[Any]]

SYSTEM_INSTRUCTIONS = """You are an extractive question-answering assistant.
Answer ONLY using the provided CONTEXT blocks.
Return the SHORTEST possible answer span.
If the answer is not present, output exactly: unknown
Rules:
- No explanations
- No prefices/suffixes (no "Answer:", no punctuation)
- If the question asks for a name, return just the name.
- If a list is requested, return a comma-separated list with no extra text.
"""

def _format_context_block(name: str, data: Context) -> str:
    if isinstance(data, (dict, list)):
        body = json.dumps(data, ensure_ascii=False, indent=2)
        kind = "json"
    else:
        body = str(data)
        kind = "text"
    return f"<CONTEXT id='{name}' type='{kind}'>\n{body}\n</CONTEXT>"

class QASession:
    def __init__(self, llm_fn: Callable[..., str], *, model: str | None = None):
        """
        llm_fn: your callable like llm(prompt, temperature=..., top_p=..., model=...)
        """
        self.llm = llm_fn
        self.model = model
        self._contexts: List[str] = []

    def add_context(self, name: str, data: Context) -> None:
        """Add any text or JSON blob as a named context block."""
        self._contexts.append(_format_context_block(name, data))

    def ask(self,
            question: str,
            *,
            default: str = "unknown",
            temperature: float = 0.1,
            top_p: float = 0.9,
            repeat_penalty: float = 1.15,
            num_predict: int = 32) -> str:
        """
        Ask a question and get a short, extractive answer.
        If not answerable from context, returns `default`.
        """
        prompt = (
            f"{SYSTEM_INSTRUCTIONS}\n\n"
            f"{''.join(self._contexts)}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )

        raw = self.llm(
            prompt,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            num_predict=num_predict,
            model=self.model
        ).strip()

        # Keep only the first line/token span, strip quotes and trailing punctuation.
        ans = raw.splitlines()[0].strip().strip(" .,:;\"'`")
        if not ans:
            ans = default
        # Enforce the "unknown" contract
        if ans.lower().startswith("i don't know") or "not provided" in ans.lower():
            ans = default
        return ans
