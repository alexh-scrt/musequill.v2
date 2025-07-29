import pytest
from typing import List
from enum import Enum
from pathlib import Path
import sys
# Assuming the NarrativePOV class is imported from the appropriate module
# from your_module import NarrativePOV

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the GovernmentType enum
from musequill.models.book.narrative_pov import NarrativePOV


class TestNarrativePOV:
    """Test suite for NarrativePOV enum functionality."""

    def test_enum_inheritance(self):
        """Test that NarrativePOV properly inherits from str and Enum."""
        assert issubclass(NarrativePOV, str)
        assert issubclass(NarrativePOV, Enum)

    def test_enum_values_exist(self):
        """Test that all expected enum values exist."""
        expected_values = [
            "first_person", "second_person", "third_person_limited",
            "third_person_omniscient", "third_person_objective", "multiple_pov",
            "alternating_pov", "rotating_pov", "dual_pov", "epistolary",
            "stream_of_consciousness", "frame_narrative", "unreliable_narrator",
            "close_third_person", "distant_third_person", "present_tense_first",
            "past_tense_first", "future_tense", "social_media", "multimedia_narrative",
            "collective_voice", "anthropomorphic", "inanimate_narrator",
            "dramatic_monologue", "interior_monologue", "free_indirect_discourse",
            "cinematic_pov"
        ]
        
        actual_values = [pov.value for pov in NarrativePOV]
        
        # Check that all expected values are present
        for expected in expected_values:
            assert expected in actual_values, f"Expected value '{expected}' not found in enum"

    def test_enum_members_accessible(self):
        """Test that enum members can be accessed by attribute name."""
        # Test a few key enum members
        assert NarrativePOV.FIRST_PERSON == "first_person"
        assert NarrativePOV.THIRD_PERSON_LIMITED == "third_person_limited"
        assert NarrativePOV.EPISTOLARY == "epistolary"
        assert NarrativePOV.STREAM_OF_CONSCIOUSNESS == "stream_of_consciousness"

    def test_display_name_property(self):
        """Test that display_name property returns strings."""
        for pov in NarrativePOV:
            display_name = pov.display_name
            assert isinstance(display_name, str), f"display_name for {pov} should be string"
            assert len(display_name) > 0, f"display_name for {pov} should not be empty"

    def test_description_property(self):
        """Test that description property returns non-empty strings."""
        for pov in NarrativePOV:
            description = pov.description
            assert isinstance(description, str), f"description for {pov} should be string"
            assert len(description) > 0, f"description for {pov} should not be empty"
            # Permissive test - just check it's a reasonable length
            assert len(description) > 20, f"description for {pov} should be substantial"

    def test_advantages_property(self):
        """Test that advantages property returns list of strings."""
        for pov in NarrativePOV:
            advantages = pov.advantages
            assert isinstance(advantages, list), f"advantages for {pov} should be list"
            assert len(advantages) > 0, f"advantages for {pov} should not be empty"
            for advantage in advantages:
                assert isinstance(advantage, str), f"Each advantage for {pov} should be string"
                assert len(advantage) > 0, f"Each advantage for {pov} should not be empty"

    def test_challenges_property(self):
        """Test that challenges property returns list of strings."""
        for pov in NarrativePOV:
            challenges = pov.challenges
            assert isinstance(challenges, list), f"challenges for {pov} should be list"
            assert len(challenges) > 0, f"challenges for {pov} should not be empty"
            for challenge in challenges:
                assert isinstance(challenge, str), f"Each challenge for {pov} should be string"
                assert len(challenge) > 0, f"Each challenge for {pov} should not be empty"

    def test_suitable_genres_property(self):
        """Test that suitable_genres property returns list of strings."""
        for pov in NarrativePOV:
            genres = pov.suitable_genres
            assert isinstance(genres, list), f"suitable_genres for {pov} should be list"
            assert len(genres) > 0, f"suitable_genres for {pov} should not be empty"
            for genre in genres:
                assert isinstance(genre, str), f"Each genre for {pov} should be string"
                assert len(genre) > 0, f"Each genre for {pov} should not be empty"

    def test_complexity_level_property(self):
        """Test that complexity_level returns valid complexity levels."""
        valid_levels = {"beginner", "intermediate", "advanced", "expert"}
        
        for pov in NarrativePOV:
            complexity = pov.complexity_level
            assert isinstance(complexity, str), f"complexity_level for {pov} should be string"
            assert complexity in valid_levels, f"complexity_level '{complexity}' for {pov} should be one of {valid_levels}"

    def test_str_representation(self):
        """Test string representation of POV enum members."""
        for pov in NarrativePOV:
            str_repr = str(pov)
            assert isinstance(str_repr, str), f"str({pov}) should return string"
            assert len(str_repr) > 0, f"str({pov}) should not be empty"

    def test_repr_representation(self):
        """Test repr representation of POV enum members."""
        for pov in NarrativePOV:
            repr_str = repr(pov)
            assert isinstance(repr_str, str), f"repr({pov}) should return string"
            assert "NarrativePOV." in repr_str, f"repr({pov}) should contain 'NarrativePOV.'"

    def test_get_beginner_povs_classmethod(self):
        """Test get_beginner_povs class method."""
        if hasattr(NarrativePOV, 'get_beginner_povs'):
            beginner_povs = NarrativePOV.get_beginner_povs()
            assert isinstance(beginner_povs, list), "get_beginner_povs should return list"
            
            for pov in beginner_povs:
                assert isinstance(pov, NarrativePOV), "Each item should be NarrativePOV instance"
                assert pov.complexity_level == "beginner", f"{pov} should have beginner complexity"

    def test_get_povs_for_genre_classmethod(self):
        """Test get_povs_for_genre class method."""
        if hasattr(NarrativePOV, 'get_povs_for_genre'):
            # Test with a common genre
            test_genres = ["mystery", "romance", "literary_fiction", "fantasy"]
            
            for genre in test_genres:
                povs = NarrativePOV.get_povs_for_genre(genre)
                assert isinstance(povs, list), f"get_povs_for_genre('{genre}') should return list"
                
                for pov in povs:
                    assert isinstance(pov, NarrativePOV), f"Each item for genre '{genre}' should be NarrativePOV instance"
                    # Permissive check - just ensure the genre appears somewhere in suitable_genres
                    genre_found = any(genre.lower() in sg.lower() for sg in pov.suitable_genres)
                    assert genre_found, f"POV {pov} should include genre '{genre}' in suitable_genres"

    def test_get_experimental_povs_classmethod(self):
        """Test get_experimental_povs class method."""
        if hasattr(NarrativePOV, 'get_experimental_povs'):
            experimental_povs = NarrativePOV.get_experimental_povs()
            assert isinstance(experimental_povs, list), "get_experimental_povs should return list"
            assert len(experimental_povs) > 0, "Should return at least some experimental POVs"
            
            for pov in experimental_povs:
                assert isinstance(pov, NarrativePOV), "Each item should be NarrativePOV instance"

    def test_enum_completeness(self):
        """Test that enum has reasonable number of members."""
        pov_count = len(list(NarrativePOV))
        assert pov_count >= 8, "Should have at least the basic POV types"
        assert pov_count <= 50, "Should not have excessive number of POV types"

    def test_value_format_consistency(self):
        """Test that enum values follow consistent naming convention."""
        for pov in NarrativePOV:
            value = pov.value
            # Should be lowercase with underscores
            assert value.islower(), f"Value '{value}' should be lowercase"
            assert " " not in value, f"Value '{value}' should not contain spaces"
            # Should only contain letters, numbers, and underscores
            assert all(c.isalnum() or c == '_' for c in value), f"Value '{value}' should only contain alphanumeric chars and underscores"

    def test_property_consistency(self):
        """Test that properties are consistent across all enum members."""
        for pov in NarrativePOV:
            # Each POV should have all required properties
            assert hasattr(pov, 'display_name'), f"{pov} should have display_name property"
            assert hasattr(pov, 'description'), f"{pov} should have description property"
            assert hasattr(pov, 'advantages'), f"{pov} should have advantages property"
            assert hasattr(pov, 'challenges'), f"{pov} should have challenges property"
            assert hasattr(pov, 'suitable_genres'), f"{pov} should have suitable_genres property"
            assert hasattr(pov, 'complexity_level'), f"{pov} should have complexity_level property"

    def test_enum_iteration(self):
        """Test that enum can be properly iterated."""
        pov_list = list(NarrativePOV)
        assert len(pov_list) > 0, "Should be able to iterate over enum members"
        
        for pov in NarrativePOV:
            assert isinstance(pov, NarrativePOV), "Each iterated item should be NarrativePOV instance"

    def test_enum_membership(self):
        """Test enum membership operations."""
        # Test that values can be found in the enum
        assert "first_person" in [pov.value for pov in NarrativePOV]
        assert "third_person_limited" in [pov.value for pov in NarrativePOV]
        
        # Test that invalid values are not in the enum
        assert "invalid_pov" not in [pov.value for pov in NarrativePOV]

    @pytest.mark.parametrize("pov_name", [
        "FIRST_PERSON", "SECOND_PERSON", "THIRD_PERSON_LIMITED", 
        "THIRD_PERSON_OMNISCIENT", "EPISTOLARY", "STREAM_OF_CONSCIOUSNESS"
    ])
    def test_specific_pov_access(self, pov_name):
        """Test that specific POV members can be accessed."""
        assert hasattr(NarrativePOV, pov_name), f"NarrativePOV should have {pov_name} member"
        pov = getattr(NarrativePOV, pov_name)
        assert isinstance(pov, NarrativePOV), f"{pov_name} should be NarrativePOV instance"

    def test_class_methods_return_types(self):
        """Test that class methods return appropriate types."""
        class_methods = ['get_beginner_povs', 'get_povs_for_genre', 'get_experimental_povs']
        
        for method_name in class_methods:
            if hasattr(NarrativePOV, method_name):
                method = getattr(NarrativePOV, method_name)
                assert callable(method), f"{method_name} should be callable"

    def test_no_duplicate_values(self):
        """Test that there are no duplicate enum values."""
        values = [pov.value for pov in NarrativePOV]
        assert len(values) == len(set(values)), "All enum values should be unique"

    def test_properties_not_none(self):
        """Test that properties don't return None values."""
        for pov in NarrativePOV:
            assert pov.display_name is not None, f"display_name for {pov} should not be None"
            assert pov.description is not None, f"description for {pov} should not be None"
            assert pov.advantages is not None, f"advantages for {pov} should not be None"
            assert pov.challenges is not None, f"challenges for {pov} should not be None"
            assert pov.suitable_genres is not None, f"suitable_genres for {pov} should not be None"
            assert pov.complexity_level is not None, f"complexity_level for {pov} should not be None"