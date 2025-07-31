import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class PlanningConfig:
    """Configuration for the planning prompt generation."""
    model_name: str = "llama3.3:70b"
    max_context_length: int = 128000
    temperature: float = 0.7
    include_examples: bool = True
    detail_level: str = "comprehensive"  # "basic", "detailed", "comprehensive"


class PlanningPromptGenerator:
    """
    Generates comprehensive book planning prompts optimized for Ollama's llama3.3:70b model.
    Handles variable JSON payload structures to create detailed writing plans.
    """
    
    def __init__(self, config: Optional[PlanningConfig] = None):
        self.config = config or PlanningConfig()
        self.phase_processors = {
            'phase1': self._process_concept_phase,
            'phase2': self._process_structure_phase,
            'phase3': self._process_worldbuilding_phase,
            'phase4': self._process_character_phase,
            'phase5': self._process_style_phase,
            'phase6': self._process_editing_phase,
            'phase7': self._process_market_phase,
        }
    
    def generate_planning_prompt(self, payload: Dict[str, Any]) -> str:
        """
        Generate a comprehensive book planning prompt from the JSON payload.
        
        Args:
            payload: Dictionary containing book project information
            
        Returns:
            str: Complete planning prompt optimized for llama3.3:70b
        """
        # Extract and process payload information
        processed_data = self._process_payload(payload)
        
        # Build the comprehensive prompt
        prompt_sections = [
            self._build_header(),
            self._build_project_overview(processed_data),
            self._build_planning_instructions(processed_data),
            self._build_output_structure(),
            self._build_quality_guidelines(),
            self._build_examples() if self.config.include_examples else "",
            self._build_footer()
        ]
        
        return "\n\n".join(filter(None, prompt_sections))
    
    def _process_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process the variable JSON payload structure."""
        processed = {
            'phases': {},
            'metadata': {
                'total_phases': len(payload),
                'available_phases': list(payload.keys())
            }
        }
        
        # Process each phase using appropriate processor
        for phase_key, phase_data in payload.items():
            if phase_key in self.phase_processors:
                processed['phases'][phase_key] = self.phase_processors[phase_key](phase_data)
            else:
                # Handle unknown phases gracefully
                processed['phases'][phase_key] = self._process_generic_phase(phase_data)
        
        return processed
    
    def _process_concept_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process book concept phase data."""
        return {
            'type': 'concept',
            'elements': {
                'title': data.get('book_concept', 'Unknown Title'),
                'author': data.get('author', 'Unknown Author'),
                'genre': data.get('genre', 'Unspecified Genre'),
                'audience': data.get('target_audience', 'General Audience'),
                'length': data.get('word_count', 'Standard Length'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['book_concept', 'author', 'genre', 'target_audience', 'word_count']}
            }
        }
    
    def _process_structure_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process story structure phase data."""
        return {
            'type': 'structure',
            'elements': {
                'framework': data.get('story_structure', 'Three-Act Structure'),
                'plot_type': data.get('plot_type', 'Linear Plot'),
                'conflict': data.get('conflict', 'Person vs Person'),
                'character_arc': data.get('character_arc', 'Character Growth'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['story_structure', 'plot_type', 'conflict', 'character_arc']}
            }
        }
    
    def _process_worldbuilding_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process world-building phase data."""
        return {
            'type': 'worldbuilding',
            'elements': {
                'world_type': data.get('world_building', 'Contemporary Setting'),
                'setting': data.get('setting', 'Unspecified Location'),
                'magic_system': data.get('magic_system', 'No Magic System'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['world_building', 'setting', 'magic_system']}
            }
        }
    
    def _process_character_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process character development phase data."""
        return {
            'type': 'character',
            'elements': {
                'development': data.get('character_development', 'Standard Character Development'),
                'supporting_characters': data.get('supporting_characters', 'Supporting Cast'),
                'relationships': data.get('character_relationships', 'Character Interactions'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['character_development', 'supporting_characters', 'character_relationships']}
            }
        }
    
    def _process_style_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process writing style phase data."""
        return {
            'type': 'style',
            'elements': {
                'writing_style': data.get('writing_style', 'Standard Prose'),
                'pacing': data.get('pacing', 'Moderate Pacing'),
                'language': data.get('language', 'English'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['writing_style', 'pacing', 'language']}
            }
        }
    
    def _process_editing_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process editing phase data."""
        return {
            'type': 'editing',
            'elements': {
                'process': data.get('editing_process', 'Standard Editing'),
                'strategy': data.get('revision_strategy', 'General Revision'),
                'additional': {k: v for k, v in data.items() 
                            if k not in ['editing_process', 'revision_strategy']}
            }
        }
    
    def _process_market_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process market/publishing phase data."""
        return {
            'type': 'market',
            'elements': data  # Keep full structure for complex market data
        }
    
    def _process_generic_phase(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process unknown phase types generically."""
        return {
            'type': 'generic',
            'elements': data
        }
    
    def _build_header(self) -> str:
        """Build the prompt header."""
        return f"""# COMPREHENSIVE BOOK PLANNING SYSTEM
## Optimized for {self.config.model_name}

You are an expert book planning consultant tasked with creating a detailed, actionable writing plan. Your goal is to transform the provided project information into a comprehensive roadmap that will guide the actual writing process.

**CRITICAL INSTRUCTIONS:**
- Create a plan so detailed that any writer could follow it to produce a cohesive book
- Consider all provided elements and their interconnections
- Maintain consistency across all planning sections
- Focus on practical implementation rather than theoretical concepts
- Ensure the plan is specific to the provided project details"""
    
    def _build_project_overview(self, processed_data: Dict[str, Any]) -> str:
        """Build the project overview section."""
        phases = processed_data['phases']
        
        overview = "# PROJECT OVERVIEW\n\n"
        
        # Extract key project information
        if 'phase1' in phases:
            concept = phases['phase1']['elements']
            overview += f"**Title:** {concept['title']}\n"
            overview += f"**Author:** {concept['author']}\n"
            overview += f"**Genre:** {concept['genre']}\n"
            overview += f"**Target Audience:** {concept['audience']}\n"
            overview += f"**Planned Length:** {concept['length']}\n\n"
        
        overview += f"**Available Project Phases:** {', '.join(processed_data['metadata']['available_phases'])}\n"
        overview += f"**Total Planning Phases:** {processed_data['metadata']['total_phases']}"
        
        return overview
    
    def _build_planning_instructions(self, processed_data: Dict[str, Any]) -> str:
        """Build the main planning instructions."""
        instructions = "# PLANNING REQUIREMENTS\n\n"
        instructions += "Create a comprehensive book writing plan that addresses each of the following areas based on the provided project information:\n\n"
        
        phase_instructions = {
            'phase1': "## 1. FOUNDATION PLANNING\nBased on the book concept information, establish:",
            'phase2': "## 2. STRUCTURAL BLUEPRINT\nUsing the story structure details, design:",
            'phase3': "## 3. WORLD DESIGN FRAMEWORK\nFrom the world-building information, develop:",
            'phase4': "## 4. CHARACTER ARCHITECTURE\nUsing character development details, create:",
            'phase5': "## 5. WRITING METHODOLOGY\nBased on style preferences, establish:",
            'phase6': "## 6. REVISION STRATEGY\nFrom editing requirements, plan:",
            'phase7': "## 7. PUBLICATION ROADMAP\nUsing market information, design:"
        }
        
        for phase_key, phase_data in processed_data['phases'].items():
            if phase_key in phase_instructions:
                instructions += f"{phase_instructions[phase_key]}\n"
                instructions += self._build_phase_specific_instructions(phase_key, phase_data)
            else:
                instructions += f"## {phase_key.upper()}\n"
                instructions += f"Address the following elements: {', '.join(phase_data['elements'].keys())}\n\n"
        
        return instructions
    
    def _build_phase_specific_instructions(self, phase_key: str, phase_data: Dict[str, Any]) -> str:
        """Build phase-specific planning instructions."""
        phase_templates = {
            'phase1': """
- Complete project scope and objectives
- Target audience analysis and requirements
- Genre conventions and reader expectations
- Success metrics and completion criteria
- Timeline and milestone planning
""",
            'phase2': """
- Detailed plot outline with major story beats
- Act/chapter breakdown with scene summaries
- Conflict escalation and resolution points
- Pacing strategy throughout the narrative
- Subplot integration and character arc alignment
""",
            'phase3': """
- Comprehensive world bible with rules and limitations
- Setting descriptions and atmospheric elements
- Cultural, historical, and technological frameworks
- Magic/technology system documentation
- Consistency guidelines for world elements
""",
            'phase4': """
- Complete character profiles with backstories
- Character development arcs and transformation points
- Relationship dynamics and interaction patterns
- Dialogue voice and speech patterns for each character
- Character motivation and goal hierarchies
""",
            'phase5': """
- Voice and tone consistency guidelines
- Narrative perspective and point-of-view strategy
- Pacing techniques and scene transition methods
- Language level and vocabulary considerations
- Style guide for maintaining consistency
""",
            'phase6': """
- Multi-stage revision process with specific focus areas
- Self-editing checklists and quality benchmarks
- Beta reader recruitment and feedback integration
- Professional editing timeline and budget
- Manuscript polishing and final preparation steps
""",
            'phase7': """
- Market positioning and competitive analysis
- Publishing pathway selection (traditional/self/hybrid)
- Marketing strategy and promotional timeline
- Launch preparation and post-publication growth
- Long-term author platform development
"""
        }
        
        return phase_templates.get(phase_key, f"- Address all elements in {phase_key}\n")
    
    def _build_output_structure(self) -> str:
        """Build the output structure requirements."""
        return """# REQUIRED OUTPUT STRUCTURE

Your response must follow this exact structure:

## EXECUTIVE SUMMARY
- 2-3 paragraph overview of the complete project plan
- Key success factors and critical path elements
- Timeline overview and major milestones

## DETAILED PLANNING SECTIONS
For each phase present in the project data, provide:

### [PHASE NAME]
**Objectives:** Clear goals for this phase
**Key Elements:** Detailed breakdown of all components
**Implementation Steps:** Actionable tasks in chronological order
**Quality Criteria:** Success metrics and evaluation standards
**Integration Points:** How this phase connects to others

## WRITING IMPLEMENTATION GUIDE
- Chapter-by-chapter outline with scene descriptions
- Character appearance and development timeline
- World-building revelation schedule
- Conflict escalation pattern
- Resolution and closure strategy

## CONSISTENCY FRAMEWORK
- Style guide summary
- Character voice reference
- World-building rules checklist
- Timeline and continuity tracking system
- Quality assurance checkpoints

## SUCCESS METRICS
- Completion criteria for each phase
- Quality benchmarks and evaluation methods
- Reader engagement targets
- Market positioning goals"""
    
    def _build_quality_guidelines(self) -> str:
        """Build quality guidelines section."""
        return """# QUALITY REQUIREMENTS

**Specificity:** Every recommendation must be actionable and specific to this project
**Consistency:** All planning elements must align and support each other
**Practicality:** Focus on implementable strategies rather than theoretical concepts
**Completeness:** Address every element provided in the project data
**Professional Standards:** Maintain industry-standard planning depth and detail

**CRITICAL:** Do not provide generic advice. Every element of your plan must be tailored to the specific project details provided."""
    
    def _build_examples(self) -> str:
        """Build examples section if enabled."""
        if not self.config.include_examples:
            return ""
        
        return """# PLANNING EXAMPLE STRUCTURE

Here's how to structure a planning section:

### WORLD DESIGN FRAMEWORK
**Objectives:** 
- Establish consistent magical system based on Slavic folklore
- Create immersive forest setting with mythological authenticity
- Design creature hierarchy and interaction rules

**Key Elements:**
- Slavic Mythology Integration: Research-based creature behaviors, traditional folklore elements, authentic cultural details
- Enchanted Forest Ecosystem: Interconnected magical zones, seasonal variations, hidden pathways and secret locations
- Magic System Rules: Folklore-based limitations, creature-specific abilities, consequence structures

**Implementation Steps:**
1. Compile comprehensive Slavic mythology reference guide
2. Map forest geography with magical significance
3. Define interaction rules between Peter and each creature type
4. Establish magical consequence system
5. Create world consistency checklist

**Quality Criteria:**
- Cultural authenticity verification
- Internal logic consistency
- Reader immersion benchmarks
- Educational value assessment

**Integration Points:**
- Character development through world encounters
- Plot advancement via environmental challenges
- Theme reinforcement through mythological symbolism"""
    
    def _build_footer(self) -> str:
        """Build the prompt footer."""
        return """# FINAL INSTRUCTIONS

Begin your response immediately with "# COMPREHENSIVE BOOK WRITING PLAN" followed by the Executive Summary. 

Ensure every section is detailed enough to serve as a practical writing guide. The completed plan should enable successful book completion by following your recommendations systematically.

Remember: This is not just a planning exercise—this is creating the foundational document that will guide the entire book creation process."""

    def save_prompt_to_file(self, prompt: str, filename: str = "book_planning_prompt.txt") -> None:
        """Save the generated prompt to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt)
    
    def get_prompt_stats(self, prompt: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get statistics about the generated prompt."""
        stats = {
            'total_characters': len(prompt),
            'total_words': len(prompt.split()),
            'total_lines': len(prompt.split('\n')),
            'estimated_tokens': len(prompt.split()) * 1.3,  # Rough token estimation
            'recommended_model_settings': self._get_recommended_model_settings(prompt, payload)
        }
        
        if payload:
            stats['template_complexity_score'] = self._calculate_complexity_score(payload)
        
        return stats
    
    def _get_recommended_model_settings(self, prompt: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate recommended model settings based on prompt complexity and payload.
        Creative approach: Higher temperature for innovative planning, dynamic adjustments.
        
        Args:
            prompt: The generated prompt string
            payload: Optional payload data for complexity analysis
            
        Returns:
            Dictionary with recommended model settings for Ollama
        """
        estimated_tokens = len(prompt.split()) * 1.3
        complexity_score = self._calculate_complexity_score(payload) if payload else 0.5
        
        # Determine planning creativity level based on genre and complexity
        creativity_boost = self._calculate_creativity_boost(payload)
        
        # Base settings optimized for creative planning
        settings = {
            "temperature": 0.85 + creativity_boost,  # Higher base for creative planning
            "top_p": 0.92,  # Slightly restrictive to maintain coherence
            "top_k": 50,    # Increased vocabulary diversity
            "repeat_penalty": 1.05,  # Lower to allow thematic repetition
            "num_ctx": min(32768, int(estimated_tokens * 1.5)),
            "num_predict": 8192,
            "stop": ["# END OF PLAN", "---END---", "\n\n# FINAL", "***END***"]
        }
        
        # Genre-specific adjustments
        genre_adjustments = self._get_genre_specific_settings(payload)
        settings.update(genre_adjustments)
        
        # Complexity-based fine-tuning (counter-intuitive approach)
        if complexity_score > 0.7:
            # High complexity: INCREASE creativity to handle interconnected elements
            settings["temperature"] = min(1.2, settings["temperature"] + 0.15)
            settings["top_p"] = 0.95  # More exploration for complex scenarios
            settings["top_k"] = 60
            settings["num_predict"] = 12288
        elif complexity_score < 0.3:
            # Low complexity: Moderate creativity, focus on solid fundamentals
            settings["temperature"] = max(0.7, settings["temperature"] - 0.1)
            settings["top_p"] = 0.88
            settings["top_k"] = 35
        
        # Audience-specific adjustments
        if self._is_children_book(payload):
            # Children's books: Higher creativity for engaging, imaginative planning
            settings["temperature"] = min(1.1, settings["temperature"] + 0.1)
            settings["top_p"] = 0.96
        elif self._is_literary_fiction(payload):
            # Literary fiction: Balanced approach with slight creativity boost
            settings["temperature"] = settings["temperature"] + 0.05
            settings["top_p"] = 0.90
        
        # Phase count adjustments
        if payload and len(payload) > 6:
            # Many phases: Need sustained creative energy
            settings["temperature"] = min(1.15, settings["temperature"] + 0.08)
            settings["num_predict"] = max(settings["num_predict"], 10240)
        
        # Ensure temperature stays within reasonable bounds
        settings["temperature"] = max(0.6, min(1.3, settings["temperature"]))
        
        return settings
    
    def _calculate_creativity_boost(self, payload: Optional[Dict[str, Any]]) -> float:
        """Calculate creativity boost based on project characteristics."""
        if not payload:
            return 0.0
        
        boost = 0.0
        
        # Genre creativity factors
        if 'phase1' in payload:
            genre = payload['phase1'].get('genre', '').lower()
            creative_genres = {
                'fantasy': 0.15,
                'sci-fi': 0.12,
                'science fiction': 0.12,
                'magical realism': 0.18,
                'surreal': 0.20,
                'experimental': 0.25,
                'children': 0.10,
                'adventure': 0.08
            }
            for genre_type, boost_value in creative_genres.items():
                if genre_type in genre:
                    boost = max(boost, boost_value)
        
        # World-building creativity boost
        if 'phase3' in payload:
            world_data = payload['phase3']
            creative_elements = ['magic', 'mythology', 'supernatural', 'alternate', 'parallel']
            if any(element in str(world_data).lower() for element in creative_elements):
                boost += 0.08
        
        # Character complexity boost
        if 'phase4' in payload:
            char_data = payload['phase4']
            if 'mythology' in str(char_data).lower() or len(str(char_data)) > 200:
                boost += 0.05
        
        return min(0.3, boost)  # Cap at 0.3 to prevent extreme values
    
    def _get_genre_specific_settings(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Get genre-specific model setting adjustments."""
        if not payload or 'phase1' not in payload:
            return {}
        
        genre = payload['phase1'].get('genre', '').lower()
        
        # Fantasy and Sci-Fi: Need high creativity for world-building
        if any(g in genre for g in ['fantasy', 'sci-fi', 'science fiction']):
            return {
                "temperature": 1.0,
                "top_p": 0.94,
                "repeat_penalty": 1.02  # Allow world-building repetition
            }
        
        # Mystery/Thriller: Structured creativity with logical coherence
        elif any(g in genre for g in ['mystery', 'thriller', 'crime']):
            return {
                "temperature": 0.8,
                "top_p": 0.87,
                "top_k": 45
            }
        
        # Romance: Emotional creativity with character focus
        elif 'romance' in genre:
            return {
                "temperature": 0.9,
                "top_p": 0.93,
                "repeat_penalty": 1.0  # Emotional themes can repeat
            }
        
        # Historical: Research-driven creativity
        elif 'historical' in genre:
            return {
                "temperature": 0.75,
                "top_p": 0.89,
                "top_k": 40
            }
        
        return {}
    
    def _is_children_book(self, payload: Optional[Dict[str, Any]]) -> bool:
        """Check if this is a children's book project."""
        if not payload or 'phase1' not in payload:
            return False
        
        phase1 = payload['phase1']
        genre = phase1.get('genre', '').lower()
        audience = phase1.get('target_audience', '').lower()
        
        return 'children' in genre or 'children' in audience or any(
            age_term in audience for age_term in ['7-12', '5-10', 'kids', 'young readers']
        )
    
    def _is_literary_fiction(self, payload: Optional[Dict[str, Any]]) -> bool:
        """Check if this is literary fiction."""
        if not payload or 'phase1' not in payload:
            return False
        
        genre = payload['phase1'].get('genre', '').lower()
        return any(term in genre for term in ['literary', 'contemporary fiction', 'literary fiction'])
    
    def _calculate_complexity_score(self, payload: Optional[Dict[str, Any]]) -> float:
        """
        Calculate complexity score for the planning task (0.0 to 1.0).
        
        Args:
            payload: The project payload data
            
        Returns:
            Float between 0.0 (simple) and 1.0 (highly complex)
        """
        if not payload:
            return 0.5
        
        complexity_factors = {
            'phase_count': 0.0,
            'data_depth': 0.0,
            'genre_complexity': 0.0,
            'audience_specificity': 0.0,
            'world_building_depth': 0.0
        }
        
        # Phase count factor (0.0 to 0.3)
        phase_count = len(payload)
        complexity_factors['phase_count'] = min(0.3, phase_count / 10)
        
        # Data depth factor (0.0 to 0.2)
        total_elements = sum(len(phase_data) if isinstance(phase_data, dict) else 1 
                           for phase_data in payload.values())
        complexity_factors['data_depth'] = min(0.2, total_elements / 50)
        
        # Genre complexity (0.0 to 0.2)
        if 'phase1' in payload:
            genre = payload['phase1'].get('genre', '').lower()
            complex_genres = ['fantasy', 'sci-fi', 'science fiction', 'historical', 'mystery', 'thriller']
            if any(g in genre for g in complex_genres):
                complexity_factors['genre_complexity'] = 0.2
            elif genre:
                complexity_factors['genre_complexity'] = 0.1
        
        # Audience specificity (0.0 to 0.15)
        if 'phase1' in payload:
            audience = payload['phase1'].get('target_audience', '').lower()
            if 'children' in audience or 'young adult' in audience:
                complexity_factors['audience_specificity'] = 0.15
            elif audience and audience != 'general':
                complexity_factors['audience_specificity'] = 0.1
        
        # World building depth (0.0 to 0.15)
        if 'phase3' in payload:
            world_data = payload['phase3']
            world_indicators = ['magic', 'fantasy', 'mythology', 'world_building', 'system']
            world_complexity = sum(1 for key, value in world_data.items() 
                                 if isinstance(value, str) and 
                                 any(indicator in value.lower() for indicator in world_indicators))
            complexity_factors['world_building_depth'] = min(0.15, world_complexity / 10)
        
        return sum(complexity_factors.values())


# Example usage and testing
if __name__ == "__main__":
    # Sample payload
    sample_payload = {
        "phase1": {
            "book_concept": "The Enchanted Forest of Peter",
            "author": "Joseph Campbell",
            "genre": "Children's Fantasy",
            "target_audience": "Children aged 7-12",
            "word_count": "40,000-60,000 words"
        },
        "phase2": {
            "story_structure": "Hero's Journey",
            "plot_type": "Voyage and Return",
            "conflict": "Person vs Supernatural",
            "character_arc": "Peter's journey of self-discovery and growth"
        },
        "phase3": {
            "world_building": "High Fantasy world with Slavic mythology elements",
            "setting": "Enchanted Forest, meadows, and mystical creatures",
            "magic_system": "Based on Slavic folklore and mythology"
        },
        "phase4": {
            "character_development": "Peter's character evolution through encounters and challenges",
            "supporting_characters": "Baba Yaga, Leshy, Domovoi, Rusalka, and other creatures from Slavic mythology",
            "character_relationships": "Peter's interactions with the creatures and their impact on his journey"
        },
        "phase5": {
            "writing_style": "Children-friendly, conversational tone with witty humor",
            "pacing": "Fast-paced narrative flow with rapid scene changes and minimal downtime",
            "language": "English, with possible inclusion of Slavic words and phrases for authenticity"
        },
        "phase6": {
            "editing_process": "Review of manuscript for consistency, coherence, and engagement",
            "revision_strategy": "Focus on character development, plot progression, and world-building refinement"
        },
        "phase7": {
            "market_positioning": {
                "genre_classification": "Children's Fantasy",
                "comp_title_analysis": "Comparison with similar books in the genre, such as 'The Spiderwick Chronicles' or 'The Golden Compass'",
                "target_reader_profile": "Children aged 7-12, parents, and educators seeking engaging and imaginative stories",
                "marketing_hooks": "Emphasis on adventure, self-discovery, and the richness of Slavic mythology"
            },
            "publishing_readiness": {
                "manuscript_requirements": "Completed manuscript, edited and revised",
                "query_letter_elements": "Introduction to the story, author bio, and marketing strategy",
                "self_publishing_checklist": "Formatting, cover design, and distribution channels",
                "beta_reader_strategy": "Selection of beta readers from the target audience for feedback and review"
            },
            "launch_strategy": {
                "pre_launch_timeline": "6-8 weeks prior to launch, including teaser releases, social media engagement, and influencer outreach",
                "launch_week_tactics": "Book signings, online promotions, and interactive events",
                "post_launch_growth": "Continued social media presence, reviews, and potential for sequels or spin-offs"
            }
        }
    }
    
    # Create generator and generate prompt
    config = PlanningConfig(detail_level="comprehensive", include_examples=True)
    generator = PlanningPromptGenerator(config)
    
    prompt = generator.generate_planning_prompt(sample_payload)
    stats = generator.get_prompt_stats(prompt, sample_payload)
    
    print("Generated Planning Prompt:")
    print("=" * 50)
    print(prompt)
    print("\n" + "=" * 50)
    print("Prompt Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")