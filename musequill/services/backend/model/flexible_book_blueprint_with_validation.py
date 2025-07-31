from pydantic import BaseModel, Field
from typing import Optional

class Phase1(BaseModel):
    book_title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    target_audience: Optional[str]
    word_count: Optional[str]
    writing_style: Optional[str]

class Phase2(BaseModel):
    story_structure: Optional[str]
    plot_type: Optional[str]
    conflict: Optional[str]
    character_arc: Optional[str]

class WorldBuilding(BaseModel):
    setting: Optional[str]
    inhabitants: Optional[str]

class Phase3(BaseModel):
    world_building: Optional[WorldBuilding]
    magic_system: Optional[str]

class CharacterDevelopment(BaseModel):
    protagonist: Optional[str]
    antagonist: Optional[str]
    supporting_characters: Optional[str]

class Phase4(BaseModel):
    character_development: Optional[CharacterDevelopment]
    character_relationships: Optional[str]

class PacingAndTone(BaseModel):
    pace: Optional[str]
    tone: Optional[str]

class LanguageAndStyle(BaseModel):
    narrative_voice: Optional[str]
    description: Optional[str]

class Phase5(BaseModel):
    pacing_and_tone: Optional[PacingAndTone]
    language_and_style: Optional[LanguageAndStyle]

class EditingAndRevision(BaseModel):
    structure: Optional[str]
    character_consistency: Optional[str]
    pacing: Optional[str]

class Proofreading(BaseModel):
    grammar_and_spelling: Optional[str]
    formatting: Optional[str]

class Phase6(BaseModel):
    editing_and_revision: Optional[EditingAndRevision]
    proofreading: Optional[Proofreading]

class MarketingStrategies(BaseModel):
    social_media: Optional[str]
    influencer_partnerships: Optional[str]

class MarketingAndPublishing(BaseModel):
    genre_classification: Optional[str]
    target_audience: Optional[str]
    marketing_strategies: Optional[MarketingStrategies]

class PublishingOptions(BaseModel):
    traditional_publishing: Optional[str]
    self_publishing: Optional[str] = Field(None, alias="self-publishing")

class Phase7(BaseModel):
    marketing_and_publishing: Optional[MarketingAndPublishing]
    publishing_options: Optional[PublishingOptions]

class FlexibleBookBlueprint(BaseModel):
    phase1: Optional[Phase1]
    phase2: Optional[Phase2]
    phase3: Optional[Phase3]
    phase4: Optional[Phase4]
    phase5: Optional[Phase5]
    phase6: Optional[Phase6]
    phase7: Optional[Phase7]


    def self_validate(self) -> None:
        from pydantic import BaseModel
        from typing import get_args, get_origin

        def count_fields(obj):
            if not isinstance(obj, BaseModel):
                return 0, 0, []

            total, filled, missing = 0, 0, []

            for name, value in obj.__dict__.items():
                total += 1
                if value is None:
                    missing.append(name)
                elif isinstance(value, BaseModel):
                    sub_total, sub_filled, sub_missing = count_fields(value)
                    total += sub_total
                    filled += sub_filled
                    missing.extend([f"{name}.{m}" for m in sub_missing])
                else:
                    filled += 1

            return total, filled, missing

        total_fields, filled_fields, missing_fields = count_fields(self)
        filled_percent = (filled_fields / total_fields * 100) if total_fields else 0

        print(f"Validation Summary:")
        print(f"  Filled Fields: {filled_fields}/{total_fields} ({filled_percent:.2f}%)")
        print(f"  Missing Fields:")
        for field in missing_fields:
            print(f"    - {field}")
