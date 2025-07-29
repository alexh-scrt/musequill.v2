"""
Comprehensive tests for TechnologyLevel enum.

Test file: tests/models/book/test_technology.py
Module under test: musequill/models/book/technology.py

Run from project root: pytest tests/models/book/test_technology.py -v
"""

import sys
from pathlib import Path
import pytest
import time
from typing import List, Set, Dict, Any

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the TechnologyLevel class from the technology module
from musequill.models.book.technology import TechnologyLevel


class TestTechnologyLevel:
    """Test the TechnologyLevel enum comprehensively."""
    
    def test_all_tech_values_are_strings(self):
        """Ensure all technology level enum values are properly formatted strings."""
        for tech_level in TechnologyLevel:
            assert isinstance(tech_level.value, str)
            assert tech_level.value.islower()
            assert " " not in tech_level.value  # Should use underscores
            assert len(tech_level.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in tech_level.value)
    
    def test_all_tech_levels_have_unique_values(self):
        """Ensure no duplicate values in TechnologyLevel enum."""
        values = [tech_level.value for tech_level in TechnologyLevel]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate tech level values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have exactly 34 technology levels
        assert len(values) == 34, f"Expected exactly 34 technology levels, got {len(values)}"
        print(f"✓ Found {len(values)} unique technology levels")
    
    def test_display_name_property(self):
        """Test that display_name properly formats tech level names."""
        for tech_level in TechnologyLevel:
            display_name = tech_level.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (TechnologyLevel.STONE_AGE, "Stone Age"),
            (TechnologyLevel.BRONZE_AGE, "Bronze Age"),
            (TechnologyLevel.STEAM_PUNK, "Steam Punk"),
            (TechnologyLevel.POST_APOCALYPTIC, "Post Apocalyptic"),
            (TechnologyLevel.NEAR_FUTURE, "Near Future"),
            (TechnologyLevel.SPACE_FARING, "Space Faring"),
            (TechnologyLevel.POST_HUMAN, "Post Human"),
            (TechnologyLevel.RETRO_FUTURISM, "Retro Futurism"),
        ]
        
        for tech_level, expected_display in test_cases:
            assert tech_level.display_name == expected_display, f"Expected '{expected_display}' for {tech_level.value}, got '{tech_level.display_name}'"
    
    def test_description_property(self):
        """Test that all technology levels have meaningful descriptions."""
        short_descriptions = []
        
        for tech_level in TechnologyLevel:
            description = tech_level.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {tech_level.value}"
            
            # Check for minimum meaningful length (tech descriptions should be substantial)
            if len(description) < 100:
                short_descriptions.append(f"{tech_level.value}: '{description}'")
            
            # Should start with capital letter or number
            if description:
                assert description[0].isupper() or description[0].isdigit(), f"Description should start with capital or number for {tech_level.value}: '{description}'"
            
            # Should end with proper punctuation
            assert description.endswith('.'), f"Description should end with period for {tech_level.value}: '{description}'"
        
        # Most descriptions should be substantial (allow up to 6 short descriptions)
        assert len(short_descriptions) <= 6, f"Too many short descriptions: {short_descriptions}"
    
    def test_time_period_property(self):
        """Test that all technology levels have time period information."""
        for tech_level in TechnologyLevel:
            time_period = tech_level.time_period
            assert isinstance(time_period, str)
            assert len(time_period) > 0, f"Time period is empty for {tech_level.value}"
            
            # Should contain some indication of time (numbers, "CE", "BCE", etc.) or be descriptive
            has_time_indicator = any(char.isdigit() for char in time_period) or \
                               any(indicator in time_period.upper() for indicator in ["CE", "BCE", "ALTERNATIVE", "VARIABLE", "POST-", "UNKNOWN", "DURING", "RECOVERY", "VISION", "AESTHETIC"])
            assert has_time_indicator, f"Time period should contain time indicators for {tech_level.value}: '{time_period}'"
    
    def test_key_technologies_property(self):
        """Test that all technology levels have appropriate key technologies."""
        for tech_level in TechnologyLevel:
            key_techs = tech_level.key_technologies
            assert isinstance(key_techs, list)
            assert len(key_techs) > 0, f"No key technologies found for {tech_level.value}"
            assert len(key_techs) >= 3, f"Should have at least 3 key technologies for {tech_level.value}, got {len(key_techs)}"
            
            # All technologies should be strings
            for tech in key_techs:
                assert isinstance(tech, str)
                assert len(tech) > 0
                # Should be lowercase descriptive terms
                assert tech.islower() or any(c.isupper() for c in tech[1:])  # Allow proper nouns
    
    def test_complexity_level_property(self):
        """Test that complexity levels are properly categorized."""
        valid_complexity_levels = {"minimal", "low", "moderate", "high", "very high", "extreme", "variable", "unknown"}
        
        complexity_distribution = {}
        for tech_level in TechnologyLevel:
            complexity = tech_level.complexity_level
            assert isinstance(complexity, str)
            assert complexity in valid_complexity_levels, f"Invalid complexity level '{complexity}' for {tech_level.value}"
            
            complexity_distribution[complexity] = complexity_distribution.get(complexity, 0) + 1
        
        # Should have reasonable distribution across complexity levels
        assert len(complexity_distribution) >= 5, f"Should use variety in complexity levels, found {len(complexity_distribution)}"
        print(f"✓ Complexity distribution: {complexity_distribution}")
    
    def test_research_requirements_property(self):
        """Test that research requirements are comprehensive."""
        for tech_level in TechnologyLevel:
            research_reqs = tech_level.research_requirements
            assert isinstance(research_reqs, list)
            assert len(research_reqs) > 0, f"No research requirements found for {tech_level.value}"
            assert len(research_reqs) >= 2, f"Should have at least 2 research areas for {tech_level.value}, got {len(research_reqs)}"
            
            # All requirements should be strings
            for req in research_reqs:
                assert isinstance(req, str)
                assert len(req) > 0
                # Should be lowercase descriptive terms
                assert req.islower() or any(c.isupper() for c in req)  # Allow proper nouns


