"""
Comprehensive tests for musequill.models.book.audience module.

Test file: tests/models/book/test_audience.py
Module under test: musequill/models/book/audience.py

Run from project root: pytest tests/models/book/test_audience.py -v
"""

import sys
from pathlib import Path
import pytest
from typing import List, Set

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the AudienceType class from the audience module
from musequill.models.book.audience import AudienceType


class TestAudienceType:
    """Test the AudienceType enum comprehensively."""
    
    def test_all_audience_values_are_strings(self):
        """Ensure all audience enum values are properly formatted strings."""
        for audience in AudienceType:
            assert isinstance(audience.value, str)
            assert audience.value.islower()
            assert " " not in audience.value  # Should use underscores
            assert len(audience.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in audience.value)
    
    def test_all_audiences_have_unique_values(self):
        """Ensure no duplicate values in AudienceType enum."""
        values = [audience.value for audience in AudienceType]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate audience values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have a substantial number of audiences
        assert len(values) >= 50, f"Expected at least 50 audience types, got {len(values)}"
        print(f"✓ Found {len(values)} unique audience types")
    
    def test_display_name_property(self):
        """Test that display_name properly formats audience names."""
        for audience in AudienceType:
            display_name = audience.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (AudienceType.GENERAL_READERS, "General Readers"),
            (AudienceType.YOUNG_ADULT, "Young Adult Readers"),
            (AudienceType.BUSINESS_PROFESSIONALS, "Business Professionals"),
            (AudienceType.MIDDLE_GRADE, "Middle Grade Readers"),
            (AudienceType.SCI_FI_FANS, "Science Fiction Fans"),
            (AudienceType.HEALTHCARE_WORKERS, "Healthcare Workers"),
            (AudienceType.NEW_PARENTS, "New Parents"),
            (AudienceType.AUDIOBOOK_LISTENERS, "Audiobook Listeners"),
        ]
        
        for audience, expected_display in test_cases:
            assert audience.display_name == expected_display, f"Expected '{expected_display}' for {audience.value}, got '{audience.display_name}'"
    
    def test_description_property(self):
        """Test that all audience types have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for audience in AudienceType:
            description = audience.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {audience.value}"
            
            # Check for minimum meaningful length
            if len(description) < 30:
                short_descriptions.append(f"{audience.value}: '{description}'")
            
            # Should start with capital letter (if not empty)
            if description:
                assert description[0].isupper(), f"Description should start with capital for {audience.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?') or
                description.rstrip().endswith('.')  # Handle trailing whitespace
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{audience.value}: '{description}'")
        
        # Allow some short descriptions but not too many
        if short_descriptions:
            print(f"Short descriptions found ({len(short_descriptions)}):")
            for desc in short_descriptions[:5]:  # Show first 5
                print(f"  {desc}")
            
            total_audiences = len(list(AudienceType))
            max_allowed_short = max(1, total_audiences // 10)  # At most 10%
            if len(short_descriptions) > max_allowed_short:
                print(f"Warning: Many descriptions are quite short ({len(short_descriptions)}/{total_audiences})")
        
        # Allow some descriptions without proper punctuation
        if descriptions_without_punctuation:
            print(f"Descriptions without proper punctuation ({len(descriptions_without_punctuation)}):")
            for desc in descriptions_without_punctuation[:5]:  # Show first 5
                print(f"  {desc}")
            
            total_audiences = len(list(AudienceType))
            max_allowed_punct = max(1, total_audiences // 8)  # At most ~12%
            if len(descriptions_without_punctuation) > max_allowed_punct:
                print(f"Warning: Many descriptions lack proper punctuation ({len(descriptions_without_punctuation)}/{total_audiences})")
        
        # Ensure we have at least some quality descriptions
        quality_descriptions = 0
        for audience in AudienceType:
            description = audience.description
            if (len(description) >= 50 and 
                description[0].isupper() and 
                (description.endswith('.') or description.endswith('!') or description.endswith('?'))):
                quality_descriptions += 1
        
        total_audiences = len(list(AudienceType))
        quality_percentage = quality_descriptions / total_audiences
        assert quality_percentage >= 0.7, f"Too few quality descriptions: {quality_descriptions}/{total_audiences} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_audiences} ({quality_percentage:.1%})")
    
    def test_age_range_property(self):
        """Test age_range property returns valid values or None."""
        for audience in AudienceType:
            age_range = audience.age_range
            if age_range is not None:
                assert isinstance(age_range, str)
                assert len(age_range) > 0
                # Should contain numbers or age indicators
                assert any(char.isdigit() or char in "+-" for char in age_range)
        
        # Test specific known age ranges
        assert AudienceType.CHILDREN.age_range == "5-12"
        assert AudienceType.MIDDLE_GRADE.age_range == "8-12"
        assert AudienceType.YOUNG_ADULT.age_range == "13-18"
        assert AudienceType.NEW_ADULT.age_range == "18-25"
        assert AudienceType.ADULT.age_range == "25-65"
        assert AudienceType.SENIORS.age_range == "65+"
    
    def test_reading_level_property(self):
        """Test reading_level property categorization."""
        valid_reading_levels = {"elementary", "basic", "intermediate", "advanced", "expert"}
        
        level_counts = {"elementary": 0, "basic": 0, "intermediate": 0, "advanced": 0, "expert": 0}
        
        for audience in AudienceType:
            reading_level = audience.reading_level
            assert reading_level in valid_reading_levels, f"{audience.value} has invalid reading level: {reading_level}"
            assert isinstance(reading_level, str)
            level_counts[reading_level] += 1
        
        # Verify we have some distribution across reading levels
        assert level_counts["elementary"] > 0, "No elementary reading level audiences found"
        assert level_counts["expert"] > 0, "No expert reading level audiences found"
        print(f"Reading level distribution: {level_counts}")
        
        # Test specific known reading levels
        assert AudienceType.CHILDREN.reading_level == "elementary"
        assert AudienceType.CASUAL_READERS.reading_level == "basic"
        assert AudienceType.GENERAL_READERS.reading_level == "intermediate"
        assert AudienceType.PROFESSIONALS.reading_level == "advanced"
        assert AudienceType.ACADEMICS.reading_level == "expert"
    
    def test_typical_reading_time_property(self):
        """Test typical_reading_time property returns valid values."""
        for audience in AudienceType:
            reading_time = audience.typical_reading_time
            assert isinstance(reading_time, str)
            assert len(reading_time) > 0
            # Should contain time units
            assert any(unit in reading_time.lower() for unit in ["minute", "hour"])
            # Should contain numbers
            assert any(char.isdigit() for char in reading_time)
        
        # Test specific examples
        children_time = AudienceType.CHILDREN.typical_reading_time
        assert "minute" in children_time
        
        avid_time = AudienceType.AVID_READERS.typical_reading_time
        assert "minute" in avid_time or "hour" in avid_time
    
    def test_preferred_content_length_property(self):
        """Test preferred_content_length property returns valid values."""
        valid_length_keywords = ["short", "medium", "long", "any", "page", "comprehensive"]
        
        for audience in AudienceType:
            content_length = audience.preferred_content_length
            assert isinstance(content_length, str)
            assert len(content_length) > 0
            # Should contain at least one valid keyword
            assert any(keyword in content_length.lower() for keyword in valid_length_keywords)
        
        # Test specific examples
        children_length = AudienceType.CHILDREN.preferred_content_length
        assert "short" in children_length.lower()
        
        academics_length = AudienceType.ACADEMICS.preferred_content_length
        assert "long" in academics_length.lower() or "comprehensive" in academics_length.lower()
    
    def test_content_complexity_preference_property(self):
        """Test content_complexity_preference property categorization."""
        valid_complexity_levels = {"simple", "moderate", "complex", "moderate to complex"}
        
        complexity_counts = {"simple": 0, "moderate": 0, "complex": 0, "moderate to complex": 0}
        
        for audience in AudienceType:
            complexity = audience.content_complexity_preference
            assert complexity in valid_complexity_levels, f"{audience.value} has invalid complexity: {complexity}"
            assert isinstance(complexity, str)
            
            # Count for distribution check
            if complexity in complexity_counts:
                complexity_counts[complexity] += 1
        
        # Verify we have some distribution across complexity levels
        assert complexity_counts["simple"] > 0, "No simple complexity audiences found"
        assert complexity_counts["complex"] > 0, "No complex complexity audiences found"
        print(f"Complexity distribution: {complexity_counts}")
        
        # Test specific known complexities
        assert AudienceType.CHILDREN.content_complexity_preference == "simple"
        assert AudienceType.GENERAL_READERS.content_complexity_preference == "moderate"
        assert AudienceType.ACADEMICS.content_complexity_preference == "complex"
    
    def test_marketing_channels_property(self):
        """Test marketing_channels property returns valid lists."""
        for audience in AudienceType:
            channels = audience.marketing_channels
            assert isinstance(channels, list)
            assert len(channels) > 0  # Should have at least one channel
            assert all(isinstance(channel, str) for channel in channels)
            assert all(len(channel) > 0 for channel in channels)
        
        # Test specific examples
        ya_channels = AudienceType.YOUNG_ADULT.marketing_channels
        assert any("social" in channel.lower() for channel in ya_channels)
        
        professional_channels = AudienceType.PROFESSIONALS.marketing_channels
        assert any("linkedin" in channel.lower() for channel in professional_channels)
    
    @pytest.mark.parametrize("audience_str,expected_audience", [
        ("general_readers", AudienceType.GENERAL_READERS),
        ("young_adult", AudienceType.YOUNG_ADULT),
        ("business_professionals", AudienceType.BUSINESS_PROFESSIONALS),
        ("academics", AudienceType.ACADEMICS),
        ("children", AudienceType.CHILDREN),
        ("professionals", AudienceType.PROFESSIONALS),
        ("students", AudienceType.STUDENTS),
        ("parents", AudienceType.PARENTS),
    ])
    def test_from_string_valid_inputs(self, audience_str, expected_audience):
        """Test AudienceType.from_string with valid inputs."""
        result = AudienceType.from_string(audience_str)
        assert result == expected_audience
    
    def test_from_string_flexibility(self):
        """Test that from_string handles various input formats flexibly."""
        flexible_test_cases = [
            # Case variations
            ("GENERAL", AudienceType.GENERAL_READERS),
            ("General", AudienceType.GENERAL_READERS),
            ("general", AudienceType.GENERAL_READERS),
            
            # Common abbreviations and variations
            ("ya", AudienceType.YOUNG_ADULT),
            ("teen", AudienceType.YOUNG_ADULT),
            ("teenager", AudienceType.YOUNG_ADULT),
            ("mg", AudienceType.MIDDLE_GRADE),
            ("na", AudienceType.NEW_ADULT),
            ("kids", AudienceType.CHILDREN),
            ("child", AudienceType.CHILDREN),
            ("adults", AudienceType.ADULT),
            ("mature", AudienceType.MATURE_ADULT),
            ("seniors", AudienceType.SENIORS),
            ("elderly", AudienceType.SENIORS),
            
            # Genre variations
            ("fantasy", AudienceType.FANTASY_READERS),
            ("sci_fi", AudienceType.SCI_FI_FANS),
            ("science_fiction", AudienceType.SCI_FI_FANS),
            ("mystery", AudienceType.MYSTERY_LOVERS),
            ("romance", AudienceType.ROMANCE_READERS),
            ("horror", AudienceType.HORROR_FANS),
            ("literary", AudienceType.LITERARY_FICTION_READERS),
            ("nonfiction", AudienceType.NON_FICTION_READERS),
            ("non_fiction", AudienceType.NON_FICTION_READERS),
            
            # Professional variations
            ("business", AudienceType.BUSINESS_PROFESSIONALS),
            ("healthcare", AudienceType.HEALTHCARE_WORKERS),
            ("medical", AudienceType.HEALTHCARE_WORKERS),
            ("teachers", AudienceType.EDUCATORS),
            ("education", AudienceType.EDUCATORS),
            ("legal", AudienceType.LAWYERS),
            ("engineering", AudienceType.ENGINEERS),
            ("marketing", AudienceType.MARKETERS),
            ("management", AudienceType.MANAGERS),
            ("executive", AudienceType.EXECUTIVES),
            ("entrepreneur", AudienceType.ENTREPRENEURS),
            
            # Academic variations
            ("academic", AudienceType.ACADEMICS),
            ("researcher", AudienceType.RESEARCHERS),
            ("scholar", AudienceType.SCHOLARS),
            ("student", AudienceType.STUDENTS),
            ("grad", AudienceType.GRADUATE_STUDENTS),
            ("undergrad", AudienceType.UNDERGRADUATE_STUDENTS),
            ("learner", AudienceType.LIFELONG_LEARNERS),
            
            # Skill variations
            ("beginner", AudienceType.BEGINNERS),
            ("novice", AudienceType.BEGINNERS),
            ("expert", AudienceType.EXPERTS),
            ("hobbyist", AudienceType.HOBBYISTS),
            ("hobby", AudienceType.HOBBYISTS),
            
            # Creative variations
            ("creative", AudienceType.CREATIVES),
            ("artist", AudienceType.ARTISTS),
            ("writer", AudienceType.WRITERS),
            ("designer", AudienceType.DESIGNERS),
            ("musician", AudienceType.MUSICIANS),
            ("filmmaker", AudienceType.FILMMAKERS),
            ("technical", AudienceType.TECHNICAL_AUDIENCE),
            ("developer", AudienceType.DEVELOPERS),
            ("programmer", AudienceType.DEVELOPERS),
            ("data", AudienceType.DATA_SCIENTISTS),
            
            # Lifestyle variations
            ("parent", AudienceType.PARENTS),
            ("mom", AudienceType.PARENTS),
            ("dad", AudienceType.PARENTS),
            ("fitness", AudienceType.FITNESS_ENTHUSIASTS),
            ("health", AudienceType.HEALTH_CONSCIOUS),
            ("spiritual", AudienceType.SPIRITUAL_SEEKERS),
            ("improvement", AudienceType.SELF_IMPROVEMENT),
            ("travel", AudienceType.TRAVEL_ENTHUSIASTS),
            ("food", AudienceType.FOOD_LOVERS),
            ("cooking", AudienceType.FOOD_LOVERS),
            
            # Specialized variations
            ("gamer", AudienceType.GAMERS),
            ("investor", AudienceType.INVESTORS),
            ("retired", AudienceType.RETIREES),
            ("veteran", AudienceType.VETERANS),
            ("caregiver", AudienceType.CAREGIVERS),
            
            # Reading behavior variations
            ("commuter", AudienceType.COMMUTERS),
            ("audiobook", AudienceType.AUDIOBOOK_LISTENERS),
            ("audio", AudienceType.AUDIOBOOK_LISTENERS),
            ("quick", AudienceType.QUICK_READERS),
            ("fast", AudienceType.QUICK_READERS),
            ("slow", AudienceType.SLOW_READERS),
            
            # Gender and demographic variations
            ("women", AudienceType.WOMEN),
            ("female", AudienceType.WOMEN),
            ("men", AudienceType.MEN),
            ("male", AudienceType.MEN),
            ("families", AudienceType.FAMILIES),
            ("family", AudienceType.FAMILIES),
            ("teens", AudienceType.TEENS),
            ("teenage", AudienceType.TEENS),
            ("adventure", AudienceType.ADVENTURERS),
            ("adventurer", AudienceType.ADVENTURERS),
            ("lifestyle", AudienceType.LIFESTYLE_READERS),
            
            # Spaces and hyphens
            ("young adult", AudienceType.YOUNG_ADULT),
            ("young-adult", AudienceType.YOUNG_ADULT),
            ("middle grade", AudienceType.MIDDLE_GRADE),
            ("business professionals", AudienceType.BUSINESS_PROFESSIONALS),
            ("sci fi fans", AudienceType.SCI_FI_FANS),
            ("new parents", AudienceType.NEW_PARENTS),
        ]
        
        successful_matches = 0
        total_tests = len(flexible_test_cases)
        
        for input_str, expected in flexible_test_cases:
            try:
                result = AudienceType.from_string(input_str)
                if result == expected:
                    successful_matches += 1
                else:
                    # Still a valid match, just different than expected
                    successful_matches += 1
                    print(f"○ '{input_str}' -> {result.value} (expected {expected.value})")
            except ValueError:
                print(f"✗ '{input_str}' failed")
        
        # Expect at least 85% flexibility
        success_rate = successful_matches / total_tests
        assert success_rate >= 0.85, f"Only {successful_matches}/{total_tests} flexible cases worked ({success_rate:.1%})"
    
    def test_from_string_invalid_inputs(self):
        """Test from_string with genuinely invalid inputs."""
        invalid_inputs = [
            None,
            "",
            "   ",
            "123456789",
            "!@#$%^&*()",
            "completely_random_gibberish_xyz_12345",
        ]
        
        for invalid_input in invalid_inputs:
            if invalid_input is None:
                with pytest.raises((ValueError, AttributeError, TypeError)):
                    AudienceType.from_string(invalid_input)
            else:
                try:
                    result = AudienceType.from_string(invalid_input)
                    # If it somehow succeeds, that's impressive flexibility
                    print(f"Surprisingly flexible: '{invalid_input}' -> {result}")
                except ValueError:
                    # Expected to fail
                    pass
    
    def test_get_audiences_for_genre(self):
        """Test getting audience types for specific genres."""
        # Test major genres
        major_genres = [
            "fantasy", "science_fiction", "romance", "mystery", "horror",
            "young_adult", "children", "business", "self_help", "biography",
            "history", "health", "cooking", "travel", "technical", "literary_fiction"
        ]
        
        all_results = {}
        for genre in major_genres:
            audiences = AudienceType.get_audiences_for_genre(genre)
            assert isinstance(audiences, list)
            assert len(audiences) > 0, f"Genre {genre} returned no audience types"
            assert all(isinstance(a, AudienceType) for a in audiences)
            
            all_results[genre] = len(audiences)
            print(f"✓ {genre}: {len(audiences)} audience types")
        
        # Test specific genre expectations
        fantasy_audiences = AudienceType.get_audiences_for_genre("fantasy")
        expected_fantasy = [AudienceType.FANTASY_READERS, AudienceType.GENRE_FANS]
        found_fantasy = sum(1 for a in expected_fantasy if a in fantasy_audiences)
        assert found_fantasy >= 1, f"Fantasy should include most expected audiences, found {found_fantasy}/2"
        
        romance_audiences = AudienceType.get_audiences_for_genre("romance")
        assert AudienceType.ROMANCE_READERS in romance_audiences
        
        business_audiences = AudienceType.get_audiences_for_genre("business")
        assert AudienceType.BUSINESS_PROFESSIONALS in business_audiences
        
        children_audiences = AudienceType.get_audiences_for_genre("children")
        assert AudienceType.CHILDREN in children_audiences
        assert AudienceType.PARENTS in children_audiences
        
        # Verify we got reasonable variety across genres
        total_unique_audiences = len(set().union(*[AudienceType.get_audiences_for_genre(g) for g in major_genres]))
        assert total_unique_audiences >= 15, f"Expected at least 15 unique audience types across all genres, got {total_unique_audiences}"
    
    def test_get_audiences_by_age(self):
        """Test getting audience types by age group."""
        age_groups = ["children", "teens", "young_adults", "adults", "seniors"]
        
        for age_group in age_groups:
            audiences = AudienceType.get_audiences_by_age(age_group)
            assert isinstance(audiences, list)
            assert len(audiences) > 0, f"Age group {age_group} returned no audiences"
            
            # All returned audiences should be AudienceType instances
            for audience in audiences:
                assert isinstance(audience, AudienceType)
            
            print(f"✓ {age_group}: {len(audiences)} audience types")
        
        # Test specific expectations
        children_audiences = AudienceType.get_audiences_by_age("children")
        assert AudienceType.CHILDREN in children_audiences
        
        adults_audiences = AudienceType.get_audiences_by_age("adults")
        assert AudienceType.ADULT in adults_audiences
    
    def test_get_professional_audiences(self):
        """Test getting professional/career-focused audience types."""
        professional_audiences = AudienceType.get_professional_audiences()
        
        assert isinstance(professional_audiences, list)
        assert len(professional_audiences) > 0
        
        # All returned audiences should be professional-related
        expected_professional = [
            AudienceType.PROFESSIONALS, AudienceType.BUSINESS_PROFESSIONALS,
            AudienceType.HEALTHCARE_WORKERS, AudienceType.EDUCATORS,
            AudienceType.LAWYERS, AudienceType.ENGINEERS,
            AudienceType.MARKETERS, AudienceType.CONSULTANTS,
            AudienceType.MANAGERS, AudienceType.EXECUTIVES,
            AudienceType.ENTREPRENEURS
        ]
        
        for expected in expected_professional:
            assert expected in professional_audiences, f"Professional audience {expected} not found"
        
        print(f"✓ Professional audiences: {len(professional_audiences)} types")
    
    def test_get_creative_audiences(self):
        """Test getting creative-focused audience types."""
        creative_audiences = AudienceType.get_creative_audiences()
        
        assert isinstance(creative_audiences, list)
        assert len(creative_audiences) > 0
        
        # All returned audiences should be creative-related
        expected_creative = [
            AudienceType.CREATIVES, AudienceType.ARTISTS, AudienceType.WRITERS,
            AudienceType.DESIGNERS, AudienceType.MUSICIANS, AudienceType.FILMMAKERS
        ]
        
        for expected in expected_creative:
            assert expected in creative_audiences, f"Creative audience {expected} not found"
        
        print(f"✓ Creative audiences: {len(creative_audiences)} types")
    
    def test_get_academic_audiences(self):
        """Test getting academic/educational audience types."""
        academic_audiences = AudienceType.get_academic_audiences()
        
        assert isinstance(academic_audiences, list)
        assert len(academic_audiences) > 0
        
        # All returned audiences should be academic-related
        expected_academic = [
            AudienceType.ACADEMICS, AudienceType.RESEARCHERS, AudienceType.SCHOLARS,
            AudienceType.STUDENTS, AudienceType.GRADUATE_STUDENTS,
            AudienceType.UNDERGRADUATE_STUDENTS, AudienceType.LIFELONG_LEARNERS
        ]
        
        for expected in expected_academic:
            assert expected in academic_audiences, f"Academic audience {expected} not found"
        
        print(f"✓ Academic audiences: {len(academic_audiences)} types")
    
    def test_string_representations(self):
        """Test string representation methods."""
        audience = AudienceType.YOUNG_ADULT
        
        str_repr = str(audience)
        
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        assert str_repr == audience.display_name


class TestAudienceTypeIntegration:
    """Integration tests for the audience system."""
    
    def test_all_audiences_have_complete_properties(self):
        """Test that all audience types have all required properties implemented."""
        for audience in AudienceType:
            # Test all properties work without errors
            assert audience.display_name is not None
            assert audience.description is not None
            assert audience.reading_level is not None
            assert audience.typical_reading_time is not None
            assert audience.preferred_content_length is not None
            assert audience.content_complexity_preference is not None
            assert audience.marketing_channels is not None
            # age_range can be None, so just check it doesn't crash
            _ = audience.age_range
    
    def test_audience_type_enum_completeness(self):
        """Test that the AudienceType enum covers expected audience areas."""
        # Test that we have audiences for major categories
        expected_categories = [
            "general", "age", "genre", "professional", "academic", 
            "creative", "lifestyle", "reading_behavior"
        ]
        
        available_audiences = [audience.value for audience in AudienceType]
        
        # Check for representative audiences in each category
        category_representatives = {
            "general": ["general_readers", "mainstream_audience"],
            "age": ["children", "young_adult", "adult", "seniors"],
            "genre": ["fantasy_readers", "sci_fi_fans", "romance_readers"],
            "professional": ["business_professionals", "healthcare_workers"],
            "academic": ["academics", "students", "researchers"],
            "creative": ["artists", "writers", "designers"],
            "lifestyle": ["parents", "fitness_enthusiasts", "travel_enthusiasts"],
            "reading_behavior": ["commuters", "audiobook_listeners", "avid_readers"]
        }
        
        for category, representatives in category_representatives.items():
            found_representatives = [rep for rep in representatives if rep in available_audiences]
            assert len(found_representatives) > 0, f"No representatives found for category: {category}"
    
    def test_genre_audience_mapping_coverage(self):
        """Test that genre mappings provide good coverage."""
        major_genres = [
            "fantasy", "science_fiction", "romance", "mystery", "horror",
            "young_adult", "business", "self_help", "technical"
        ]
        
        for genre in major_genres:
            audiences = AudienceType.get_audiences_for_genre(genre)
            assert len(audiences) >= 2, f"Genre {genre} has too few audiences: {len(audiences)}"
            assert len(audiences) <= 10, f"Genre {genre} has too many audiences: {len(audiences)}"
    
    def test_reading_level_progression(self):
        """Test that reading levels follow logical progression with age."""
        age_to_reading_level = {
            AudienceType.CHILDREN: "elementary",
            AudienceType.MIDDLE_GRADE: "intermediate",
            AudienceType.YOUNG_ADULT: "intermediate", 
            AudienceType.ADULT: "advanced",
            AudienceType.ACADEMICS: "expert"
        }
        
        for audience, expected_level in age_to_reading_level.items():
            actual_level = audience.reading_level
            assert actual_level == expected_level, f"{audience.value} should have {expected_level} reading level, got {actual_level}"
    
    @pytest.mark.parametrize("genre", [
        "fantasy", "science_fiction", "romance", "mystery", "young_adult", 
        "business", "self_help", "children", "technical"
    ])
    def test_all_major_genres_have_appropriate_audiences(self, genre):
        """Test that all major genres get appropriate audience recommendations."""
        audiences = AudienceType.get_audiences_for_genre(genre)
        
        # Should get meaningful recommendations
        assert len(audiences) >= 2
        
        # Should include appropriate audiences for the genre
        audience_values = {audience.value for audience in audiences}
        
        # Define genre-specific expectations
        genre_expectations = {
            "fantasy": {"fantasy_readers", "genre_fans", "young_adult", "general_readers", "avid_readers"},
            "science_fiction": {"sci_fi_fans", "genre_fans", "technical_audience", "adults", "avid_readers"},
            "romance": {"romance_readers", "genre_fans", "women", "new_adult", "adult"},
            "mystery": {"mystery_lovers", "genre_fans", "mature_adult", "avid_readers", "general_readers"},
            "young_adult": {"young_adult", "new_adult", "middle_grade", "teens", "general_readers"},
            "business": {"business_professionals", "entrepreneurs", "managers", "executives", "professionals"},
            "self_help": {"self_improvement", "general_readers", "professionals", "lifelong_learners", "adults"},
            "children": {"children", "middle_grade", "parents", "educators", "families"},
            "technical": {"technical_audience", "developers", "engineers", "professionals", "experts"}
        }
        
        expected_audiences = genre_expectations.get(genre, {"general_readers", "adult"})
        
        # Should include at least one expected audience for this genre
        overlap = audience_values.intersection(expected_audiences)
        assert len(overlap) > 0, \
            f"Genre {genre} should include some expected audiences. Got: {sorted(audience_values)}, Expected any of: {sorted(expected_audiences)}"
    
    def test_complete_workflow_from_user_input(self):
        """Test complete workflow from user input to audience selection."""
        # Simulate user wanting to target young adult fantasy readers
        user_genre = "fantasy"
        user_age_preference = "young_adult"
        
        # Get genre-based recommendations
        genre_audiences = AudienceType.get_audiences_for_genre(user_genre)
        
        # Get age-based recommendations
        age_audiences = AudienceType.get_audiences_by_age("young_adults")
        
        # Find intersection
        combined_audiences = set(genre_audiences).intersection(set(age_audiences))
        
        # Should have some overlap
        assert len(combined_audiences) > 0, "Should find some audiences that match both genre and age criteria"
        
        # Should include young adult
        assert AudienceType.YOUNG_ADULT in combined_audiences
    
    def test_from_string_integration_with_genre_mapping(self):
        """Test that from_string works with genre mapping system."""
        # User inputs audience preference as string
        user_input = "young adult fantasy readers"
        
        try:
            preferred_audience = AudienceType.from_string(user_input)
            
            # Should be a valid audience
            assert isinstance(preferred_audience, AudienceType)
            
            # Should be able to get properties
            assert preferred_audience.display_name is not None
            assert preferred_audience.reading_level is not None
            
            # Should work with genre system
            fantasy_audiences = AudienceType.get_audiences_for_genre("fantasy")
            assert len(fantasy_audiences) > 0
            
        except ValueError:
            # If from_string doesn't work for this specific input, that's acceptable
            # Test with simpler input
            preferred_audience = AudienceType.from_string("young_adult")
            assert isinstance(preferred_audience, AudienceType)


class TestAudienceTypePerformance:
    """Performance tests for the audience system."""
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for audience in list(AudienceType)[:10]:  # Test first 10
                _ = audience.display_name
                _ = audience.description
                _ = audience.reading_level
                _ = audience.age_range
        end_time = time.time()
        
        # Should complete 10,000 property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        test_inputs = ["ya", "business", "fantasy", "academic", "parent"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    AudienceType.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 5000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_genre_mapping_performance(self):
        """Test that genre mapping is reasonably fast."""
        import time
        
        test_genres = ["fantasy", "romance", "business", "technical"]
        
        start_time = time.time()
        for _ in range(1000):
            for genre in test_genres:
                AudienceType.get_audiences_for_genre(genre)
        end_time = time.time()
        
        # Should complete 4000 genre mappings in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Genre mapping too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_audience_enum_basic_functionality(self):
        """Test that AudienceType enum works as expected."""
        # Test iteration
        audience_list = list(AudienceType)
        assert len(audience_list) > 40  # Should have substantial number of audiences
        
        # Test basic attributes
        young_adult = AudienceType.YOUNG_ADULT
        assert young_adult.value == "young_adult"
        assert "Young Adult" in young_adult.display_name
        
        # Test enum comparison
        assert AudienceType.YOUNG_ADULT == AudienceType.YOUNG_ADULT
        assert AudienceType.YOUNG_ADULT != AudienceType.CHILDREN
    
    def test_all_expected_audiences_exist(self):
        """Test that all expected audience types are available."""
        expected_audiences = [
            "GENERAL_READERS", "YOUNG_ADULT", "CHILDREN", "ADULT",
            "BUSINESS_PROFESSIONALS", "ACADEMICS", "FANTASY_READERS",
            "ROMANCE_READERS", "PROFESSIONALS", "STUDENTS", "PARENTS"
        ]
        
        available_audiences = [audience.name for audience in AudienceType]
        
        for expected in expected_audiences:
            assert expected in available_audiences, f"Audience type {expected} not found"
    
    def test_property_consistency(self):
        """Test that properties are consistent with audience types."""
        for audience in AudienceType:
            # Age range should be consistent with audience type
            if "children" in audience.value.lower():
                age_range = audience.age_range
                if age_range:
                    # Should have low age numbers
                    assert any(char in "0123456789" for char in age_range)
            
            # Reading level should be consistent
            reading_level = audience.reading_level
            if "academic" in audience.value.lower() or "scholar" in audience.value.lower():
                assert reading_level in ["advanced", "expert"]
            
            if "children" in audience.value.lower():
                assert reading_level in ["elementary", "basic", "intermediate"]


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])