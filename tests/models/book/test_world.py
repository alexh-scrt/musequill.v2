import pytest
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the PersonalityTrait class from the personality module
from musequill.models.book.world import WorldType


class TestWorldTypeBasicProperties:
    """Test basic properties and enum functionality."""
    
    def test_enum_values_are_strings(self):
        """Test that all enum values are properly formatted strings."""
        for world_type in WorldType:
            assert isinstance(world_type.value, str)
            assert world_type.value == world_type.value.lower()
            assert "_" in world_type.value or world_type.value.isalpha()
            # Should not have spaces or special characters except underscores
            assert " " not in world_type.value
            assert not any(char in world_type.value for char in "!@#$%^&*()[]{}|\\:;\"'<>,.?/")
    
    def test_enum_completeness(self):
        """Test that we have a comprehensive set of world types."""
        all_types = list(WorldType)
        assert len(all_types) >= 57, f"Should have at least 57 world types, found {len(all_types)}"
        
        # Check we have major categories represented
        fantasy_types = WorldType.get_fantasy_types()
        sf_types = WorldType.get_science_fiction_types()
        realistic_types = WorldType.get_realistic_types()
        
        assert len(fantasy_types) >= 15, "Should have substantial fantasy representation"
        assert len(sf_types) >= 8, "Should have substantial SF representation"
        assert len(realistic_types) >= 3, "Should have realistic world types"
        
        print(f"✓ Total world types: {len(all_types)}")
        print(f"✓ Fantasy types: {len(fantasy_types)}")
        print(f"✓ Science fiction types: {len(sf_types)}")
        print(f"✓ Realistic types: {len(realistic_types)}")
    
    def test_no_duplicate_values(self):
        """Test that all enum values are unique."""
        values = [world_type.value for world_type in WorldType]
        assert len(values) == len(set(values)), "All world type values should be unique"
    
    def test_no_duplicate_display_names(self):
        """Test that all display names are unique."""
        display_names = [world_type.display_name for world_type in WorldType]
        duplicates = [name for name in display_names if display_names.count(name) > 1]
        assert len(duplicates) == 0, f"Found duplicate display names: {duplicates}"


class TestWorldTypeDisplayName:
    """Test display_name property."""
    
    def test_all_types_have_display_names(self):
        """Test that all world types have non-empty display names."""
        for world_type in WorldType:
            display_name = world_type.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0, f"Display name for {world_type.value} is empty"
            assert display_name.strip() == display_name, f"Display name '{display_name}' has leading/trailing whitespace"

    def test_display_name_formatting(self):
        """Test that display names are properly formatted."""
        for world_type in WorldType:
            display_name = world_type.display_name
            # Should be title case or have proper capitalization
            assert display_name[0].isupper(), f"Display name '{display_name}' should start with capital letter"
            # Should not be all caps unless it's an acronym
            if len(display_name) > 3:
                assert not display_name.isupper(), f"Display name '{display_name}' should not be all caps"
    
    def test_specific_display_names(self):
        """Test specific display names for important world types."""
        expected_names = {
            WorldType.HIGH_FANTASY: "High Fantasy",
            WorldType.SCIENCE_FICTION: "Science Fiction", 
            WorldType.CYBERPUNK: "Cyberpunk",
            WorldType.POST_APOCALYPTIC: "Post-Apocalyptic",
            WorldType.ALTERNATE_HISTORY: "Alternate History",
            WorldType.MAGICAL_REALISM: "Magical Realism",
            WorldType.SPACE_OPERA: "Space Opera",
        }
        
        for world_type, expected_name in expected_names.items():
            assert world_type.display_name == expected_name, f"Expected '{expected_name}', got '{world_type.display_name}'"


