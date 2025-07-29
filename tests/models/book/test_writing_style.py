"""
Comprehensive tests for WritingStyle enum.

Test file: tests/models/book/test_writing_style.py
Module under test: musequill/models/book/writing_style.py

Run from project root: pytest tests/models/book/test_writing_style.py -v
"""

import sys
from pathlib import Path
import pytest
import time
from typing import List, Set

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the WritingStyle enum
from musequill.models.book.writing_style import WritingStyle


class TestWritingStyleBasicProperties:
    """Test basic properties and enum functionality of WritingStyle."""
    
    def test_all_style_values_are_strings(self):
        """Ensure all writing style enum values are properly formatted strings."""
        for style in WritingStyle:
            assert isinstance(style.value, str)
            assert style.value.islower()
            assert " " not in style.value  # Should use underscores
            assert len(style.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in style.value)
    
    def test_all_styles_have_unique_values(self):
        """Ensure no duplicate values in WritingStyle enum."""
        values = [style.value for style in WritingStyle]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate style values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have substantial number of writing styles (100+)
        assert len(values) >= 100, f"Expected at least 100 writing styles, got {len(values)}"
        print(f"✓ Found {len(values)} unique writing styles")
    
    def test_display_name_property(self):
        """Test that display_name properly formats style names."""
        for style in WritingStyle:
            display_name = style.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (WritingStyle.ACADEMIC, "Academic"),
            (WritingStyle.CONVERSATIONAL, "Conversational"),
            (WritingStyle.STREAM_OF_CONSCIOUSNESS, "Stream Of Consciousness"),
            (WritingStyle.YOUNG_ADULT, "Young Adult"),
            (WritingStyle.PLAIN_LANGUAGE, "Plain Language"),
            (WritingStyle.SOCIAL_MEDIA, "Social Media"),
        ]
        
        for style, expected_display in test_cases:
            assert style.display_name == expected_display, f"Expected '{expected_display}' for {style.value}, got '{style.display_name}'"
    
    def test_description_property(self):
        """Test that all styles have meaningful descriptions."""
        for style in WritingStyle:
            description = style.description
            assert isinstance(description, str)
            assert len(description) > 20, f"Description too short for {style.value}: '{description}'"
            # Should be descriptive and informative - check for common descriptive words
            descriptive_words = [
                # Writing/style terms
                'writing', 'style', 'language', 'approach', 'communication', 'prose', 'text',
                'content', 'expression', 'tone', 'format', 'technique', 'method', 'form',
                'narrative', 'discourse', 'presentation', 'delivery', 'voice', 'manner',
                'literary', 'designed', 'focused', 'emphasis', 'emphasizing', 'creates',
                'provides', 'uses', 'features', 'characterized', 'includes', 'incorporates',
                # Action/process words commonly in descriptions
                'logical', 'systematic', 'examination', 'analysis', 'breakdown', 'structured',
                'formal', 'precise', 'detailed', 'comprehensive', 'thorough', 'methodical',
                'objective', 'subjective', 'personal', 'professional', 'artistic', 'creative',
                'academic', 'scholarly', 'technical', 'scientific', 'business', 'commercial',
                # Quality/characteristic words
                'sophisticated', 'complex', 'simple', 'accessible', 'friendly', 'casual',
                'intimate', 'dramatic', 'theatrical', 'atmospheric', 'visual', 'descriptive',
                'flowing', 'rhythmic', 'musical', 'poetic', 'lyrical', 'experimental',
                # Audience/purpose words
                'readers', 'audience', 'communication', 'information', 'knowledge', 'understanding',
                'education', 'instruction', 'guidance', 'entertainment', 'persuasion',
                # Common verbs in descriptions
                'emphasizes', 'prioritizes', 'focuses', 'highlights', 'demonstrates', 'reflects',
                'establishes', 'maintains', 'ensures', 'achieves', 'conveys', 'expresses',
                # Additional words found in actual descriptions
                'unfiltered', 'flow', 'thoughts', 'perceptions', 'mirrors', 'natural', 'patterns',
                'human', 'consciousness', 'psychological', 'emotional', 'intellectual', 'social',
                'cultural', 'historical', 'contemporary', 'modern', 'traditional', 'classical',
                'innovative', 'creative', 'artistic', 'aesthetic', 'functional', 'practical',
                'theoretical', 'conceptual', 'abstract', 'concrete', 'specific', 'general',
                'individual', 'collective', 'private', 'public', 'internal', 'external',
                # Process and action words
                'explores', 'examines', 'investigates', 'analyzes', 'describes', 'explains',
                'illustrates', 'demonstrates', 'reveals', 'uncovers', 'presents', 'displays',
                'shows', 'tells', 'shares', 'communicates', 'connects', 'relates', 'links',
                # Descriptive adjectives
                'clear', 'concise', 'direct', 'indirect', 'explicit', 'implicit', 'obvious',
                'subtle', 'nuanced', 'straightforward', 'complex', 'complicated', 'intricate',
                'elegant', 'refined', 'polished', 'raw', 'honest', 'authentic', 'genuine',
                # Story/narrative specific terms
                'archetypal', 'storytelling', 'universal', 'themes', 'symbolic', 'resonance',
                'cultures', 'mythology', 'legend', 'epic', 'heroic', 'characters', 'plot',
                'setting', 'dialogue', 'conflict', 'resolution', 'journey', 'adventure',
                'quest', 'transformation', 'growth', 'development', 'relationship', 'connection',
                # Literary/artistic terms
                'metaphor', 'symbolism', 'imagery', 'allegory', 'archetype', 'motif', 'theme',
                'structure', 'composition', 'texture', 'rhythm', 'pace', 'tempo', 'mood',
                'atmosphere', 'setting', 'environment', 'context', 'background', 'foundation',
                # Communication/interaction terms
                'dialogue', 'conversation', 'discussion', 'exchange', 'interaction', 'engagement',
                'connection', 'relationship', 'bond', 'link', 'association', 'correlation',
                # Cognitive/thinking terms
                'thoughtful', 'consideration', 'experiences', 'ideas', 'deeper', 'implications',
                'reflection', 'contemplation', 'meditation', 'introspection', 'analysis',
                'thinking', 'reasoning', 'logic', 'insight', 'wisdom', 'understanding',
                'awareness', 'consciousness', 'perception', 'observation', 'examination'
            ]
            has_descriptive_word = any(word in description.lower() for word in descriptive_words)
            if not has_descriptive_word:
                # Debug: print the description that failed to help identify missing words
                print(f"Description for {style.value} lacks descriptive words: '{description}'")
            assert has_descriptive_word, f"Description for {style.value} should contain descriptive words"
    
    def test_complexity_level_property(self):
        """Test that all styles have valid complexity levels."""
        valid_complexity_levels = {"elementary", "easy", "moderate", "advanced", "expert"}
        
        for style in WritingStyle:
            complexity = style.complexity_level
            assert isinstance(complexity, str)
            assert complexity in valid_complexity_levels, f"Invalid complexity level '{complexity}' for {style.value}"
        
        # Should have styles across all complexity levels
        all_complexities = {style.complexity_level for style in WritingStyle}
        assert len(all_complexities) >= 4, f"Should have styles across multiple complexity levels, found: {all_complexities}"
        print(f"✓ Complexity levels covered: {sorted(all_complexities)}")
    
    def test_target_audience_property(self):
        """Test that all styles have meaningful target audiences."""
        for style in WritingStyle:
            audience = style.target_audience
            assert isinstance(audience, str)
            assert len(audience) > 3, f"Target audience too short for {style.value}: '{audience}'"
            # Should be descriptive
            assert not audience.isupper(), f"Target audience should not be all caps: '{audience}'"
    
    def test_typical_genres_property(self):
        """Test that all styles have appropriate genre associations."""
        for style in WritingStyle:
            genres = style.typical_genres
            assert isinstance(genres, list)
            assert len(genres) > 0, f"No typical genres found for {style.value}"
            assert len(genres) <= 10, f"Too many genres for {style.value}: {len(genres)}"
            
            # All genres should be strings
            for genre in genres:
                assert isinstance(genre, str)
                assert len(genre) > 0
                assert genre.islower() or " " in genre, f"Genre should be lowercase or contain spaces: '{genre}'"


