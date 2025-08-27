from __future__ import annotations
from typing import Dict, List, Iterable, Optional, Tuple
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


class RefinedResearch(BaseModel):
    """
    Generic, content-agnostic research container.

    Structure:
      {
        "<category>": [
          "<concise, sourced or source-ready statement>",
          ...
        ],
        ...
      }

    - Categories are free-form strings (e.g., "medical", "finance", "NYC landscape & landmarks").
    - Each category holds a list of concise statements (strings).
    - Extra keys are forbidden to avoid shape drift.
    """
    model_config = ConfigDict(extra="forbid")

    # Primary payload: category -> list of statements
    categories: Dict[str, List[str]] = Field(default_factory=dict)

    # --------- Validators ---------

    @field_validator("categories")
    @classmethod
    def _normalize_categories(
        cls, v: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        - Trim category names.
        - Drop empty category names.
        - For each list: trim items, drop empties, de-duplicate while preserving order.
        """
        def _dedupe_keep_order(items: Iterable[str]) -> List[str]:
            seen = set()
            out: List[str] = []
            for s in items:
                if s not in seen:
                    seen.add(s)
                    out.append(s)
            return out

        cleaned: Dict[str, List[str]] = {}
        for raw_key, items in (v or {}).items():
            key = (raw_key or "").strip()
            if not key:
                # Skip empty category names
                continue
            # Normalize each statement
            normalized = [it.strip() for it in (items or []) if isinstance(it, str) and it.strip()]
            normalized = _dedupe_keep_order(normalized)
            cleaned[key] = normalized

        return cleaned

    @model_validator(mode="after")
    def _basic_integrity(self) -> "RefinedResearch":
        if not self.categories:
            raise ValueError("categories must contain at least one category with at least one statement.")
        nonempty = {k: v for k, v in self.categories.items() if v}
        if not nonempty:
            raise ValueError("all categories are empty; provide at least one non-empty list of statements.")
        return self

    # --------- Convenience API ---------

    def add_item(self, category: str, statement: str) -> None:
        """Add a single statement to a category (creates the category if missing)."""
        c = category.strip()
        s = statement.strip()
        if not c or not s:
            return
        bucket = self.categories.setdefault(c, [])
        if s not in bucket:
            bucket.append(s)

    def add_items(self, category: str, statements: Iterable[str]) -> None:
        """Add multiple statements to a category (deduplicates)."""
        for st in statements:
            self.add_item(category, st)

    def remove_item(self, category: str, statement: str) -> None:
        """Remove a specific statement from a category (no error if absent)."""
        c = category.strip()
        s = statement.strip()
        if not c or not s or c not in self.categories:
            return
        self.categories[c] = [it for it in self.categories[c] if it != s]
        if not self.categories[c]:
            # Keep empty category or drop? Here we drop to keep data tight.
            del self.categories[c]

    def rename_category(self, old: str, new: str) -> None:
        """Rename a category, merging if target exists."""
        o, n = old.strip(), new.strip()
        if not o or not n or o == n or o not in self.categories:
            return
        if n in self.categories:
            # Merge and dedupe
            existing = self.categories[n]
            for it in self.categories[o]:
                if it not in existing:
                    existing.append(it)
            del self.categories[o]
        else:
            self.categories[n] = self.categories.pop(o)

    def merge(self, other: "RefinedResearch") -> "RefinedResearch":
        """Return a new RefinedResearch that merges this with another (deduplicated)."""
        out = RefinedResearch(categories={k: v[:] for k, v in self.categories.items()})
        for cat, items in other.categories.items():
            out.add_items(cat, items)
        return out

    def filter_categories(self, keep: Iterable[str]) -> "RefinedResearch":
        """Return a new RefinedResearch with only selected categories."""
        wanted = {k.strip() for k in keep if isinstance(k, str)}
        subset = {k: v[:] for k, v in self.categories.items() if k in wanted}
        return RefinedResearch(categories=subset)

    def search(self, keyword: str, case_sensitive: bool = False) -> Dict[str, List[str]]:
        """
        Simple keyword search across statements, returning matched items per category.
        """
        if not keyword:
            return {}
        key = keyword if case_sensitive else keyword.lower()
        hits: Dict[str, List[str]] = {}
        for cat, items in self.categories.items():
            matched: List[str] = []
            for s in items:
                hay = s if case_sensitive else s.lower()
                if key in hay:
                    matched.append(s)
            if matched:
                hits[cat] = matched
        return hits

    def counts(self) -> Tuple[int, int]:
        """Return (num_categories, total_statements)."""
        total = sum(len(v) for v in self.categories.values())
        return (len(self.categories), total)

    # --------- JSON helpers ---------

    def to_json_dict(self) -> Dict[str, List[str]]:
        """Dump in the flat mapping format shown in the sample (exclude empty categories)."""
        return {k: v[:] for k, v in self.categories.items() if v}

    def to_json_str(self, indent: int = 2) -> str:
        return self.model_dump_json(by_alias=False, exclude_none=True, indent=indent)

    @classmethod
    def from_json_dict(cls, data: Dict[str, List[str]]) -> "RefinedResearch":
        # Handle both flat mapping and nested structure
        if "categories" in data and isinstance(data["categories"], dict):
            return cls.model_validate(data)
        else:
            return cls.model_validate({"categories": data})

    @classmethod
    def from_json_str(cls, text: str) -> "RefinedResearch":
        # Accepts either {"categories": {...}} or a plain {"cat": [...]} mapping
        try:
            # First try the canonical shape
            return cls.model_validate_json(text)
        except Exception:
            # If the JSON is a flat mapping, wrap it
            import json as _json
            raw = _json.loads(text)
            if isinstance(raw, dict) and "categories" not in raw:
                return cls.model_validate({"categories": raw})
            raise
