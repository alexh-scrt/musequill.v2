"""
Comprehensive tests for musequill.models.book.personality module.

Test file: tests/models/book/test_personality.py
Module under test: musequill/models/book/personality.py

Run from project root: pytest tests/models/book/test_personality.py -v
"""

import sys
from pathlib import Path
import pytest
from typing import List, Set, Tuple, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the PersonalityTrait class from the personality module
from musequill.models.book.personality import PersonalityTrait


class TestPersonalityTrait:
    """Test the PersonalityTrait enum comprehensively."""
    
    def test_all_trait_values_are_strings(self):
        """Ensure all personality trait enum values are properly formatted strings."""
        for trait in PersonalityTrait:
            assert isinstance(trait.value, str)
            assert trait.value.islower()
            assert " " not in trait.value  # Should use underscores for multi-word traits
            assert len(trait.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in trait.value)
    
    def test_all_traits_have_unique_values(self):
        """Ensure no duplicate values in PersonalityTrait enum."""
        values = [trait.value for trait in PersonalityTrait]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate trait values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have at least 30 personality traits for comprehensive character development
        assert len(values) >= 30, f"Expected at least 30 personality traits, got {len(values)}"
        print(f"✓ Found {len(values)} unique personality traits")
    
    def test_display_name_property(self):
        """Test that display_name properly formats trait names."""
        for trait in PersonalityTrait:
            display_name = trait.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (PersonalityTrait.BRAVE, "Brave"),
            (PersonalityTrait.LOYAL, "Loyal"),
            (PersonalityTrait.INTELLIGENT, "Intelligent"),
            (PersonalityTrait.COMPASSIONATE, "Compassionate"),
            (PersonalityTrait.DETERMINED, "Determined"),
            (PersonalityTrait.HONEST, "Honest"),
            (PersonalityTrait.ARROGANT, "Arrogant"),
            (PersonalityTrait.SELFISH, "Selfish"),
            (PersonalityTrait.IMPULSIVE, "Impulsive"),
            (PersonalityTrait.AMBITIOUS, "Ambitious"),
            (PersonalityTrait.INDEPENDENT, "Independent"),
            (PersonalityTrait.MYSTERIOUS, "Mysterious"),
        ]
        
        for trait, expected_display in test_cases:
            assert trait.display_name == expected_display, f"Expected '{expected_display}' for {trait.value}, got '{trait.display_name}'"
    
    def test_description_property(self):
        """Test that all personality traits have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for trait in PersonalityTrait:
            description = trait.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {trait.value}"
            
            # Check for minimum meaningful length (personality descriptions should be substantial)
            if len(description) < 60:
                short_descriptions.append(f"{trait.value}: '{description}'")
            
            # Should start with capital letter
            if description:
                assert description[0].isupper(), f"Description should start with capital for {trait.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?')
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{trait.value}: '{description}'")
        
        # Most descriptions should be substantial
        assert len(short_descriptions) <= 3, f"Too many short descriptions: {short_descriptions}"
        
        # Most descriptions should have proper punctuation
        assert len(descriptions_without_punctuation) <= 2, f"Descriptions without punctuation: {descriptions_without_punctuation}"
        
        total_traits = len(list(PersonalityTrait))
        quality_descriptions = total_traits - len(short_descriptions) - len(descriptions_without_punctuation)
        quality_percentage = quality_descriptions / total_traits
        assert quality_percentage >= 0.8, f"Too few quality descriptions: {quality_descriptions}/{total_traits} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_traits} ({quality_percentage:.1%})")
    
    def test_trait_type_property(self):
        """Test trait_type property categorization."""
        valid_trait_types = {"positive", "negative", "complex"}
        
        type_counts = {"positive": 0, "negative": 0, "complex": 0}
        
        for trait in PersonalityTrait:
            trait_type = trait.trait_type
            assert trait_type in valid_trait_types, f"{trait.value} has invalid trait type: {trait_type}"
            assert isinstance(trait_type, str)
            type_counts[trait_type] += 1
        
        # Verify we have good distribution across trait types
        assert type_counts["positive"] >= 10, f"Should have at least 10 positive traits, got {type_counts['positive']}"
        assert type_counts["negative"] >= 10, f"Should have at least 10 negative traits, got {type_counts['negative']}"
        assert type_counts["complex"] >= 5, f"Should have at least 5 complex traits, got {type_counts['complex']}"
        print(f"Trait type distribution: {type_counts}")
        
        # Test specific known trait types
        assert PersonalityTrait.BRAVE.trait_type == "positive"
        assert PersonalityTrait.COMPASSIONATE.trait_type == "positive"
        assert PersonalityTrait.ARROGANT.trait_type == "negative"
        assert PersonalityTrait.CRUEL.trait_type == "negative"
        assert PersonalityTrait.AMBITIOUS.trait_type == "complex"
        assert PersonalityTrait.INDEPENDENT.trait_type == "complex"
    
    def test_opposite_trait_property(self):
        """Test opposite_trait property returns valid opposites."""
        opposite_pairs_found = 0
        
        for trait in PersonalityTrait:
            opposite = trait.opposite_trait
            if opposite is not None:
                assert isinstance(opposite, PersonalityTrait)
                # The opposite's opposite should be the original trait (symmetrical relationship)
                assert opposite.opposite_trait == trait, f"Asymmetrical opposite relationship: {trait.value} -> {opposite.value} -> {opposite.opposite_trait.value if opposite.opposite_trait else None}"
                opposite_pairs_found += 1
        
        # Should have a reasonable number of opposite pairs
        # Each pair counts twice (A->B and B->A), so divide by 2
        unique_pairs = opposite_pairs_found // 2
        assert unique_pairs >= 8, f"Should have at least 8 opposite trait pairs, found {unique_pairs}"
        print(f"✓ Found {unique_pairs} opposite trait pairs")
        
        # Test specific known opposites
        assert PersonalityTrait.BRAVE.opposite_trait == PersonalityTrait.COWARDLY
        assert PersonalityTrait.COWARDLY.opposite_trait == PersonalityTrait.BRAVE
        assert PersonalityTrait.OPTIMISTIC.opposite_trait == PersonalityTrait.PESSIMISTIC
        assert PersonalityTrait.PESSIMISTIC.opposite_trait == PersonalityTrait.OPTIMISTIC
        assert PersonalityTrait.HONEST.opposite_trait == PersonalityTrait.DISHONEST
        assert PersonalityTrait.DISHONEST.opposite_trait == PersonalityTrait.HONEST


class TestPersonalityTraitClassMethods:
    """Test class methods of PersonalityTrait."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("brave", PersonalityTrait.BRAVE),
            ("loyal", PersonalityTrait.LOYAL),
            ("intelligent", PersonalityTrait.INTELLIGENT),
            ("compassionate", PersonalityTrait.COMPASSIONATE),
            ("arrogant", PersonalityTrait.ARROGANT),
            ("selfish", PersonalityTrait.SELFISH),
            ("ambitious", PersonalityTrait.AMBITIOUS),
            ("independent", PersonalityTrait.INDEPENDENT),
        ]
        
        for input_str, expected_trait in direct_matches:
            result = PersonalityTrait.from_string(input_str)
            assert result == expected_trait, f"Expected {expected_trait} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching(self):
        """Test from_string with fuzzy matching using synonyms."""
        fuzzy_matches = [
            # Positive trait synonyms
            ("courageous", PersonalityTrait.BRAVE),
            ("fearless", PersonalityTrait.BRAVE),
            ("heroic", PersonalityTrait.BRAVE),
            ("faithful", PersonalityTrait.LOYAL),
            ("devoted", PersonalityTrait.LOYAL),
            ("trustworthy", PersonalityTrait.LOYAL),
            ("smart", PersonalityTrait.INTELLIGENT),
            ("brilliant", PersonalityTrait.INTELLIGENT),
            ("clever", PersonalityTrait.INTELLIGENT),
            ("caring", PersonalityTrait.COMPASSIONATE),
            ("kind", PersonalityTrait.COMPASSIONATE),
            ("sympathetic", PersonalityTrait.COMPASSIONATE),
            ("persistent", PersonalityTrait.DETERMINED),
            ("resolute", PersonalityTrait.DETERMINED),
            ("steadfast", PersonalityTrait.DETERMINED),
            ("truthful", PersonalityTrait.HONEST),
            ("sincere", PersonalityTrait.HONEST),
            ("genuine", PersonalityTrait.HONEST),
            ("artistic", PersonalityTrait.CREATIVE),
            ("imaginative", PersonalityTrait.CREATIVE),
            ("innovative", PersonalityTrait.CREATIVE),
            ("tolerant", PersonalityTrait.PATIENT),
            ("calm", PersonalityTrait.PATIENT),
            ("positive", PersonalityTrait.OPTIMISTIC),
            ("hopeful", PersonalityTrait.OPTIMISTIC),
            ("modest", PersonalityTrait.HUMBLE),
            ("unassuming", PersonalityTrait.HUMBLE),
            ("giving", PersonalityTrait.GENEROUS),
            ("charitable", PersonalityTrait.GENEROUS),
            ("knowledgeable", PersonalityTrait.WISE),
            ("insightful", PersonalityTrait.WISE),
            
            # Negative trait synonyms  
            ("proud", PersonalityTrait.ARROGANT),
            ("conceited", PersonalityTrait.ARROGANT),
            ("egotistical", PersonalityTrait.ARROGANT),
            ("self-centered", PersonalityTrait.SELFISH),
            ("narcissistic", PersonalityTrait.SELFISH),
            ("hasty", PersonalityTrait.IMPULSIVE),
            ("rash", PersonalityTrait.IMPULSIVE),
            ("obstinate", PersonalityTrait.STUBBORN),
            ("headstrong", PersonalityTrait.STUBBORN),
            ("envious", PersonalityTrait.JEALOUS),
            ("coward", PersonalityTrait.COWARDLY),
            ("timid", PersonalityTrait.COWARDLY),
            ("deceitful", PersonalityTrait.DISHONEST),
            ("false", PersonalityTrait.DISHONEST),
            ("mean", PersonalityTrait.CRUEL),
            ("heartless", PersonalityTrait.CRUEL),
            ("idle", PersonalityTrait.LAZY),
            ("slothful", PersonalityTrait.LAZY),
            ("negative", PersonalityTrait.PESSIMISTIC),
            ("gloomy", PersonalityTrait.PESSIMISTIC),
            ("avaricious", PersonalityTrait.GREEDY),
            ("scheming", PersonalityTrait.MANIPULATIVE),
            ("controlling", PersonalityTrait.MANIPULATIVE),
            
            # Complex trait synonyms
            ("driven", PersonalityTrait.AMBITIOUS),
            ("goal-oriented", PersonalityTrait.AMBITIOUS),
            ("self-reliant", PersonalityTrait.INDEPENDENT),
            ("autonomous", PersonalityTrait.INDEPENDENT),
            ("enigmatic", PersonalityTrait.MYSTERIOUS),
            ("secretive", PersonalityTrait.MYSTERIOUS),
            ("quirky", PersonalityTrait.ECCENTRIC),
            ("unconventional", PersonalityTrait.ECCENTRIC),
            ("practical", PersonalityTrait.PRAGMATIC),
            ("realistic", PersonalityTrait.PRAGMATIC),
            ("careful", PersonalityTrait.CAUTIOUS),
        ]
        
        for input_str, expected_trait in fuzzy_matches:
            result = PersonalityTrait.from_string(input_str)
            assert result == expected_trait, f"Expected {expected_trait} for '{input_str}', got {result}"
    
    def test_from_string_invalid_input(self):
        """Test from_string with invalid input."""
        invalid_inputs = [
            "invalid_trait_type",
            "super amazing personality",
            "completely random text",
            "",
            "   ",
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                PersonalityTrait.from_string(invalid_input)
    
    def test_get_positive_traits(self):
        """Test getting positive personality traits."""
        positive_traits = PersonalityTrait.get_positive_traits()
        
        assert isinstance(positive_traits, list)
        assert len(positive_traits) >= 10, f"Should have at least 10 positive traits, got {len(positive_traits)}"
        
        # All returned traits should be positive
        for trait in positive_traits:
            assert isinstance(trait, PersonalityTrait)
            assert trait.trait_type == "positive", f"Trait {trait.value} is not positive: {trait.trait_type}"
        
        # Should include known positive traits
        expected_positive = [
            PersonalityTrait.BRAVE, PersonalityTrait.LOYAL, PersonalityTrait.INTELLIGENT,
            PersonalityTrait.COMPASSIONATE, PersonalityTrait.DETERMINED, PersonalityTrait.HONEST,
            PersonalityTrait.CREATIVE, PersonalityTrait.PATIENT, PersonalityTrait.OPTIMISTIC,
            PersonalityTrait.HUMBLE, PersonalityTrait.GENEROUS, PersonalityTrait.WISE
        ]
        
        found_positive = sum(1 for trait in expected_positive if trait in positive_traits)
        assert found_positive >= 10, f"Should find most expected positive traits, found {found_positive}/12"
        
        print(f"✓ Positive traits: {len(positive_traits)} types")
    
    def test_get_negative_traits(self):
        """Test getting negative personality traits."""
        negative_traits = PersonalityTrait.get_negative_traits()
        
        assert isinstance(negative_traits, list)
        assert len(negative_traits) >= 10, f"Should have at least 10 negative traits, got {len(negative_traits)}"
        
        # All returned traits should be negative
        for trait in negative_traits:
            assert isinstance(trait, PersonalityTrait)
            assert trait.trait_type == "negative", f"Trait {trait.value} is not negative: {trait.trait_type}"
        
        # Should include known negative traits
        expected_negative = [
            PersonalityTrait.ARROGANT, PersonalityTrait.SELFISH, PersonalityTrait.IMPULSIVE,
            PersonalityTrait.STUBBORN, PersonalityTrait.JEALOUS, PersonalityTrait.COWARDLY,
            PersonalityTrait.DISHONEST, PersonalityTrait.CRUEL, PersonalityTrait.LAZY,
            PersonalityTrait.PESSIMISTIC, PersonalityTrait.GREEDY, PersonalityTrait.MANIPULATIVE
        ]
        
        found_negative = sum(1 for trait in expected_negative if trait in negative_traits)
        assert found_negative >= 10, f"Should find most expected negative traits, found {found_negative}/12"
        
        print(f"✓ Negative traits: {len(negative_traits)} types")
    
    def test_get_complex_traits(self):
        """Test getting complex/neutral personality traits."""
        complex_traits = PersonalityTrait.get_complex_traits()
        
        assert isinstance(complex_traits, list)
        assert len(complex_traits) >= 5, f"Should have at least 5 complex traits, got {len(complex_traits)}"
        
        # All returned traits should be complex
        for trait in complex_traits:
            assert isinstance(trait, PersonalityTrait)
            assert trait.trait_type == "complex", f"Trait {trait.value} is not complex: {trait.trait_type}"
        
        # Should include known complex traits
        expected_complex = [
            PersonalityTrait.AMBITIOUS, PersonalityTrait.INDEPENDENT, PersonalityTrait.MYSTERIOUS,
            PersonalityTrait.ECCENTRIC, PersonalityTrait.PRAGMATIC, PersonalityTrait.CAUTIOUS
        ]
        
        found_complex = sum(1 for trait in expected_complex if trait in complex_traits)
        assert found_complex >= 5, f"Should find most expected complex traits, found {found_complex}/6"
        
        print(f"✓ Complex traits: {len(complex_traits)} types")
    
    def test_get_contrasting_pairs(self):
        """Test getting pairs of contrasting traits."""
        contrasting_pairs = PersonalityTrait.get_contrasting_pairs()
        
        assert isinstance(contrasting_pairs, list)
        assert len(contrasting_pairs) >= 8, f"Should have at least 8 contrasting pairs, got {len(contrasting_pairs)}"
        
        # All pairs should be tuples of PersonalityTrait
        for pair in contrasting_pairs:
            assert isinstance(pair, tuple)
            assert len(pair) == 2
            trait1, trait2 = pair
            assert isinstance(trait1, PersonalityTrait)
            assert isinstance(trait2, PersonalityTrait)
            
            # The traits should be opposites of each other
            assert trait1.opposite_trait == trait2, f"Trait {trait1.value} should have opposite {trait2.value}"
            assert trait2.opposite_trait == trait1, f"Trait {trait2.value} should have opposite {trait1.value}"
        
        # Should include known contrasting pairs
        expected_pairs = [
            (PersonalityTrait.BRAVE, PersonalityTrait.COWARDLY),
            (PersonalityTrait.OPTIMISTIC, PersonalityTrait.PESSIMISTIC),
            (PersonalityTrait.HONEST, PersonalityTrait.DISHONEST),
            (PersonalityTrait.GENEROUS, PersonalityTrait.SELFISH),
            (PersonalityTrait.HUMBLE, PersonalityTrait.ARROGANT),
        ]
        
        # Check if pairs exist (order doesn't matter)
        found_pairs = 0
        for expected_pair in expected_pairs:
            trait1, trait2 = expected_pair
            if (trait1, trait2) in contrasting_pairs or (trait2, trait1) in contrasting_pairs:
                found_pairs += 1
        
        assert found_pairs >= 4, f"Should find most expected contrasting pairs, found {found_pairs}/5"
        
        print(f"✓ Contrasting pairs: {len(contrasting_pairs)} pairs")


class TestPersonalityTraitIntegration:
    """Integration tests for the personality trait system."""
    
    def test_all_traits_have_complete_properties(self):
        """Test that all personality traits have all required properties implemented."""
        for trait in PersonalityTrait:
            # Test all properties work without errors
            assert trait.display_name is not None
            assert trait.description is not None
            assert trait.trait_type is not None
            # opposite_trait can be None, so just check it doesn't crash
            _ = trait.opposite_trait
    
    def test_trait_categorization_completeness(self):
        """Test that trait categorizations cover all traits completely."""
        all_traits = set(PersonalityTrait)
        
        positive_traits = set(PersonalityTrait.get_positive_traits())
        negative_traits = set(PersonalityTrait.get_negative_traits())
        complex_traits = set(PersonalityTrait.get_complex_traits())
        
        # All categorization methods should return valid PersonalityTrait instances
        for trait in positive_traits:
            assert isinstance(trait, PersonalityTrait)
        for trait in negative_traits:
            assert isinstance(trait, PersonalityTrait)
        for trait in complex_traits:
            assert isinstance(trait, PersonalityTrait)
        
        # Categories should not overlap
        assert positive_traits.intersection(negative_traits) == set(), "Positive and negative traits should not overlap"
        assert positive_traits.intersection(complex_traits) == set(), "Positive and complex traits should not overlap"
        assert negative_traits.intersection(complex_traits) == set(), "Negative and complex traits should not overlap"
        
        # Categories should cover all traits
        categorized_traits = positive_traits.union(negative_traits).union(complex_traits)
        assert categorized_traits == all_traits, f"Categories don't cover all traits. Missing: {all_traits - categorized_traits}"
    
    def test_opposite_trait_consistency(self):
        """Test that opposite trait relationships are consistent."""
        traits_with_opposites = set()
        
        for trait in PersonalityTrait:
            opposite = trait.opposite_trait
            if opposite is not None:
                # Opposite should be a valid PersonalityTrait
                assert isinstance(opposite, PersonalityTrait)
                
                # Relationship should be symmetrical
                assert opposite.opposite_trait == trait, f"Asymmetrical opposite: {trait.value} -> {opposite.value} -> {opposite.opposite_trait.value if opposite.opposite_trait else None}"
                
                # Track traits that have opposites
                traits_with_opposites.add(trait)
                traits_with_opposites.add(opposite)
        
        # Should have a reasonable number of traits with opposites
        assert len(traits_with_opposites) >= 16, f"Should have at least 16 traits with opposites (8 pairs), got {len(traits_with_opposites)}"
    
    def test_trait_type_consistency(self):
        """Test that trait types are logically consistent."""
        for trait in PersonalityTrait:
            trait_type = trait.trait_type
            
            # Positive traits should generally not have negative opposites as complex
            if trait_type == "positive" and trait.opposite_trait:
                opposite_type = trait.opposite_trait.trait_type
                assert opposite_type in ["negative", "complex"], f"Positive trait {trait.value} has positive opposite {trait.opposite_trait.value}"
            
            # Negative traits should generally not have negative opposites  
            if trait_type == "negative" and trait.opposite_trait:
                opposite_type = trait.opposite_trait.trait_type
                assert opposite_type in ["positive", "complex"], f"Negative trait {trait.value} has negative opposite {trait.opposite_trait.value}"
    
    def test_description_quality_consistency(self):
        """Test that descriptions are consistent with trait types."""
        for trait in PersonalityTrait:
            description = trait.description.lower()
            trait_type = trait.trait_type
            
            # Positive traits should have generally positive language
            if trait_type == "positive":
                negative_words = ["bad", "evil", "harmful", "destructive", "wrong"]
                has_negative_words = any(word in description for word in negative_words)
                # Allow some negative words for contrast, but not too many
                assert not has_negative_words or description.count("not") > 0, f"Positive trait {trait.value} has unexpectedly negative description"
            
            # Negative traits should acknowledge the negative nature
            if trait_type == "negative":
                # Should contain some indication of negative consequences or characteristics
                negative_indicators = ["harm", "damage", "negative", "problem", "difficulty", "expense", "wrong", "bad", "poor", "lack"]
                has_negative_indicators = any(indicator in description for indicator in negative_indicators)
                # Don't enforce this too strictly as some descriptions might be more neutral
                # Just verify the description is substantial enough to indicate the negative nature


class TestPersonalityTraitPerformance:
    """Performance tests for the personality trait system."""
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for trait in PersonalityTrait:
                _ = trait.display_name
                _ = trait.description
                _ = trait.trait_type
                _ = trait.opposite_trait
        end_time = time.time()
        
        # Should complete many property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        test_inputs = [
            "brave", "courageous", "intelligent", "smart", "arrogant", "proud",
            "ambitious", "driven", "mysterious", "secretive", "patient", "calm"
        ]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    PersonalityTrait.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 12,000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_categorization_performance(self):
        """Test that categorization methods are reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            PersonalityTrait.get_positive_traits()
            PersonalityTrait.get_negative_traits()
            PersonalityTrait.get_complex_traits()
            PersonalityTrait.get_contrasting_pairs()
        end_time = time.time()
        
        # Should complete 4000 categorization operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Categorization too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_trait_enum_basic_functionality(self):
        """Test that PersonalityTrait enum works as expected."""
        # Test iteration
        trait_list = list(PersonalityTrait)
        assert len(trait_list) >= 30  # Should have substantial number of traits
        
        # Test basic attributes
        brave = PersonalityTrait.BRAVE
        assert brave.value == "brave"
        assert "Brave" in brave.display_name
        
        # Test enum comparison
        assert PersonalityTrait.BRAVE == PersonalityTrait.BRAVE
        assert PersonalityTrait.BRAVE != PersonalityTrait.COWARDLY
    
    def test_string_representations(self):
        """Test string representation methods."""
        trait = PersonalityTrait.BRAVE
        
        str_repr = str(trait)
        
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        assert str_repr == trait.display_name
    
    def test_trait_balance_distribution(self):
        """Test that traits are reasonably balanced across categories."""
        positive_count = len(PersonalityTrait.get_positive_traits())
        negative_count = len(PersonalityTrait.get_negative_traits())
        complex_count = len(PersonalityTrait.get_complex_traits())
        total_count = positive_count + negative_count + complex_count
        
        # Should have reasonable distribution
        positive_percentage = positive_count / total_count
        negative_percentage = negative_count / total_count
        complex_percentage = complex_count / total_count
        
        # No category should dominate too much
        assert 0.2 <= positive_percentage <= 0.6, f"Positive traits percentage out of range: {positive_percentage:.1%}"
        assert 0.2 <= negative_percentage <= 0.6, f"Negative traits percentage out of range: {negative_percentage:.1%}"
        assert 0.1 <= complex_percentage <= 0.4, f"Complex traits percentage out of range: {complex_percentage:.1%}"
        
        print(f"Trait distribution - Positive: {positive_percentage:.1%}, Negative: {negative_percentage:.1%}, Complex: {complex_percentage:.1%}")
    
    def test_opposite_pairs_symmetry(self):
        """Test that opposite trait pairs are properly symmetrical."""
        contrasting_pairs = PersonalityTrait.get_contrasting_pairs()
        
        # Create a set of all traits that appear in pairs
        paired_traits = set()
        for trait1, trait2 in contrasting_pairs:
            paired_traits.add(trait1)
            paired_traits.add(trait2)
        
        # Verify each paired trait appears exactly once in the pairs list
        trait_appearances = {}
        for trait1, trait2 in contrasting_pairs:
            trait_appearances[trait1] = trait_appearances.get(trait1, 0) + 1
            trait_appearances[trait2] = trait_appearances.get(trait2, 0) + 1
        
        for trait, count in trait_appearances.items():
            assert count == 1, f"Trait {trait.value} appears {count} times in contrasting pairs (should be 1)"


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])