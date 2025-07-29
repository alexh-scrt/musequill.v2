"""
Comprehensive tests for musequill.models.book.conflict module.

Test file: tests/models/book/test_conflict.py
Module under test: musequill/models/book/conflict.py

Run from project root: pytest tests/models/book/test_conflict.py -v
"""

import sys
from pathlib import Path
import pytest
from typing import List, Set

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the ConflictType class from the conflict module
from musequill.models.book.conflict import ConflictType


class TestConflictType:
    """Test the ConflictType enum comprehensively."""
    
    def test_all_conflict_values_are_strings(self):
        """Ensure all conflict enum values are properly formatted strings."""
        for conflict in ConflictType:
            assert isinstance(conflict.value, str)
            assert conflict.value.islower()
            assert " " not in conflict.value  # Should use underscores
            assert len(conflict.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in conflict.value)
    
    def test_all_conflicts_have_unique_values(self):
        """Ensure no duplicate values in ConflictType enum."""
        values = [conflict.value for conflict in ConflictType]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate conflict values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have exactly 8 conflict types
        assert len(values) == 8, f"Expected exactly 8 conflict types, got {len(values)}"
        print(f"✓ Found {len(values)} unique conflict types")
    
    def test_display_name_property(self):
        """Test that display_name properly formats conflict names."""
        for conflict in ConflictType:
            display_name = conflict.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
            # Should contain "vs" for conflict types
            assert "vs" in display_name.lower() or "v" in display_name.lower()
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (ConflictType.PERSON_VS_PERSON, "Person vs Person"),
            (ConflictType.PERSON_VS_SELF, "Person vs Self"),
            (ConflictType.PERSON_VS_SOCIETY, "Person vs Society"),
            (ConflictType.PERSON_VS_NATURE, "Person vs Nature"),
            (ConflictType.PERSON_VS_TECHNOLOGY, "Person vs Technology"),
            (ConflictType.PERSON_VS_SUPERNATURAL, "Person vs Supernatural"),
            (ConflictType.PERSON_VS_FATE, "Person vs Fate"),
            (ConflictType.PERSON_VS_GOD, "Person vs God"),
        ]
        
        for conflict, expected_display in test_cases:
            assert conflict.display_name == expected_display, f"Expected '{expected_display}' for {conflict.value}, got '{conflict.display_name}'"
    
    def test_description_property(self):
        """Test that all conflict types have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for conflict in ConflictType:
            description = conflict.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {conflict.value}"
            
            # Check for minimum meaningful length
            if len(description) < 50:
                short_descriptions.append(f"{conflict.value}: '{description}'")
            
            # Should start with capital letter (if not empty)
            if description:
                assert description[0].isupper(), f"Description should start with capital for {conflict.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?')
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{conflict.value}: '{description}'")
        
        # Most descriptions should be substantial
        assert len(short_descriptions) <= 2, f"Too many short descriptions: {short_descriptions}"
        
        # Most descriptions should have proper punctuation
        assert len(descriptions_without_punctuation) <= 2, f"Descriptions without punctuation: {descriptions_without_punctuation}"
        
        total_conflicts = len(list(ConflictType))
        quality_descriptions = total_conflicts - len(short_descriptions) - len(descriptions_without_punctuation)
        quality_percentage = quality_descriptions / total_conflicts
        assert quality_percentage >= 0.7, f"Too few quality descriptions: {quality_descriptions}/{total_conflicts} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_conflicts} ({quality_percentage:.1%})")
    
    def test_complexity_level_property(self):
        """Test complexity level categorization."""
        valid_complexity_levels = {"basic", "intermediate", "advanced", "expert"}
        
        level_counts = {"basic": 0, "intermediate": 0, "advanced": 0, "expert": 0}
        
        for conflict in ConflictType:
            complexity_level = conflict.complexity_level
            assert complexity_level in valid_complexity_levels, f"{conflict.value} has invalid complexity level: {complexity_level}"
            assert isinstance(complexity_level, str)
            level_counts[complexity_level] += 1
        
        # Verify we have some distribution across complexity levels
        assert level_counts["basic"] > 0, "No basic complexity level conflicts found"
        assert level_counts["advanced"] > 0, "No advanced complexity level conflicts found"
        print(f"Complexity level distribution: {level_counts}")
        
        # Test specific known complexity levels
        assert ConflictType.PERSON_VS_NATURE.complexity_level == "basic"
        assert ConflictType.PERSON_VS_SELF.complexity_level == "advanced"
        assert ConflictType.PERSON_VS_GOD.complexity_level == "expert"
    
    def test_typical_genres_property(self):
        """Test typical_genres property returns valid genre lists."""
        for conflict in ConflictType:
            genres = conflict.typical_genres
            assert isinstance(genres, list)
            assert len(genres) > 0, f"No genres found for {conflict.value}"
            
            # All genres should be strings
            for genre in genres:
                assert isinstance(genre, str)
                assert len(genre) > 0
                # Should be lowercase with underscores
                assert genre.islower()
        
        # Test that external conflicts have more varied genres
        external_conflicts = ConflictType.get_external_conflicts()
        external_genre_variety = set()
        for conflict in external_conflicts:
            external_genre_variety.update(conflict.typical_genres)
        
        assert len(external_genre_variety) >= 10, f"External conflicts should cover many genres, found {len(external_genre_variety)}"
    
    def test_narrative_focus_property(self):
        """Test narrative_focus property returns valid focus types."""
        valid_focus_types = {
            "external_action", "internal_development", "thematic_exploration",
            "survival_tension", "conceptual_exploration", "atmospheric_tension",
            "philosophical_exploration", "spiritual_exploration", "balanced"
        }
        
        for conflict in ConflictType:
            focus = conflict.narrative_focus
            assert isinstance(focus, str)
            assert focus in valid_focus_types, f"{conflict.value} has invalid narrative focus: {focus}"
        
        # Test specific known focuses
        assert ConflictType.PERSON_VS_PERSON.narrative_focus == "external_action"
        assert ConflictType.PERSON_VS_SELF.narrative_focus == "internal_development"
        assert ConflictType.PERSON_VS_SOCIETY.narrative_focus == "thematic_exploration"
    
    def test_emotional_tone_property(self):
        """Test emotional_tone property returns valid tone lists."""
        for conflict in ConflictType:
            tones = conflict.emotional_tone
            assert isinstance(tones, list)
            assert len(tones) > 0, f"No emotional tones found for {conflict.value}"
            
            # All tones should be strings
            for tone in tones:
                assert isinstance(tone, str)
                assert len(tone) > 0
                # Should be lowercase with underscores for multi-word tones
                assert tone.islower()
        
        # Test that different conflicts have different emotional profiles
        all_tones = set()
        for conflict in ConflictType:
            all_tones.update(conflict.emotional_tone)
        
        assert len(all_tones) >= 15, f"Should have variety in emotional tones, found {len(all_tones)}"


class TestConflictTypeClassMethods:
    """Test class methods of ConflictType."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("person_vs_person", ConflictType.PERSON_VS_PERSON),
            ("person_vs_self", ConflictType.PERSON_VS_SELF),
            ("person_vs_society", ConflictType.PERSON_VS_SOCIETY),
            ("person_vs_nature", ConflictType.PERSON_VS_NATURE),
        ]
        
        for input_str, expected_conflict in direct_matches:
            result = ConflictType.from_string(input_str)
            assert result == expected_conflict, f"Expected {expected_conflict} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching."""
        fuzzy_matches = [
            # Person vs Person variants
            ("character vs character", ConflictType.PERSON_VS_PERSON),
            ("protagonist vs antagonist", ConflictType.PERSON_VS_PERSON),
            ("rivalry", ConflictType.PERSON_VS_PERSON),
            ("enemy", ConflictType.PERSON_VS_PERSON),
            
            # Person vs Self variants
            ("internal conflict", ConflictType.PERSON_VS_SELF),
            ("psychological", ConflictType.PERSON_VS_SELF),
            ("inner struggle", ConflictType.PERSON_VS_SELF),
            ("moral dilemma", ConflictType.PERSON_VS_SELF),
            
            # Person vs Society variants
            ("social conflict", ConflictType.PERSON_VS_SOCIETY),
            ("system", ConflictType.PERSON_VS_SOCIETY),
            ("government", ConflictType.PERSON_VS_SOCIETY),
            ("institution", ConflictType.PERSON_VS_SOCIETY),
            
            # Person vs Nature variants
            ("environmental", ConflictType.PERSON_VS_NATURE),
            ("wilderness", ConflictType.PERSON_VS_NATURE),
            ("survival", ConflictType.PERSON_VS_NATURE),
            ("disaster", ConflictType.PERSON_VS_NATURE),
            
            # Person vs Technology variants
            ("tech", ConflictType.PERSON_VS_TECHNOLOGY),
            ("ai", ConflictType.PERSON_VS_TECHNOLOGY),
            ("artificial intelligence", ConflictType.PERSON_VS_TECHNOLOGY),
            ("robot", ConflictType.PERSON_VS_TECHNOLOGY),
            
            # Person vs Supernatural variants
            ("paranormal", ConflictType.PERSON_VS_SUPERNATURAL),
            ("ghost", ConflictType.PERSON_VS_SUPERNATURAL),
            ("magic", ConflictType.PERSON_VS_SUPERNATURAL),
            ("demon", ConflictType.PERSON_VS_SUPERNATURAL),
            
            # Person vs Fate variants
            ("destiny", ConflictType.PERSON_VS_FATE),
            ("prophecy", ConflictType.PERSON_VS_FATE),
            ("inevitable", ConflictType.PERSON_VS_FATE),
            
            # Person vs God variants
            ("divine", ConflictType.PERSON_VS_GOD),
            ("religious", ConflictType.PERSON_VS_GOD),
            ("spiritual", ConflictType.PERSON_VS_GOD),
            ("faith", ConflictType.PERSON_VS_GOD),
        ]
        
        for input_str, expected_conflict in fuzzy_matches:
            result = ConflictType.from_string(input_str)
            assert result == expected_conflict, f"Expected {expected_conflict} for '{input_str}', got {result}"
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid input."""
        invalid_inputs = [
            "invalid_conflict_type",
            "person vs alien",
            "completely random text",
            "",
            "   ",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                ConflictType.from_string(invalid_input)
    
    def test_get_conflicts_for_genre(self):
        """Test getting conflicts for specific genres."""
        # Test major genres
        major_genres = [
            "fantasy", "science_fiction", "horror", "thriller", "literary_fiction",
            "romance", "mystery", "adventure", "dystopian", "historical_fiction"
        ]
        
        for genre in major_genres:
            conflicts = ConflictType.get_conflicts_for_genre(genre)
            assert isinstance(conflicts, list)
            assert len(conflicts) >= 2, f"Genre {genre} should have at least 2 conflicts: {len(conflicts)}"
            assert len(conflicts) <= 6, f"Genre {genre} has too many conflicts: {len(conflicts)}"
            
            # All returned conflicts should be valid
            for conflict in conflicts:
                assert isinstance(conflict, ConflictType)
        
        # Test specific genre mappings
        fantasy_conflicts = ConflictType.get_conflicts_for_genre("fantasy")
        assert ConflictType.PERSON_VS_SUPERNATURAL in fantasy_conflicts
        
        sci_fi_conflicts = ConflictType.get_conflicts_for_genre("science_fiction")
        assert ConflictType.PERSON_VS_TECHNOLOGY in sci_fi_conflicts
        
        literary_conflicts = ConflictType.get_conflicts_for_genre("literary_fiction")
        assert ConflictType.PERSON_VS_SELF in literary_conflicts
    
    def test_get_conflicts_for_unknown_genre(self):
        """Test getting conflicts for unknown genre returns defaults."""
        unknown_conflicts = ConflictType.get_conflicts_for_genre("unknown_genre_12345")
        
        assert isinstance(unknown_conflicts, list)
        assert len(unknown_conflicts) >= 2, "Unknown genre should return default conflicts"
        
        # Should include common conflicts
        common_conflicts = {ConflictType.PERSON_VS_PERSON, ConflictType.PERSON_VS_SELF, ConflictType.PERSON_VS_SOCIETY}
        found_common = sum(1 for c in unknown_conflicts if c in common_conflicts)
        assert found_common >= 2, "Unknown genre should return common conflict types"
    
    def test_get_external_conflicts(self):
        """Test getting external conflict types."""
        external_conflicts = ConflictType.get_external_conflicts()
        
        assert isinstance(external_conflicts, list)
        assert len(external_conflicts) == 7  # All except PERSON_VS_SELF
        
        # Should include all external conflicts
        expected_external = [
            ConflictType.PERSON_VS_PERSON, ConflictType.PERSON_VS_SOCIETY,
            ConflictType.PERSON_VS_NATURE, ConflictType.PERSON_VS_TECHNOLOGY,
            ConflictType.PERSON_VS_SUPERNATURAL, ConflictType.PERSON_VS_FATE,
            ConflictType.PERSON_VS_GOD
        ]
        
        for expected in expected_external:
            assert expected in external_conflicts, f"External conflict {expected} not found"
        
        # Should NOT include internal conflicts
        assert ConflictType.PERSON_VS_SELF not in external_conflicts
        
        print(f"✓ External conflicts: {len(external_conflicts)} types")
    
    def test_get_internal_conflicts(self):
        """Test getting internal conflict types."""
        internal_conflicts = ConflictType.get_internal_conflicts()
        
        assert isinstance(internal_conflicts, list)
        assert len(internal_conflicts) == 1  # Only PERSON_VS_SELF
        
        # Should only include PERSON_VS_SELF
        assert ConflictType.PERSON_VS_SELF in internal_conflicts
        
        # Should NOT include external conflicts
        external_conflicts = ConflictType.get_external_conflicts()
        for external in external_conflicts:
            assert external not in internal_conflicts
        
        print(f"✓ Internal conflicts: {len(internal_conflicts)} types")
    
    def test_get_classic_conflicts(self):
        """Test getting classic literary conflict types."""
        classic_conflicts = ConflictType.get_classic_conflicts()
        
        assert isinstance(classic_conflicts, list)
        assert len(classic_conflicts) == 4  # The traditional four
        
        # Should include the classic four
        expected_classic = [
            ConflictType.PERSON_VS_PERSON, ConflictType.PERSON_VS_SELF,
            ConflictType.PERSON_VS_SOCIETY, ConflictType.PERSON_VS_NATURE
        ]
        
        for expected in expected_classic:
            assert expected in classic_conflicts, f"Classic conflict {expected} not found"
        
        print(f"✓ Classic conflicts: {len(classic_conflicts)} types")
    
    def test_get_modern_conflicts(self):
        """Test getting modern/contemporary conflict types."""
        modern_conflicts = ConflictType.get_modern_conflicts()
        
        assert isinstance(modern_conflicts, list)
        assert len(modern_conflicts) == 4  # The modern four
        
        # Should include modern conflicts
        expected_modern = [
            ConflictType.PERSON_VS_TECHNOLOGY, ConflictType.PERSON_VS_SUPERNATURAL,
            ConflictType.PERSON_VS_FATE, ConflictType.PERSON_VS_GOD
        ]
        
        for expected in expected_modern:
            assert expected in modern_conflicts, f"Modern conflict {expected} not found"
        
        print(f"✓ Modern conflicts: {len(modern_conflicts)} types")


class TestConflictTypeIntegration:
    """Integration tests for the conflict type system."""
    
    def test_all_conflicts_have_complete_properties(self):
        """Test that all conflict types have all required properties implemented."""
        for conflict in ConflictType:
            # Test all properties work without errors
            assert conflict.display_name is not None
            assert conflict.description is not None
            assert conflict.complexity_level is not None
            assert conflict.typical_genres is not None
            assert conflict.narrative_focus is not None
            assert conflict.emotional_tone is not None
    
    def test_conflict_type_enum_completeness(self):
        """Test that the ConflictType enum covers expected conflict areas."""
        # Test that we have the expected 8 classic conflict types
        expected_conflicts = [
            "PERSON_VS_PERSON", "PERSON_VS_SELF", "PERSON_VS_SOCIETY", "PERSON_VS_NATURE",
            "PERSON_VS_TECHNOLOGY", "PERSON_VS_SUPERNATURAL", "PERSON_VS_FATE", "PERSON_VS_GOD"
        ]
        
        available_conflicts = [conflict.name for conflict in ConflictType]
        
        for expected in expected_conflicts:
            assert expected in available_conflicts, f"Conflict type {expected} not found"
    
    def test_genre_conflict_mapping_coverage(self):
        """Test that genre mappings provide good coverage."""
        major_genres = [
            "fantasy", "science_fiction", "horror", "thriller", "literary_fiction",
            "romance", "mystery", "adventure", "dystopian", "historical_fiction"
        ]
        
        for genre in major_genres:
            conflicts = ConflictType.get_conflicts_for_genre(genre)
            assert len(conflicts) >= 2, f"Genre {genre} has too few conflicts: {len(conflicts)}"
            assert len(conflicts) <= 6, f"Genre {genre} has too many conflicts: {len(conflicts)}"
    
    def test_complexity_distribution(self):
        """Test that conflict types are well-distributed across complexity levels."""
        complexity_counts = {"basic": 0, "intermediate": 0, "advanced": 0, "expert": 0}
        
        for conflict in ConflictType:
            complexity_counts[conflict.complexity_level] += 1
        
        total_conflicts = sum(complexity_counts.values())
        
        # Each complexity level should have at least one conflict
        for complexity, count in complexity_counts.items():
            percentage = count / total_conflicts
            assert percentage >= 0.1, f"Complexity {complexity} has too few conflicts: {percentage:.1%}"
            assert percentage <= 0.5, f"Complexity {complexity} has too many conflicts: {percentage:.1%}"
    
    def test_property_consistency(self):
        """Test that properties are consistent with conflict types."""
        for conflict in ConflictType:
            # Internal conflicts should have internal development focus
            if conflict == ConflictType.PERSON_VS_SELF:
                assert conflict.narrative_focus == "internal_development"
            
            # External conflicts should not have internal development focus (except for thematic exploration)
            if conflict in ConflictType.get_external_conflicts():
                assert conflict.narrative_focus != "internal_development"
            
            # Technology conflicts should include sci-fi genres
            if conflict == ConflictType.PERSON_VS_TECHNOLOGY:
                assert "science_fiction" in conflict.typical_genres
            
            # Supernatural conflicts should include fantasy/horror genres
            if conflict == ConflictType.PERSON_VS_SUPERNATURAL:
                genres = conflict.typical_genres
                assert "fantasy" in genres or "horror" in genres


class TestConflictTypePerformance:
    """Performance tests for the conflict type system."""
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for conflict in ConflictType:
                _ = conflict.display_name
                _ = conflict.description
                _ = conflict.complexity_level
                _ = conflict.typical_genres
                _ = conflict.narrative_focus
                _ = conflict.emotional_tone
        end_time = time.time()
        
        # Should complete 48,000 property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        test_inputs = ["internal conflict", "technology", "survival", "religious", "rivalry"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    ConflictType.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 5000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_genre_mapping_performance(self):
        """Test that genre mapping is reasonably fast."""
        import time
        
        test_genres = ["fantasy", "science_fiction", "horror", "thriller"]
        
        start_time = time.time()
        for _ in range(1000):
            for genre in test_genres:
                ConflictType.get_conflicts_for_genre(genre)
        end_time = time.time()
        
        # Should complete 4000 genre mappings in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Genre mapping too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_conflict_enum_basic_functionality(self):
        """Test that ConflictType enum works as expected."""
        # Test iteration
        conflict_list = list(ConflictType)
        assert len(conflict_list) == 8  # Should have exactly 8 conflict types
        
        # Test basic attributes
        person_vs_person = ConflictType.PERSON_VS_PERSON
        assert person_vs_person.value == "person_vs_person"
        assert "Person vs Person" in person_vs_person.display_name
        
        # Test enum comparison
        assert ConflictType.PERSON_VS_PERSON == ConflictType.PERSON_VS_PERSON
        assert ConflictType.PERSON_VS_PERSON != ConflictType.PERSON_VS_SELF
    
    def test_string_representations(self):
        """Test string representation methods."""
        conflict = ConflictType.PERSON_VS_SELF
        
        str_repr = str(conflict)
        
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        assert str_repr == conflict.display_name
    
    def test_conflict_categorization_logic(self):
        """Test that conflict categorizations make logical sense."""
        # Test that classic + modern = all conflicts
        classic = set(ConflictType.get_classic_conflicts())
        modern = set(ConflictType.get_modern_conflicts())
        all_conflicts = set(ConflictType)
        
        assert classic.union(modern) == all_conflicts, "Classic + Modern should equal all conflicts"
        assert classic.intersection(modern) == set(), "Classic and Modern should not overlap"
        
        # Test that internal + external = all conflicts
        internal = set(ConflictType.get_internal_conflicts())
        external = set(ConflictType.get_external_conflicts())
        
        assert internal.union(external) == all_conflicts, "Internal + External should equal all conflicts"
        assert internal.intersection(external) == set(), "Internal and External should not overlap"


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])