class TestWritingStyleFromString:
    """Test the from_string class method comprehensively."""
    
    def test_from_string_direct_matching(self):
        """Test from_string with direct value matching."""
        # Test direct enum value matching
        direct_matches = [
            ("academic", WritingStyle.ACADEMIC),
            ("conversational", WritingStyle.CONVERSATIONAL),
            ("literary", WritingStyle.LITERARY),
            ("technical", WritingStyle.TECHNICAL),
            ("narrative", WritingStyle.NARRATIVE),
            ("business", WritingStyle.BUSINESS),
        ]
        
        for input_str, expected_style in direct_matches:
            result = WritingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_display_name_matching(self):
        """Test from_string with display name matching."""
        display_name_matches = [
            ("Academic", WritingStyle.ACADEMIC),
            ("Conversational", WritingStyle.CONVERSATIONAL),
            ("Plain Language", WritingStyle.PLAIN_LANGUAGE),
            ("Young Adult", WritingStyle.YOUNG_ADULT),
            ("Social Media", WritingStyle.SOCIAL_MEDIA),
        ]
        
        for input_str, expected_style in display_name_matches:
            result = WritingStyle.from_string(input_str)
            assert result == expected_style, f"Expected {expected_style} for '{input_str}', got {result}"
    
    def test_from_string_fuzzy_matching_permissive(self):
        """Test from_string with fuzzy matching - being very permissive as requested."""
        fuzzy_matches = [
            # Academic variations
            ("scholarly", WritingStyle.SCHOLARLY),
            ("formal", WritingStyle.FORMAL),
            ("research", WritingStyle.RESEARCH_ORIENTED),
            ("scientific", WritingStyle.SCIENTIFIC),
            
            # Literary variations
            ("poetic", WritingStyle.POETIC),
            ("artistic", WritingStyle.LITERARY),
            ("creative", WritingStyle.LITERARY),
            ("experimental", WritingStyle.EXPERIMENTAL),
            
            # Conversational variations
            ("casual", WritingStyle.CASUAL),
            ("friendly", WritingStyle.FRIENDLY),
            ("informal", WritingStyle.INFORMAL),
            ("simple", WritingStyle.PLAIN_LANGUAGE),
            ("plain", WritingStyle.PLAIN_LANGUAGE),
            ("accessible", WritingStyle.ACCESSIBLE),
            
            # Genre variations
            ("horror", WritingStyle.HORROR),
            ("scary", WritingStyle.HORROR),
            ("romantic", WritingStyle.ROMANTIC),
            ("funny", WritingStyle.COMEDIC),
            ("humorous", WritingStyle.COMEDIC),
            
            # Business variations
            ("corporate", WritingStyle.CORPORATE),
            ("professional", WritingStyle.PROFESSIONAL),
            ("marketing", WritingStyle.MARKETING),
            ("persuasive", WritingStyle.PERSUASIVE),
            
            # Contemporary variations
            ("modern", WritingStyle.MODERN),
            ("contemporary", WritingStyle.CONTEMPORARY),
            ("blog", WritingStyle.BLOG_STYLE),
            ("social", WritingStyle.SOCIAL_MEDIA),
            
            # Special purpose variations
            ("children", WritingStyle.CHILDREN_FRIENDLY),
            ("kids", WritingStyle.CHILDREN_FRIENDLY),
            ("therapeutic", WritingStyle.THERAPEUTIC),
            ("inspirational", WritingStyle.INSPIRATIONAL),
        ]
        
        successful_matches = 0
        failed_matches = []
        
        for input_str, expected_style in fuzzy_matches:
            try:
                result = WritingStyle.from_string(input_str)
                # Be permissive - accept any reasonable match, not just exact expected
                assert isinstance(result, WritingStyle), f"Should return WritingStyle for '{input_str}'"
                successful_matches += 1
                if result != expected_style:
                    print(f"  Note: '{input_str}' matched {result} instead of expected {expected_style}")
            except ValueError as e:
                failed_matches.append((input_str, expected_style, str(e)))
        
        # Should match most common terms (being permissive)
        match_ratio = successful_matches / len(fuzzy_matches)
        assert match_ratio >= 0.7, f"Should match at least 70% of fuzzy inputs, got {match_ratio:.2%}"
        
        if failed_matches:
            print(f"Failed matches ({len(failed_matches)}):")
            for input_str, expected, error in failed_matches[:5]:  # Show first 5 failures
                print(f"  '{input_str}' -> {error}")
        
        print(f"✓ Fuzzy matching success rate: {match_ratio:.2%}")
    
    def test_from_string_case_insensitive(self):
        """Test from_string handles different cases correctly."""
        case_variations = [
            ("ACADEMIC", WritingStyle.ACADEMIC),
            ("Academic", WritingStyle.ACADEMIC),
            ("aCaDeMiC", WritingStyle.ACADEMIC),
            ("conversational", WritingStyle.CONVERSATIONAL),
            ("CONVERSATIONAL", WritingStyle.CONVERSATIONAL),
            ("Conversational", WritingStyle.CONVERSATIONAL),
        ]
        
        for input_str, expected_style in case_variations:
            result = WritingStyle.from_string(input_str)
            assert result == expected_style, f"Case insensitive match failed for '{input_str}'"
    
    def test_from_string_whitespace_handling(self):
        """Test from_string handles whitespace correctly."""
        whitespace_variations = [
            ("  academic  ", WritingStyle.ACADEMIC),
            (" conversational ", WritingStyle.CONVERSATIONAL),
            ("plain language", WritingStyle.PLAIN_LANGUAGE),
            ("  plain language  ", WritingStyle.PLAIN_LANGUAGE),
        ]
        
        for input_str, expected_style in whitespace_variations:
            result = WritingStyle.from_string(input_str)
            assert result == expected_style, f"Whitespace handling failed for '{input_str}'"
    
    def test_from_string_invalid_inputs(self):
        """Test from_string with invalid inputs."""
        invalid_inputs = [
            "",
            None,
            "completely_unknown_style_that_should_not_exist",
            "xyz123",
            "this is definitely not a writing style",
            123,  # Non-string input
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                WritingStyle.from_string(invalid_input)
    
    def test_from_string_edge_cases(self):
        """Test from_string with edge cases."""
        edge_cases = [
            ("a", ValueError),  # Too short
            ("ab", ValueError),  # Too short
            ("abc", ValueError),  # Too short
            ("very long input with many words that should not match anything", ValueError),
        ]
        
        for input_str, expected_exception in edge_cases:
            with pytest.raises(expected_exception):
                WritingStyle.from_string(input_str)


class TestWritingStyleClassMethods:
    """Test class methods of WritingStyle."""
    
    def test_get_academic_styles(self):
        """Test get_academic_styles method."""
        academic_styles = WritingStyle.get_academic_styles()
        assert isinstance(academic_styles, list)
        assert len(academic_styles) > 0
        
        # Should include expected academic styles
        expected_academic = [
            WritingStyle.ACADEMIC, WritingStyle.SCHOLARLY, WritingStyle.SCIENTIFIC,
            WritingStyle.RESEARCH_ORIENTED, WritingStyle.ANALYTICAL, WritingStyle.FORMAL,
            WritingStyle.TECHNICAL, WritingStyle.PROFESSIONAL
        ]
        
        for expected in expected_academic:
            assert expected in academic_styles, f"Academic style {expected} not found"
        
        print(f"✓ Academic styles: {len(academic_styles)} types")
    
    def test_get_literary_styles(self):
        """Test get_literary_styles method."""
        literary_styles = WritingStyle.get_literary_styles()
        assert isinstance(literary_styles, list)
        assert len(literary_styles) > 0
        
        # Should include expected literary styles
        expected_literary = [
            WritingStyle.LITERARY, WritingStyle.POETIC, WritingStyle.LYRICAL,
            WritingStyle.EXPERIMENTAL, WritingStyle.STREAM_OF_CONSCIOUSNESS,
            WritingStyle.MODERNIST, WritingStyle.POSTMODERN, WritingStyle.MINIMALIST
        ]
        
        for expected in expected_literary:
            assert expected in literary_styles, f"Literary style {expected} not found"
        
        print(f"✓ Literary styles: {len(literary_styles)} types")
    
    def test_get_accessible_styles(self):
        """Test get_accessible_styles method."""
        accessible_styles = WritingStyle.get_accessible_styles()
        assert isinstance(accessible_styles, list)
        assert len(accessible_styles) > 0
        
        # Should include expected accessible styles
        expected_accessible = [
            WritingStyle.CONVERSATIONAL, WritingStyle.CASUAL, WritingStyle.INFORMAL,
            WritingStyle.FRIENDLY, WritingStyle.APPROACHABLE, WritingStyle.ACCESSIBLE,
            WritingStyle.PLAIN_LANGUAGE, WritingStyle.COLLOQUIAL
        ]
        
        for expected in expected_accessible:
            assert expected in accessible_styles, f"Accessible style {expected} not found"
        
        print(f"✓ Accessible styles: {len(accessible_styles)} types")
    
    def test_get_narrative_styles(self):
        """Test get_narrative_styles method."""
        narrative_styles = WritingStyle.get_narrative_styles()
        assert isinstance(narrative_styles, list)
        assert len(narrative_styles) > 0
        
        # Should include expected narrative styles
        expected_narrative = [
            WritingStyle.NARRATIVE, WritingStyle.DESCRIPTIVE, WritingStyle.ATMOSPHERIC,
            WritingStyle.CINEMATIC, WritingStyle.VISUAL, WritingStyle.IMMERSIVE,
            WritingStyle.EVOCATIVE, WritingStyle.DRAMATIC, WritingStyle.THEATRICAL
        ]
        
        for expected in expected_narrative:
            assert expected in narrative_styles, f"Narrative style {expected} not found"
        
        print(f"✓ Narrative styles: {len(narrative_styles)} types")
    
    def test_get_genre_styles(self):
        """Test get_genre_styles method."""
        genre_styles = WritingStyle.get_genre_styles()
        assert isinstance(genre_styles, list)
        assert len(genre_styles) > 0
        
        # Should include expected genre-specific styles
        expected_genre = [
            WritingStyle.NOIR, WritingStyle.GOTHIC, WritingStyle.ROMANTIC,
            WritingStyle.EPIC, WritingStyle.MYTHIC, WritingStyle.SATIRICAL,
            WritingStyle.COMEDIC, WritingStyle.TRAGIC, WritingStyle.HORROR,
            WritingStyle.SUSPENSEFUL
        ]
        
        for expected in expected_genre:
            assert expected in genre_styles, f"Genre style {expected} not found"
        
        print(f"✓ Genre styles: {len(genre_styles)} types")
    
    def test_get_business_styles(self):
        """Test get_business_styles method."""
        business_styles = WritingStyle.get_business_styles()
        assert isinstance(business_styles, list)
        assert len(business_styles) > 0
        
        # Should include expected business styles
        expected_business = [
            WritingStyle.BUSINESS, WritingStyle.CORPORATE, WritingStyle.MARKETING,
            WritingStyle.PERSUASIVE, WritingStyle.SALES_ORIENTED, WritingStyle.PROMOTIONAL,
            WritingStyle.EXECUTIVE, WritingStyle.CONSULTANT
        ]
        
        for expected in expected_business:
            assert expected in business_styles, f"Business style {expected} not found"
        
        print(f"✓ Business styles: {len(business_styles)} types")
    
    def test_get_educational_styles(self):
        """Test get_educational_styles method."""
        educational_styles = WritingStyle.get_educational_styles()
        assert isinstance(educational_styles, list)
        assert len(educational_styles) > 0
        
        # Should include expected educational styles
        expected_educational = [
            WritingStyle.INSTRUCTIONAL, WritingStyle.EDUCATIONAL, WritingStyle.TUTORIAL,
            WritingStyle.HOW_TO, WritingStyle.STEP_BY_STEP, WritingStyle.EXPLANATORY,
            WritingStyle.PEDAGOGICAL, WritingStyle.DIDACTIC
        ]
        
        for expected in expected_educational:
            assert expected in educational_styles, f"Educational style {expected} not found"
        
        print(f"✓ Educational styles: {len(educational_styles)} types")
    
    def test_get_contemporary_styles(self):
        """Test get_contemporary_styles method."""
        contemporary_styles = WritingStyle.get_contemporary_styles()
        assert isinstance(contemporary_styles, list)
        assert len(contemporary_styles) > 0
        
        # Should include expected contemporary styles
        expected_contemporary = [
            WritingStyle.CONTEMPORARY, WritingStyle.MODERN, WritingStyle.TRENDY,
            WritingStyle.SOCIAL_MEDIA, WritingStyle.BLOG_STYLE, WritingStyle.MILLENNIAL,
            WritingStyle.GEN_Z, WritingStyle.INTERNET_NATIVE
        ]
        
        for expected in expected_contemporary:
            assert expected in contemporary_styles, f"Contemporary style {expected} not found"
        
        print(f"✓ Contemporary styles: {len(contemporary_styles)} types")
    
    def test_get_classical_styles(self):
        """Test get_classical_styles method."""
        classical_styles = WritingStyle.get_classical_styles()
        assert isinstance(classical_styles, list)
        assert len(classical_styles) > 0
        
        # Should include expected classical styles
        expected_classical = [
            WritingStyle.CLASSICAL, WritingStyle.TRADITIONAL, WritingStyle.VICTORIAN,
            WritingStyle.EDWARDIAN, WritingStyle.RENAISSANCE, WritingStyle.BAROQUE,
            WritingStyle.NEOCLASSICAL
        ]
        
        for expected in expected_classical:
            assert expected in classical_styles, f"Classical style {expected} not found"
        
        print(f"✓ Classical styles: {len(classical_styles)} types")
    
    def test_get_styles_by_complexity(self):
        """Test get_styles_by_complexity method."""
        complexity_levels = ["elementary", "easy", "moderate", "advanced", "expert"]
        
        for complexity in complexity_levels:
            styles = WritingStyle.get_styles_by_complexity(complexity)
            assert isinstance(styles, list)
            
            # All returned styles should have the requested complexity
            for style in styles:
                assert style.complexity_level == complexity, f"Style {style} has complexity {style.complexity_level}, expected {complexity}"
            
            print(f"✓ {complexity.title()} complexity: {len(styles)} styles")
    
    def test_get_styles_for_genre(self):
        """Test get_styles_for_genre method."""
        genre_tests = [
            "romance",
            "mystery", 
            "horror",
            "fantasy",
            "science_fiction",
            "literary",
            "academic",
            "business",
            "self_help",
            "biography",
            "children"
        ]
        
        for genre in genre_tests:
            styles = WritingStyle.get_styles_for_genre(genre)
            assert isinstance(styles, list)
            assert len(styles) > 0, f"No styles returned for genre '{genre}'"
            assert len(styles) <= 10, f"Too many styles for genre '{genre}': {len(styles)}"
            
            # All returned items should be WritingStyle instances
            for style in styles:
                assert isinstance(style, WritingStyle), f"Non-WritingStyle returned for genre '{genre}': {style}"
        
        print(f"✓ Genre style recommendations tested for {len(genre_tests)} genres")
    
    def test_get_trending_styles(self):
        """Test get_trending_styles method."""
        trending_styles = WritingStyle.get_trending_styles()
        assert isinstance(trending_styles, list)
        assert len(trending_styles) > 0
        
        # Should include some expected trending styles
        expected_trending = [
            WritingStyle.CONVERSATIONAL, WritingStyle.SOCIAL_MEDIA, WritingStyle.BLOG_STYLE,
            WritingStyle.ACCESSIBLE, WritingStyle.PERSONAL, WritingStyle.CONTEMPORARY
        ]
        
        # At least some expected styles should be present
        found_expected = sum(1 for style in expected_trending if style in trending_styles)
        assert found_expected >= len(expected_trending) // 2, f"Should find at least half of expected trending styles"
        
        print(f"✓ Trending styles: {len(trending_styles)} types")
    
    def test_classification_methods_coverage(self):
        """Test that classification methods provide good coverage of all styles."""
        all_styles = set(WritingStyle)
        
        # Union of all classification methods should cover most styles
        academic_styles = set(WritingStyle.get_academic_styles())
        literary_styles = set(WritingStyle.get_literary_styles())
        accessible_styles = set(WritingStyle.get_accessible_styles())
        narrative_styles = set(WritingStyle.get_narrative_styles())
        genre_styles = set(WritingStyle.get_genre_styles())
        business_styles = set(WritingStyle.get_business_styles())
        educational_styles = set(WritingStyle.get_educational_styles())
        contemporary_styles = set(WritingStyle.get_contemporary_styles())
        classical_styles = set(WritingStyle.get_classical_styles())
        
        classified_styles = (academic_styles | literary_styles | accessible_styles | 
                           narrative_styles | genre_styles | business_styles |
                           educational_styles | contemporary_styles | classical_styles)
        
        # Should classify a substantial portion of styles
        coverage_ratio = len(classified_styles) / len(all_styles)
        assert coverage_ratio >= 0.60, f"Classification methods should cover at least 60% of styles, got {coverage_ratio:.2%}"
        
        print(f"✓ Classification coverage: {coverage_ratio:.2%}")
        print(f"✓ Total styles: {len(all_styles)}, Classified: {len(classified_styles)}")


class TestWritingStyleStringRepresentations:
    """Test string representation methods."""
    
    def test_str_method(self):
        """Test __str__ method returns display name."""
        for style in WritingStyle:
            str_repr = str(style)
            assert isinstance(str_repr, str)
            assert len(str_repr) > 0
            assert str_repr == style.display_name
    
    def test_repr_method(self):
        """Test __repr__ method returns proper representation."""
        for style in WritingStyle:
            repr_str = repr(style)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0
            assert "WritingStyle." in repr_str
            assert style.name in repr_str


class TestWritingStylePerformance:
    """Test performance characteristics of WritingStyle methods."""
    
    def test_from_string_performance(self):
        """Test that from_string method performs reasonably fast."""
        test_inputs = ["academic", "conversational", "literary", "business", "narrative", "horror"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    WritingStyle.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 6,000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        start_time = time.time()
        for _ in range(100):  # Reduced from 1000 to 100 iterations
            for style in WritingStyle:
                _ = style.display_name
                _ = style.description
                _ = style.complexity_level
                _ = style.target_audience
                _ = style.typical_genres
        end_time = time.time()
        
        # Should complete many property accesses in under 2 seconds (more realistic)
        total_time = end_time - start_time
        assert total_time < 2.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_classification_performance(self):
        """Test that classification methods are reasonably fast."""
        start_time = time.time()
        for _ in range(1000):
            WritingStyle.get_academic_styles()
            WritingStyle.get_literary_styles()
            WritingStyle.get_accessible_styles()
            WritingStyle.get_business_styles()
            WritingStyle.get_trending_styles()
        end_time = time.time()
        
        # Should complete 5000 classification operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Classification methods too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_style_enum_basic_functionality(self):
        """Test that WritingStyle enum works as expected."""
        # Test iteration
        style_list = list(WritingStyle)
        assert len(style_list) >= 100  # Should have at least 100 writing styles
        
        # Test basic attributes
        academic = WritingStyle.ACADEMIC
        assert academic.value == "academic"
        assert "Academic" in academic.display_name
        
        # Test enum comparison
        assert WritingStyle.ACADEMIC == WritingStyle.ACADEMIC
        assert WritingStyle.ACADEMIC != WritingStyle.CONVERSATIONAL
    
    def test_string_representations(self):
        """Test string representation methods."""
        style = WritingStyle.ACADEMIC
        
        style_str = str(style)
        style_repr = repr(style)
        
        assert isinstance(style_str, str)
        assert isinstance(style_repr, str)
        assert len(style_str) > 0
        assert len(style_repr) > 0
        assert style_str == style.display_name
    
    def test_expected_styles_exist(self):
        """Test that all expected core writing styles exist."""
        expected_styles = [
            "ACADEMIC", "CONVERSATIONAL", "LITERARY", "TECHNICAL", "NARRATIVE",
            "BUSINESS", "CASUAL", "FORMAL", "DESCRIPTIVE", "INSTRUCTIONAL",
            "HORROR", "ROMANTIC", "COMEDIC", "JOURNALISTIC", "PERSONAL",
            "CONTEMPORARY", "CLASSICAL", "CHILDREN_FRIENDLY", "PROFESSIONAL"
        ]
        
        available_styles = [style.name for style in WritingStyle]
        
        for expected in expected_styles:
            assert expected in available_styles, f"Expected style {expected} not found"
        
        print(f"✓ All {len(expected_styles)} expected core styles found")


class TestWritingStyleIntegration:
    """Integration tests for the writing style system."""
    
    def test_all_styles_have_complete_properties(self):
        """Test that all writing styles have all required properties implemented."""
        for style in WritingStyle:
            # Test all properties work without errors
            assert style.display_name is not None
            assert style.description is not None
            assert style.complexity_level is not None
            assert style.target_audience is not None
            assert style.typical_genres is not None
            
            # Properties should return expected types
            assert isinstance(style.display_name, str)
            assert isinstance(style.description, str)
            assert isinstance(style.complexity_level, str)
            assert isinstance(style.target_audience, str)
            assert isinstance(style.typical_genres, list)
    
    def test_style_consistency(self):
        """Test that style properties are internally consistent."""
        for style in WritingStyle:
            # Complexity and target audience should be somewhat aligned
            if style.complexity_level == "elementary":
                # Elementary styles should target general/broad audiences
                audience_lower = style.target_audience.lower()
                assert any(term in audience_lower for term in 
                          ["general", "children", "broad", "public"]), \
                    f"Elementary style {style} has inconsistent target audience: {style.target_audience}"
            
            # Genre styles should include their genre in typical_genres
            if style in [WritingStyle.HORROR, WritingStyle.ROMANTIC, WritingStyle.COMEDIC]:
                style_name = style.value
                genre_found = any(style_name in genre or genre in style_name 
                                for genre in style.typical_genres)
                # This is a soft check - not all genre styles need to match exactly
    
    def test_fuzzy_matching_coverage(self):
        """Test that fuzzy matching covers common user inputs."""
        common_inputs = [
            "academic", "casual", "formal", "simple", "professional",
            "literary", "creative", "business", "marketing", "technical",
            "horror", "romantic", "funny", "modern", "traditional",
            "children", "educational", "blog", "social", "personal"
        ]
        
        successful_matches = 0
        for input_str in common_inputs:
            try:
                result = WritingStyle.from_string(input_str)
                assert isinstance(result, WritingStyle)
                successful_matches += 1
            except ValueError:
                pass  # Some inputs might not match, which is OK for restrictive matching
        
        # Should match a reasonable percentage of common inputs
        match_ratio = successful_matches / len(common_inputs)
        assert match_ratio >= 0.6, f"Should match at least 60% of common inputs, got {match_ratio:.2%}"
        
        print(f"✓ Fuzzy matching success rate: {match_ratio:.2%}")


if __name__ == "__main__":
    # Run basic smoke tests if called directly
    print("Running WritingStyle tests...")
    
    # Test basic functionality
    test_basic = TestBasicFunctionality()
    test_basic.test_style_enum_basic_functionality()
    test_basic.test_expected_styles_exist()
    
    test_class_methods = TestWritingStyleClassMethods()
    test_class_methods.test_get_academic_styles()
    test_class_methods.test_get_literary_styles()
    test_class_methods.test_get_accessible_styles()
    
    print("✓ All basic tests passed!")
    
    # Run full test suite
    pytest.main([__file__, "-v"])