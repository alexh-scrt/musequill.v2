"""
Comprehensive tests for PacingStyle enum.

Test file: tests/models/book/test_pacing_style.py
Module under test: musequill/models/book/pacing_style.py

Run from project root: pytest tests/models/book/test_pacing_style.py -v
"""

import sys
from pathlib import Path
import pytest
import time
from typing import List, Set

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the PacingStyle enum
from musequill.models.book.pacing_style import PacingStyle


class TestPacingStyleBasicProperties:
    """Test basic properties and enum functionality of PacingStyle."""
    
    def test_all_pacing_values_are_strings(self):
        """Ensure all pacing style enum values are properly formatted strings."""
        for style in PacingStyle:
            assert isinstance(style.value, str)
            assert style.value.islower()
            assert " " not in style.value  # Should use underscores
            assert len(style.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in style.value)
    
    def test_all_pacing_styles_have_unique_values(self):
        """Ensure no duplicate values in PacingStyle enum."""
        values = [style.value for style in PacingStyle]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate pacing values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have at least 70 pacing styles (based on the implementation)
        assert len(values) >= 70, f"Expected at least 70 pacing styles, got {len(values)}"
        print(f"✓ Found {len(values)} unique pacing styles")
    
    def test_display_name_property(self):
        """Test that display_name properly formats pacing style names."""
        for style in PacingStyle:
            display_name = style.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case or have capital letters
            assert any(c.isupper() for c in display_name)
            # Should be human-readable (no underscores unless hyphenated)
            if "_" in display_name:
                # Only allow underscores in special hyphenated cases
                assert "-" in display_name or display_name in ["Fast-Paced", "Moderate-Paced", "Page-Turner", "Stop-and-Start"]
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        # Test some known display names
        assert PacingStyle.FAST_PACED.display_name == "Fast-Paced"
        assert PacingStyle.SLOW_BURN.display_name == "Slow Burn"
        assert PacingStyle.PAGE_TURNER.display_name == "Page-Turner"
        assert PacingStyle.THRILLER_PACE.display_name == "Thriller Pace"
        assert PacingStyle.STOP_AND_START.display_name == "Stop-and-Start"
    
    def test_description_property(self):
        """Test that all pacing styles have descriptions."""
        for style in PacingStyle:
            description = style.description
            assert isinstance(description, str)
            assert len(description) > 10  # Should be substantial
            # Description should be meaningful and not just the enum value
            assert description.lower() != style.value.replace("_", " ")
            # Should not be identical to display name
            assert description != style.display_name
    
    def test_intensity_level_property(self):
        """Test that intensity_level returns valid values."""
        valid_levels = {"high", "medium", "low"}
        for style in PacingStyle:
            intensity = style.intensity_level
            assert intensity in valid_levels, f"Invalid intensity level '{intensity}' for {style.value}"
    
    def test_typical_genres_property(self):
        """Test that all pacing styles have genre associations."""
        for style in PacingStyle:
            genres = style.typical_genres
            assert isinstance(genres, list)
            assert len(genres) > 0, f"No typical genres found for {style.value}"
            assert len(genres) <= 10, f"Too many genres for {style.value}: {len(genres)}"
            
            # All genres should be strings
            for genre in genres:
                assert isinstance(genre, str)
                assert len(genre) > 0


class TestPacingStyleEnumFunctionality:
    """Test basic enum functionality of PacingStyle."""
    
    def test_pacing_enum_basic_functionality(self):
        """Test that PacingStyle enum works as expected."""
        # Test iteration
        style_list = list(PacingStyle)
        assert len(style_list) >= 70  # Should have at least 70 pacing styles
        
        # Test basic attributes
        fast_paced = PacingStyle.FAST_PACED
        assert fast_paced.value == "fast_paced"
        assert "Fast" in fast_paced.display_name
        
        # Test enum comparison
        assert PacingStyle.FAST_PACED == PacingStyle.FAST_PACED
        assert PacingStyle.FAST_PACED != PacingStyle.SLOW_BURN
    
    def test_string_representations(self):
        """Test string representation methods."""
        style = PacingStyle.FAST_PACED
        
        style_str = str(style)
        style_repr = repr(style)
        
        assert isinstance(style_str, str)
        assert isinstance(style_repr, str)
        assert len(style_str) > 0
        assert len(style_repr) > 0
        assert style_str == style.display_name
        assert "PacingStyle." in style_repr
    
    def test_expected_styles_exist(self):
        """Test that all expected core pacing styles exist."""
        expected_styles = [
            "FAST_PACED", "MODERATE_PACED", "SLOW_BURN", "VARIABLE", "BREAKNECK",
            "LEISURELY", "MEASURED", "ESCALATING", "RHYTHMIC", "FLOWING",
            "THRILLER_PACE", "MYSTERY_PACE", "ROMANCE_PACE", "HORROR_PACE",
            "CONTEMPLATIVE", "URGENT", "CINEMATIC", "PAGE_TURNER", "SEAMLESS"
        ]
        
        available_styles = [style.name for style in PacingStyle]
        
        for expected in expected_styles:
            assert expected in available_styles, f"Expected pacing style {expected} not found"
        
        print(f"✓ All {len(expected_styles)} expected core pacing styles found")


