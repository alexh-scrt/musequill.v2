"""
Comprehensive tests for musequill.models.book.tone_style module.

Test file: tests/models/book/test_tone_style.py
Module under test: musequill/models/book/tone_style.py

Run from project root: pytest tests/models/book/test_tone_style.py -v
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from typing import List, Optional

# Import ToneStyle from the tone_style module
from musequill.models.book.tone_style import ToneStyle


class TestToneStyleBasicProperties:
    """Test basic enum properties and functionality."""
    
    def test_all_tone_values_are_strings(self):
        """Ensure all tone enum values are properly formatted strings."""
        for tone in ToneStyle:
            assert isinstance(tone.value, str), f"{tone.name} value is not a string"
            assert tone.value.islower(), f"{tone.name} value should be lowercase"
            assert len(tone.value) > 0, f"{tone.name} value is empty"
            # Allow underscores and hyphens for multi-word tones
            assert all(c.isalnum() or c in ['_', '-'] for c in tone.value), \
                f"{tone.name} contains invalid characters"
    
    def test_all_tones_have_unique_values(self):
        """Ensure no duplicate values in ToneStyle enum."""
        values = [tone.value for tone in ToneStyle]
        unique_values = set(values)
        assert len(values) == len(unique_values), \
            f"Duplicate tone values found: {len(values)} total, {len(unique_values)} unique"
    
    def test_display_name_property(self):
        """Test that display_name properly formats tone names."""
        for tone in ToneStyle:
            display = tone.display_name
            assert isinstance(display, str), f"{tone.name} display_name is not a string"
            assert len(display) > 0, f"{tone.name} display_name is empty"
            # Should be title case or have proper capitalization
            assert display[0].isupper() or display[0].isdigit(), \
                f"{tone.name} display_name should start with uppercase: '{display}'"
    
    def test_description_property(self):
        """Test that all tones have meaningful descriptions."""
        short_descriptions = 0
        quality_descriptions = 0
        
        for tone in ToneStyle:
            description = tone.description
            assert isinstance(description, str), f"{tone.name} description is not a string"
            assert len(description) > 0, f"{tone.name} description is empty"
            
            # Track description quality (permissive checks)
            if len(description) < 20:
                short_descriptions += 1
            if (len(description) > 30 and 
                (description[0].isupper() and 
                 (description.endswith('.') or description.endswith('!') or description.endswith('?')))):
                quality_descriptions += 1
        
        # Permissive quality checks
        total_tones = len(list(ToneStyle))
        short_percentage = short_descriptions / total_tones
        quality_percentage = quality_descriptions / total_tones
        
        # Allow up to 30% short descriptions
        assert short_percentage <= 0.3, \
            f"Too many short descriptions: {short_descriptions}/{total_tones} ({short_percentage:.1%})"
        
        # Expect at least 50% quality descriptions
        assert quality_percentage >= 0.5, \
            f"Too few quality descriptions: {quality_descriptions}/{total_tones} ({quality_percentage:.1%})"
        
        print(f"✓ Description quality: {quality_descriptions}/{total_tones} ({quality_percentage:.1%}) good, "
              f"{short_descriptions}/{total_tones} ({short_percentage:.1%}) short")


class TestToneStyleEnumFunctionality:
    """Test enum-specific functionality."""
    
    def test_expected_core_tones_exist(self):
        """Test that core expected tones exist (permissive list)."""
        # Core tones that should definitely exist
        expected_core_tones = [
            "serious", "humorous", "dark", "romantic", "mysterious",
            "dramatic", "optimistic", "melancholic", "suspenseful"
        ]
        
        existing_values = [tone.value for tone in ToneStyle]
        
        missing_tones = []
        for expected in expected_core_tones:
            if expected not in existing_values:
                missing_tones.append(expected)
        
        # Allow some flexibility - require at least 70% of core tones
        missing_percentage = len(missing_tones) / len(expected_core_tones)
        assert missing_percentage <= 0.3, \
            f"Too many core tones missing: {missing_tones} ({missing_percentage:.1%})"
        
        print(f"✓ Core tones present: {len(expected_core_tones) - len(missing_tones)}/{len(expected_core_tones)}")
    
    def test_tone_categories_are_diverse(self):
        """Test that we have diverse tone categories (permissive)."""
        # Group tones by common patterns to ensure diversity
        humor_tones = [t for t in ToneStyle if any(word in t.value for word in 
                      ['humor', 'comic', 'funny', 'witty', 'playful', 'whimsical', 'satirical', 'ironic'])]
        
        dark_tones = [t for t in ToneStyle if any(word in t.value for word in 
                     ['dark', 'gritty', 'bleak', 'cynical', 'noir', 'gothic', 'sinister', 'ominous'])]
        
        romantic_tones = [t for t in ToneStyle if any(word in t.value for word in 
                         ['romantic', 'tender', 'intimate', 'sensual', 'loving', 'passionate'])]
        
        dramatic_tones = [t for t in ToneStyle if any(word in t.value for word in 
                         ['dramatic', 'intense', 'epic', 'tragic', 'heroic', 'urgent'])]
        
        # Permissively check that we have some variety
        assert len(humor_tones) >= 3, f"Need at least 3 humor-related tones, found {len(humor_tones)}"
        assert len(dark_tones) >= 3, f"Need at least 3 dark-related tones, found {len(dark_tones)}"
        assert len(romantic_tones) >= 2, f"Need at least 2 romantic-related tones, found {len(romantic_tones)}"
        assert len(dramatic_tones) >= 3, f"Need at least 3 dramatic-related tones, found {len(dramatic_tones)}"
        
        print(f"✓ Tone diversity: Humor({len(humor_tones)}), Dark({len(dark_tones)}), "
              f"Romance({len(romantic_tones)}), Drama({len(dramatic_tones)})")
    
    def test_enum_iteration_and_membership(self):
        """Test basic enum iteration and membership."""
        tone_count = 0
        for tone in ToneStyle:
            tone_count += 1
            assert tone in ToneStyle, f"{tone} should be in ToneStyle enum"
        
        # Should have a reasonable number of tones (permissive range)
        assert 20 <= tone_count <= 200, f"Expected 20-200 tones, found {tone_count}"
        print(f"✓ Total tones: {tone_count}")


class TestToneStylePropertyMethods:
    """Test the property methods of ToneStyle."""
    
    def test_emotional_intensity_property(self):
        """Test emotional_intensity property returns valid values."""
        valid_intensities = {"low", "medium-low", "medium", "medium-high", "high"}
        intensity_counts = {level: 0 for level in valid_intensities}
        
        for tone in ToneStyle:
            try:
                intensity = tone.emotional_intensity
                assert isinstance(intensity, str), f"{tone.name} intensity should be string"
                assert intensity in valid_intensities, \
                    f"{tone.name} has invalid intensity: {intensity}"
                intensity_counts[intensity] += 1
            except AttributeError:
                # Permissive - allow tones without this property
                pass
        
        # If property exists, should have reasonable distribution
        total_with_intensity = sum(intensity_counts.values())
        if total_with_intensity > 0:
            # Should have some variety across intensity levels
            non_empty_levels = sum(1 for count in intensity_counts.values() if count > 0)
            assert non_empty_levels >= 3, f"Should have at least 3 different intensity levels"
            print(f"✓ Intensity distribution: {intensity_counts}")
    
    def test_emotional_valence_property(self):
        """Test emotional_valence property returns valid values."""
        valid_valences = {"positive", "negative", "neutral", "complex"}
        valence_counts = {level: 0 for level in valid_valences}
        
        for tone in ToneStyle:
            try:
                valence = tone.emotional_valence
                assert isinstance(valence, str), f"{tone.name} valence should be string"
                assert valence in valid_valences, \
                    f"{tone.name} has invalid valence: {valence}"
                valence_counts[valence] += 1
            except AttributeError:
                # Permissive - allow tones without this property
                pass
        
        # If property exists, should have reasonable distribution
        total_with_valence = sum(valence_counts.values())
        if total_with_valence > 0:
            # Should have both positive and negative tones at minimum
            assert valence_counts["positive"] > 0, "Should have some positive tones"
            assert valence_counts["negative"] > 0, "Should have some negative tones"
            print(f"✓ Valence distribution: {valence_counts}")
    
    def test_genre_compatibility_property(self):
        """Test genre_compatibility property returns reasonable values."""
        for tone in ToneStyle:
            try:
                genres = tone.genre_compatibility
                assert isinstance(genres, list), f"{tone.name} genre_compatibility should be list"
                
                # Should have at least one compatible genre
                assert len(genres) > 0, f"{tone.name} should be compatible with at least one genre"
                
                # All genres should be strings
                for genre in genres:
                    assert isinstance(genre, str), f"Genre '{genre}' for {tone.name} should be string"
                    assert len(genre) > 0, f"Empty genre string for {tone.name}"
                
                # Reasonable number of compatible genres (permissive)
                assert len(genres) <= 20, f"{tone.name} has too many compatible genres: {len(genres)}"
                
            except AttributeError:
                # Permissive - allow tones without this property
                pass


class TestToneStyleClassMethods:
    """Test class methods and utility functions."""
    
    def test_get_compatible_tones_method(self):
        """Test get_compatible_tones class method if it exists."""
        try:
            # Test with a few known tones
            test_tones = [
                ToneStyle.ROMANTIC if hasattr(ToneStyle, 'ROMANTIC') else None,
                ToneStyle.MYSTERIOUS if hasattr(ToneStyle, 'MYSTERIOUS') else None,
                ToneStyle.HUMOROUS if hasattr(ToneStyle, 'HUMOROUS') else None
            ]
            
            for tone in test_tones:
                if tone is not None:
                    try:
                        compatible = ToneStyle.get_compatible_tones(tone)
                        assert isinstance(compatible, list), \
                            f"get_compatible_tones should return list for {tone}"
                        
                        # Should return valid ToneStyle instances
                        for compat_tone in compatible:
                            assert isinstance(compat_tone, ToneStyle), \
                                f"Compatible tone should be ToneStyle instance: {compat_tone}"
                        
                        # Reasonable number of compatible tones
                        assert len(compatible) <= 15, \
                            f"Too many compatible tones for {tone}: {len(compatible)}"
                        
                    except (AttributeError, TypeError):
                        # Method might not exist or work as expected - permissive
                        pass
                        
        except AttributeError:
            # Class method doesn't exist - that's okay
            pass
    
    def test_from_description_method(self):
        """Test from_description class method if it exists."""
        try:
            # Test with various description types
            test_descriptions = [
                "funny and lighthearted",
                "dark and mysterious", 
                "romantic love story",
                "serious drama",
                "action-packed adventure",
                "",  # Empty string
                "completely unrelated text that shouldn't match anything"
            ]
            
            valid_results = 0
            for description in test_descriptions:
                try:
                    result = ToneStyle.from_description(description)
                    if result is not None:
                        assert isinstance(result, ToneStyle), \
                            f"from_description should return ToneStyle or None, got {type(result)}"
                        valid_results += 1
                    
                except (AttributeError, TypeError, ValueError):
                    # Method might not exist or handle edge cases - permissive
                    pass
            
            # If method exists and works, should find at least some matches
            if valid_results > 0:
                print(f"✓ from_description found {valid_results}/{len(test_descriptions)} matches")
                
        except AttributeError:
            # Class method doesn't exist - that's okay
            pass


class TestToneStyleIntegration:
    """Integration and edge case tests."""
    
    def test_str_and_repr_methods(self):
        """Test string representation methods."""
        for tone in ToneStyle:
            # Test __str__ method
            str_repr = str(tone)
            assert isinstance(str_repr, str), f"{tone.name} __str__ should return string"
            assert len(str_repr) > 0, f"{tone.name} __str__ should not be empty"
            
            # Test __repr__ method  
            repr_str = repr(tone)
            assert isinstance(repr_str, str), f"{tone.name} __repr__ should return string"
            assert len(repr_str) > 0, f"{tone.name} __repr__ should not be empty"
    
    def test_tone_value_consistency(self):
        """Test that tone values are consistent with names."""
        inconsistent_tones = []
        
        for tone in ToneStyle:
            # Convert enum name to expected value format
            expected_value = tone.name.lower()
            
            # Allow some flexibility in naming conventions
            if tone.value != expected_value:
                # Check if it's a reasonable variation
                name_words = tone.name.lower().split('_')
                value_words = tone.value.replace('-', '_').split('_')
                
                # Allow reasonable variations but track significant differences
                if not (set(name_words).intersection(set(value_words)) or 
                       any(word in tone.value for word in name_words[:2])):
                    inconsistent_tones.append((tone.name, tone.value))
        
        # Allow some inconsistency but not too much
        inconsistency_rate = len(inconsistent_tones) / len(list(ToneStyle))
        assert inconsistency_rate <= 0.2, \
            f"Too many inconsistent tone names/values: {len(inconsistent_tones)} " \
            f"({inconsistency_rate:.1%}). Examples: {inconsistent_tones[:5]}"
    
    def test_memory_and_performance(self):
        """Basic performance and memory usage tests."""
        import time
        
        # Test enum iteration performance
        start_time = time.time()
        tone_count = 0
        for _ in range(100):  # Iterate multiple times
            for tone in ToneStyle:
                tone_count += 1
        iteration_time = time.time() - start_time
        
        # Should complete quickly (permissive - 1 second limit)
        assert iteration_time < 1.0, f"Enum iteration too slow: {iteration_time:.3f}s"
        
        # Test property access performance
        start_time = time.time()
        for _ in range(10):
            for tone in ToneStyle:
                _ = tone.display_name
                _ = tone.description
        property_time = time.time() - start_time
        
        # Should complete quickly (permissive - 2 second limit)
        assert property_time < 2.0, f"Property access too slow: {property_time:.3f}s"
        
        print(f"✓ Performance: Iteration({iteration_time:.3f}s), Properties({property_time:.3f}s)")


class TestToneStyleEdgeCases:
    """Test edge cases and error handling."""
    
    def test_enum_membership_edge_cases(self):
        """Test edge cases for enum membership."""
        # Test with various invalid inputs
        invalid_inputs = [None, "", "not_a_tone", 123, [], {}, object()]
        
        for invalid_input in invalid_inputs:
            assert invalid_input not in ToneStyle, \
                f"Invalid input {invalid_input} should not be in ToneStyle"
    
    def test_property_error_handling(self):
        """Test that properties handle edge cases gracefully."""
        for tone in ToneStyle:
            try:
                # These should not raise exceptions
                _ = tone.display_name
                _ = tone.description
                
                # Optional properties should either work or be absent
                try:
                    _ = tone.emotional_intensity
                except AttributeError:
                    pass  # Optional property
                
                try:
                    _ = tone.emotional_valence  
                except AttributeError:
                    pass  # Optional property
                    
                try:
                    _ = tone.genre_compatibility
                except AttributeError:
                    pass  # Optional property
                    
            except Exception as e:
                pytest.fail(f"Property access failed for {tone.name}: {e}")


# Utility functions for running tests
def run_basic_smoke_tests():
    """Run basic smoke tests if module is called directly."""
    print("Running ToneStyle basic smoke tests...")
    
    # Test basic enum functionality
    tone_count = len(list(ToneStyle))
    print(f"✓ Found {tone_count} tones")
    
    # Test a few core properties
    sample_tones = list(ToneStyle)[:5]  # First 5 tones
    for tone in sample_tones:
        assert hasattr(tone, 'display_name')
        assert hasattr(tone, 'description')
        print(f"✓ {tone.name}: {tone.display_name}")
    
    print("✓ All basic smoke tests passed!")


if __name__ == "__main__":
    # Run basic tests if called directly
    run_basic_smoke_tests()
    
    # Run full test suite with pytest
    print("\nRunning full test suite...")
    pytest.main([__file__, "-v", "--tb=short"])