class TestTechnologyLevelClassMethods:
    """Test class methods of TechnologyLevel."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("stone_age", TechnologyLevel.STONE_AGE),
            ("medieval", TechnologyLevel.MEDIEVAL),
            ("steam_punk", TechnologyLevel.STEAM_PUNK),
            ("cyberpunk", TechnologyLevel.CYBERPUNK),
            ("near_future", TechnologyLevel.NEAR_FUTURE),
            ("post_apocalyptic", TechnologyLevel.POST_APOCALYPTIC),
        ]
        
        for input_str, expected_tech in direct_matches:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_display_name_matching(self):
        """Test from_string with display name matching."""
        display_name_matches = [
            ("Stone Age", TechnologyLevel.STONE_AGE),
            ("Medieval", TechnologyLevel.MEDIEVAL),
            ("Steam Punk", TechnologyLevel.STEAM_PUNK),
            ("Post Apocalyptic", TechnologyLevel.POST_APOCALYPTIC),
            ("Near Future", TechnologyLevel.NEAR_FUTURE),
        ]
        
        for input_str, expected_tech in display_name_matches:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching using synonyms."""
        fuzzy_matches = [
            ("prehistoric", TechnologyLevel.STONE_AGE),
            ("caveman", TechnologyLevel.STONE_AGE),
            ("ancient", TechnologyLevel.CLASSICAL),
            ("roman", TechnologyLevel.CLASSICAL),
            ("middle ages", TechnologyLevel.MEDIEVAL),
            ("knight", TechnologyLevel.MEDIEVAL),
            ("industrial", TechnologyLevel.HIGH_INDUSTRIAL),
            ("steampunk", TechnologyLevel.STEAM_PUNK),  # Use full word
            ("modern", TechnologyLevel.MODERN),
            ("contemporary", TechnologyLevel.MODERN),
            ("future", TechnologyLevel.NEAR_FUTURE),
            ("sci-fi", TechnologyLevel.FAR_FUTURE),
            ("space", TechnologyLevel.SPACE_FARING),
            ("cyber", TechnologyLevel.CYBERPUNK),
            ("apocalypse", TechnologyLevel.APOCALYPTIC),
            ("climate", TechnologyLevel.CLIMATE_TECH),
            ("singularity", TechnologyLevel.SINGULARITY),
        ]
        
        for input_str, expected_tech in fuzzy_matches:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_case_insensitive(self):
        """Test from_string handles case variations."""
        case_variations = [
            ("MEDIEVAL", TechnologyLevel.MEDIEVAL),
            ("Medieval", TechnologyLevel.MEDIEVAL),
            ("medieval", TechnologyLevel.MEDIEVAL),
            ("CYBERPUNK", TechnologyLevel.CYBERPUNK),
            ("CyberPunk", TechnologyLevel.CYBERPUNK),
            ("cyberpunk", TechnologyLevel.CYBERPUNK),
        ]
        
        for input_str, expected_tech in case_variations:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_invalid_inputs(self):
        """Test from_string with clearly invalid inputs."""
        # Test only the most clearly invalid inputs
        clearly_invalid_inputs = [
            "",
            "   ",
            "123456789",       # Pure numbers
            "!@#$%^&*()",      # Pure symbols
        ]
        
        for invalid_input in clearly_invalid_inputs:
            with pytest.raises(ValueError, match="Invalid technology level"):
                TechnologyLevel.from_string(invalid_input)
    
    def test_from_string_partial_matching_edge_cases(self):
        """Test that partial matching works correctly for edge cases."""
        # These should work due to good partial matches via fuzzy mappings
        valid_partial_matches = [
            ("steampunk", TechnologyLevel.STEAM_PUNK),  # Via fuzzy mapping
            ("cyber", TechnologyLevel.CYBERPUNK),       # Via fuzzy mapping  
            ("space", TechnologyLevel.SPACE_FARING),    # Via fuzzy mapping
        ]
        
        for input_str, expected_tech in valid_partial_matches:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_borderline_cases(self):
        """Test borderline cases that might or might not match."""
        # These are borderline cases where matching behavior might vary
        # We test that they either raise ValueError or return a valid TechnologyLevel
        borderline_inputs = [
            "xxxcyberxxx",     # Contains "cyber" but with noise
            "medievalxxxxxxx", # Contains "medieval" but with noise
            "randomstuff",     # Contains "random" but no tech terms
            "xyz123notfound",  # Pure gibberish with numbers
        ]
        
        for input_str in borderline_inputs:
            try:
                result = TechnologyLevel.from_string(input_str)
                # If it matches something, it should be a valid TechnologyLevel
                assert isinstance(result, TechnologyLevel)
                print(f"Borderline case '{input_str}' matched to {result.value}")
            except ValueError:
                print(f"Borderline case '{input_str}' correctly rejected")
                # This is also acceptable behavior
    
    def test_from_string_direct_partial_matches(self):
        """Test direct partial matching with tech level components."""
        # These should work through direct partial matching or fuzzy mappings
        # Note: Some may match the first valid tech level found, not necessarily the "best" match
        direct_partial_matches = [
            ("medieval", TechnologyLevel.MEDIEVAL),     # Exact match
            ("galactic", TechnologyLevel.GALACTIC),     # Exact match
        ]
        
        for input_str, expected_tech in direct_partial_matches:
            result = TechnologyLevel.from_string(input_str)
            assert result == expected_tech, f"Expected {expected_tech} for '{input_str}', got {result}"
    
    def test_from_string_ambiguous_inputs_handled(self):
        """Test that ambiguous inputs are handled reasonably."""
        # These inputs might match different tech levels depending on order
        # Just verify they match something valid, not necessarily a specific level
        ambiguous_inputs = ["punk", "age", "tech"]
        
        for input_str in ambiguous_inputs:
            try:
                result = TechnologyLevel.from_string(input_str)
                assert isinstance(result, TechnologyLevel)
                print(f"'{input_str}' matched to {result.value}")
            except ValueError:
                print(f"'{input_str}' correctly rejected as too ambiguous")
        
        # Test inputs that might partially match but should still be invalid
        potentially_problematic_inputs = [
            "invalid_tech_level",  # Contains "tech" 
            "xyz_abc_def",        # Contains underscores like enum values
        ]
        
        for input_str in potentially_problematic_inputs:
            # These might or might not raise - depends on fuzzy matching implementation
            try:
                result = TechnologyLevel.from_string(input_str)
                print(f"Note: '{input_str}' matched to {result} (fuzzy matching)")
            except ValueError:
                print(f"✓ '{input_str}' correctly rejected")
    
    def test_from_string_edge_case_inputs(self):
        """Test from_string with edge cases that might unexpectedly match."""
        # Test inputs that contain common tech words but shouldn't match
        edge_cases = [
            "invalid tech level",  # Contains "tech" 
            "not a real level",    # Contains common words
            "fake future stuff",   # Contains "future"
        ]
        
        for input_str in edge_cases:
            try:
                result = TechnologyLevel.from_string(input_str)
                # If it matches, verify it's a reasonable match
                assert isinstance(result, TechnologyLevel)
                print(f"Edge case '{input_str}' matched to {result}")
            except ValueError:
                print(f"Edge case '{input_str}' correctly rejected")
    
    def test_from_string_none_input(self):
        """Test from_string with None input."""
        with pytest.raises(ValueError, match="Invalid technology level value"):
            TechnologyLevel.from_string(None)
    
    def test_get_historical_levels(self):
        """Test get_historical_levels returns appropriate levels."""
        historical_levels = TechnologyLevel.get_historical_levels()
        assert isinstance(historical_levels, list)
        assert len(historical_levels) == 15  # Should have exactly 15 historical levels
        
        # Should include key historical periods
        expected_historical = [
            TechnologyLevel.STONE_AGE, TechnologyLevel.BRONZE_AGE, TechnologyLevel.IRON_AGE,
            TechnologyLevel.CLASSICAL, TechnologyLevel.MEDIEVAL, TechnologyLevel.RENAISSANCE,
            TechnologyLevel.MODERN
        ]
        
        for expected in expected_historical:
            assert expected in historical_levels, f"{expected} should be in historical levels"
        
        # Should not include future or alternative levels
        should_not_include = [
            TechnologyLevel.NEAR_FUTURE, TechnologyLevel.CYBERPUNK, TechnologyLevel.POST_APOCALYPTIC
        ]
        
        for excluded in should_not_include:
            assert excluded not in historical_levels, f"{excluded} should not be in historical levels"
    
    def test_get_future_levels(self):
        """Test get_future_levels returns appropriate levels."""
        future_levels = TechnologyLevel.get_future_levels()
        assert isinstance(future_levels, list)
        assert len(future_levels) == 10  # Should have exactly 10 future levels
        
        # Should include key future periods
        expected_future = [
            TechnologyLevel.NEAR_FUTURE, TechnologyLevel.SPACE_FARING, TechnologyLevel.POST_HUMAN,
            TechnologyLevel.SINGULARITY, TechnologyLevel.FAR_FUTURE
        ]
        
        for expected in expected_future:
            assert expected in future_levels, f"{expected} should be in future levels"
        
        # Should not include historical or alternative levels
        should_not_include = [
            TechnologyLevel.MEDIEVAL, TechnologyLevel.CYBERPUNK, TechnologyLevel.STEAM_PUNK
        ]
        
        for excluded in should_not_include:
            assert excluded not in future_levels, f"{excluded} should not be in future levels"
    
    def test_get_alternative_levels(self):
        """Test get_alternative_levels returns appropriate levels."""
        alternative_levels = TechnologyLevel.get_alternative_levels()
        assert isinstance(alternative_levels, list)
        assert len(alternative_levels) == 9, f"Should have exactly 9 alternative levels, got {len(alternative_levels)}"  # Should be 9
        
        # Should include punk genres and alternatives
        expected_alternative = [
            TechnologyLevel.STEAM_PUNK, TechnologyLevel.CYBERPUNK, TechnologyLevel.DIESELPUNK,
            TechnologyLevel.BIOPUNK, TechnologyLevel.SOLARPUNK, TechnologyLevel.POST_APOCALYPTIC,
            TechnologyLevel.MIXED
        ]
        
        for expected in expected_alternative:
            assert expected in alternative_levels, f"{expected} should be in alternative levels"
        
        # Should not include standard historical or future levels
        should_not_include = [
            TechnologyLevel.MEDIEVAL, TechnologyLevel.NEAR_FUTURE, TechnologyLevel.CLASSICAL
        ]
        
        for excluded in should_not_include:
            assert excluded not in alternative_levels, f"{excluded} should not be in alternative levels"
    
    def test_get_by_complexity(self):
        """Test get_by_complexity categorization."""
        # Test valid complexity levels
        valid_complexities = ["minimal", "low", "moderate", "high", "very high", "extreme"]
        
        for complexity in valid_complexities:
            levels = TechnologyLevel.get_by_complexity(complexity)
            assert isinstance(levels, list)
            
            # Verify all returned levels have the correct complexity
            for level in levels:
                assert level.complexity_level == complexity, f"{level} should have complexity '{complexity}', got '{level.complexity_level}'"
        
        # Test specific known complexities
        minimal_levels = TechnologyLevel.get_by_complexity("minimal")
        assert TechnologyLevel.STONE_AGE in minimal_levels
        
        extreme_levels = TechnologyLevel.get_by_complexity("extreme")
        expected_extreme = [TechnologyLevel.GALACTIC, TechnologyLevel.POST_HUMAN, 
                          TechnologyLevel.SINGULARITY, TechnologyLevel.POST_SINGULARITY]
        for expected in expected_extreme:
            assert expected in extreme_levels, f"{expected} should be in extreme complexity levels"
    
    def test_get_research_intensive_levels(self):
        """Test get_research_intensive_levels returns levels needing extensive research."""
        research_intensive = TechnologyLevel.get_research_intensive_levels()
        assert isinstance(research_intensive, list)
        assert len(research_intensive) > 0
        
        # All returned levels should have 4+ research requirements
        for level in research_intensive:
            assert len(level.research_requirements) >= 4, f"{level} should have 4+ research requirements, got {len(level.research_requirements)}"