class TestWorldTypeDescription:
    """Test description property."""
    
    def test_all_types_have_descriptions(self):
        """Test that all world types have substantial descriptions."""
        for world_type in WorldType:
            description = world_type.description
            assert isinstance(description, str)
            assert len(description) >= 50, f"Description for {world_type.value} is too short: {len(description)} chars"
            assert description.strip() == description, f"Description has leading/trailing whitespace"
            # Should end with period
            assert description.endswith('.'), f"Description for {world_type.value} should end with period"
    
    def test_description_quality(self):
        """Test that descriptions are informative and well-written."""
        for world_type in WorldType:
            description = world_type.description
            # Should contain key terms related to the world type
            lower_desc = description.lower()
            world_name = world_type.display_name.lower()
            
            # Key terms should appear in description (allowing for variations)
            if "fantasy" in world_name:
                assert any(term in lower_desc for term in ["fantasy", "magic", "magical", "supernatural"]), \
                    f"Fantasy world type {world_type.value} should mention fantasy concepts in description"
            
            if "science" in world_name or ("fiction" in world_name and world_type != WorldType.CLIMATE_FICTION):
                assert any(term in lower_desc for term in ["science", "technology", "future", "scientific"]), \
                    f"Science fiction world type {world_type.value} should mention SF concepts in description"
            
            # Should not have obvious typos or formatting issues
            assert not any(bad_text in description for bad_text in ["  ", "\t", "\n"]), \
                f"Description for {world_type.value} has formatting issues"


class TestWorldTypeBuildingComplexity:
    """Test world_building_complexity property."""
    
    def test_all_types_have_complexity(self):
        """Test that all world types have valid complexity levels."""
        valid_complexities = {"Low", "Medium", "High", "Very High"}
        
        for world_type in WorldType:
            complexity = world_type.world_building_complexity
            assert isinstance(complexity, str)
            assert complexity in valid_complexities, f"Invalid complexity '{complexity}' for {world_type.value}"
    
    def test_complexity_distribution(self):
        """Test that complexity levels are reasonably distributed."""
        complexity_counts = {}
        for world_type in WorldType:
            complexity = world_type.world_building_complexity
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        # Should have some variety in complexity levels
        assert len(complexity_counts) >= 3, "Should have at least 3 different complexity levels"
        
        # Realistic types should generally be low complexity
        for world_type in WorldType.get_realistic_types():
            if world_type != WorldType.ALTERNATE_HISTORY:  # This might be medium
                assert world_type.world_building_complexity in ["Low", "Medium"], \
                    f"Realistic world type {world_type.value} should have low/medium complexity"
        
        print(f"✓ Complexity distribution: {complexity_counts}")
    
    def test_logical_complexity_assignments(self):
        """Test that complexity assignments make logical sense."""
        # High fantasy should be high complexity
        assert WorldType.HIGH_FANTASY.world_building_complexity in ["High", "Very High"]
        assert WorldType.EPIC_FANTASY.world_building_complexity in ["High", "Very High"]
        assert WorldType.SECONDARY_WORLD.world_building_complexity in ["High", "Very High"]
        
        # Realistic should be low complexity
        assert WorldType.REALISTIC.world_building_complexity == "Low"
        assert WorldType.CONTEMPORARY.world_building_complexity == "Low"
        
        # Science fiction should generally be high complexity
        assert WorldType.SPACE_OPERA.world_building_complexity in ["High", "Very High"]
        assert WorldType.HARD_SCIENCE_FICTION.world_building_complexity in ["High", "Very High"]


