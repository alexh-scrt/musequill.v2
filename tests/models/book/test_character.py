"""
Comprehensive tests for musequill.models.book.character module.

Test file: tests/models/book/test_character.py
Module under test: musequill/models/book/character.py

Run from project root: pytest tests/models/book/test_character.py -v
"""

import sys
from pathlib import Path
import pytest
from typing import List, Set, Tuple

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the classes from the character module
from musequill.models.book.character import CharacterRole, CharacterArchetype


class TestCharacterRole:
    """Test the CharacterRole enum comprehensively."""
    
    def test_all_role_values_are_strings(self):
        """Ensure all character role enum values are properly formatted strings."""
        for role in CharacterRole:
            assert isinstance(role.value, str)
            assert role.value.islower()
            assert " " not in role.value  # Should use underscores
            assert len(role.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in role.value)
    
    def test_all_roles_have_unique_values(self):
        """Ensure no duplicate values in CharacterRole enum."""
        values = [role.value for role in CharacterRole]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate role values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have exactly 14 character roles
        assert len(values) == 14, f"Expected exactly 14 character roles, got {len(values)}"
        print(f"✓ Found {len(values)} unique character roles")
    
    def test_display_name_property(self):
        """Test that display_name properly formats role names."""
        for role in CharacterRole:
            display_name = role.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (CharacterRole.PROTAGONIST, "Protagonist"),
            (CharacterRole.ANTAGONIST, "Antagonist"),
            (CharacterRole.DEUTERAGONIST, "Deuteragonist"),
            (CharacterRole.LOVE_INTEREST, "Love Interest"),
            (CharacterRole.MENTOR, "Mentor"),
            (CharacterRole.ALLY, "Ally"),
            (CharacterRole.THRESHOLD_GUARDIAN, "Threshold Guardian"),
            (CharacterRole.HERALD, "Herald"),
            (CharacterRole.TRICKSTER, "Trickster"),
            (CharacterRole.SHAPESHIFTER, "Shapeshifter"),
            (CharacterRole.SUPPORTING, "Supporting Character"),
            (CharacterRole.MINOR, "Minor Character"),
            (CharacterRole.NARRATOR, "Narrator"),
            (CharacterRole.FOIL, "Foil Character"),
        ]
        
        for role, expected_display in test_cases:
            assert role.display_name == expected_display, f"Expected '{expected_display}' for {role.value}, got '{role.display_name}'"
    
    def test_description_property(self):
        """Test that all character roles have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for role in CharacterRole:
            description = role.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {role.value}"
            
            # Check for minimum meaningful length
            if len(description) < 50:
                short_descriptions.append(f"{role.value}: '{description}'")
            
            # Should start with capital letter
            if description:
                assert description[0].isupper(), f"Description should start with capital for {role.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?')
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{role.value}: '{description}'")
        
        # Most descriptions should be substantial
        assert len(short_descriptions) <= 2, f"Too many short descriptions: {short_descriptions}"
        
        # Most descriptions should have proper punctuation
        assert len(descriptions_without_punctuation) <= 2, f"Descriptions without punctuation: {descriptions_without_punctuation}"
        
        total_roles = len(list(CharacterRole))
        quality_descriptions = total_roles - len(short_descriptions) - len(descriptions_without_punctuation)
        quality_percentage = quality_descriptions / total_roles
        assert quality_percentage >= 0.7, f"Too few quality descriptions: {quality_descriptions}/{total_roles} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_roles} ({quality_percentage:.1%})")
    
    def test_narrative_importance_property(self):
        """Test narrative_importance property categorization."""
        valid_importance_levels = {"primary", "major", "secondary", "tertiary", "structural"}
        
        level_counts = {"primary": 0, "major": 0, "secondary": 0, "tertiary": 0, "structural": 0}
        
        for role in CharacterRole:
            importance = role.narrative_importance
            assert importance in valid_importance_levels, f"{role.value} has invalid narrative importance: {importance}"
            assert isinstance(importance, str)
            level_counts[importance] += 1
        
        # Verify we have some distribution across importance levels
        assert level_counts["primary"] > 0, "No primary importance level roles found"
        assert level_counts["major"] > 0, "No major importance level roles found"
        assert level_counts["secondary"] > 0, "No secondary importance level roles found"
        print(f"Narrative importance distribution: {level_counts}")
        
        # Test specific known importance levels
        assert CharacterRole.PROTAGONIST.narrative_importance == "primary"
        assert CharacterRole.ANTAGONIST.narrative_importance == "primary"
        assert CharacterRole.MENTOR.narrative_importance == "major"
        assert CharacterRole.MINOR.narrative_importance == "tertiary"
    
    def test_typical_functions_property(self):
        """Test typical_functions property returns valid function lists."""
        for role in CharacterRole:
            functions = role.typical_functions
            assert isinstance(functions, list)
            assert len(functions) > 0, f"No functions found for {role.value}"
            
            # All functions should be strings
            for function in functions:
                assert isinstance(function, str)
                assert len(function) > 0
                # Should be lowercase descriptive phrases
                assert function.islower()
        
        # Test that primary roles have more functions
        primary_roles = [CharacterRole.PROTAGONIST, CharacterRole.ANTAGONIST]
        for role in primary_roles:
            functions = role.typical_functions
            assert len(functions) >= 3, f"Primary role {role.value} should have at least 3 functions, got {len(functions)}"


class TestCharacterRoleClassMethods:
    """Test class methods of CharacterRole."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("protagonist", CharacterRole.PROTAGONIST),
            ("antagonist", CharacterRole.ANTAGONIST),
            ("love_interest", CharacterRole.LOVE_INTEREST),
            ("mentor", CharacterRole.MENTOR),
        ]
        
        for input_str, expected_role in direct_matches:
            result = CharacterRole.from_string(input_str)
            assert result == expected_role, f"Expected {expected_role} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching."""
        fuzzy_matches = [
            # Primary roles
            ("main character", CharacterRole.PROTAGONIST),
            ("hero", CharacterRole.PROTAGONIST),
            ("heroine", CharacterRole.PROTAGONIST),
            ("primary character", CharacterRole.PROTAGONIST),
            ("villain", CharacterRole.ANTAGONIST),
            ("bad guy", CharacterRole.ANTAGONIST),
            ("enemy", CharacterRole.ANTAGONIST),
            ("opponent", CharacterRole.ANTAGONIST),
            
            # Secondary roles
            ("second main character", CharacterRole.DEUTERAGONIST),
            ("secondary protagonist", CharacterRole.DEUTERAGONIST),
            ("co-protagonist", CharacterRole.DEUTERAGONIST),
            ("romantic interest", CharacterRole.LOVE_INTEREST),
            ("love interest", CharacterRole.LOVE_INTEREST),
            ("romantic partner", CharacterRole.LOVE_INTEREST),
            ("teacher", CharacterRole.MENTOR),
            ("guide", CharacterRole.MENTOR),
            ("wise one", CharacterRole.MENTOR),
            ("friend", CharacterRole.ALLY),
            ("companion", CharacterRole.ALLY),
            ("supporter", CharacterRole.ALLY),
            ("helper", CharacterRole.ALLY),
            
            # Archetypal roles
            ("threshold guardian", CharacterRole.THRESHOLD_GUARDIAN),
            ("guardian", CharacterRole.THRESHOLD_GUARDIAN),
            ("gatekeeper", CharacterRole.THRESHOLD_GUARDIAN),
            ("messenger", CharacterRole.HERALD),
            ("announcer", CharacterRole.HERALD),
            ("comic relief", CharacterRole.TRICKSTER),
            ("joker", CharacterRole.TRICKSTER),
            ("shape shifter", CharacterRole.SHAPESHIFTER),
            ("shape-shifter", CharacterRole.SHAPESHIFTER),
            ("betrayer", CharacterRole.SHAPESHIFTER),
            
            # Supporting roles
            ("supporting character", CharacterRole.SUPPORTING),
            ("side character", CharacterRole.SUPPORTING),
            ("minor character", CharacterRole.MINOR),
            ("background character", CharacterRole.MINOR),
            ("storyteller", CharacterRole.NARRATOR),
            ("voice", CharacterRole.NARRATOR),
            ("contrast character", CharacterRole.FOIL),
            ("opposite", CharacterRole.FOIL),
        ]
        
        for input_str, expected_role in fuzzy_matches:
            result = CharacterRole.from_string(input_str)
            assert result == expected_role, f"Expected {expected_role} for '{input_str}', got {result}"
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid input."""
        invalid_inputs = [
            "invalid_role_type",
            "character with superpowers",
            "completely random text",
            "",
            "   ",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                CharacterRole.from_string(invalid_input)
    
    def test_get_primary_roles(self):
        """Test getting primary character roles."""
        primary_roles = CharacterRole.get_primary_roles()
        
        assert isinstance(primary_roles, list)
        assert len(primary_roles) == 2  # Should be exactly 2 primary roles
        
        # Should include protagonist and antagonist
        expected_primary = [CharacterRole.PROTAGONIST, CharacterRole.ANTAGONIST]
        
        for expected in expected_primary:
            assert expected in primary_roles, f"Primary role {expected} not found"
        
        print(f"✓ Primary roles: {len(primary_roles)} types")
    
    def test_get_major_roles(self):
        """Test getting major character roles."""
        major_roles = CharacterRole.get_major_roles()
        
        assert isinstance(major_roles, list)
        assert len(major_roles) == 6  # Should be exactly 6 major roles
        
        # Should include the specified major roles
        expected_major = [
            CharacterRole.PROTAGONIST, CharacterRole.ANTAGONIST, CharacterRole.DEUTERAGONIST,
            CharacterRole.LOVE_INTEREST, CharacterRole.MENTOR, CharacterRole.SHAPESHIFTER
        ]
        
        for expected in expected_major:
            assert expected in major_roles, f"Major role {expected} not found"
        
        print(f"✓ Major roles: {len(major_roles)} types")
    
    def test_get_archetypal_roles(self):
        """Test getting archetypal character roles."""
        archetypal_roles = CharacterRole.get_archetypal_roles()
        
        assert isinstance(archetypal_roles, list)
        assert len(archetypal_roles) == 7  # Should be exactly 7 archetypal roles
        
        # Should include the classic archetypal roles
        expected_archetypal = [
            CharacterRole.MENTOR, CharacterRole.ALLY, CharacterRole.THRESHOLD_GUARDIAN,
            CharacterRole.HERALD, CharacterRole.TRICKSTER, CharacterRole.SHAPESHIFTER,
            CharacterRole.FOIL
        ]
        
        for expected in expected_archetypal:
            assert expected in archetypal_roles, f"Archetypal role {expected} not found"
        
        print(f"✓ Archetypal roles: {len(archetypal_roles)} types")


class TestCharacterArchetype:
    """Test the CharacterArchetype enum comprehensively."""
    
    def test_all_archetype_values_are_strings(self):
        """Ensure all character archetype enum values are properly formatted strings."""
        for archetype in CharacterArchetype:
            assert isinstance(archetype.value, str)
            assert archetype.value.islower()
            assert " " not in archetype.value  # Should use underscores
            assert len(archetype.value) > 0
            # Should start with "the_"
            assert archetype.value.startswith("the_")
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in archetype.value)
    
    def test_all_archetypes_have_unique_values(self):
        """Ensure no duplicate values in CharacterArchetype enum."""
        values = [archetype.value for archetype in CharacterArchetype]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate archetype values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have exactly 12 character archetypes
        assert len(values) == 12, f"Expected exactly 12 character archetypes, got {len(values)}"
        print(f"✓ Found {len(values)} unique character archetypes")
    
    def test_display_name_property(self):
        """Test that display_name properly formats archetype names."""
        for archetype in CharacterArchetype:
            display_name = archetype.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should start with "The"
            assert display_name.startswith("The ")
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (CharacterArchetype.THE_HERO, "The Hero"),
            (CharacterArchetype.THE_INNOCENT, "The Innocent"),
            (CharacterArchetype.THE_EXPLORER, "The Explorer"),
            (CharacterArchetype.THE_SAGE, "The Sage"),
            (CharacterArchetype.THE_OUTLAW, "The Outlaw"),
            (CharacterArchetype.THE_MAGICIAN, "The Magician"),
            (CharacterArchetype.THE_REGULAR_PERSON, "The Regular Person"),
            (CharacterArchetype.THE_LOVER, "The Lover"),
            (CharacterArchetype.THE_JESTER, "The Jester"),
            (CharacterArchetype.THE_CAREGIVER, "The Caregiver"),
            (CharacterArchetype.THE_RULER, "The Ruler"),
            (CharacterArchetype.THE_CREATOR, "The Creator"),
        ]
        
        for archetype, expected_display in test_cases:
            assert archetype.display_name == expected_display, f"Expected '{expected_display}' for {archetype.value}, got '{archetype.display_name}'"
    
    def test_description_property(self):
        """Test that all character archetypes have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for archetype in CharacterArchetype:
            description = archetype.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {archetype.value}"
            
            # Check for minimum meaningful length
            if len(description) < 80:
                short_descriptions.append(f"{archetype.value}: '{description}'")
            
            # Should start with capital letter
            if description:
                assert description[0].isupper(), f"Description should start with capital for {archetype.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?')
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{archetype.value}: '{description}'")
        
        # Most descriptions should be substantial
        assert len(short_descriptions) <= 2, f"Too many short descriptions: {short_descriptions}"
        
        # Most descriptions should have proper punctuation
        assert len(descriptions_without_punctuation) <= 1, f"Descriptions without punctuation: {descriptions_without_punctuation}"
        
        total_archetypes = len(list(CharacterArchetype))
        quality_descriptions = total_archetypes - len(short_descriptions) - len(descriptions_without_punctuation)
        quality_percentage = quality_descriptions / total_archetypes
        assert quality_percentage >= 0.8, f"Too few quality descriptions: {quality_descriptions}/{total_archetypes} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_archetypes} ({quality_percentage:.1%})")
    
    def test_core_motivation_property(self):
        """Test core_motivation property returns valid motivations."""
        for archetype in CharacterArchetype:
            motivation = archetype.core_motivation
            assert isinstance(motivation, str)
            assert len(motivation) > 0, f"No core motivation found for {archetype.value}"
            # Should start with "To" (infinitive form)
            assert motivation.startswith("To "), f"Core motivation should start with 'To' for {archetype.value}: '{motivation}'"
        
        # Test specific known motivations
        assert CharacterArchetype.THE_HERO.core_motivation == "To prove worth through courageous action"
        assert CharacterArchetype.THE_INNOCENT.core_motivation == "To be happy and live in harmony"
        assert CharacterArchetype.THE_EXPLORER.core_motivation == "To experience freedom and find purpose"
    
    def test_greatest_fear_property(self):
        """Test greatest_fear property returns valid fears."""
        for archetype in CharacterArchetype:
            fear = archetype.greatest_fear
            assert isinstance(fear, str)
            assert len(fear) > 0, f"No greatest fear found for {archetype.value}"
            # Should be a descriptive phrase
            assert len(fear.split()) >= 2, f"Greatest fear too short for {archetype.value}: '{fear}'"
        
        # Test specific known fears
        assert CharacterArchetype.THE_HERO.greatest_fear == "Weakness, vulnerability, cowardice"
        assert CharacterArchetype.THE_INNOCENT.greatest_fear == "Doing something wrong or bad"
        assert CharacterArchetype.THE_OUTLAW.greatest_fear == "Being powerless, ineffectual"
    
    def test_typical_traits_property(self):
        """Test typical_traits property returns valid trait lists."""
        for archetype in CharacterArchetype:
            traits = archetype.typical_traits
            assert isinstance(traits, list)
            assert len(traits) > 0, f"No typical traits found for {archetype.value}"
            assert len(traits) >= 3, f"Should have at least 3 traits for {archetype.value}, got {len(traits)}"
            
            # All traits should be strings
            for trait in traits:
                assert isinstance(trait, str)
                assert len(trait) > 0
                # Should be lowercase descriptive words
                assert trait.islower()
                # Should not contain underscores (should be simple adjectives)
                assert "_" not in trait or "-" in trait  # Allow hyphenated traits
        
        # Test that different archetypes have different trait profiles
        all_traits = set()
        for archetype in CharacterArchetype:
            all_traits.update(archetype.typical_traits)
        
        assert len(all_traits) >= 30, f"Should have variety in typical traits, found {len(all_traits)}"


