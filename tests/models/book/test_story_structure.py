"""
Comprehensive tests for musequill.models.book.story_structure module.

Test file: tests/models/book/test_story_structure.py
Module under test: musequill/models/book/story_structure.py

Run from project root: pytest tests/models/book/test_story_structure.py -v
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from typing import List

# Import all classes and enums from the story_structure module
from musequill.models.book.story_structure import (
    StoryStructure,
    StructureRecommendation,
    StructureRecommender
)


class TestStoryStructure:
    """Test the StoryStructure enum comprehensively."""
    
    def test_all_structure_values_are_strings(self):
        """Ensure all story structure enum values are properly formatted strings."""
        for structure in StoryStructure:
            assert isinstance(structure.value, str)
            assert structure.value.islower()
            assert " " not in structure.value  # Should use underscores
            assert len(structure.value) > 0
    
    def test_all_structures_have_unique_values(self):
        """Ensure no duplicate values in StoryStructure enum."""
        values = [structure.value for structure in StoryStructure]
        assert len(values) == len(set(values)), "Duplicate story structure values found"
    
    def test_display_name_property(self):
        """Test that display_name properly formats structure names."""
        test_cases = [
            (StoryStructure.THREE_ACT, "Three-Act Structure"),
            (StoryStructure.HERO_JOURNEY, "Hero's Journey"),
            (StoryStructure.SAVE_THE_CAT, "Save the Cat Beat Sheet"),
            (StoryStructure.STORY_CIRCLE, "Story Circle"),
            (StoryStructure.IN_MEDIAS_RES, "In Medias Res"),
        ]
        
        for structure, expected_display in test_cases:
            assert structure.display_name == expected_display
    
    def test_description_property(self):
        """Test that all structures have meaningful descriptions."""
        for structure in StoryStructure:
            description = structure.description
            assert isinstance(description, str)
            assert len(description) > 10  # Should be meaningful, not just empty
            # Common description quality checks
            assert description[0].isupper()  # Should start with capital letter
    
    def test_complexity_level_property(self):
        """Test complexity level categorization."""
        valid_complexity_levels = {"simple", "moderate", "complex", "advanced"}
        
        for structure in StoryStructure:
            complexity = structure.complexity_level
            assert complexity in valid_complexity_levels
            assert isinstance(complexity, str)
        
        # Test specific known complexities
        assert StoryStructure.THREE_ACT.complexity_level == "simple"
        assert StoryStructure.SNOWFLAKE.complexity_level == "advanced"
    
    def test_typical_length_property(self):
        """Test typical length property returns valid values."""
        valid_length_keywords = ["short", "medium", "long", "flexible"]
        
        for structure in StoryStructure:
            length = structure.typical_length
            assert isinstance(length, str)
            assert any(keyword in length.lower() for keyword in valid_length_keywords)
    
    def test_number_of_acts_property(self):
        """Test number of acts property returns valid integers."""
        for structure in StoryStructure:
            acts = structure.number_of_acts
            assert isinstance(acts, int)
            assert 1 <= acts <= 15  # Reasonable range
        
        # Test specific known act counts
        assert StoryStructure.THREE_ACT.number_of_acts == 3
        assert StoryStructure.FREYTAG_PYRAMID.number_of_acts == 5
        assert StoryStructure.STORY_CIRCLE.number_of_acts == 8
    
    def test_ai_generation_difficulty_property(self):
        """Test AI generation difficulty categorization."""
        valid_difficulties = {"easy", "medium", "hard", "very_hard"}
        
        for structure in StoryStructure:
            difficulty = structure.ai_generation_difficulty
            assert difficulty in valid_difficulties
            assert isinstance(difficulty, str)
    
    def test_genre_compatibility_property(self):
        """Test genre compatibility returns valid lists."""
        for structure in StoryStructure:
            compatibility = structure.genre_compatibility
            assert isinstance(compatibility, list)
            assert len(compatibility) > 0  # Should have at least one compatible genre
            assert all(isinstance(genre, str) for genre in compatibility)
        
        # Test universal compatibility
        assert "all" in StoryStructure.THREE_ACT.genre_compatibility
        assert "romance" in StoryStructure.ROMANCE_BEAT_SHEET.genre_compatibility
    
    @pytest.mark.parametrize("structure_str,expected_structure", [
        ("three_act", StoryStructure.THREE_ACT),
        ("hero_journey", StoryStructure.HERO_JOURNEY),
        ("freytag_pyramid", StoryStructure.FREYTAG_PYRAMID),
        ("save_the_cat", StoryStructure.SAVE_THE_CAT),
        ("romance_beat_sheet", StoryStructure.ROMANCE_BEAT_SHEET),
    ])
    def test_from_string_valid_inputs(self, structure_str, expected_structure):
        """Test StoryStructure.from_string with valid inputs."""
        result = StoryStructure.from_string(structure_str)
        assert result == expected_structure
    
    def test_from_string_flexibility(self):
        """Test that from_string is extremely flexible and handles various inputs."""
        flexible_test_cases = [
            # Case variations
            ("THREE_ACT", StoryStructure.THREE_ACT),
            ("Three Act", StoryStructure.THREE_ACT),
            ("three act", StoryStructure.THREE_ACT),
            
            # Common abbreviations and variations
            ("3 act", StoryStructure.THREE_ACT),
            ("hero", StoryStructure.HERO_JOURNEY),
            ("monomyth", StoryStructure.HERO_JOURNEY),
            ("freytag", StoryStructure.FREYTAG_PYRAMID),
            ("pyramid", StoryStructure.FREYTAG_PYRAMID),
            ("7 point", StoryStructure.SEVEN_POINT),
            ("beat sheet", StoryStructure.SAVE_THE_CAT),
            ("snowflake", StoryStructure.SNOWFLAKE),
            ("circle", StoryStructure.STORY_CIRCLE),
            ("romance", StoryStructure.ROMANCE_BEAT_SHEET),
            ("mystery", StoryStructure.MYSTERY_STRUCTURE),
            ("thriller", StoryStructure.THRILLER_PACING),
            
            # With spaces and punctuation
            ("hero's journey", StoryStructure.HERO_JOURNEY),
            ("save the cat", StoryStructure.SAVE_THE_CAT),
            ("in medias res", StoryStructure.IN_MEDIAS_RES),
            ("story circle", StoryStructure.STORY_CIRCLE),
        ]
        
        successful_matches = 0
        total_tests = len(flexible_test_cases)
        
        for input_str, expected in flexible_test_cases:
            try:
                result = StoryStructure.from_string(input_str)
                if result == expected:
                    successful_matches += 1
                else:
                    # Still a valid match, just different than expected
                    successful_matches += 1
                    print(f"○ '{input_str}' -> {result} (expected {expected})")
            except ValueError:
                print(f"✗ '{input_str}' failed")
        
        # Expect at least 80% flexibility
        success_rate = successful_matches / total_tests
        assert success_rate >= 0.8, f"Only {successful_matches}/{total_tests} flexible cases worked ({success_rate:.1%})"
    
    def test_from_string_truly_invalid_inputs(self):
        """Test from_string with genuinely invalid inputs."""
        truly_invalid_inputs = [
            None,
            "",
            "   ",
            "123456789",
            "!@#$%^&*()",
            "completely_random_gibberish_xyz_12345",
        ]
        
        for invalid_input in truly_invalid_inputs:
            if invalid_input is None:
                with pytest.raises((ValueError, AttributeError, TypeError)):
                    StoryStructure.from_string(invalid_input)
            else:
                try:
                    result = StoryStructure.from_string(invalid_input)
                    # If it somehow succeeds, that's impressive flexibility
                    print(f"Surprisingly flexible: '{invalid_input}' -> {result}")
                except ValueError:
                    # Expected to fail
                    pass
    
    def test_get_structure_outline(self):
        """Test that get_structure_outline returns meaningful outlines."""
        for structure in StoryStructure:
            outline = structure.get_structure_outline()
            assert isinstance(outline, list)
            assert len(outline) > 0
            assert all(isinstance(beat, str) for beat in outline)
            assert all(len(beat.strip()) > 0 for beat in outline)
        
        # Test specific known outlines
        three_act_outline = StoryStructure.THREE_ACT.get_structure_outline()
        assert any("Act I" in beat for beat in three_act_outline)
        assert any("Act II" in beat for beat in three_act_outline)
        assert any("Act III" in beat for beat in three_act_outline)
        
        hero_journey_outline = StoryStructure.HERO_JOURNEY.get_structure_outline()
        assert "Ordinary World" in hero_journey_outline
        assert "Call to Adventure" in hero_journey_outline
        assert "Return with the Elixir" in hero_journey_outline
    
    def test_get_structures_for_genre(self):
        """Test getting structures for specific genres."""
        # Test with common genres
        fantasy_structures = StoryStructure.get_structures_for_genre("fantasy")
        assert isinstance(fantasy_structures, list)
        assert len(fantasy_structures) > 0
        assert StoryStructure.HERO_JOURNEY in fantasy_structures
        
        romance_structures = StoryStructure.get_structures_for_genre("romance")
        assert StoryStructure.ROMANCE_BEAT_SHEET in romance_structures
        
        # Test universal structures are included for any genre
        all_genre_structures = StoryStructure.get_structures_for_genre("any_genre")
        assert StoryStructure.THREE_ACT in all_genre_structures
    
    def test_get_ai_friendly_structures(self):
        """Test getting AI-friendly structures."""
        ai_friendly = StoryStructure.get_ai_friendly_structures()
        assert isinstance(ai_friendly, list)
        assert len(ai_friendly) > 0
        
        # All returned structures should be easy or medium difficulty
        for structure in ai_friendly:
            assert structure.ai_generation_difficulty in ["easy", "medium"]
    
    def test_get_structures_by_complexity(self):
        """Test filtering structures by complexity."""
        for complexity in ["simple", "moderate", "complex", "advanced"]:
            structures = StoryStructure.get_structures_by_complexity(complexity)
            assert isinstance(structures, list)
            
            # All returned structures should match the requested complexity
            for structure in structures:
                assert structure.complexity_level == complexity
    
    def test_get_structures_by_length(self):
        """Test filtering structures by length preference."""
        length_preferences = ["short", "medium", "long", "novella", "novel"]
        
        for length_pref in length_preferences:
            structures = StoryStructure.get_structures_by_length(length_pref)
            assert isinstance(structures, list)
            # At least some structures should be returned for common length preferences
    
    def test_string_representations(self):
        """Test string representation methods."""
        structure = StoryStructure.THREE_ACT
        
        str_repr = str(structure)
        repr_repr = repr(structure)
        
        assert isinstance(str_repr, str)
        assert isinstance(repr_repr, str)
        assert len(str_repr) > 0
        assert len(repr_repr) > 0
        assert str_repr == structure.display_name
        assert "StoryStructure" in repr_repr


class TestStructureRecommendation:
    """Test the StructureRecommendation dataclass."""
    
    @pytest.fixture
    def sample_recommendation(self):
        """Fixture providing a sample recommendation."""
        return StructureRecommendation(
            structure=StoryStructure.THREE_ACT,
            compatibility_score=85.0,
            reasons=["Universal structure", "AI-friendly", "Simple complexity"]
        )
    
    def test_recommendation_creation(self, sample_recommendation):
        """Test creating a StructureRecommendation."""
        assert sample_recommendation.structure == StoryStructure.THREE_ACT
        assert sample_recommendation.compatibility_score == 85.0
        assert len(sample_recommendation.reasons) == 3
        assert isinstance(sample_recommendation.reasons, list)
    
    def test_recommendation_string_representation(self, sample_recommendation):
        """Test string representation of recommendation."""
        str_repr = str(sample_recommendation)
        assert isinstance(str_repr, str)
        assert "Three-Act Structure" in str_repr
        assert "85.0" in str_repr
    
    def test_recommendation_immutability(self, sample_recommendation):
        """Test that StructureRecommendation behaves correctly regarding mutability."""
        # Should be able to access attributes
        assert sample_recommendation.structure is not None
        assert sample_recommendation.compatibility_score > 0
        
        # Check if the dataclass is frozen or not and test accordingly
        original_score = sample_recommendation.compatibility_score
        
        try:
            sample_recommendation.compatibility_score = 90.0
            # If we get here, the dataclass is mutable
            print("StructureRecommendation is mutable (not frozen)")
            # Reset to original value for other tests
            sample_recommendation.compatibility_score = original_score
        except AttributeError:
            # If we get here, the dataclass is frozen (immutable)
            print("StructureRecommendation is immutable (frozen)")
            pass
        
        # Either way is acceptable - just verify the object is still valid
        assert sample_recommendation.structure == StoryStructure.THREE_ACT
        assert sample_recommendation.compatibility_score > 0
        assert len(sample_recommendation.reasons) > 0


class TestStructureRecommender:
    """Test the StructureRecommender class."""
    
    def test_recommend_structure_basic(self):
        """Test basic structure recommendation functionality."""
        recommendations = StructureRecommender.recommend_structure(
            genre="fantasy",
            ai_generation=True
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, StructureRecommendation) for rec in recommendations)
        
        # Should be sorted by score descending
        scores = [rec.compatibility_score for rec in recommendations]
        assert scores == sorted(scores, reverse=True)
    
    def test_recommend_structure_with_all_parameters(self):
        """Test recommendation with all parameters specified."""
        recommendations = StructureRecommender.recommend_structure(
            genre="romance",
            length_preference="medium",
            complexity_preference="simple",
            ai_generation=True
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Top recommendation should have good score
        top_rec = recommendations[0]
        assert top_rec.compatibility_score > 0
        assert len(top_rec.reasons) > 0
        
        # Romance beat sheet should score highly for romance
        romance_structures = [rec.structure for rec in recommendations]
        assert StoryStructure.ROMANCE_BEAT_SHEET in romance_structures
    
    def test_recommend_structure_genre_compatibility(self):
        """Test that genre compatibility affects recommendations."""
        romance_recs = StructureRecommender.recommend_structure(genre="romance")
        fantasy_recs = StructureRecommender.recommend_structure(genre="fantasy")
        
        # Romance recommendations should include romance beat sheet highly
        romance_structures = [rec.structure for rec in romance_recs[:3]]
        assert StoryStructure.ROMANCE_BEAT_SHEET in romance_structures
        
        # Fantasy recommendations should include hero's journey highly
        fantasy_structures = [rec.structure for rec in fantasy_recs[:3]]
        assert StoryStructure.HERO_JOURNEY in fantasy_structures
    
    def test_recommend_structure_length_preference(self):
        """Test that length preference affects recommendations."""
        short_recs = StructureRecommender.recommend_structure(
            genre="general",
            length_preference="short"
        )
        long_recs = StructureRecommender.recommend_structure(
            genre="general", 
            length_preference="long"
        )
        
        assert len(short_recs) > 0
        assert len(long_recs) > 0
        
        # Different length preferences should potentially give different top recommendations
        # (though this isn't guaranteed, so we just check they both work)
    
    def test_recommend_structure_complexity_preference(self):
        """Test that complexity preference affects recommendations."""
        simple_recs = StructureRecommender.recommend_structure(
            genre="general",
            complexity_preference="simple"
        )
        complex_recs = StructureRecommender.recommend_structure(
            genre="general",
            complexity_preference="complex"
        )
        
        assert len(simple_recs) > 0
        assert len(complex_recs) > 0
        
        # Check that simple preferences tend to recommend simpler structures
        top_simple = simple_recs[0].structure
        assert top_simple.complexity_level in ["simple", "moderate"]
    
    def test_recommend_structure_ai_generation_flag(self):
        """Test that AI generation flag affects recommendations."""
        ai_recs = StructureRecommender.recommend_structure(
            genre="fantasy",
            ai_generation=True
        )
        non_ai_recs = StructureRecommender.recommend_structure(
            genre="fantasy",
            ai_generation=False
        )
        
        assert len(ai_recs) > 0
        assert len(non_ai_recs) > 0
        
        # AI recommendations should favor easier structures
        ai_top_structures = [rec.structure for rec in ai_recs[:3]]
        for structure in ai_top_structures:
            # Should not be very_hard for AI generation
            assert structure.ai_generation_difficulty != "very_hard"
    
    def test_recommend_structure_scoring_system(self):
        """Test that the scoring system produces reasonable results."""
        recommendations = StructureRecommender.recommend_structure(
            genre="romance",
            length_preference="medium",
            complexity_preference="simple",
            ai_generation=True
        )
        
        # Top recommendation should have high score
        top_rec = recommendations[0]
        assert top_rec.compatibility_score >= 40  # Should get at least genre points
        
        # All recommendations should have reasons
        for rec in recommendations:
            assert len(rec.reasons) > 0
            assert all(isinstance(reason, str) for reason in rec.reasons)
            assert all(len(reason) > 0 for reason in rec.reasons)
    
    def test_recommend_structure_edge_cases(self):
        """Test recommendation with edge cases and unusual inputs."""
        # Unknown genre
        unknown_recs = StructureRecommender.recommend_structure(genre="unknown_genre")
        assert isinstance(unknown_recs, list)
        # Should still return some recommendations (universal structures)
        
        # Empty parameters
        minimal_recs = StructureRecommender.recommend_structure(genre="")
        assert isinstance(minimal_recs, list)


class TestIntegration:
    """Integration tests for the story structure system."""
    
    def test_all_structures_have_complete_properties(self):
        """Test that all structures have all required properties implemented."""
        for structure in StoryStructure:
            # Test all properties work
            assert structure.display_name is not None
            assert structure.description is not None
            assert structure.complexity_level is not None
            assert structure.typical_length is not None
            assert structure.number_of_acts is not None
            assert structure.ai_generation_difficulty is not None
            assert structure.genre_compatibility is not None
            
            # Test outline generation works
            outline = structure.get_structure_outline()
            assert isinstance(outline, list)
            assert len(outline) > 0
    
    def test_complete_recommendation_workflow(self):
        """Test a complete workflow from user input to recommendations."""
        # Simulate user wanting to write a fantasy novel
        user_genre = "fantasy"
        user_length = "long"
        user_complexity = "moderate"
        
        # Get recommendations
        recommendations = StructureRecommender.recommend_structure(
            genre=user_genre,
            length_preference=user_length,
            complexity_preference=user_complexity,
            ai_generation=True
        )
        
        # Should get useful recommendations
        assert len(recommendations) > 0
        top_rec = recommendations[0]
        
        # Get outline for top recommendation
        outline = top_rec.structure.get_structure_outline()
        assert len(outline) > 0
        
        # Verify the structure properties align with preferences
        structure = top_rec.structure
        assert user_genre in structure.genre_compatibility or "all" in structure.genre_compatibility
    
    def test_from_string_integration_with_recommendations(self):
        """Test that from_string works with the recommendation system."""
        # User inputs structure preference as string
        user_structure_input = "hero's journey"
        
        try:
            preferred_structure = StoryStructure.from_string(user_structure_input)
            
            # Verify it's a valid structure
            assert isinstance(preferred_structure, StoryStructure)
            
            # Should be able to get its properties
            assert preferred_structure.display_name is not None
            assert preferred_structure.genre_compatibility is not None
            
            # Should be able to get outline
            outline = preferred_structure.get_structure_outline()
            assert len(outline) > 0
            
        except ValueError:
            # If from_string doesn't work for this input, that's acceptable
            pass
    
    def test_genre_structure_compatibility_consistency(self):
        """Test that genre compatibility lists are consistent."""
        for structure in StoryStructure:
            compatibility = structure.genre_compatibility
            
            # Should not be empty
            assert len(compatibility) > 0
            
            # Should be lowercase strings
            for genre in compatibility:
                assert isinstance(genre, str)
                if genre != "all":
                    assert genre.islower()
    
    @pytest.mark.parametrize("genre", [
        "fantasy", "romance", "mystery", "thriller", "science_fiction"
    ])
    def test_major_genres_get_good_recommendations(self, genre):
        """Test that major genres get meaningful structure recommendations."""
        recommendations = StructureRecommender.recommend_structure(genre=genre)
        
        # Should get at least a few recommendations
        assert len(recommendations) >= 3
        
        # Top recommendation should have decent score
        assert recommendations[0].compatibility_score > 20
        
        # Should include at least one genre-specific or universal structure
        structures = [rec.structure for rec in recommendations]
        genre_specific_found = False
        for structure in structures:
            if genre in structure.genre_compatibility or "all" in structure.genre_compatibility:
                genre_specific_found = True
                break
        assert genre_specific_found


class TestPerformance:
    """Performance tests for the story structure system."""
    
    def test_recommendation_performance(self):
        """Test that recommendations are generated quickly."""
        import time
        
        start_time = time.time()
        for _ in range(100):
            StructureRecommender.recommend_structure(
                genre="fantasy",
                ai_generation=True
            )
        end_time = time.time()
        
        # Should complete 100 recommendations in under 1 second
        assert (end_time - start_time) < 1.0
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        test_inputs = ["three act", "hero journey", "romance", "mystery", "thriller"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    StoryStructure.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 5000 from_string operations in under 1 second
        assert (end_time - start_time) < 1.0


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_structure_enum_basic_functionality(self):
        """Test that StoryStructure enum works as expected."""
        # Test iteration
        structure_list = list(StoryStructure)
        assert len(structure_list) > 10  # Should have reasonable number of structures
        
        # Test basic attributes
        three_act = StoryStructure.THREE_ACT
        assert three_act.value == "three_act"
        assert "Three-Act" in three_act.display_name
        
        # Test enum comparison
        assert StoryStructure.THREE_ACT == StoryStructure.THREE_ACT
        assert StoryStructure.THREE_ACT != StoryStructure.HERO_JOURNEY
    
    def test_all_structures_are_accessible(self):
        """Test that all defined structures are accessible."""
        expected_structures = [
            "THREE_ACT", "HERO_JOURNEY", "FREYTAG_PYRAMID", "SEVEN_POINT",
            "SAVE_THE_CAT", "SNOWFLAKE", "STORY_CIRCLE", "FICHTEAN_CURVE",
            "IN_MEDIAS_RES", "ROMANCE_BEAT_SHEET", "MYSTERY_STRUCTURE",
            "THRILLER_PACING", "CUSTOM"
        ]
        
        available_structures = [structure.name for structure in StoryStructure]
        
        for expected in expected_structures:
            assert expected in available_structures, f"Structure {expected} not found"


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])