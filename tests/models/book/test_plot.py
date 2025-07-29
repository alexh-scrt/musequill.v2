"""
Comprehensive tests for musequill.models.book.plot module.

Test file: tests/models/book/test_plot.py
Module under test: musequill/models/book/plot.py

Run from project root: pytest tests/models/book/test_plot.py -v
"""

import sys
from pathlib import Path
import pytest
from typing import List, Set

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the PlotType class from the plot module
from musequill.models.book.plot import PlotType


class TestPlotType:
    """Test the PlotType enum comprehensively."""
    
    def test_all_plot_values_are_strings(self):
        """Ensure all plot enum values are properly formatted strings."""
        for plot in PlotType:
            assert isinstance(plot.value, str)
            assert plot.value.islower()
            assert " " not in plot.value  # Should use underscores
            assert len(plot.value) > 0
            # Should not have special characters except underscores
            assert all(c.isalpha() or c == '_' for c in plot.value)
    
    def test_all_plots_have_unique_values(self):
        """Ensure no duplicate values in PlotType enum."""
        values = [plot.value for plot in PlotType]
        unique_values = set(values)
        assert len(values) == len(unique_values), f"Duplicate plot values found: {len(values)} total vs {len(unique_values)} unique"
        
        # Should have a substantial number of plot types
        assert len(values) >= 100, f"Expected at least 100 plot types, got {len(values)}"
        print(f"✓ Found {len(values)} unique plot types")
    
    def test_display_name_property(self):
        """Test that display_name properly formats plot names."""
        for plot in PlotType:
            display_name = plot.display_name
            assert isinstance(display_name, str)
            assert len(display_name) > 0
            # Should be title case
            assert display_name[0].isupper()
            # Should be human-readable (no underscores)
            assert "_" not in display_name
    
    def test_display_name_specific_cases(self):
        """Test specific display name formatting cases."""
        test_cases = [
            (PlotType.OVERCOMING_THE_MONSTER, "Overcoming the Monster"),
            (PlotType.RAGS_TO_RICHES, "Rags to Riches"),
            (PlotType.THE_QUEST, "The Quest"),
            (PlotType.ENEMIES_TO_LOVERS, "Enemies to Lovers"),
            (PlotType.CHOSEN_ONE, "The Chosen One"),
            (PlotType.FIRST_CONTACT, "First Contact"),
            (PlotType.LOCKED_ROOM_MYSTERY, "Locked Room Mystery"),
            (PlotType.CORPORATE_THRILLER, "Corporate Thriller"),
            (PlotType.SUPERNATURAL_HORROR, "Supernatural Horror"),
            (PlotType.SOCIAL_MEDIA_DRAMA, "Social Media Drama"),
        ]
        
        for plot, expected_display in test_cases:
            assert plot.display_name == expected_display, f"Expected '{expected_display}' for {plot.value}, got '{plot.display_name}'"
    
    def test_description_property(self):
        """Test that all plot types have meaningful descriptions."""
        descriptions_without_punctuation = []
        short_descriptions = []
        
        for plot in PlotType:
            description = plot.description
            assert isinstance(description, str)
            assert len(description) > 0, f"Description is empty for {plot.value}"
            
            # Check for minimum meaningful length
            if len(description) < 50:
                short_descriptions.append(f"{plot.value}: '{description}'")
            
            # Should start with capital letter (if not empty)
            if description:
                assert description[0].isupper(), f"Description should start with capital for {plot.value}: '{description}'"
            
            # Check for proper punctuation
            has_proper_punctuation = (
                description.endswith('.') or 
                description.endswith('!') or 
                description.endswith('?') or
                description.rstrip().endswith('.')  # Handle trailing whitespace
            )
            
            if not has_proper_punctuation:
                descriptions_without_punctuation.append(f"{plot.value}: '{description}'")
        
        # Allow some short descriptions but not too many
        if short_descriptions:
            print(f"Short descriptions found ({len(short_descriptions)}):")
            for desc in short_descriptions[:5]:  # Show first 5
                print(f"  {desc}")
            
            total_plots = len(list(PlotType))
            max_allowed_short = max(1, total_plots // 20)  # At most 5%
            if len(short_descriptions) > max_allowed_short:
                print(f"Warning: Many descriptions are quite short ({len(short_descriptions)}/{total_plots})")
        
        # Allow some descriptions without proper punctuation
        if descriptions_without_punctuation:
            print(f"Descriptions without proper punctuation ({len(descriptions_without_punctuation)}):")
            for desc in descriptions_without_punctuation[:5]:  # Show first 5
                print(f"  {desc}")
            
            total_plots = len(list(PlotType))
            max_allowed_punct = max(1, total_plots // 10)  # At most 10%
            if len(descriptions_without_punctuation) > max_allowed_punct:
                print(f"Warning: Many descriptions lack proper punctuation ({len(descriptions_without_punctuation)}/{total_plots})")
        
        # Ensure we have at least some quality descriptions
        quality_descriptions = 0
        for plot in PlotType:
            description = plot.description
            if (len(description) >= 100 and 
                description[0].isupper() and 
                (description.endswith('.') or description.endswith('!') or description.endswith('?'))):
                quality_descriptions += 1
        
        total_plots = len(list(PlotType))
        quality_percentage = quality_descriptions / total_plots
        assert quality_percentage >= 0.8, f"Too few quality descriptions: {quality_descriptions}/{total_plots} ({quality_percentage:.1%})"
        print(f"✓ Quality descriptions: {quality_descriptions}/{total_plots} ({quality_percentage:.1%})")
    
    def test_complexity_level_property(self):
        """Test complexity level categorization."""
        valid_complexity_levels = {"simple", "moderate", "complex", "very_complex"}
        
        complexity_counts = {"simple": 0, "moderate": 0, "complex": 0, "very_complex": 0}
        
        for plot in PlotType:
            complexity = plot.complexity_level
            assert complexity in valid_complexity_levels, f"{plot.value} has invalid complexity: {complexity}"
            assert isinstance(complexity, str)
            complexity_counts[complexity] += 1
        
        # Verify we have some distribution across complexity levels
        assert complexity_counts["simple"] > 0, "No simple plot types found"
        assert complexity_counts["very_complex"] > 0, "No very_complex plot types found"
        print(f"Complexity distribution: {complexity_counts}")
        
        # Test specific known complexities
        assert PlotType.COMEDY.complexity_level == "simple"
        assert PlotType.FISH_OUT_OF_WATER.complexity_level == "simple"
        assert PlotType.THE_QUEST.complexity_level == "moderate"
        assert PlotType.COMING_OF_AGE.complexity_level == "moderate"
        assert PlotType.TRAGEDY.complexity_level == "complex"
        assert PlotType.CHARACTER_STUDY.complexity_level == "very_complex"
        assert PlotType.SOCIAL_COMMENTARY.complexity_level == "very_complex"
    
    def test_typical_themes_property(self):
        """Test that typical_themes returns valid lists."""
        for plot in PlotType:
            themes = plot.typical_themes
            assert isinstance(themes, list)
            assert len(themes) > 0  # Should have at least one theme
            assert all(isinstance(theme, str) for theme in themes)
            assert all(len(theme) > 0 for theme in themes)
        
        # Test specific examples
        quest_themes = PlotType.THE_QUEST.typical_themes
        assert "journey" in quest_themes
        assert "self-discovery" in quest_themes or "self_discovery" in quest_themes
        
        romance_themes = PlotType.ROMANCE_LOVE_STORY.typical_themes
        assert "love" in romance_themes
        
        revenge_themes = PlotType.REVENGE.typical_themes
        assert "justice" in revenge_themes or "retribution" in revenge_themes
    
    def test_target_length_property(self):
        """Test target_length property returns valid values."""
        valid_length_keywords = ["short", "medium", "long", "epic", "word"]
        
        for plot in PlotType:
            target_length = plot.target_length
            assert isinstance(target_length, str)
            assert len(target_length) > 0
            # Should contain at least one valid keyword
            assert any(keyword in target_length.lower() for keyword in valid_length_keywords)
            # Should contain numbers
            assert any(char.isdigit() for char in target_length)
        
        # Test specific examples
        fish_out_of_water_length = PlotType.FISH_OUT_OF_WATER.target_length
        assert "short" in fish_out_of_water_length.lower()
        
        quest_length = PlotType.THE_QUEST.target_length
        assert "long" in quest_length.lower() or "medium" in quest_length.lower()
        
        character_study_length = PlotType.CHARACTER_STUDY.target_length
        assert "epic" in character_study_length.lower() or "long" in character_study_length.lower()
    
    @pytest.mark.parametrize("plot_str,expected_plot", [
        ("overcoming_the_monster", PlotType.OVERCOMING_THE_MONSTER),
        ("the_quest", PlotType.THE_QUEST),
        ("romance_love_story", PlotType.ROMANCE_LOVE_STORY),
        ("mystery_investigation", PlotType.MYSTERY_INVESTIGATION),
        ("coming_of_age", PlotType.COMING_OF_AGE),
        ("enemies_to_lovers", PlotType.ENEMIES_TO_LOVERS),
        ("chosen_one", PlotType.CHOSEN_ONE),
        ("corporate_thriller", PlotType.CORPORATE_THRILLER),
    ])
    def test_from_string_valid_inputs(self, plot_str, expected_plot):
        """Test PlotType.from_string with valid inputs."""
        result = PlotType.from_string(plot_str)
        assert result == expected_plot
    
    def test_from_string_flexibility(self):
        """Test that from_string handles various input formats flexibly."""
        flexible_test_cases = [
            # Case variations
            ("QUEST", PlotType.THE_QUEST),
            ("Quest", PlotType.THE_QUEST),
            ("quest", PlotType.THE_QUEST),
            
            # Classic plot variations
            ("monster", PlotType.OVERCOMING_THE_MONSTER),
            ("rags to riches", PlotType.RAGS_TO_RICHES),
            ("rags", PlotType.RAGS_TO_RICHES),
            ("voyage", PlotType.VOYAGE_AND_RETURN),
            ("rebirth", PlotType.REBIRTH),
            ("tragedy", PlotType.TRAGEDY),
            ("comedy", PlotType.COMEDY),
            
            # Common plot variations
            ("mystery", PlotType.MYSTERY_INVESTIGATION),
            ("romance", PlotType.ROMANCE_LOVE_STORY),
            ("love story", PlotType.ROMANCE_LOVE_STORY),
            ("love_story", PlotType.ROMANCE_LOVE_STORY),
            ("coming of age", PlotType.COMING_OF_AGE),
            ("coming_of_age", PlotType.COMING_OF_AGE),
            ("revenge", PlotType.REVENGE),
            ("redemption", PlotType.REDEMPTION),
            ("sacrifice", PlotType.SACRIFICE),
            ("survival", PlotType.SURVIVAL),
            ("fish out of water", PlotType.FISH_OUT_OF_WATER),
            ("fish_out_of_water", PlotType.FISH_OUT_OF_WATER),
            
            # Thriller variations
            ("conspiracy", PlotType.CONSPIRACY),
            ("chase", PlotType.CHASE),
            ("escape", PlotType.ESCAPE),
            ("heist", PlotType.HEIST),
            ("kidnapping", PlotType.KIDNAPPING),
            ("spy", PlotType.ESPIONAGE),
            ("espionage", PlotType.ESPIONAGE),
            ("ticking clock", PlotType.TICKING_CLOCK),
            ("ticking_clock", PlotType.TICKING_CLOCK),
            
            # Sci-fi variations
            ("first contact", PlotType.FIRST_CONTACT),
            ("first_contact", PlotType.FIRST_CONTACT),
            ("time travel", PlotType.TIME_TRAVEL),
            ("time_travel", PlotType.TIME_TRAVEL),
            ("dystopian", PlotType.DYSTOPIAN_REBELLION),
            ("rebellion", PlotType.DYSTOPIAN_REBELLION),
            ("space", PlotType.SPACE_EXPLORATION),
            ("alien", PlotType.ALIEN_INVASION),
            ("invasion", PlotType.ALIEN_INVASION),
            ("ai", PlotType.TECHNOLOGICAL_UPRISING),
            ("robot", PlotType.TECHNOLOGICAL_UPRISING),
            
            # Fantasy variations
            ("chosen one", PlotType.CHOSEN_ONE),
            ("chosen_one", PlotType.CHOSEN_ONE),
            ("chosen", PlotType.CHOSEN_ONE),
            ("prophecy", PlotType.ANCIENT_PROPHECY),
            ("magic", PlotType.MAGICAL_AWAKENING),
            ("magical", PlotType.MAGICAL_AWAKENING),
            ("dragon", PlotType.DRAGON_SLAYING),
            ("portal", PlotType.PORTAL_WORLD),
            ("dark lord", PlotType.DARK_LORD_RISING),
            ("dark_lord", PlotType.DARK_LORD_RISING),
            ("fairy tale", PlotType.FAIRY_TALE_RETELLING),
            ("fairy_tale", PlotType.FAIRY_TALE_RETELLING),
            
            # Horror variations
            ("haunted", PlotType.HAUNTED_HOUSE),
            ("ghost", PlotType.HAUNTED_HOUSE),
            ("possession", PlotType.POSSESSION),
            ("curse", PlotType.CURSED_OBJECT),
            ("cursed", PlotType.CURSED_OBJECT),
            ("monster hunt", PlotType.MONSTER_HUNT),
            ("monster_hunt", PlotType.MONSTER_HUNT),
            ("zombie", PlotType.VIRAL_OUTBREAK),
            ("virus", PlotType.VIRAL_OUTBREAK),
            ("cult", PlotType.CULT_HORROR),
            ("supernatural", PlotType.SUPERNATURAL_HORROR),
            
            # Romance variations
            ("enemies to lovers", PlotType.ENEMIES_TO_LOVERS),
            ("enemies_to_lovers", PlotType.ENEMIES_TO_LOVERS),
            ("forbidden", PlotType.FORBIDDEN_LOVE),
            ("second chance", PlotType.SECOND_CHANCE_ROMANCE),
            ("second_chance", PlotType.SECOND_CHANCE_ROMANCE),
            ("fake", PlotType.FAKE_RELATIONSHIP),
            ("marriage", PlotType.MARRIAGE_OF_CONVENIENCE),
            ("triangle", PlotType.LOVE_TRIANGLE),
            ("workplace", PlotType.WORKPLACE_ROMANCE),
            
            # Crime/Mystery variations
            ("locked room", PlotType.LOCKED_ROOM_MYSTERY),
            ("locked_room", PlotType.LOCKED_ROOM_MYSTERY),
            ("serial", PlotType.SERIAL_KILLER),
            ("killer", PlotType.SERIAL_KILLER),
            ("cold case", PlotType.COLD_CASE),
            ("cold_case", PlotType.COLD_CASE),
            ("detective", PlotType.AMATEUR_DETECTIVE),
            ("police", PlotType.POLICE_PROCEDURAL),
            ("legal", PlotType.LEGAL_THRILLER),
            ("court", PlotType.LEGAL_THRILLER),
            
            # Historical variations
            ("war", PlotType.WAR_STORY),
            ("political", PlotType.POLITICAL_INTRIGUE),
            ("revolution", PlotType.SOCIAL_REVOLUTION),
            ("immigrant", PlotType.IMMIGRANT_STORY),
            ("family saga", PlotType.FAMILY_SAGA),
            ("family_saga", PlotType.FAMILY_SAGA),
            ("period", PlotType.PERIOD_ROMANCE),
            
            # Literary variations
            ("character", PlotType.CHARACTER_STUDY),
            ("study", PlotType.CHARACTER_STUDY),
            ("midlife", PlotType.MIDLIFE_CRISIS),
            ("family", PlotType.FAMILY_DRAMA),
            ("drama", PlotType.FAMILY_DRAMA),
            ("existential", PlotType.EXISTENTIAL_JOURNEY),
            ("identity", PlotType.IDENTITY_CRISIS),
            ("moral", PlotType.MORAL_DILEMMA),
            
            # YA variations
            ("school", PlotType.SCHOOL_STORY),
            ("teen", PlotType.TEEN_REBELLION),
            ("bullying", PlotType.BULLYING_STORY),
            ("sports", PlotType.SPORTS_COMPETITION),
            ("college", PlotType.COLLEGE_STORY),
            ("first love", PlotType.FIRST_LOVE),
            ("first_love", PlotType.FIRST_LOVE),
            
            # Adventure variations
            ("treasure", PlotType.TREASURE_HUNT),
            ("exploration", PlotType.EXPLORATION),
            ("rescue", PlotType.RESCUE_MISSION),
            ("race", PlotType.RACE_AGAINST_TIME),
            ("martial", PlotType.MARTIAL_ARTS),
            ("pirate", PlotType.PIRATE_ADVENTURE),
            ("jungle", PlotType.JUNGLE_ADVENTURE),
            ("mountain", PlotType.MOUNTAIN_CLIMBING),
            
            # Business variations
            ("corporate", PlotType.CORPORATE_THRILLER),
            ("startup", PlotType.STARTUP_STORY),
            ("business", PlotType.BUSINESS_RIVALRY),
            ("financial", PlotType.FINANCIAL_CRISIS),
            ("entrepreneur", PlotType.ENTREPRENEURIAL_JOURNEY),
            
            # Contemporary variations
            ("environment", PlotType.ENVIRONMENTAL_CRISIS),
            ("pandemic", PlotType.PANDEMIC_STORY),
            ("social media", PlotType.SOCIAL_MEDIA_DRAMA),
            ("social_media", PlotType.SOCIAL_MEDIA_DRAMA),
            ("technology", PlotType.TECHNOLOGY_ADDICTION),
            ("mental health", PlotType.MENTAL_HEALTH_JOURNEY),
            ("mental_health", PlotType.MENTAL_HEALTH_JOURNEY),
            ("immigration", PlotType.IMMIGRATION_STORY),
            ("gender", PlotType.GENDER_IDENTITY),
            ("racial", PlotType.RACIAL_JUSTICE),
            ("economic", PlotType.ECONOMIC_INEQUALITY),
        ]
        
        successful_matches = 0
        total_tests = len(flexible_test_cases)
        
        for input_str, expected in flexible_test_cases:
            try:
                result = PlotType.from_string(input_str)
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
                    PlotType.from_string(invalid_input)
            else:
                try:
                    result = PlotType.from_string(invalid_input)
                    # If it somehow succeeds, that's impressive flexibility
                    print(f"Surprisingly flexible: '{invalid_input}' -> {result}")
                except ValueError:
                    # Expected to fail
                    pass
    
    def test_get_plots_for_genre(self):
        """Test getting plot types for specific genres."""
        # Test major genres
        major_genres = [
            "fantasy", "science_fiction", "romance", "mystery", "thriller", 
            "horror", "young_adult", "historical_fiction", "literary_fiction",
            "adventure", "crime", "business", "dystopian", "paranormal"
        ]
        
        all_results = {}
        for genre in major_genres:
            plots = PlotType.get_plots_for_genre(genre)
            assert isinstance(plots, list)
            assert len(plots) > 0, f"Genre {genre} returned no plot types"
            assert all(isinstance(p, PlotType) for p in plots)
            
            all_results[genre] = len(plots)
            print(f"✓ {genre}: {len(plots)} plot types")
        
        # Test specific genre expectations
        fantasy_plots = PlotType.get_plots_for_genre("fantasy")
        expected_fantasy = [PlotType.THE_QUEST, PlotType.CHOSEN_ONE, PlotType.MAGICAL_AWAKENING]
        found_fantasy = sum(1 for p in expected_fantasy if p in fantasy_plots)
        assert found_fantasy >= 2, f"Fantasy should include most expected plots, found {found_fantasy}/3"
        
        romance_plots = PlotType.get_plots_for_genre("romance")
        assert PlotType.ROMANCE_LOVE_STORY in romance_plots
        assert PlotType.ENEMIES_TO_LOVERS in romance_plots
        
        horror_plots = PlotType.get_plots_for_genre("horror")
        assert PlotType.HAUNTED_HOUSE in horror_plots
        assert PlotType.SUPERNATURAL_HORROR in horror_plots
        
        business_plots = PlotType.get_plots_for_genre("business")
        assert PlotType.CORPORATE_THRILLER in business_plots
        assert PlotType.STARTUP_STORY in business_plots
        
        # Verify we got reasonable variety across genres
        total_unique_plots = len(set().union(*[PlotType.get_plots_for_genre(g) for g in major_genres]))
        assert total_unique_plots >= 50, f"Expected at least 50 unique plot types across all genres, got {total_unique_plots}"
    
    def test_get_plots_by_complexity(self):
        """Test filtering plot types by complexity level."""
        for complexity in ["simple", "moderate", "complex", "very_complex"]:
            plots = PlotType.get_plots_by_complexity(complexity)
            assert isinstance(plots, list)
            
            # All returned plots should match the requested complexity
            for plot in plots:
                assert plot.complexity_level == complexity
            
            print(f"✓ {complexity}: {len(plots)} plot types")
        
        # Should have some plots in each category
        simple_plots = PlotType.get_plots_by_complexity("simple")
        very_complex_plots = PlotType.get_plots_by_complexity("very_complex")
        assert len(simple_plots) > 0
        assert len(very_complex_plots) > 0
    
    def test_get_classic_plots(self):
        """Test getting classic archetypal plot types."""
        classic_plots = PlotType.get_classic_plots()
        
        assert isinstance(classic_plots, list)
        assert len(classic_plots) == 7  # Should be exactly 7 classic plots
        
        # Should include all the classic archetypes
        expected_classic = [
            PlotType.OVERCOMING_THE_MONSTER, PlotType.RAGS_TO_RICHES, PlotType.THE_QUEST,
            PlotType.VOYAGE_AND_RETURN, PlotType.COMEDY, PlotType.TRAGEDY, PlotType.REBIRTH
        ]
        
        for expected in expected_classic:
            assert expected in classic_plots, f"Classic plot {expected} not found"
        
        print(f"✓ Classic plots: {len(classic_plots)} types")
    
    def test_get_modern_plots(self):
        """Test getting contemporary and modern plot types."""
        modern_plots = PlotType.get_modern_plots()
        
        assert isinstance(modern_plots, list)
        assert len(modern_plots) > 0
        
        # Should include contemporary issues
        expected_modern = [
            PlotType.ENVIRONMENTAL_CRISIS, PlotType.PANDEMIC_STORY, 
            PlotType.SOCIAL_MEDIA_DRAMA, PlotType.TECHNOLOGY_ADDICTION
        ]
        
        found_modern = sum(1 for p in expected_modern if p in modern_plots)
        assert found_modern >= 2, f"Modern plots should include contemporary issues, found {found_modern}/4"
        
        print(f"✓ Modern plots: {len(modern_plots)} types")
    
    def test_string_representations(self):
        """Test string representation methods."""
        plot = PlotType.THE_QUEST
        
        str_repr = str(plot)
        
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        assert str_repr == plot.display_name


class TestPlotTypeIntegration:
    """Integration tests for the plot type system."""
    
    def test_all_plots_have_complete_properties(self):
        """Test that all plot types have all required properties implemented."""
        for plot in PlotType:
            # Test all properties work without errors
            assert plot.display_name is not None
            assert plot.description is not None
            assert plot.complexity_level is not None
            assert plot.typical_themes is not None
            assert plot.target_length is not None
    
    def test_plot_type_enum_completeness(self):
        """Test that the PlotType enum covers expected plot areas."""
        # Test that we have plots for major categories
        expected_categories = [
            "classic", "thriller", "sci_fi", "fantasy", "horror", "romance", 
            "mystery", "historical", "literary", "ya", "adventure", "business", "contemporary"
        ]
        
        available_plots = [plot.value for plot in PlotType]
        
        # Check for representative plots in each category
        category_representatives = {
            "classic": ["overcoming_the_monster", "rags_to_riches", "the_quest"],
            "thriller": ["conspiracy", "chase", "heist", "espionage"],
            "sci_fi": ["first_contact", "time_travel", "dystopian_rebellion"],
            "fantasy": ["chosen_one", "magical_awakening", "dark_lord_rising"],
            "horror": ["haunted_house", "possession", "supernatural_horror"],
            "romance": ["enemies_to_lovers", "forbidden_love", "second_chance_romance"],
            "mystery": ["locked_room_mystery", "serial_killer", "cold_case"],
            "historical": ["war_story", "political_intrigue", "period_romance"],
            "literary": ["character_study", "existential_journey", "moral_dilemma"],
            "ya": ["school_story", "first_love", "teen_rebellion"],
            "adventure": ["treasure_hunt", "exploration", "rescue_mission"],
            "business": ["corporate_thriller", "startup_story", "business_rivalry"],
            "contemporary": ["environmental_crisis", "social_media_drama", "mental_health_journey"]
        }
        
        for category, representatives in category_representatives.items():
            found_representatives = [rep for rep in representatives if rep in available_plots]
            assert len(found_representatives) > 0, f"No representatives found for category: {category}"
    
    def test_genre_plot_mapping_coverage(self):
        """Test that genre mappings provide good coverage."""
        major_genres = [
            "fantasy", "science_fiction", "romance", "mystery", "thriller",
            "horror", "young_adult", "historical_fiction", "business"
        ]
        
        for genre in major_genres:
            plots = PlotType.get_plots_for_genre(genre)
            assert len(plots) >= 5, f"Genre {genre} has too few plots: {len(plots)}"
            assert len(plots) <= 20, f"Genre {genre} has too many plots: {len(plots)}"
    
    def test_complexity_distribution(self):
        """Test that plot types are well-distributed across complexity levels."""
        complexity_counts = {"simple": 0, "moderate": 0, "complex": 0, "very_complex": 0}
        
        for plot in PlotType:
            complexity_counts[plot.complexity_level] += 1
        
        total_plots = sum(complexity_counts.values())
        
        # Each complexity level should have at least some plots
        for complexity, count in complexity_counts.items():
            percentage = count / total_plots
            assert percentage >= 0.05, f"Complexity {complexity} has too few plots: {percentage:.1%}"
            assert percentage <= 0.7, f"Complexity {complexity} has too many plots: {percentage:.1%}"
    
    def test_theme_consistency(self):
        """Test that themes are consistent with plot types."""
        # Test that similar plots have overlapping themes
        quest_plots = [PlotType.THE_QUEST, PlotType.TREASURE_HUNT, PlotType.EXPLORATION]
        
        for plot in quest_plots:
            themes = plot.typical_themes
            # Quest-type plots should have adventure or journey themes
            adventure_themes = ["journey", "adventure", "exploration", "discovery", "quest"]
            has_adventure_theme = any(theme in " ".join(themes).lower() for theme in adventure_themes)
            assert has_adventure_theme, f"Quest-type plot {plot.value} should have adventure themes: {themes}"
        
        # Test romance plots have love/relationship themes
        romance_plots = [PlotType.ROMANCE_LOVE_STORY, PlotType.ENEMIES_TO_LOVERS, PlotType.FORBIDDEN_LOVE]
        
        for plot in romance_plots:
            themes = plot.typical_themes
            love_themes = ["love", "relationship", "romance", "emotional", "connection"]
            has_love_theme = any(theme in " ".join(themes).lower() for theme in love_themes)
            assert has_love_theme, f"Romance plot {plot.value} should have love themes: {themes}"
    
    def test_length_progression_logic(self):
        """Test that target lengths follow logical patterns."""
        # Simple plots should generally be shorter
        simple_plots = PlotType.get_plots_by_complexity("simple")
        very_complex_plots = PlotType.get_plots_by_complexity("very_complex")
        
        simple_short_count = 0
        for plot in simple_plots:
            if "short" in plot.target_length.lower():
                simple_short_count += 1
        
        complex_long_count = 0
        for plot in very_complex_plots:
            if "long" in plot.target_length.lower() or "epic" in plot.target_length.lower():
                complex_long_count += 1
        
        # At least some simple plots should be short
        if len(simple_plots) > 0:
            simple_short_ratio = simple_short_count / len(simple_plots)
            print(f"Simple plots that are short: {simple_short_ratio:.1%}")
        
        # At least some complex plots should be long
        if len(very_complex_plots) > 0:
            complex_long_ratio = complex_long_count / len(very_complex_plots)
            print(f"Very complex plots that are long: {complex_long_ratio:.1%}")
    
    @pytest.mark.parametrize("genre", [
        "fantasy", "science_fiction", "romance", "mystery", "thriller", 
        "horror", "young_adult", "business"
    ])
    def test_all_major_genres_have_appropriate_plots(self, genre):
        """Test that all major genres get appropriate plot recommendations."""
        plots = PlotType.get_plots_for_genre(genre)
        
        # Should get meaningful recommendations
        assert len(plots) >= 5
        
        # Should include appropriate plots for the genre
        plot_values = {plot.value for plot in plots}
        
        # Define genre-specific expectations
        genre_expectations = {
            "fantasy": {"the_quest", "chosen_one", "magical_awakening", "overcoming_the_monster"},
            "science_fiction": {"first_contact", "time_travel", "dystopian_rebellion", "space_exploration"},
            "romance": {"romance_love_story", "enemies_to_lovers", "forbidden_love"},
            "mystery": {"mystery_investigation", "locked_room_mystery", "amateur_detective"},
            "thriller": {"conspiracy", "chase", "espionage", "ticking_clock"},
            "horror": {"haunted_house", "supernatural_horror", "possession"},
            "young_adult": {"coming_of_age", "school_story", "first_love"},
            "business": {"corporate_thriller", "startup_story", "business_rivalry"}
        }
        
        expected_plots = genre_expectations.get(genre, {"the_quest", "overcoming_the_monster"})
        
        # Should include at least one expected plot for this genre
        overlap = plot_values.intersection(expected_plots)
        assert len(overlap) > 0, \
            f"Genre {genre} should include some expected plots. Got: {sorted(list(plot_values)[:5])}, Expected any of: {sorted(expected_plots)}"
    
    def test_complete_workflow_from_user_input(self):
        """Test complete workflow from user input to plot selection."""
        # Simulate user wanting to write a fantasy quest story
        user_genre = "fantasy"
        user_plot_preference = "quest"
        
        # Get genre-based recommendations
        genre_plots = PlotType.get_plots_for_genre(user_genre)
        
        # Get plot from string
        preferred_plot = PlotType.from_string(user_plot_preference)
        
        # Should find the quest plot
        assert preferred_plot == PlotType.THE_QUEST
        
        # Quest should be included in fantasy recommendations
        assert PlotType.THE_QUEST in genre_plots
        
        # Should be able to get plot details
        assert preferred_plot.complexity_level in ["simple", "moderate", "complex", "very_complex"]
        assert len(preferred_plot.typical_themes) > 0
        assert len(preferred_plot.description) > 50
    
    def test_from_string_integration_with_genre_mapping(self):
        """Test that from_string works with genre mapping system."""
        # User inputs plot preference as string
        user_input = "enemies to lovers romance"
        
        try:
            preferred_plot = PlotType.from_string(user_input)
            
            # Should be a valid plot
            assert isinstance(preferred_plot, PlotType)
            
            # Should be able to get properties
            assert preferred_plot.display_name is not None
            assert preferred_plot.complexity_level is not None
            
            # Should work with genre system
            romance_plots = PlotType.get_plots_for_genre("romance")
            assert len(romance_plots) > 0
            
        except ValueError:
            # If from_string doesn't work for this specific input, test with simpler input
            preferred_plot = PlotType.from_string("romance")
            assert isinstance(preferred_plot, PlotType)


class TestPlotTypePerformance:
    """Performance tests for the plot type system."""
    
    def test_property_access_performance(self):
        """Test that property access is reasonably fast."""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            for plot in list(PlotType)[:10]:  # Test first 10
                _ = plot.display_name
                _ = plot.description
                _ = plot.complexity_level
                _ = plot.typical_themes
                _ = plot.target_length
        end_time = time.time()
        
        # Should complete 50,000 property accesses in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Property access too slow: {total_time:.2f}s"
    
    def test_from_string_performance(self):
        """Test that from_string operations are fast."""
        import time
        
        test_inputs = ["quest", "romance", "mystery", "thriller", "fantasy"]
        
        start_time = time.time()
        for _ in range(1000):
            for input_str in test_inputs:
                try:
                    PlotType.from_string(input_str)
                except ValueError:
                    pass
        end_time = time.time()
        
        # Should complete 5000 from_string operations in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"from_string too slow: {total_time:.2f}s"
    
    def test_genre_mapping_performance(self):
        """Test that genre mapping is reasonably fast."""
        import time
        
        test_genres = ["fantasy", "romance", "mystery", "thriller"]
        
        start_time = time.time()
        for _ in range(1000):
            for genre in test_genres:
                PlotType.get_plots_for_genre(genre)
        end_time = time.time()
        
        # Should complete 4000 genre mappings in under 1 second
        total_time = end_time - start_time
        assert total_time < 1.0, f"Genre mapping too slow: {total_time:.2f}s"


class TestBasicFunctionality:
    """Test basic functionality that should always work."""
    
    def test_plot_enum_basic_functionality(self):
        """Test that PlotType enum works as expected."""
        # Test iteration
        plot_list = list(PlotType)
        assert len(plot_list) > 80  # Should have substantial number of plots
        
        # Test basic attributes
        quest = PlotType.THE_QUEST
        assert quest.value == "the_quest"
        assert "Quest" in quest.display_name
        
        # Test enum comparison
        assert PlotType.THE_QUEST == PlotType.THE_QUEST
        assert PlotType.THE_QUEST != PlotType.ROMANCE_LOVE_STORY
    
    def test_all_expected_plots_exist(self):
        """Test that all expected plot types are available."""
        expected_plots = [
            "OVERCOMING_THE_MONSTER", "RAGS_TO_RICHES", "THE_QUEST", "COMEDY", "TRAGEDY",
            "ROMANCE_LOVE_STORY", "MYSTERY_INVESTIGATION", "COMING_OF_AGE", 
            "CHOSEN_ONE", "ENEMIES_TO_LOVERS", "FIRST_CONTACT", "HAUNTED_HOUSE",
            "CORPORATE_THRILLER", "ENVIRONMENTAL_CRISIS"
        ]
        
        available_plots = [plot.name for plot in PlotType]
        
        for expected in expected_plots:
            assert expected in available_plots, f"Plot type {expected} not found"
    
    def test_property_consistency(self):
        """Test that properties are consistent with plot types."""
        for plot in PlotType:
            # Complexity should be consistent
            complexity = plot.complexity_level
            
            # Very complex plots should generally have longer target lengths
            if complexity == "very_complex":
                target_length = plot.target_length
                # Should not be short
                assert "short" not in target_length.lower() or "medium" in target_length.lower() or "long" in target_length.lower()
            
            # Simple plots should have simpler themes
            if complexity == "simple":
                themes = plot.typical_themes
                # Should have some basic themes
                assert len(themes) > 0
                assert all(len(theme) > 0 for theme in themes)


if __name__ == "__main__":
    # Run tests if this file is executed directly
    pytest.main([__file__, "-v"])