class TestCharacterArchetypeClassMethods:
    """Test class methods of CharacterArchetype."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("the_hero", CharacterArchetype.THE_HERO),
            ("the_innocent", CharacterArchetype.THE_INNOCENT),
            ("the_explorer", CharacterArchetype.THE_EXPLORER),
            ("the_sage", CharacterArchetype.THE_SAGE),
        ]
        
        for input_str, expected_archetype in direct_matches:
            result = CharacterArchetype.from_string(input_str)
            assert result == expected_archetype, f"Expected {expected_archetype} for '{input_str}', got {result}"
    
    def test_from_string_without_the_prefix(self):
        """Test from_string handling of inputs without 'the' prefix."""
        no_the_matches = [
            ("hero", CharacterArchetype.THE_HERO),
            ("innocent", CharacterArchetype.THE_INNOCENT),
            ("explorer", CharacterArchetype.THE_EXPLORER),
            ("sage", CharacterArchetype.THE_SAGE),
            ("outlaw", CharacterArchetype.THE_OUTLAW),
            ("magician", CharacterArchetype.THE_MAGICIAN),
        ]
        
        for input_str, expected_archetype in no_the_matches:
            result = CharacterArchetype.from_string(input_str)
            assert result == expected_archetype, f"Expected {expected_archetype} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching."""
        fuzzy_matches = [
            # Hero variants
            ("champion", CharacterArchetype.THE_HERO),
            ("warrior", CharacterArchetype.THE_HERO),
            
            # Innocent variants
            ("child", CharacterArchetype.THE_INNOCENT),
            ("pure one", CharacterArchetype.THE_INNOCENT),
            
            # Explorer variants
            ("adventurer", CharacterArchetype.THE_EXPLORER),
            ("wanderer", CharacterArchetype.THE_EXPLORER),
            ("seeker", CharacterArchetype.THE_EXPLORER),
            
            # Sage variants
            ("wise one", CharacterArchetype.THE_SAGE),
            ("mentor", CharacterArchetype.THE_SAGE),
            ("teacher", CharacterArchetype.THE_SAGE),
            
            # Outlaw variants
            ("rebel", CharacterArchetype.THE_OUTLAW),
            ("revolutionary", CharacterArchetype.THE_OUTLAW),
            
            # Magician variants
            ("wizard", CharacterArchetype.THE_MAGICIAN),
            ("transformer", CharacterArchetype.THE_MAGICIAN),
            
            # Regular Person variants
            ("regular person", CharacterArchetype.THE_REGULAR_PERSON),
            ("everyman", CharacterArchetype.THE_REGULAR_PERSON),
            ("common person", CharacterArchetype.THE_REGULAR_PERSON),
            ("ordinary person", CharacterArchetype.THE_REGULAR_PERSON),
            
            # Lover variants
            ("romantic", CharacterArchetype.THE_LOVER),
            ("partner", CharacterArchetype.THE_LOVER),
            
            # Jester variants
            ("fool", CharacterArchetype.THE_JESTER),
            ("joker", CharacterArchetype.THE_JESTER),
            ("comedian", CharacterArchetype.THE_JESTER),
            
            # Caregiver variants
            ("nurturer", CharacterArchetype.THE_CAREGIVER),
            ("helper", CharacterArchetype.THE_CAREGIVER),
            ("protector", CharacterArchetype.THE_CAREGIVER),
            
            # Ruler variants
            ("leader", CharacterArchetype.THE_RULER),
            ("king", CharacterArchetype.THE_RULER),
            ("queen", CharacterArchetype.THE_RULER),
            ("boss", CharacterArchetype.THE_RULER),
            
            # Creator variants
            ("artist", CharacterArchetype.THE_CREATOR),
            ("inventor", CharacterArchetype.THE_CREATOR),
            ("builder", CharacterArchetype.THE_CREATOR),
        ]
        
        for input_str, expected_archetype in fuzzy_matches:
            result = CharacterArchetype.from_string(input_str)
            assert result == expected_archetype, f"Expected {expected_archetype} for '{input_str}', got {result}"
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid input."""
        invalid_inputs = [
            "invalid_archetype_type",
            "the unknown archetype",
            "completely random text",
            "",
            "   ",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                CharacterArchetype.from_string(invalid_input)
    
    def test_get_positive_archetypes(self):
        """Test getting positive character archetypes."""
        positive_archetypes = CharacterArchetype.get_positive_archetypes()
        
        assert isinstance(positive_archetypes, list)
        assert len(positive_archetypes) == 7  # Should be exactly 7 positive archetypes
        
        # Should include the specified positive archetypes
        expected_positive = [
            CharacterArchetype.THE_HERO, CharacterArchetype.THE_INNOCENT, 
            CharacterArchetype.THE_SAGE, CharacterArchetype.THE_CAREGIVER,
            CharacterArchetype.THE_EXPLORER, CharacterArchetype.THE_CREATOR,
            CharacterArchetype.THE_LOVER
        ]
        
        for expected in expected_positive:
            assert expected in positive_archetypes, f"Positive archetype {expected} not found"
        
        print(f"✓ Positive archetypes: {len(positive_archetypes)} types")
    
    def test_get_complex_archetypes(self):
        """Test getting complex character archetypes."""
        complex_archetypes = CharacterArchetype.get_complex_archetypes()
        
        assert isinstance(complex_archetypes, list)
        assert len(complex_archetypes) == 5  # Should be exactly 5 complex archetypes
        
        # Should include the specified complex archetypes
        expected_complex = [
            CharacterArchetype.THE_OUTLAW, CharacterArchetype.THE_MAGICIAN,
            CharacterArchetype.THE_RULER, CharacterArchetype.THE_JESTER,
            CharacterArchetype.THE_REGULAR_PERSON
        ]
        
        for expected in expected_complex:
            assert expected in complex_archetypes, f"Complex archetype {expected} not found"
        
        print(f"✓ Complex archetypes: {len(complex_archetypes)} types")


class TestCharacterIntegration:
    """Integration tests for the character system."""
    
    def test_all_roles_have_complete_properties(self):
        """Test that all character roles have all required properties implemented."""
        for role in CharacterRole:
            # Test all properties work without errors
            assert role.display_name is not None
            assert role.description is not None
            assert role.narrative_importance is not None
            assert role.typical_functions is not None
    
    def test_all_archetypes_have_complete_properties(self):
        """Test that all character archetypes have all required properties implemented."""
        for archetype in CharacterArchetype:
            # Test all properties work without errors
            assert archetype.display_name is not None
            assert archetype.description is not None
            assert archetype.core_motivation is not None
            assert archetype.greatest_fear is not None
            assert archetype.typical_traits is not None
    
    def test_role_archetype_compatibility(self):
        """Test logical compatibility between roles and archetypes."""
        # Test that hero archetype makes sense with protagonist role
        hero_traits = CharacterArchetype.THE_HERO.typical_traits
        protagonist_functions = CharacterRole.PROTAGONIST.typical_functions
        
        # Hero should have traits that support protagonist functions
        assert "brave" in hero_traits or "courageous" in " ".join(hero_traits)
        assert "drives plot" in protagonist_functions
        
        # Test that sage archetype makes sense with mentor role
        sage_traits = CharacterArchetype.THE_SAGE.typical_traits
        mentor_functions = CharacterRole.MENTOR.typical_functions
        
        assert "wise" in sage_traits or "knowledgeable" in sage_traits
        assert "provides wisdom" in mentor_functions or "offers guidance" in mentor_functions
    
    def test_categorization_completeness(self):
        """Test that categorizations cover all items completely."""
        # Test that all roles have valid importance levels
        all_roles = set(CharacterRole)
        categorized_roles = set()
        
        # Add roles from different importance categories
        for role in CharacterRole:
            assert role.narrative_importance in {"primary", "major", "secondary", "tertiary", "structural"}
            categorized_roles.add(role)
        
        assert categorized_roles == all_roles, "Not all roles are properly categorized by importance"
        
        # Test that positive + complex archetypes = all archetypes
        all_archetypes = set(CharacterArchetype)
        positive_archetypes = set(CharacterArchetype.get_positive_archetypes())
        complex_archetypes = set(CharacterArchetype.get_complex_archetypes())
        
        assert positive_archetypes.union(complex_archetypes) == all_archetypes, "Positive + Complex should equal all archetypes"
        assert positive_archetypes.intersection(complex_archetypes) == set(), "Positive and Complex should not overlap"


class TestCharacterPerformance:
    """Performance tests for the character system."""
    
    def test_role_property_access_performance(self):
        """Test that character role property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for role in CharacterRole:
                _ = role.display_name
                _ = role.description
                _ = role.narrative_importance
                _ = role.typical_functions
        end_time = time.time()
        
        # Should complete 56,000 property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Role property access too slow: {total_time:.2f}s"
    
    def test_archetype_property_access_performance(self):
        """Test that character archetype property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for archetype in CharacterArchetype:
                _ = archetype.display_name
                _ = archetype.description
                _ = archetype.core_motivation
                _ = archetype.greatest_fear
                _ = archetype.typical_traits
        end_time = time.time()
        
        # Should complete 60,000 property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Archetype property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        role_test_inputs = ["main character", "villain", "mentor", "comic relief", "helper"]
        archetype_test_inputs = ["hero", "sage", "rebel", "artist", "leader"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in role_test_inputs:
                try:
                    CharacterRole.from_string(input_str)
                except ValueError:
                    pass
            for input_str in archetype_test_inputs:
                try:
                    CharacterArchetype.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 10,000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_role_enum_basic_functionality(self):
        """Test that CharacterRole enum works as expected."""
        # Test iteration
        role_list = list(CharacterRole)
        assert len(role_list) == 14  # Should have exactly 14 character roles
        
        # Test basic attributes
        protagonist = CharacterRole.PROTAGONIST
        assert protagonist.value == "protagonist"
        assert "Protagonist" in protagonist.display_name
        
        # Test enum comparison
        assert CharacterRole.PROTAGONIST == CharacterRole.PROTAGONIST
        assert CharacterRole.PROTAGONIST != CharacterRole.ANTAGONIST
    
    def test_archetype_enum_basic_functionality(self):
        """Test that CharacterArchetype enum works as expected."""
        # Test iteration
        archetype_list = list(CharacterArchetype)
        assert len(archetype_list) == 12  # Should have exactly 12 character archetypes
        
        # Test basic attributes
        hero = CharacterArchetype.THE_HERO
        assert hero.value == "the_hero"
        assert "The Hero" in hero.display_name
        
        # Test enum comparison
        assert CharacterArchetype.THE_HERO == CharacterArchetype.THE_HERO
        assert CharacterArchetype.THE_HERO != CharacterArchetype.THE_INNOCENT
    
    def test_string_representations(self):
        """Test string representation methods."""
        role = CharacterRole.PROTAGONIST
        archetype = CharacterArchetype.THE_HERO
        
        role_str = str(role)
        archetype_str = str(archetype)
        
        assert isinstance(role_str, str)
        assert isinstance(archetype_str, str)
        assert len(role_str) > 0
        assert len(archetype_str) > 0
        assert role_str == role.display_name
        assert archetype_str == archetype.display_name


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])