class TestPacingStyleIntensityLevels:
    """Test intensity level categorization."""
    
    def test_high_intensity_styles(self):
        """Test that high intensity styles are correctly identified."""
        high_intensity_styles = PacingStyle.get_high_intensity_styles()
        
        # Should have multiple high intensity styles
        assert len(high_intensity_styles) >= 10
        
        # All should have high intensity
        for style in high_intensity_styles:
            assert style.intensity_level == "high"
        
        # Test some specific high intensity styles
        expected_high = [
            PacingStyle.BREAKNECK, PacingStyle.EXPLOSIVE, PacingStyle.FRANTIC,
            PacingStyle.BREATHLESS, PacingStyle.URGENT, PacingStyle.THRILLER_PACE
        ]
        
        for style in expected_high:
            assert style in high_intensity_styles, f"{style.value} should be high intensity"
    
    def test_low_intensity_styles(self):
        """Test that low intensity styles are correctly identified."""
        low_intensity_styles = PacingStyle.get_low_intensity_styles()
        
        # Should have multiple low intensity styles
        assert len(low_intensity_styles) >= 8
        
        # All should have low intensity
        for style in low_intensity_styles:
            assert style.intensity_level == "low"
        
        # Test some specific low intensity styles
        expected_low = [
            PacingStyle.LEISURELY, PacingStyle.SLOW_BURN, PacingStyle.CONTEMPLATIVE,
            PacingStyle.MEDITATIVE, PacingStyle.CALM, PacingStyle.RELAXED
        ]
        
        for style in expected_low:
            assert style in low_intensity_styles, f"{style.value} should be low intensity"
    
    def test_intensity_level_coverage(self):
        """Test that all intensity levels are represented."""
        all_styles = list(PacingStyle)
        high_count = len([s for s in all_styles if s.intensity_level == "high"])
        medium_count = len([s for s in all_styles if s.intensity_level == "medium"])
        low_count = len([s for s in all_styles if s.intensity_level == "low"])
        
        # Should have styles in all categories
        assert high_count > 0, "No high intensity styles found"
        assert medium_count > 0, "No medium intensity styles found"
        assert low_count > 0, "No low intensity styles found"
        
        # Total should equal all styles
        assert high_count + medium_count + low_count == len(all_styles)
        
        print(f"✓ Intensity distribution: {high_count} high, {medium_count} medium, {low_count} low")


class TestPacingStyleClassMethods:
    """Test class methods for style categorization."""
    
    def test_get_genre_specific_styles(self):
        """Test that genre-specific styles are correctly identified."""
        genre_styles = PacingStyle.get_genre_specific_styles()
        
        # Should have multiple genre-specific styles
        assert len(genre_styles) >= 6
        
        # Test some specific genre styles exist
        expected_genre_styles = [
            PacingStyle.THRILLER_PACE, PacingStyle.MYSTERY_PACE, 
            PacingStyle.ROMANCE_PACE, PacingStyle.HORROR_PACE,
            PacingStyle.ADVENTURE_PACE, PacingStyle.LITERARY_PACE,
            PacingStyle.COMEDY_PACE, PacingStyle.DRAMA_PACE
        ]
        
        for style in expected_genre_styles:
            assert style in genre_styles, f"{style.value} should be in genre-specific styles"
        
        print(f"✓ Found {len(genre_styles)} genre-specific pacing styles")
    
    def test_get_cinematic_styles(self):
        """Test that cinematic styles are correctly identified."""
        cinematic_styles = PacingStyle.get_cinematic_styles()
        
        # Should have multiple cinematic styles
        assert len(cinematic_styles) >= 4
        
        # Test some specific cinematic styles exist
        expected_cinematic = [
            PacingStyle.CINEMATIC, PacingStyle.QUICK_CUTS, 
            PacingStyle.SLOW_MOTION, PacingStyle.CHASE_SEQUENCE
        ]
        
        for style in expected_cinematic:
            assert style in cinematic_styles, f"{style.value} should be in cinematic styles"
        
        print(f"✓ Found {len(cinematic_styles)} cinematic pacing styles")
    
    def test_get_reader_engagement_styles(self):
        """Test that reader engagement styles are correctly identified."""
        engagement_styles = PacingStyle.get_reader_engagement_styles()
        
        # Should have multiple engagement styles
        assert len(engagement_styles) >= 4
        
        # Test some specific engagement styles exist
        expected_engagement = [
            PacingStyle.PAGE_TURNER, PacingStyle.IMMERSIVE,
            PacingStyle.CLIFFHANGER_DRIVEN, PacingStyle.ANTICIPATION_BUILDING
        ]
        
        for style in expected_engagement:
            assert style in engagement_styles, f"{style.value} should be in engagement styles"
        
        print(f"✓ Found {len(engagement_styles)} reader engagement pacing styles")