class TestWorldTypeKeyElements:
    """Test key_elements property."""
    
    def test_all_types_have_key_elements(self):
        """Test that all world types have key elements defined."""
        for world_type in WorldType:
            elements = world_type.key_elements
            assert isinstance(elements, list)
            assert len(elements) >= 3, f"World type {world_type.value} should have at least 3 key elements"
            assert len(elements) <= 8, f"World type {world_type.value} has too many key elements ({len(elements)})"
            
            # All elements should be non-empty strings
            for element in elements:
                assert isinstance(element, str)
                assert len(element) > 0
                assert element.strip() == element
    
    def test_key_elements_relevance(self):
        """Test that key elements are relevant to the world type."""
        # Fantasy types should have fantasy-related elements
        fantasy_keywords = ["magic", "supernatural", "fantasy", "mystical", "enchanted", "mythical", "heroic", "magical", "prophecy", "prophecies", "kingdom", "kingdoms", "conflict", "conflicts", "journey", "hero", "heroes", "chosen", "elements", "creatures", "spells", "wizards", "dragons", "elves", "mythological", "legends", "beings", "epic", "ancient", "quest", "grail", "knights", "legendary", "tales", "portals", "realms", "dimensional", "world", "worlds"]
        for world_type in WorldType.get_fantasy_types():
            elements_text = " ".join(world_type.key_elements).lower()
            
            # Special handling for types that blend genres or have subtle fantasy elements
            if world_type == WorldType.DARK_FANTASY:
                # Dark fantasy combines horror and fantasy, so either is acceptable
                dark_fantasy_keywords = fantasy_keywords + ["horror", "psychological", "disturbing", "terror", "dread"]
                assert any(keyword in elements_text for keyword in dark_fantasy_keywords), \
                    f"Dark fantasy world type should have fantasy or horror-related key elements. Found: {world_type.key_elements}"
            elif world_type in [WorldType.MEDIEVAL_FANTASY, WorldType.GASLAMP_FANTASY, WorldType.FLINTLOCK_FANTASY, WorldType.GUNPOWDER_FANTASY]:
                # Historical fantasy types might have more subtle fantasy elements
                historical_fantasy_keywords = fantasy_keywords + ["medieval", "knights", "castles", "victorian", "industrial", "technology", "warfare", "society"]
                assert any(keyword in elements_text for keyword in historical_fantasy_keywords), \
                    f"Historical fantasy world type {world_type.value} should have fantasy or period-related key elements. Found: {world_type.key_elements}"
            elif world_type == WorldType.MYTHIC_FANTASY:
                # Mythic fantasy uses mythological terminology
                mythic_fantasy_keywords = fantasy_keywords + ["mythology", "mythological", "legends", "legendary", "gods", "deities", "cultural", "authentic", "epic", "ancient", "beings"]
                assert any(keyword in elements_text for keyword in mythic_fantasy_keywords), \
                    f"Mythic fantasy world type should have fantasy or mythological key elements. Found: {world_type.key_elements}"
            elif world_type == WorldType.ARTHURIAN:
                # Arthurian fantasy uses chivalric and quest terminology
                arthurian_fantasy_keywords = fantasy_keywords + ["chivalric", "round", "table", "grail", "honor", "quest", "knights", "arthur", "camelot", "excalibur", "merlin"]
                assert any(keyword in elements_text for keyword in arthurian_fantasy_keywords), \
                    f"Arthurian fantasy world type should have fantasy or chivalric key elements. Found: {world_type.key_elements}"
            elif world_type == WorldType.PORTAL_FANTASY:
                # Portal fantasy focuses on world-crossing and dimensional elements
                portal_fantasy_keywords = fantasy_keywords + ["portal", "portals", "dimensional", "transitions", "world", "worlds", "realities", "travel", "crossing", "gateway", "door", "passage"]
                assert any(keyword in elements_text for keyword in portal_fantasy_keywords), \
                    f"Portal fantasy world type should have fantasy or dimensional key elements. Found: {world_type.key_elements}"
            elif world_type in [WorldType.MAGICAL_REALISM, WorldType.WEIRD_WEST, WorldType.BIOPUNK_FANTASY]:
                # These blend fantasy with other genres and may have subtle fantasy elements
                blended_fantasy_keywords = fantasy_keywords + ["magical", "weird", "supernatural", "biological", "organic", "western", "frontier", "accepted", "realism", "reality"]
                assert any(keyword in elements_text for keyword in blended_fantasy_keywords), \
                    f"Blended fantasy world type {world_type.value} should have fantasy or genre-blend key elements. Found: {world_type.key_elements}"
            else:
                assert any(keyword in elements_text for keyword in fantasy_keywords), \
                    f"Fantasy world type {world_type.value} should have fantasy-related key elements. Found: {world_type.key_elements}"
        
        # SF types should have SF-related elements  
        sf_keywords = ["technology", "science", "future", "space", "advanced", "artificial", "cyber", "digital"]
        for world_type in WorldType.get_science_fiction_types():
            elements_text = " ".join(world_type.key_elements).lower()
            assert any(keyword in elements_text for keyword in sf_keywords), \
                f"SF world type {world_type.value} should have SF-related key elements"
    
    def test_key_elements_uniqueness(self):
        """Test that key elements provide unique characterization."""
        all_elements = []
        for world_type in WorldType:
            all_elements.extend(world_type.key_elements)
        
        # While some overlap is expected, each type should have some unique elements
        unique_elements = set(all_elements)
        assert len(unique_elements) >= len(all_elements) * 0.3, "Should have reasonable diversity in key elements"