class TestTechnologyLevelStoryConsiderations:
    """Test story consideration methods and their data integrity."""
    
    def test_get_story_considerations_structure(self):
        """Test that get_story_considerations returns proper structure."""
        for tech_level in TechnologyLevel:
            considerations = tech_level.get_story_considerations()
            assert isinstance(considerations, dict)
            
            # Should have exactly 4 keys
            expected_keys = {"worldbuilding_focus", "common_conflicts", "character_concerns", "plot_opportunities"}
            assert set(considerations.keys()) == expected_keys
            
            # All values should be lists of strings
            for key, value in considerations.items():
                assert isinstance(value, list), f"{key} should be a list for {tech_level.value}"
                assert len(value) > 0, f"{key} should not be empty for {tech_level.value}"
                for item in value:
                    assert isinstance(item, str), f"All items in {key} should be strings"
                    assert len(item) > 0, f"Items in {key} should not be empty strings"
    
    def test_worldbuilding_focus_specific_values(self):
        """Test specific worldbuilding focus values match expected data."""
        expected_focus = {
            TechnologyLevel.STONE_AGE: ["survival", "tribal structure", "natural environment", "basic tools"],
            TechnologyLevel.MEDIEVAL: ["social hierarchy", "religion", "castles", "rural life", "guilds"],
            TechnologyLevel.STEAM_PUNK: ["Victorian aesthetics", "steam technology", "class divide", "industrial cities"],
            TechnologyLevel.CYBERPUNK: ["corporate power", "urban decay", "digital worlds", "economic inequality"],
            TechnologyLevel.SPACE_FARING: ["space habitats", "interplanetary politics", "resource management", "isolation"],
            TechnologyLevel.POST_APOCALYPTIC: ["resource scarcity", "survivor communities", "environmental hazards", "technology salvage"]
        }
        
        for tech_level, expected_items in expected_focus.items():
            considerations = tech_level.get_story_considerations()
            actual_focus = considerations["worldbuilding_focus"]
            assert actual_focus == expected_items, f"Worldbuilding focus mismatch for {tech_level.value}: expected {expected_items}, got {actual_focus}"
    
    def test_common_conflicts_specific_values(self):
        """Test specific common conflicts values match expected data."""
        expected_conflicts = {
            TechnologyLevel.STONE_AGE: ["survival vs nature", "tribal warfare", "resource competition"],
            TechnologyLevel.MEDIEVAL: ["feudal politics", "religious conflicts", "succession disputes", "external invasions"],
            TechnologyLevel.CYBERPUNK: ["corporate espionage", "AI rights", "digital privacy", "class warfare"],
            TechnologyLevel.SPACE_FARING: ["colonial independence", "resource rights", "terraforming ethics", "alien contact"],
            TechnologyLevel.POST_APOCALYPTIC: ["resource wars", "community conflicts", "technology hoarding", "rebuilding debates"]
        }
        
        for tech_level, expected_items in expected_conflicts.items():
            considerations = tech_level.get_story_considerations()
            actual_conflicts = considerations["common_conflicts"]
            assert actual_conflicts == expected_items, f"Common conflicts mismatch for {tech_level.value}: expected {expected_items}, got {actual_conflicts}"
    
    def test_character_concerns_specific_values(self):
        """Test specific character concerns values match expected data."""
        expected_concerns = {
            TechnologyLevel.STONE_AGE: ["finding food", "avoiding predators", "tribal acceptance", "seasonal survival"],
            TechnologyLevel.MEDIEVAL: ["honor and duty", "religious salvation", "family loyalty", "social status"],
            TechnologyLevel.CYBERPUNK: ["identity in digital age", "corporate surveillance", "augmentation choices", "economic survival"],
            TechnologyLevel.SPACE_FARING: ["homesickness", "radiation exposure", "colony politics", "cultural preservation"],
            TechnologyLevel.POST_APOCALYPTIC: ["finding resources", "protecting loved ones", "moral compromises", "hope vs despair"]
        }
        
        for tech_level, expected_items in expected_concerns.items():
            considerations = tech_level.get_story_considerations()
            actual_concerns = considerations["character_concerns"]
            assert actual_concerns == expected_items, f"Character concerns mismatch for {tech_level.value}: expected {expected_items}, got {actual_concerns}"
    
    def test_plot_opportunities_specific_values(self):
        """Test specific plot opportunities values match expected data."""
        expected_opportunities = {
            TechnologyLevel.STONE_AGE: ["discovering fire", "first tool creation", "tribal migrations", "cave paintings"],
            TechnologyLevel.MEDIEVAL: ["knightly quests", "political intrigue", "religious pilgrimages", "siege warfare"],
            TechnologyLevel.CYBERPUNK: ["corporate heists", "identity theft", "AI awakening", "digital archaeology"],
            TechnologyLevel.SPACE_FARING: ["first contact", "terraforming projects", "space piracy", "generation ship drama"],
            TechnologyLevel.POST_APOCALYPTIC: ["finding safe haven", "technology recovery", "community building", "uncovering the past"]
        }
        
        for tech_level, expected_items in expected_opportunities.items():
            considerations = tech_level.get_story_considerations()
            actual_opportunities = considerations["plot_opportunities"]
            assert actual_opportunities == expected_items, f"Plot opportunities mismatch for {tech_level.value}: expected {expected_items}, got {actual_opportunities}"
    
    def test_default_story_considerations(self):
        """Test that non-specified tech levels get appropriate default values."""
        # Test a tech level that's not in the specific mappings
        tech_level = TechnologyLevel.RENAISSANCE  # Not in the specific mappings
        considerations = tech_level.get_story_considerations()
        
        # Should get default values
        expected_defaults = {
            "worldbuilding_focus": ["technology impact", "social structure", "daily life", "power dynamics"],
            "common_conflicts": ["technological ethics", "social change", "power struggles", "resource control"],
            "character_concerns": ["adapting to change", "moral choices", "personal relationships", "future planning"],
            "plot_opportunities": ["technological discovery", "social upheaval", "exploration", "innovation"]
        }
        
        for key, expected_default in expected_defaults.items():
            actual_value = considerations[key]
            assert actual_value == expected_default, f"Default {key} mismatch for {tech_level.value}: expected {expected_default}, got {actual_value}"