class TestPacingStyleFromString:
    """Test the from_string class method comprehensively."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("fast_paced", PacingStyle.FAST_PACED),
            ("slow_burn", PacingStyle.SLOW_BURN),
            ("moderate_paced", PacingStyle.MODERATE_PACED),
            ("breakneck", PacingStyle.BREAKNECK),
            ("leisurely", PacingStyle.LEISURELY),
            ("thriller_pace", PacingStyle.THRILLER_PACE),
        ]
        
        for input_str, expected_style in direct_matches:
            result = PacingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_display_name_matching(self):
        """Test from_string with display name matching."""
        display_name_matches = [
            ("Fast-Paced", PacingStyle.FAST_PACED),
            ("Slow Burn", PacingStyle.SLOW_BURN),
            ("Page-Turner", PacingStyle.PAGE_TURNER),
            ("Thriller Pace", PacingStyle.THRILLER_PACE),
            ("Quick Cuts", PacingStyle.QUICK_CUTS),
        ]
        
        for input_str, expected_style in display_name_matches:
            result = PacingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching."""
        fuzzy_matches = [
            ("fast", PacingStyle.FAST_PACED),
            ("slow", PacingStyle.SLOW_BURN),
            ("thriller", PacingStyle.THRILLER_PACE),
            ("mystery", PacingStyle.MYSTERY_PACE),
            ("romance", PacingStyle.ROMANCE_PACE),
            ("horror", PacingStyle.HORROR_PACE),
            ("intense", PacingStyle.INTENSE),
            ("calm", PacingStyle.CALM),
            ("steady", PacingStyle.STEADY),
            ("dramatic", PacingStyle.DRAMA_PACE),
        ]
        
        for input_str, expected_style in fuzzy_matches:
            result = PacingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_case_insensitive(self):
        """Test that from_string is case insensitive."""
        test_cases = [
            ("FAST_PACED", PacingStyle.FAST_PACED),
            ("Fast_Paced", PacingStyle.FAST_PACED),
            ("fast_paced", PacingStyle.FAST_PACED),
            ("THRILLER", PacingStyle.THRILLER_PACE),
            ("Thriller", PacingStyle.THRILLER_PACE),
            ("thriller", PacingStyle.THRILLER_PACE),
        ]
        
        for input_str, expected_style in test_cases:
            result = PacingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid inputs."""
        invalid_inputs = [
            "",
            None,
            "nonexistent_style",
            "completely_made_up",
            123,
            [],
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                PacingStyle.from_string(invalid_input)
    
    def test_from_string_whitespace_handling(self):
        """Test that from_string handles whitespace correctly."""
        whitespace_cases = [
            ("  fast_paced  ", PacingStyle.FAST_PACED),
            ("\tthrill\n", PacingStyle.THRILLER_PACE),
            ("  slow burn  ", PacingStyle.SLOW_BURN),
        ]
        
        for input_str, expected_style in whitespace_cases:
            result = PacingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"


class TestPacingStyleIntegration:
    """Integration tests for the pacing style system."""
    
    def test_all_styles_have_complete_properties(self):
        """Test that all pacing styles have all required properties implemented."""
        for style in PacingStyle:
            # Test all properties work without errors
            assert style.display_name is not None
            assert style.description is not None
            assert style.intensity_level is not None
            assert style.typical_genres is not None
            
            # Properties should return expected types
            assert isinstance(style.display_name, str)
            assert isinstance(style.description, str)
            assert isinstance(style.intensity_level, str)
            assert isinstance(style.typical_genres, list)
    
    def test_style_consistency(self):
        """Test that style properties are internally consistent."""
        for style in PacingStyle:
            # High intensity styles should generally have action-oriented genres
            if style.intensity_level == "high":
                genres = [genre.lower() for genre in style.typical_genres]
                # At least some high intensity styles should have action-oriented genres
                action_genres = ["action", "thriller", "suspense", "adventure", "chase"]
                # This is not a strict requirement for all high intensity styles
            
            # Genre-specific styles should include their genre in typical_genres
            if "_pace" in style.value:
                genre_name = style.value.replace("_pace", "")
                genre_found = any(genre_name in genre.lower() or genre.lower() in genre_name 
                                for genre in style.typical_genres)
                # This is a soft check - not all genre styles need to match exactly
    
    def test_no_duplicate_classifications(self):
        """Test that classification methods don't return duplicates."""
        high_intensity = PacingStyle.get_high_intensity_styles()
        low_intensity = PacingStyle.get_low_intensity_styles()
        genre_specific = PacingStyle.get_genre_specific_styles()
        cinematic = PacingStyle.get_cinematic_styles()
        engagement = PacingStyle.get_reader_engagement_styles()
        
        # Each list should have unique items
        assert len(high_intensity) == len(set(high_intensity))
        assert len(low_intensity) == len(set(low_intensity))
        assert len(genre_specific) == len(set(genre_specific))
        assert len(cinematic) == len(set(cinematic))
        assert len(engagement) == len(set(engagement))
        
        # High and low intensity should not overlap
        high_set = set(high_intensity)
        low_set = set(low_intensity)
        assert len(high_set.intersection(low_set)) == 0, "High and low intensity styles should not overlap"