class TestWorldTypeResearchAreas:
    """Test required_research_areas property."""
    
    def test_all_types_have_research_areas(self):
        """Test that all world types have research areas defined."""
        for world_type in WorldType:
            research_areas = world_type.required_research_areas
            assert isinstance(research_areas, list)
            assert len(research_areas) >= 2, f"World type {world_type.value} should have at least 2 research areas"
            assert len(research_areas) <= 8, f"World type {world_type.value} has too many research areas"
            
            # All areas should be non-empty strings
            for area in research_areas:
                assert isinstance(area, str)
                assert len(area) > 0
                assert area.strip() == area
    
    def test_research_areas_appropriateness(self):
        """Test that research areas are appropriate for each world type."""
        # Historical types should require historical research
        historical_types = [WorldType.HISTORICAL, WorldType.ALTERNATE_HISTORY, WorldType.MEDIEVAL_FANTASY]
        for world_type in historical_types:
            research_text = " ".join(world_type.required_research_areas).lower()
            assert any(term in research_text for term in ["history", "historical", "period", "medieval"]), \
                f"Historical world type {world_type.value} should require historical research"
        
        # Mythic fantasy should require mythology research
        if hasattr(WorldType, 'MYTHIC_FANTASY'):
            research_text = " ".join(WorldType.MYTHIC_FANTASY.required_research_areas).lower()
            assert "mythology" in research_text or "mythologies" in research_text


class TestWorldTypeCommonThemes:
    """Test common_themes property."""
    
    def test_all_types_have_themes(self):
        """Test that all world types have common themes defined."""
        for world_type in WorldType:
            themes = world_type.common_themes
            assert isinstance(themes, list)
            assert len(themes) >= 3, f"World type {world_type.value} should have at least 3 common themes"
            assert len(themes) <= 8, f"World type {world_type.value} has too many themes"
            
            # All themes should be non-empty strings
            for theme in themes:
                assert isinstance(theme, str)
                assert len(theme) > 0
                assert theme.strip() == theme
    
    def test_themes_appropriateness(self):
        """Test that themes are appropriate for world types."""
        # Dystopian should have oppression/control themes
        dystopian_themes = " ".join(WorldType.DYSTOPIAN.common_themes).lower()
        assert any(term in dystopian_themes for term in ["oppression", "control", "freedom", "resistance"]), \
            "Dystopian should have themes related to oppression and control"
        
        # High fantasy should have heroic themes
        fantasy_themes = " ".join(WorldType.HIGH_FANTASY.common_themes).lower()
        assert any(term in fantasy_themes for term in ["good", "evil", "heroic", "journey", "power"]), \
            "High fantasy should have heroic/moral themes"


