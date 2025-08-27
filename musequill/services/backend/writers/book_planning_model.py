from __future__ import annotations
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


# ---------- Leaf models ----------

class Metadata(BaseModel):
    """Generic book metadata."""
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1)
    logline: str = Field(..., min_length=1)
    theme: Optional[str] = Field(None)  # keep single combined theme string (generic)
    target_chapters: Optional[int] = Field(None, ge=1)
    act_count: Optional[int] = Field(None, ge=1)
    audience_fit: Optional[str] = None
    content_warnings: List[str] = Field(default_factory=list)

    @field_validator("title", "logline", "theme", "audience_fit")
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

    @field_validator("content_warnings")
    @classmethod
    def _clean_warnings(cls, v: List[str]) -> List[str]:
        return [w.strip() for w in v if w and w.strip()]


class GlobalSettings(BaseModel):
    """Global narrative settings (open-ended)."""
    model_config = ConfigDict(extra="forbid")
    tone: Optional[str] = None
    pov: Optional[str] = None

    @field_validator("tone", "pov")
    @classmethod
    def _strip_text(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class ActEntry(BaseModel):
    """Act description; act can be any positive integer."""
    model_config = ConfigDict(extra="forbid")
    act: int = Field(..., ge=1)
    chapters: Optional[int] = Field(None, ge=0)  # number of chapters in act (optional)
    description: str = Field(..., min_length=1)
    turning_points: List[str] = Field(default_factory=list)
    motifs: List[str] = Field(default_factory=list)

    @field_validator("description")
    @classmethod
    def _strip_desc(cls, v: str) -> str:
        return v.strip()

    @field_validator("turning_points", "motifs")
    @classmethod
    def _clean_lists(cls, v: List[str]) -> List[str]:
        return [x.strip() for x in v if x and x.strip()]


class ChapterBeats(BaseModel):
    """Single chapter entry with beats."""
    model_config = ConfigDict(extra="forbid")
    chapter: int = Field(..., ge=1)
    beats: List[str] = Field(..., min_items=1)

    @field_validator("beats")
    @classmethod
    def _trim_beats(cls, v: List[str]) -> List[str]:
        cleaned = [b.strip() for b in v if b and b.strip()]
        if not cleaned:
            raise ValueError("beats must contain at least one non-empty string.")
        return cleaned


# ---------- Root model ----------

class GenericBookPlan(BaseModel):
    """
    Content-agnostic plan model that matches the given structure:
      - metadata
      - global_settings
      - acts[]
      - chapter_beats[]
    """
    model_config = ConfigDict(extra="forbid")

    metadata: Metadata
    global_settings: GlobalSettings
    acts: List[ActEntry] = Field(default_factory=list)
    chapter_beats: List[ChapterBeats] = Field(default_factory=list)

    # ---------- Validators ----------

    @model_validator(mode="after")
    def _integrity_checks(self) -> "GenericBookPlan":
        # Acts: ensure unique act numbers
        act_nums = [a.act for a in self.acts]
        if len(act_nums) != len(set(act_nums)):
            raise ValueError("acts contains duplicate act numbers.")

        # Chapter beats: ensure unique chapter indices
        chap_nums = [c.chapter for c in self.chapter_beats]
        if len(chap_nums) != len(set(chap_nums)):
            raise ValueError("chapter_beats contains duplicate chapter numbers.")

        # Optional: if target_chapters is provided, sanity check count
        if self.metadata.target_chapters is not None:
            if len(self.chapter_beats) > self.metadata.target_chapters * 2:
                # Very loose guardrail; keep generic (can adjust or remove)
                raise ValueError(
                    "chapter_beats length is implausibly larger than target_chapters*2."
                )

        # Optional: if act_count provided, check against acts length (soft)
        if self.metadata.act_count is not None and self.acts:
            if self.metadata.act_count != len(self.acts):
                # Not a hard fail; choose to warn by raising or skip. We enforce here.
                raise ValueError(
                    "metadata.act_count does not match the number of items in acts."
                )

        # Minimal usefulness
        if not self.acts:
            raise ValueError("acts must contain at least one act entry.")
        if not self.chapter_beats:
            raise ValueError("chapter_beats must contain at least one chapter entry.")

        return self

    # ---------- Convenience I/O ----------

    def to_json_dict(self) -> Dict[str, Union[str, int, list, dict]]:
        """JSON-friendly dict (exclude None)."""
        return self.model_dump(mode="json", exclude_none=True)

    def to_json_str(self, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent, exclude_none=True)

    @classmethod
    def from_json_str(cls, text: str) -> "GenericBookPlan":
        return cls.model_validate_json(text)
