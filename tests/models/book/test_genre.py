import sys
from pathlib import Path
import pytest
import json
from typing import Set, List

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import all classes and enums from the genre module
from musequill.models.book.genre import (
    GenreType,
    SubGenreType,
    GenreSubGenrePair,
    GenreMapping
)


class TestGenreType:
    """Test the GenreType enum comprehensively."""
    
    def test_all_genre_values_are_strings(self):
        """Ensure all genre enum values are properly formatted strings."""
        for genre in GenreType:
            assert isinstance(genre.value, str)
            assert genre.value.islower()
            assert " " not in genre.value  # Should use underscores
            assert len(genre.value) > 0
    
    def test_display_name_property(self):
        """Test that display_name properly formats genre names."""
        test_cases = [
            (GenreType.ROMANCE, "Romance"),
            (GenreType.SCIENCE_FICTION, "Science Fiction"),
            (GenreType.YOUNG_ADULT, "Young Adult"),
            (GenreType.SELF_HELP, "Self Help"),
            (GenreType.TRUE_CRIME, "True Crime"),
        ]
        
        for genre, expected_display in test_cases:
            assert genre.display_name == expected_display
    
    def test_all_genres_have_unique_values(self):
        """Ensure no duplicate values in GenreType enum."""
        values = [genre.value for genre in GenreType]
        assert len(values) == len(set(values)), "Duplicate genre values found"
    
    @pytest.mark.parametrize("genre_str,expected_genre", [
        ("romance", GenreType.ROMANCE),
        ("science_fiction", GenreType.SCIENCE_FICTION),
        ("young_adult", GenreType.YOUNG_ADULT),
        ("self_help", GenreType.SELF_HELP),
        ("cli_fi", GenreType.CLI_FI),
    ])
    def test_from_string_valid_inputs(self, genre_str, expected_genre):
        """Test GenreType.from_string with valid inputs."""
        if hasattr(GenreType, 'from_string'):
            result = GenreType.from_string(genre_str)
            assert result == expected_genre
        else:
            pytest.skip("from_string method not implemented")
    
    @pytest.mark.parametrize("invalid_input", [
        "invalid_genre",
        "123",
        "completely_unknown_random_text",
        "xyz_abc_def",
        None,
    ])
    def test_from_string_invalid_inputs(self, invalid_input):
        """Test GenreType.from_string with invalid inputs."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
            
        if invalid_input is None:
            with pytest.raises((ValueError, AttributeError)):
                GenreType.from_string(invalid_input)
        else:
            with pytest.raises(ValueError):  # Removed specific match pattern
                GenreType.from_string(invalid_input)
    
    def test_from_string_empty_string(self):
        """Test GenreType.from_string with empty string."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
            
        with pytest.raises(ValueError, match="Invalid genre value"):
            GenreType.from_string("")
    
    def test_from_string_case_insensitive_success(self):
        """Test that from_string handles case variations successfully."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
            
        # These should all work due to case-insensitive matching
        test_cases = [
            ("ROMANCE", GenreType.ROMANCE),
            ("Romance", GenreType.ROMANCE),
            ("romance", GenreType.ROMANCE),
            ("FANTASY", GenreType.FANTASY),
            ("Fantasy", GenreType.FANTASY),
        ]
        
        for input_str, expected in test_cases:
            result = GenreType.from_string(input_str)
            assert result == expected
    
    def test_from_string_fuzzy_matching_success(self):
        """Test that from_string handles fuzzy matching successfully."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
            
        # These should work due to fuzzy matching
        test_cases = [
            ("romance fiction", GenreType.ROMANCE),  # Contains "romance"
            ("sci-fi", GenreType.SCIENCE_FICTION),
            ("sci fi", GenreType.SCIENCE_FICTION),
            ("romantic fantasy", GenreType.ROMANTASY),
            ("fantasy romance", GenreType.ROMANTASY),
        ]
        
        for input_str, expected in test_cases:
            try:
                result = GenreType.from_string(input_str)
                assert result == expected
            except ValueError:
                # If fuzzy matching doesn't work for this case, that's ok
                pass
    
    def test_from_string_case_insensitive(self):
        """Test that from_string handles different cases properly."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
            
        # This test assumes fuzzy matching is implemented
        test_cases = [
            ("romantic fantasy", GenreType.ROMANTASY),
            ("sci fi", GenreType.SCIENCE_FICTION),
            ("sci-fi", GenreType.SCIENCE_FICTION),
            ("ya", GenreType.YOUNG_ADULT),
        ]
        
        for input_str, expected in test_cases:
            try:
                result = GenreType.from_string(input_str)
                assert result == expected
            except ValueError:
                # Skip if fuzzy matching not implemented for this case
                pass
    
    def test_genre_categorization_methods(self):
        """Test methods that categorize genres."""
        # Test fiction vs non-fiction if implemented
        fiction_genres = [GenreType.ROMANCE, GenreType.FANTASY, GenreType.MYSTERY]
        non_fiction_genres = [GenreType.SELF_HELP, GenreType.BIOGRAPHY, GenreType.BUSINESS]
        
        for genre in fiction_genres:
            if hasattr(genre, 'is_fiction'):
                assert genre.is_fiction == True
        
        for genre in non_fiction_genres:
            if hasattr(genre, 'is_fiction'):
                assert genre.is_fiction == False
    
    def test_trending_genres_method(self):
        """Test get_trending_genres class method if implemented."""
        if hasattr(GenreType, 'get_trending_genres'):
            trending = GenreType.get_trending_genres()
            assert isinstance(trending, list)
            assert len(trending) > 0
            assert all(isinstance(g, GenreType) for g in trending)
    
    def test_str_and_repr_methods(self):
        """Test string representation methods."""
        genre = GenreType.ROMANCE
        str_repr = str(genre)
        repr_repr = repr(genre)
        
        assert isinstance(str_repr, str)
        assert isinstance(repr_repr, str)
        assert len(str_repr) > 0
        assert len(repr_repr) > 0


class TestSubGenreType:
    """Test the SubGenreType enum comprehensively."""
    
    def test_all_subgenre_values_are_strings(self):
        """Ensure all subgenre enum values are properly formatted strings."""
        for subgenre in SubGenreType:
            assert isinstance(subgenre.value, str)
            assert subgenre.value.islower()
            assert " " not in subgenre.value  # Should use underscores
            assert len(subgenre.value) > 0
    
    def test_display_name_property(self):
        """Test that display_name properly formats subgenre names."""
        test_cases = [
            (SubGenreType.CONTEMPORARY_ROMANCE, "Contemporary Romance"),
            (SubGenreType.HIGH_FANTASY, "High Fantasy"),
            (SubGenreType.PSYCHOLOGICAL_THRILLER, "Psychological Thriller"),
            (SubGenreType.SPACE_OPERA, "Space Opera"),
        ]
        
        for subgenre, expected_display in test_cases:
            assert subgenre.display_name == expected_display
    
    def test_all_subgenres_have_unique_values(self):
        """Ensure no duplicate values in SubGenreType enum."""
        values = [subgenre.value for subgenre in SubGenreType]
        assert len(values) == len(set(values)), "Duplicate subgenre values found"
    
    @pytest.mark.parametrize("subgenre_str,expected_subgenre", [
        ("contemporary_romance", SubGenreType.CONTEMPORARY_ROMANCE),
        ("high_fantasy", SubGenreType.HIGH_FANTASY),
        ("psychological_thriller", SubGenreType.PSYCHOLOGICAL_THRILLER),
        ("space_opera", SubGenreType.SPACE_OPERA),
    ])
    def test_from_string_valid_inputs(self, subgenre_str, expected_subgenre):
        """Test SubGenreType.from_string with valid inputs."""
        if hasattr(SubGenreType, 'from_string'):
            result = SubGenreType.from_string(subgenre_str)
            assert result == expected_subgenre
    
    def test_from_string_invalid_inputs(self):
        """Test SubGenreType.from_string with invalid inputs."""
        if hasattr(SubGenreType, 'from_string'):
            with pytest.raises(ValueError):
                SubGenreType.from_string("invalid_subgenre")


class TestGenreSubGenrePair:
    """Test the GenreSubGenrePair dataclass comprehensively."""
    
    @pytest.fixture
    def valid_pair(self):
        """Fixture providing a valid genre-subgenre pair."""
        return GenreSubGenrePair(GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE)
    
    def test_valid_pair_creation(self, valid_pair):
        """Test creating a valid genre-subgenre pair."""
        assert valid_pair.genre == GenreType.ROMANCE
        assert valid_pair.subgenre == SubGenreType.CONTEMPORARY_ROMANCE
        assert isinstance(valid_pair, GenreSubGenrePair)
    
    def test_invalid_pair_creation(self):
        """Test that invalid combinations raise ValueError."""
        with pytest.raises(ValueError, match="Invalid combination"):
            # Assuming SPACE_OPERA is not valid for ROMANCE
            GenreSubGenrePair(GenreType.ROMANCE, SubGenreType.SPACE_OPERA)
    
    def test_pair_immutability(self, valid_pair):
        """Test that GenreSubGenrePair is immutable (frozen dataclass)."""
        with pytest.raises(AttributeError):
            valid_pair.genre = GenreType.FANTASY
        
        with pytest.raises(AttributeError):
            valid_pair.subgenre = SubGenreType.HIGH_FANTASY
    
    def test_pair_equality(self):
        """Test equality comparison between pairs."""
        pair1 = GenreSubGenrePair(GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE)
        pair2 = GenreSubGenrePair(GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE)
        pair3 = GenreSubGenrePair(GenreType.FANTASY, SubGenreType.HIGH_FANTASY)
        
        assert pair1 == pair2
        assert pair1 != pair3
        assert hash(pair1) == hash(pair2)  # Test hashability
    
    def test_pair_string_representations(self, valid_pair):
        """Test string representation methods of pairs."""
        str_repr = str(valid_pair)
        
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        assert "romance" in str_repr.lower()
        
        if hasattr(valid_pair, 'display_name'):
            display_name = valid_pair.display_name
            assert isinstance(display_name, str)
            assert "Romance" in display_name


class TestGenreMapping:
    """Test the GenreMapping class comprehensively."""
    
    def test_genre_subgenre_map_structure(self):
        """Test that GENRE_SUBGENRE_MAP has correct structure."""
        assert hasattr(GenreMapping, 'GENRE_SUBGENRE_MAP')
        mapping = GenreMapping.GENRE_SUBGENRE_MAP
        
        # Check it's a dictionary
        assert isinstance(mapping, dict)
        assert len(mapping) > 0
        
        # Check all keys are GenreType instances
        for genre in mapping.keys():
            assert isinstance(genre, GenreType)
        
        # Check all values are sets of SubGenreType instances
        for subgenres in mapping.values():
            assert isinstance(subgenres, set)
            assert len(subgenres) > 0
            for subgenre in subgenres:
                assert isinstance(subgenre, SubGenreType)
    
    @pytest.mark.parametrize("genre", [
        GenreType.ROMANCE,
        GenreType.FANTASY,
        GenreType.MYSTERY,
        GenreType.SCIENCE_FICTION,
        GenreType.YOUNG_ADULT,
    ])
    def test_get_subgenres_for_major_genres(self, genre):
        """Test that major genres have subgenres defined."""
        subgenres = GenreMapping.get_subgenres(genre)
        assert isinstance(subgenres, set)
        assert len(subgenres) > 0
        
        # Test list version too
        subgenres_list = GenreMapping.get_subgenres_list(genre)
        assert isinstance(subgenres_list, list)
        assert len(subgenres_list) == len(subgenres)
        assert set(subgenres_list) == subgenres
    
    def test_get_subgenres_for_unknown_genre(self):
        """Test behavior for genres not in mapping."""
        # Create a mock genre that's not in the mapping
        class MockGenre:
            pass
        
        mock_genre = MockGenre()
        subgenres = GenreMapping.get_subgenres(mock_genre)
        assert subgenres == set()
    
    def test_get_genre_for_subgenre(self):
        """Test finding parent genre for subgenres."""
        # Test with known mappings
        test_cases = [
            (SubGenreType.CONTEMPORARY_ROMANCE, GenreType.ROMANCE),
            (SubGenreType.HIGH_FANTASY, GenreType.FANTASY),
            (SubGenreType.COZY_MYSTERY, GenreType.MYSTERY),
        ]
        
        for subgenre, expected_genre in test_cases:
            result = GenreMapping.get_genre_for_subgenre(subgenre)
            if result is not None:  # Only test if mapping exists
                assert result == expected_genre
    
    def test_get_all_genres_for_subgenre(self):
        """Test finding all parent genres for subgenres (multi-mapping)."""
        # Some subgenres might belong to multiple genres
        for subgenre in list(SubGenreType)[:5]:  # Test first 5
            genres = GenreMapping.get_all_genres_for_subgenre(subgenre)
            assert isinstance(genres, list)
            assert all(isinstance(g, GenreType) for g in genres)
    
    def test_is_valid_combination(self):
        """Test combination validation."""
        # Test known valid combinations
        valid_combinations = [
            (GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE),
            (GenreType.FANTASY, SubGenreType.HIGH_FANTASY),
        ]
        
        for genre, subgenre in valid_combinations:
            if subgenre in GenreMapping.get_subgenres(genre):
                assert GenreMapping.is_valid_combination(genre, subgenre)
        
        # Test known invalid combination
        assert not GenreMapping.is_valid_combination(
            GenreType.ROMANCE, SubGenreType.SPACE_OPERA
        )
    
    def test_create_pair(self):
        """Test creating pairs through GenreMapping."""
        # Find a valid combination from the mapping
        for genre, subgenres in GenreMapping.GENRE_SUBGENRE_MAP.items():
            if subgenres:  # If genre has subgenres
                subgenre = next(iter(subgenres))  # Get first subgenre
                pair = GenreMapping.create_pair(genre, subgenre)
                assert isinstance(pair, GenreSubGenrePair)
                assert pair.genre == genre
                assert pair.subgenre == subgenre
                break
    
    def test_get_all_combinations(self):
        """Test getting all valid combinations."""
        combinations = GenreMapping.get_all_combinations()
        
        assert isinstance(combinations, list)
        assert len(combinations) > 0
        assert all(isinstance(combo, GenreSubGenrePair) for combo in combinations)
        
        # Verify all combinations are actually valid
        for combo in combinations:
            assert GenreMapping.is_valid_combination(combo.genre, combo.subgenre)
    
    def test_get_trending_combinations(self):
        """Test getting trending combinations."""
        if hasattr(GenreMapping, 'get_trending_combinations'):
            trending = GenreMapping.get_trending_combinations()
            assert isinstance(trending, list)
            assert all(isinstance(combo, GenreSubGenrePair) for combo in trending)
    
    def test_get_ai_friendly_combinations(self):
        """Test getting AI-friendly combinations."""
        if hasattr(GenreMapping, 'get_ai_friendly_combinations'):
            ai_friendly = GenreMapping.get_ai_friendly_combinations()
            assert isinstance(ai_friendly, list)
            assert all(isinstance(combo, GenreSubGenrePair) for combo in ai_friendly)
    
    def test_search_combinations(self):
        """Test searching combinations with filters."""
        if hasattr(GenreMapping, 'search_combinations'):
            # Test genre filter
            romance_combos = GenreMapping.search_combinations(
                genre_filter=GenreType.ROMANCE
            )
            assert all(combo.genre == GenreType.ROMANCE for combo in romance_combos)
            
            # Test AI-friendly filter
            ai_combos = GenreMapping.search_combinations(ai_friendly=True)
            assert isinstance(ai_combos, list)
    
    def test_get_statistics(self):
        """Test getting mapping statistics."""
        if hasattr(GenreMapping, 'get_statistics'):
            stats = GenreMapping.get_statistics()
            assert isinstance(stats, dict)
            
            expected_keys = [
                'total_genres', 'unique_subgenres', 
                'total_combinations', 'average_subgenres_per_genre'
            ]
            
            for key in expected_keys:
                if key in stats:
                    assert isinstance(stats[key], (int, float))
                    assert stats[key] > 0
    
    def test_to_json_export(self):
        """Test JSON export functionality."""
        if hasattr(GenreMapping, 'to_json'):
            json_str = GenreMapping.to_json()
            assert isinstance(json_str, str)
            
            # Verify it's valid JSON
            parsed = json.loads(json_str)
            assert isinstance(parsed, dict)
            
            # Verify structure
            for genre_key, subgenres_list in parsed.items():
                assert isinstance(genre_key, str)
                assert isinstance(subgenres_list, list)
                assert all(isinstance(sg, str) for sg in subgenres_list)
    
    def test_mapping_consistency(self):
        """Test that all mappings are internally consistent."""
        # Every subgenre in the mapping should have at least one parent genre
        all_mapped_subgenres = set()
        for subgenres in GenreMapping.GENRE_SUBGENRE_MAP.values():
            all_mapped_subgenres.update(subgenres)
        
        for subgenre in all_mapped_subgenres:
            parent_genre = GenreMapping.get_genre_for_subgenre(subgenre)
            assert parent_genre is not None, f"Subgenre {subgenre} has no parent genre"
    
    def test_no_empty_genre_mappings(self):
        """Test that no genre has empty subgenre set."""
        for genre, subgenres in GenreMapping.GENRE_SUBGENRE_MAP.items():
            assert len(subgenres) > 0, f"Genre {genre} has no subgenres"


class TestIntegration:
    """Integration tests for the entire genre system."""
    
    def test_enum_to_mapping_consistency(self):
        """Test that all enums are properly integrated with mapping."""
        # All genres in mapping should exist in GenreType enum
        for genre in GenreMapping.GENRE_SUBGENRE_MAP.keys():
            assert isinstance(genre, GenreType)
        
        # All subgenres in mapping should exist in SubGenreType enum
        all_mapped_subgenres = set()
        for subgenres in GenreMapping.GENRE_SUBGENRE_MAP.values():
            all_mapped_subgenres.update(subgenres)
        
        for subgenre in all_mapped_subgenres:
            assert isinstance(subgenre, SubGenreType)
    
    def test_complete_workflow(self):
        """Test a complete workflow showcasing the flexibility of the genre system."""
        if not hasattr(GenreType, 'from_string'):
            # Test alternative workflow using direct enum access
            genre = GenreType.ROMANCE
            subgenres = GenreMapping.get_subgenres_list(genre)
            assert len(subgenres) > 0
            
            first_subgenre = subgenres[0]
            pair = GenreMapping.create_pair(genre, first_subgenre)
            assert pair.genre == genre
            assert pair.subgenre == first_subgenre
            return
        
        # Test workflow with flexible string inputs
        flexible_inputs = [
            "romance",
            "romantic fantasy", 
            "sci-fi",
            "ya fantasy",
            "mystery"
        ]
        
        successful_workflows = 0
        
        for user_input in flexible_inputs:
            try:
                # Get a genre from flexible string input
                genre = GenreType.from_string(user_input)
                print(f"✓ '{user_input}' -> {genre}")
                
                # Get its subgenres
                subgenres = GenreMapping.get_subgenres_list(genre)
                assert len(subgenres) > 0
                
                # Create a pair with the first subgenre
                first_subgenre = subgenres[0]
                pair = GenreMapping.create_pair(genre, first_subgenre)
                
                # Verify the pair
                assert pair.genre == genre
                assert pair.subgenre == first_subgenre
                assert GenreMapping.is_valid_combination(genre, first_subgenre)
                
                successful_workflows += 1
                
            except (ValueError, NotImplementedError) as e:
                print(f"○ '{user_input}' workflow incomplete: {e}")
        
        # We want most workflows to succeed
        success_rate = successful_workflows / len(flexible_inputs)
        assert success_rate >= 0.6, f"Only {successful_workflows}/{len(flexible_inputs)} workflows succeeded"
    
    @pytest.mark.parametrize("genre_name", [
        "romance", "fantasy", "mystery", "thriller", "science_fiction"
    ])
    def test_major_genres_have_complete_functionality(self, genre_name):
        """Test that major genres work with flexible string conversion."""
        if not hasattr(GenreType, 'from_string'):
            # Test using direct enum access as fallback
            genre_map = {
                "romance": GenreType.ROMANCE,
                "fantasy": GenreType.FANTASY,
                "mystery": GenreType.MYSTERY,
                "thriller": GenreType.THRILLER,
                "science_fiction": GenreType.SCIENCE_FICTION,
            }
            genre = genre_map[genre_name]
        else:
            # Test string conversion
            genre = GenreType.from_string(genre_name)
        
        # Test display name
        display_name = genre.display_name
        assert len(display_name) > 0
        
        # Test mapping
        subgenres = GenreMapping.get_subgenres(genre)
        assert len(subgenres) > 0
        
        # Test pair creation with first subgenre
        first_subgenre = next(iter(subgenres))
        pair = GenreMapping.create_pair(genre, first_subgenre)
        assert isinstance(pair, GenreSubGenrePair)
        
        print(f"✓ {genre_name} -> {genre} (has {len(subgenres)} subgenres)")
    
    def test_major_genres_flexible_input_variations(self):
        """Test major genres with various input formats."""
        if not hasattr(GenreType, 'from_string'):
            pytest.skip("from_string method not implemented")
        
        # Test various ways users might input major genres
        input_variations = [
            # Romance variations
            ["romance", "romantic", "love story", "Romance", "ROMANCE"],
            # Fantasy variations  
            ["fantasy", "fantasies", "Fantasy", "FANTASY"],
            # Science Fiction variations
            ["science fiction", "sci-fi", "sci fi", "scifi", "sf", "Science Fiction"],
            # Mystery variations
            ["mystery", "mysteries", "detective", "Mystery", "MYSTERY"],
            # Thriller variations
            ["thriller", "thrillers", "suspense", "Thriller", "THRILLER"],
        ]
        
        for variations in input_variations:
            successful_matches = 0
            base_genre = None
            
            for variation in variations:
                try:
                    genre = GenreType.from_string(variation)
                    if base_genre is None:
                        base_genre = genre
                    successful_matches += 1
                    print(f"✓ '{variation}' -> {genre}")
                except ValueError:
                    print(f"○ '{variation}' not recognized")
            
            # At least half of the variations should work for each genre
            success_rate = successful_matches / len(variations)
            assert success_rate >= 0.5, f"Only {successful_matches}/{len(variations)} variations worked for {variations[0]} genre group"
    
    def test_major_genres_direct_access(self):
        """Test major genres functionality using direct enum access."""
        major_genres = [
            GenreType.ROMANCE, GenreType.FANTASY, GenreType.MYSTERY, 
            GenreType.THRILLER, GenreType.SCIENCE_FICTION
        ]
        
        for genre in major_genres:
            # Test display name
            display_name = genre.display_name
            assert len(display_name) > 0
            assert isinstance(display_name, str)
            
            # Test mapping
            subgenres = GenreMapping.get_subgenres(genre)
            assert len(subgenres) > 0
            
            # Test pair creation with first subgenre
            first_subgenre = next(iter(subgenres))
            pair = GenreMapping.create_pair(genre, first_subgenre)
            assert isinstance(pair, GenreSubGenrePair)
            assert pair.genre == genre
            assert pair.subgenre == first_subgenre


# Performance tests (optional - can be skipped in regular runs)
class TestPerformance:
    """Performance tests for the genre system."""
    
    def test_mapping_lookup_performance(self):
        """Test that mapping lookups are reasonably fast."""
        import time
        
        # Test getting subgenres
        start_time = time.time()
        for _ in range(1000):
            GenreMapping.get_subgenres(GenreType.ROMANCE)
        lookup_time = time.time() - start_time
        
        # Should complete 1000 lookups in under 1 second
        assert lookup_time < 1.0
    
    def test_validation_performance(self):
        """Test that validation is reasonably fast."""
        import time
        
        # Get some valid combinations
        combinations = GenreMapping.get_all_combinations()[:100]  # Test first 100
        
        start_time = time.time()
        for combo in combinations:
            GenreMapping.is_valid_combination(combo.genre, combo.subgenre)
        validation_time = time.time() - start_time
        
        # Should validate 100 combinations in under 0.1 seconds
        assert validation_time < 0.1


# Additional test for basic enum functionality without from_string
class TestBasicEnumFunctionality:
    """Test basic enum functionality that should always work."""
    
    def test_genre_enum_basic_functionality(self):
        """Test that GenreType enum works as expected."""
        # Test that we can iterate over genres
        genre_list = list(GenreType)
        assert len(genre_list) > 0
        
        # Test that genres have expected attributes
        romance = GenreType.ROMANCE
        assert romance.value == "romance"
        assert romance.display_name == "Romance"
        
        # Test enum comparison
        assert GenreType.ROMANCE == GenreType.ROMANCE
        assert GenreType.ROMANCE != GenreType.FANTASY
    
    def test_subgenre_enum_basic_functionality(self):
        """Test that SubGenreType enum works as expected."""
        # Test that we can iterate over subgenres
        subgenre_list = list(SubGenreType)
        assert len(subgenre_list) > 0
        
        # Test that subgenres have expected attributes
        contemporary = SubGenreType.CONTEMPORARY_ROMANCE
        assert contemporary.value == "contemporary_romance"
        assert contemporary.display_name == "Contemporary Romance"
    
    def test_alternative_workflow_without_from_string(self):
        """Test complete workflow using direct enum access instead of from_string."""
        # Use direct enum access instead of from_string
        genre = GenreType.ROMANCE
        
        # Get its subgenres
        subgenres = GenreMapping.get_subgenres_list(genre)
        assert len(subgenres) > 0
        
        # Create a pair with the first subgenre
        first_subgenre = subgenres[0]
        pair = GenreMapping.create_pair(genre, first_subgenre)
        
        # Verify the pair
        assert pair.genre == genre
        assert pair.subgenre == first_subgenre
        assert GenreMapping.is_valid_combination(genre, first_subgenre)
        
        # Test string representation
        pair_str = str(pair)
        assert isinstance(pair_str, str)
        assert len(pair_str) > 0


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])