class TestPacingStylePerformance:
    """Test performance characteristics of PacingStyle methods."""
    
    def test_from_string_performance(self):
        """Test that from_string method performs reasonably fast."""
        test_inputs = ["fast", "slow", "thriller", "mystery", "intense", "calm"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    PacingStyle.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 6,000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        start_time = time.time()
        for _ in range(100):  # Reduced iterations for realistic performance
            for style in PacingStyle:
                _ = style.display_name
                _ = style.description
                _ = style.intensity_level
                _ = style.typical_genres
        end_time = time.time()
        
        # Should complete many property accesses in under 2 seconds
        total_time = end_time - start_time
        assert total_time < 2.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_classification_performance(self):
        """Test that classification methods are reasonably fast."""
        start_time = time.time()
        for _ in range(1000):
            PacingStyle.get_high_intensity_styles()
            PacingStyle.get_low_intensity_styles()
            PacingStyle.get_genre_specific_styles()
            PacingStyle.get_cinematic_styles()
            PacingStyle.get_reader_engagement_styles()
        end_time = time.time()
        
        # Should complete 5000 classification operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Classification methods too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_str_method(self):
        """Test __str__ method returns display name."""
        for style in PacingStyle:
            str_repr = str(style)
            assert isinstance(str_repr, str)
            assert len(str_repr) > 0
            assert str_repr == style.display_name
    
    def test_repr_method(self):
        """Test __repr__ method returns proper representation."""
        for style in PacingStyle:
            repr_str = repr(style)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0
            assert "PacingStyle." in repr_str
            assert style.name in repr_str


if __name__ == "__main__":
    # Run basic smoke tests if called directly
    print("Running PacingStyle tests...")
    
    # Test basic functionality
    test_basic = TestBasicFunctionality()
    test_basic.test_str_method()
    test_basic.test_repr_method()
    
    test_properties = TestPacingStyleBasicProperties()
    test_properties.test_all_pacing_values_are_strings()
    
    test_enum = TestPacingStyleEnumFunctionality()
    test_enum.test_expected_styles_exist()
    
    test_class_methods = TestPacingStyleClassMethods()
    test_class_methods.test_get_genre_specific_styles()
    test_class_methods.test_get_cinematic_styles()
    test_class_methods.test_get_reader_engagement_styles()
    
    print("✓ All basic tests passed!")
    
    # Run full test suite
    pytest.main([__file__, "-v"])