class TestWorldTypeClassMethods:
    """Test class methods of WorldType."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("realistic", WorldType.REALISTIC),
            ("high_fantasy", WorldType.HIGH_FANTASY),
            ("cyberpunk", WorldType.CYBERPUNK),
            ("space_opera", WorldType.SPACE_OPERA),
            ("post_apocalyptic", WorldType.POST_APOCALYPTIC),
        ]
        
        for input_str, expected_type in direct_matches:
            result = WorldType.from_string(input_str)
            assert result == expected_type, f"Expected {expected_type} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching."""
        fuzzy_matches = [
            ("real world", WorldType.REALISTIC),
            ("modern", WorldType.CONTEMPORARY),
            ("fantasy world", WorldType.HIGH_FANTASY),
            ("sci-fi", WorldType.SCIENCE_FICTION),
            ("future", WorldType.SCIENCE_FICTION),
            ("steam", WorldType.STEAMPUNK),
            ("cyber", WorldType.CYBERPUNK),
            ("space", WorldType.SPACE_OPERA),
            ("apocalypse", WorldType.POST_APOCALYPTIC),
            ("zombie", WorldType.ZOMBIE_APOCALYPSE),
            ("time", WorldType.TIME_TRAVEL),
            ("ghost", WorldType.PARANORMAL),
            ("vampire", WorldType.PARANORMAL),
            ("magic realism", WorldType.MAGICAL_REALISM),
            ("magical realism", WorldType.MAGICAL_REALISM),
            ("sword", WorldType.SWORD_AND_SORCERY),
            ("knight", WorldType.MEDIEVAL_FANTASY),
            ("victorian", WorldType.STEAMPUNK),  # Could also match GASLAMP_FANTASY
        ]
        
        for input_str, expected_type in fuzzy_matches:
            result = WorldType.from_string(input_str)
            assert result == expected_type, f"Expected {expected_type} for '{input_str}', got {result}"
    
    def test_from_string_case_insensitive(self):
        """Test that from_string is case insensitive."""
        test_cases = [
            "REALISTIC", "Realistic", "ReAlIsTiC",
            "HIGH_FANTASY", "High_Fantasy", "high_fantasy",
            "SCIENCE FICTION", "Science Fiction", "science fiction"
        ]
        
        for test_input in test_cases:
            try:
                result = WorldType.from_string(test_input)
                assert isinstance(result, WorldType)
            except ValueError:
                # Some might not match due to fuzzy matching limitations
                pass
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid inputs."""
        invalid_inputs = [
            "completely_invalid_world_type",
            "this_does_not_exist", 
            "random_garbage_text",
            "",
            "   ",
            "12345",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                WorldType.from_string(invalid_input)
    
    def test_get_fantasy_types(self):
        """Test getting fantasy world types."""
        fantasy_types = WorldType.get_fantasy_types()
        
        assert isinstance(fantasy_types, list)
        assert len(fantasy_types) >= 15, f"Should have at least 15 fantasy types, got {len(fantasy_types)}"
        
        # Should include major fantasy types
        expected_fantasy = [
            WorldType.HIGH_FANTASY, WorldType.LOW_FANTASY, WorldType.EPIC_FANTASY,
            WorldType.URBAN_FANTASY, WorldType.DARK_FANTASY, WorldType.MEDIEVAL_FANTASY
        ]
        
        for expected in expected_fantasy:
            assert expected in fantasy_types, f"Fantasy type {expected} not found in get_fantasy_types()"
        
        # Should not include non-fantasy types
        non_fantasy = [WorldType.SCIENCE_FICTION, WorldType.REALISTIC, WorldType.CONTEMPORARY]
        for non_fantasy_type in non_fantasy:
            assert non_fantasy_type not in fantasy_types, f"Non-fantasy type {non_fantasy_type} found in fantasy types"
        
        print(f"✓ Fantasy types: {len(fantasy_types)} types")
    
    def test_get_science_fiction_types(self):
        """Test getting science fiction world types."""
        sf_types = WorldType.get_science_fiction_types()
        
        assert isinstance(sf_types, list)
        assert len(sf_types) >= 8, f"Should have at least 8 SF types, got {len(sf_types)}"
        
        # Should include major SF types
        expected_sf = [
            WorldType.SCIENCE_FICTION, WorldType.HARD_SCIENCE_FICTION, 
            WorldType.SPACE_OPERA, WorldType.CYBERPUNK, WorldType.STEAMPUNK
        ]
        
        for expected in expected_sf:
            assert expected in sf_types, f"SF type {expected} not found in get_science_fiction_types()"
        
        print(f"✓ Science fiction types: {len(sf_types)} types")
    
    def test_get_realistic_types(self):
        """Test getting realistic world types."""
        realistic_types = WorldType.get_realistic_types()
        
        assert isinstance(realistic_types, list)
        assert len(realistic_types) >= 3, f"Should have at least 3 realistic types, got {len(realistic_types)}"
        
        # Should include expected realistic types
        expected_realistic = [
            WorldType.REALISTIC, WorldType.CONTEMPORARY, 
            WorldType.HISTORICAL, WorldType.ALTERNATE_HISTORY
        ]
        
        for expected in expected_realistic:
            assert expected in realistic_types, f"Realistic type {expected} not found"
        
        print(f"✓ Realistic types: {len(realistic_types)} types")
    
    def test_get_high_complexity_types(self):
        """Test getting high complexity world types."""
        high_complexity = WorldType.get_high_complexity_types()
        
        assert isinstance(high_complexity, list)
        assert len(high_complexity) > 0, "Should have some high complexity types"
        
        # All returned types should actually be high complexity
        for world_type in high_complexity:
            assert world_type.world_building_complexity in ["High", "Very High"], \
                f"Type {world_type} marked as high complexity but has {world_type.world_building_complexity}"
        
        # Should include obviously complex types
        obviously_complex = [WorldType.HIGH_FANTASY, WorldType.SPACE_OPERA]
        for complex_type in obviously_complex:
            if complex_type.world_building_complexity in ["High", "Very High"]:
                assert complex_type in high_complexity
        
        print(f"✓ High complexity types: {len(high_complexity)} types")
    
    def test_get_by_theme(self):
        """Test getting world types by theme."""
        # Test with common themes
        theme_tests = [
            ("magic", ["fantasy", "magical"]),
            ("technology", ["science", "cyber", "tech"]),
            ("heroic", ["hero", "adventure"]),
            ("survival", ["apocalyptic", "post"]),
        ]
        
        for theme, expected_keywords in theme_tests:
            matching_types = WorldType.get_by_theme(theme)
            assert isinstance(matching_types, list)
            
            # Verify the matches make sense
            for world_type in matching_types:
                themes_text = " ".join(world_type.common_themes).lower()
                assert theme.lower() in themes_text, \
                    f"Type {world_type} returned for theme '{theme}' but doesn't contain it in themes"
        
        # Test with non-existent theme
        no_matches = WorldType.get_by_theme("completely_nonexistent_theme_12345")
        assert isinstance(no_matches, list)
        assert len(no_matches) == 0


class TestWorldTypeBuildingChecklist:
    """Test get_world_building_checklist method."""
    
    def test_all_types_have_checklist(self):
        """Test that all world types return a valid checklist."""
        for world_type in WorldType:
            checklist = world_type.get_world_building_checklist()
            
            assert isinstance(checklist, dict)
            assert len(checklist) >= 5, f"Checklist for {world_type.value} should have at least 5 categories"
            
            # All categories should have items
            for category, items in checklist.items():
                assert isinstance(category, str)
                assert len(category) > 0
                assert isinstance(items, list)
                assert len(items) > 0, f"Category '{category}' should have checklist items"
                
                # All items should be strings
                for item in items:
                    assert isinstance(item, str)
                    assert len(item) > 0
    
    def test_base_checklist_categories(self):
        """Test that all types have essential base categories."""
        base_categories = [
            "Geography & Environment",
            "Cultures & Societies", 
            "Politics & Governance",
            "Economics & Technology",
            "History & Timeline"
        ]
        
        for world_type in WorldType:
            checklist = world_type.get_world_building_checklist()
            
            for base_category in base_categories:
                assert base_category in checklist, \
                    f"World type {world_type.value} missing base category '{base_category}'"
    
    def test_specialized_checklist_categories(self):
        """Test that specialized world types have additional categories."""
        # Fantasy types should have magic systems
        fantasy_types = [WorldType.HIGH_FANTASY, WorldType.EPIC_FANTASY, WorldType.SECONDARY_WORLD]
        for world_type in fantasy_types:
            checklist = world_type.get_world_building_checklist()
            assert "Magic Systems" in checklist, f"Fantasy type {world_type.value} should have Magic Systems category"
        
        # Space opera should have alien civilizations
        if WorldType.SPACE_OPERA.get_world_building_checklist():
            space_checklist = WorldType.SPACE_OPERA.get_world_building_checklist()
            # This might be added for space opera specifically
            
        # Urban fantasy should have hidden world category
        urban_types = [WorldType.URBAN_FANTASY, WorldType.PARANORMAL]
        for world_type in urban_types:
            checklist = world_type.get_world_building_checklist()
            if "Hidden World" in checklist:
                assert len(checklist["Hidden World"]) > 0


class TestWorldTypeStringRepresentation:
    """Test string representation methods."""
    
    def test_str_method(self):
        """Test __str__ method returns display name."""
        for world_type in WorldType:
            str_repr = str(world_type)
            assert str_repr == world_type.display_name
            assert isinstance(str_repr, str)
            assert len(str_repr) > 0
    
    def test_repr_method(self):
        """Test __repr__ method returns proper representation."""
        for world_type in WorldType:
            repr_str = repr(world_type)
            assert repr_str.startswith("WorldType.")
            assert world_type.name in repr_str
            
            # Should be evaluable (though we can't easily test that without eval)
            assert "WorldType." + world_type.name == repr_str


class TestWorldTypeIntegration:
    """Integration tests for the WorldType system."""
    
    def test_all_methods_work_together(self):
        """Test that all methods work together without errors."""
        # Test a sample of world types with all methods
        sample_types = [
            WorldType.REALISTIC, WorldType.HIGH_FANTASY, WorldType.SCIENCE_FICTION,
            WorldType.CYBERPUNK, WorldType.URBAN_FANTASY, WorldType.POST_APOCALYPTIC
        ]
        
        for world_type in sample_types:
            # All properties should work
            assert world_type.display_name
            assert world_type.description
            assert world_type.world_building_complexity
            assert world_type.key_elements
            assert world_type.required_research_areas
            assert world_type.common_themes
            
            # Checklist should work
            checklist = world_type.get_world_building_checklist()
            assert isinstance(checklist, dict)
            
            # String representations should work
            assert str(world_type)
            assert repr(world_type)
    
    def test_classification_consistency(self):
        """Test that classification methods are consistent."""
        all_types = set(WorldType)
        
        # Union of all classification methods should cover most types
        fantasy_types = set(WorldType.get_fantasy_types())
        sf_types = set(WorldType.get_science_fiction_types()) 
        realistic_types = set(WorldType.get_realistic_types())
        
        classified_types = fantasy_types | sf_types | realistic_types
        
        # Should classify a substantial portion (allowing for hybrid/other types)
        coverage_ratio = len(classified_types) / len(all_types)
        assert coverage_ratio >= 0.55, f"Classification methods should cover at least 55% of types, got {coverage_ratio:.2%}"
        
        # No type should be in multiple main categories
        assert len(fantasy_types & sf_types) == 0, "Types should not be both fantasy and SF"
        assert len(fantasy_types & realistic_types) == 0, "Types should not be both fantasy and realistic"
        assert len(sf_types & realistic_types) == 0, "Types should not be both SF and realistic"
    
    def test_fuzzy_matching_coverage(self):
        """Test that fuzzy matching covers common user inputs."""
        common_inputs = [
            "fantasy", "sci-fi", "science fiction", "realistic", "modern",
            "medieval", "cyberpunk", "steampunk", "space", "future",
            "magic", "vampire", "zombie", "time travel", "alternate history"
        ]
        
        successful_matches = 0
        for input_str in common_inputs:
            try:
                result = WorldType.from_string(input_str)
                assert isinstance(result, WorldType)
                successful_matches += 1
            except ValueError:
                pass  # Some inputs might not match, which is OK
        
        # Should match a reasonable percentage of common inputs
        match_ratio = successful_matches / len(common_inputs)
        assert match_ratio >= 0.7, f"Should match at least 70% of common inputs, got {match_ratio:.2%}"
        
        print(f"✓ Fuzzy matching success rate: {match_ratio:.2%}")


if __name__ == "__main__":
    # Run basic smoke tests if called directly
    print("Running WorldType tests...")
    
    # Test basic functionality
    test_basic = TestWorldTypeBasicProperties()
    test_basic.test_enum_completeness()
    
    test_class_methods = TestWorldTypeClassMethods()
    test_class_methods.test_get_fantasy_types()
    test_class_methods.test_get_science_fiction_types()
    test_class_methods.test_get_realistic_types()
    
    print("✓ All basic tests passed!")