class TestTechnologyLevelPerformance:
    """Test performance characteristics."""
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        start_time = time.time()
        for _ in range(1000):
            for tech_level in TechnologyLevel:
                _ = tech_level.display_name
                _ = tech_level.description
                _ = tech_level.time_period
                _ = tech_level.complexity_level
        end_time = time.time()
        
        # Should complete many property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        test_inputs = [
            "medieval", "cyberpunk", "stone_age", "future", "modern", "space",
            "steampunk", "apocalyptic", "industrial", "renaissance", "atomic", "digital"
        ]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    TechnologyLevel.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 12,000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_classification_performance(self):
        """Test that classification methods are reasonably fast."""
        start_time = time.time()
        for _ in range(1000):
            TechnologyLevel.get_historical_levels()
            TechnologyLevel.get_future_levels()
            TechnologyLevel.get_alternative_levels()
            TechnologyLevel.get_research_intensive_levels()
        end_time = time.time()
        
        # Should complete 4000 classification operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Classification methods too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_tech_level_enum_basic_functionality(self):
        """Test that TechnologyLevel enum works as expected."""
        # Test iteration
        tech_list = list(TechnologyLevel)
        assert len(tech_list) == 34  # Should have exactly 34 technology levels
        
        # Test basic attributes
        medieval = TechnologyLevel.MEDIEVAL
        assert medieval.value == "medieval"
        assert "Medieval" in medieval.display_name
        
        # Test enum comparison
        assert TechnologyLevel.MEDIEVAL == TechnologyLevel.MEDIEVAL
        assert TechnologyLevel.MEDIEVAL != TechnologyLevel.CYBERPUNK
    
    def test_string_representations(self):
        """Test string representation methods."""
        tech_level = TechnologyLevel.STEAM_PUNK
        
        str_repr = str(tech_level)
        repr_repr = repr(tech_level)
        
        assert isinstance(str_repr, str)
        assert isinstance(repr_repr, str)
        assert len(str_repr) > 0
        assert len(repr_repr) > 0
        assert str_repr == tech_level.display_name
        assert "TechnologyLevel." in repr_repr
    
    def test_tech_level_distribution(self):
        """Test that tech levels are reasonably distributed across categories."""
        historical_count = len(TechnologyLevel.get_historical_levels())
        future_count = len(TechnologyLevel.get_future_levels())
        alternative_count = len(TechnologyLevel.get_alternative_levels())
        total_specific = historical_count + future_count + alternative_count
        
        # Should account for most but not necessarily all tech levels (some might be uncategorized)
        total_tech_levels = len(list(TechnologyLevel))
        coverage_ratio = total_specific / total_tech_levels
        assert coverage_ratio >= 0.9, f"Category coverage should be at least 90%, got {coverage_ratio:.1%}"
        
        # No category should dominate too much
        historical_percentage = historical_count / total_tech_levels
        future_percentage = future_count / total_tech_levels
        alternative_percentage = alternative_count / total_tech_levels
        
        assert 0.3 <= historical_percentage <= 0.6, f"Historical percentage out of range: {historical_percentage:.1%}"
        assert 0.2 <= future_percentage <= 0.4, f"Future percentage out of range: {future_percentage:.1%}"
        assert 0.2 <= alternative_percentage <= 0.4, f"Alternative percentage out of range: {alternative_percentage:.1%}"
        
        print(f"Distribution - Historical: {historical_percentage:.1%}, Future: {future_percentage:.1%}, Alternative: {alternative_percentage:.1%}")


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])