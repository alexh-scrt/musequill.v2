import asyncio
import logging
from typing import Dict, List, Optional, Any
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import langchain and ollama
from langchain_ollama import OllamaLLM
from langchain.schema import BaseMessage, HumanMessage, SystemMessage


logger = logging.getLogger(__name__)

# ============================================================================
# LLM Service Integration
# ============================================================================

class LLMService:
    """Service for LLM communication via Ollama."""
    
    def __init__(self, model_name: str = "llama3.3:70b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        
    async def initialize(self):
        """Initialize LLM connection."""
        try:
            self.llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=1.3  # Lower temperature for more consistent suggestions
            )
            logger.info(f"LLM service initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    async def analyze_concept(self, concept: str, additional_notes: str) -> Dict[str, Any]:
        """Analyze book concept and recommend genres/subgenres using one-shot learning."""
        from musequill.models.book.genre import GenreMapping, GenreType, SubGenreType
        
        # Get all valid genre-subgenre combinations
        all_combinations = GenreMapping.get_all_combinations()
        
        # Create comprehensive examples for each genre/subgenre combination
        examples_prompt = self._build_genre_examples()
        
        if not additional_notes:
            additional_notes = "N/A"

        prompt = f"""
        You are an expert book genre classifier. Using the comprehensive examples provided below, analyze the given book concept and recommend the most suitable genres and subgenres.

        {all_combinations}

        Now analyze this book concept:
        Concept: "{concept}"

        Additionl Notes: "{additional_notes}"

        Based on the examples above and the concept provided, recommend 2-4 of the most suitable genre-subgenre combinations from the available options. Consider:
        1. Primary themes and elements in the concept
        2. Target audience indicators (age, interests)
        3. Setting and world-building elements
        4. Tone and style indicators
        5. Story elements and plot suggestions

        You must use only a valid genre value from the list of examples. Do not use value GenreType as genre value.

        Respond in JSON format with this exact structure:
        {{
            "recommended_combinations": [
                {{
                    "genre": "genre_value",
                    "subgenre": "subgenre_value",
                    "confidence": 0.95,
                    "reasoning": "Brief explanation of why this combination fits"
                }}
            ]
        }}

        Only recommend combinations that exist in the examples above. Use the exact genre and subgenre values from the examples.
        """

        try:
            # response = await self.llm_client.generate_response(prompt)
            
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            # Extract JSON from response if it's wrapped in text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                response = response[start:end]
            result = json.loads(response)
            
            # Validate that recommended combinations are valid
            validated_combinations = self._validate_genre_recommendations(
                result.get("recommended_combinations", [])
            )
            
            return {
                "genre_recommendations": validated_combinations,
                "analysis_successful": True,
                "total_recommendations": len(validated_combinations)
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in concept analysis: {e}")
            return {
                "genre_recommendations": [],
                "analysis_successful": False,
                "error": f"Invalid JSON response: {e}"
            }
        except Exception as e:
            print(f"Error in concept analysis: {e}")
            return {
                "genre_recommendations": [],
                "analysis_successful": False,
                "error": str(e)
            }

    def _validate_genre_recommendations(self, recommendations: list) -> list:
        """Validate and filter genre recommendations from LLM response."""
        from musequill.models.book.genre import GenreMapping, GenreType, SubGenreType
        
        validated_combinations = []
        
        for combo in recommendations:
            try:
                # Ensure required fields exist
                if not all(key in combo for key in ["genre", "subgenre"]):
                    print(f"Missing required fields in recommendation: {combo}")
                    continue
                
                # Convert string values to enum types
                genre = GenreType.from_string(combo["genre"].lower())
                subgenre = SubGenreType.from_string(combo["subgenre"].lower())
                
                # Validate the combination exists
                if GenreMapping.is_valid_combination(genre, subgenre):
                    validated_combinations.append({
                        "genre": genre,
                        "subgenre": subgenre,
                        "confidence": float(combo.get("confidence", 0.8)),
                        "reasoning": combo.get("reasoning", ""),
                        "display_name": f"{genre.display_name} - {subgenre.display_name}"
                    })
                else:
                    print(f"Invalid genre-subgenre combination: {genre.value}/{subgenre.value}")
                    
            except (ValueError, KeyError, TypeError) as e:
                print(f"Invalid combination skipped: {combo} - {e}")
                continue
        
        # Sort by confidence score (highest first)
        validated_combinations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return validated_combinations

    def _build_genre_examples(self) -> str:
        """Build comprehensive one-shot learning examples for all genre-subgenre combinations."""
        from musequill.models.book.genre import GenreMapping, GenreType, SubGenreType
        
        # Define example concepts for each genre-subgenre combination
        genre_examples = {
            # ROMANCE examples
            (GenreType.ROMANCE, SubGenreType.CONTEMPORARY_ROMANCE): 
                "A marketing executive falls for her rival at a competing firm in modern-day New York",
            (GenreType.ROMANCE, SubGenreType.HISTORICAL_ROMANCE): 
                "A Victorian-era governess and a mysterious duke find forbidden love in 1800s England",
            (GenreType.ROMANCE, SubGenreType.PARANORMAL_ROMANCE): 
                "A vampire hunter discovers she's destined to love the very creature she's sworn to destroy",
            (GenreType.ROMANCE, SubGenreType.DARK_ROMANCE): 
                "A kidnapped woman develops Stockholm syndrome for her captor, a dangerous mafia boss",
            (GenreType.ROMANCE, SubGenreType.BILLIONAIRE_ROMANCE): 
                "A struggling artist becomes the personal assistant to a ruthless tech billionaire",
            (GenreType.ROMANCE, SubGenreType.ENEMIES_TO_LOVERS): 
                "Two rival lawyers are forced to work together on a high-profile case",
            (GenreType.ROMANCE, SubGenreType.SECOND_CHANCE_ROMANCE): 
                "High school sweethearts reunite at their 15-year reunion after bitter breakup",

            # FANTASY examples
            (GenreType.FANTASY, SubGenreType.HIGH_FANTASY): 
                "A farm boy discovers he's the chosen one destined to defeat an ancient dark lord",
            (GenreType.FANTASY, SubGenreType.URBAN_FANTASY): 
                "A detective in modern Chicago investigates murders committed by supernatural creatures",
            (GenreType.FANTASY, SubGenreType.DARK_FANTASY): 
                "A necromancer seeks revenge against the kingdom that burned her family alive",
            (GenreType.FANTASY, SubGenreType.EPIC_FANTASY): 
                "Multiple kingdoms unite against an awakening ancient evil threatening all realms",
            (GenreType.FANTASY, SubGenreType.FAIRY_TALE_RETELLING): 
                "Cinderella reimagined as a cyberpunk hacker fighting corporate oppression",
            
            # ROMANTASY examples
            (GenreType.ROMANTASY, SubGenreType.ROMANTASY_SUB): 
                "A fae prince and mortal woman navigate forbidden love across magical realms",
            
            # COZY FANTASY examples
            (GenreType.COZY_FANTASY, SubGenreType.COZY_FANTASY_SUB): 
                "A dragon opens a peaceful tea shop in a magical village where all creatures live harmoniously",

            # MYSTERY examples
            (GenreType.MYSTERY, SubGenreType.COZY_MYSTERY): 
                "A librarian in a small town keeps stumbling upon murders during her book club meetings",
            (GenreType.MYSTERY, SubGenreType.POLICE_PROCEDURAL): 
                "A detective team works systematically through evidence to solve a serial killer case",
            (GenreType.MYSTERY, SubGenreType.DETECTIVE_FICTION): 
                "A private investigator with a photographic memory solves cases the police can't crack",

            # THRILLER examples
            (GenreType.THRILLER, SubGenreType.PSYCHOLOGICAL_THRILLER): 
                "A woman begins to question her sanity when her husband insists events she remembers never happened",
            (GenreType.THRILLER, SubGenreType.DOMESTIC_THRILLER): 
                "A perfect suburban marriage hides deadly secrets that threaten to destroy everything",
            (GenreType.THRILLER, SubGenreType.LEGAL_THRILLER): 
                "A lawyer defending a murder case discovers the victim was involved in a conspiracy",

            # SCIENCE FICTION examples
            (GenreType.SCIENCE_FICTION, SubGenreType.SPACE_OPERA): 
                "A rebel alliance fights against an galactic empire across multiple star systems",
            (GenreType.SCIENCE_FICTION, SubGenreType.CYBERPUNK): 
                "A hacker in a dystopian future fights corporate control through digital rebellion",
            (GenreType.SCIENCE_FICTION, SubGenreType.TIME_TRAVEL): 
                "A scientist accidentally changes the past and must fix the timeline before reality collapses",
            (GenreType.SCIENCE_FICTION, SubGenreType.POST_APOCALYPTIC): 
                "Survivors of a nuclear war rebuild civilization in the wasteland decades later",

            # YOUNG ADULT examples
            (GenreType.YOUNG_ADULT, SubGenreType.YA_FANTASY): 
                "A teenage girl discovers she has magical powers and must attend a secret supernatural academy",
            (GenreType.YOUNG_ADULT, SubGenreType.YA_ROMANCE): 
                "Two high school students navigate first love amid family drama and college pressures",
            (GenreType.YOUNG_ADULT, SubGenreType.YA_DYSTOPIAN): 
                "Teenagers rebel against an oppressive government in a future totalitarian society",
            (GenreType.YOUNG_ADULT, SubGenreType.YA_CONTEMPORARY): 
                "A shy teenager gains confidence through joining the school's debate team",

            # COMING OF AGE examples
            (GenreType.COMING_OF_AGE, SubGenreType.COMING_OF_AGE_SUB): 
                "A child story about a bunny adventure in Africa, learning about courage and friendship",

            # HORROR examples
            (GenreType.HORROR, SubGenreType.PSYCHOLOGICAL_HORROR): 
                "A writer's grip on reality deteriorates as the characters from his novel seem to come alive",
            (GenreType.HORROR, SubGenreType.SUPERNATURAL_HORROR): 
                "A family moves into a haunted house where vengeful spirits torment the living",
            (GenreType.HORROR, SubGenreType.VAMPIRE): 
                "A small town is terrorized by an ancient vampire who feeds on fear as much as blood",

            # SELF-HELP examples
            (GenreType.SELF_HELP, SubGenreType.MOTIVATIONAL): 
                "A guide to overcoming limiting beliefs and achieving your biggest dreams",
            (GenreType.SELF_HELP, SubGenreType.PERSONAL_FINANCE): 
                "How to build wealth and achieve financial independence through smart investing",
            (GenreType.SELF_HELP, SubGenreType.MINDFULNESS): 
                "Daily meditation practices for reducing stress and finding inner peace",

            # CHILDREN'S FICTION examples (if available in your system)
            # Note: Add these if GenreType.CHILDRENS_FICTION exists in your enum
            # (GenreType.CHILDRENS_FICTION, SubGenreType.CHILDRENS_PICTURE_BOOK): 
            #     "A brave little bunny goes on an adventure through the magical forest to help lost animals",
            # (GenreType.CHILDRENS_FICTION, SubGenreType.CHILDRENS_CHAPTER_BOOK): 
            #     "Third-grader Emma learns about friendship when a new student joins her class",

            # NON-FICTION examples
            (GenreType.TRUE_CRIME, SubGenreType.TRUE_CRIME_SUB): 
                "The investigation into a serial killer who terrorized a small town for decades",
            (GenreType.BIOGRAPHY, SubGenreType.CELEBRITY_BIOGRAPHY): 
                "The rise and fall of a Hollywood star who overcame addiction to rebuild their career",
            (GenreType.BUSINESS, SubGenreType.ENTREPRENEURSHIP): 
                "How to start and scale a successful startup from idea to IPO",
        }

        # Get all available combinations from the actual system
        all_combinations = GenreMapping.get_all_combinations()
        
        # Build the examples string
        examples_text = "Here are examples of book concepts and their correct genre-subgenre classifications:\n\n"
        
        # Add examples for combinations we have defined
        for (genre, subgenre), example in genre_examples.items():
            examples_text += f'Concept: "{example}"\n'
            examples_text += f'Genre: "{genre.value}", Subgenre: "{subgenre.value}"\n\n'

        # Add generic examples for remaining combinations not covered above
        additional_examples = {
            "literary_fiction": "A character study exploring family relationships across three generations",
            "memoir": "A personal account of overcoming childhood trauma and finding healing",
            "health": "Evidence-based strategies for improving physical and mental wellness",
            "cooking": "Traditional family recipes passed down through generations with modern twists",
            "travel": "A comprehensive guide to backpacking through Southeast Asia on a budget",
            "technology": "How artificial intelligence is transforming modern healthcare",
        }

        # Find combinations not yet covered and add basic examples
        covered_combinations = set(genre_examples.keys())
        for combo in all_combinations:
            if (combo.genre, combo.subgenre) not in covered_combinations:
                # Generate a basic example based on genre type
                genre_key = combo.genre.value.lower()
                if genre_key in additional_examples:
                    example = additional_examples[genre_key]
                else:
                    example = f"A story in the {combo.genre.display_name} genre with {combo.subgenre.display_name} elements"
                
                examples_text += f'Concept: "{example}"\n'
                examples_text += f'Genre: "{combo.genre.value}", Subgenre: "{combo.subgenre.value}"\n\n'

        examples_text += "\nIMPORTANT: Only recommend combinations from the available genre-subgenre pairs listed above.\n"
        examples_text += "Each recommendation should include confidence score (0.0-1.0) and reasoning.\n"

        return examples_text


    async def analyze_concept_old(self, concept: str) -> Dict[str, Any]:
        """Analyze initial book concept and extract key elements."""
        prompt = f"""
        Analyze this book concept and extract key elements:
        
        Concept: "{concept}"
        
        Please identify:
        1. Primary genre signals (fantasy, romance, mystery, etc.)
        2. Target audience indicators (adult, young adult, children)
        3. Setting type (contemporary, historical, fantasy world, etc.)
        4. Tone and style indicators (dark, humorous, serious, etc.)
        5. Story complexity level (simple, moderate, complex)
        
        Respond in JSON format with these fields:
        {{
            "genre_signals": ["list", "of", "detected", "genres"],
            "audience_signals": ["target", "audience", "indicators"],
            "setting_signals": ["setting", "type", "indicators"],
            "tone_signals": ["tone", "indicators"],
            "complexity": "simple/moderate/complex"
        }}
        """
        
        try:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            # Parse JSON response (basic parsing for POC)
            import json
            # Extract JSON from response if it's wrapped in text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback if JSON parsing fails
                return {"genre_signals": ["general"], "audience_signals": ["adult"], 
                       "setting_signals": ["contemporary"], "tone_signals": ["neutral"], 
                       "complexity": "moderate"}
        except Exception as e:
            logger.error(f"Error analyzing concept: {e}")
            return {"genre_signals": ["general"], "audience_signals": ["adult"], 
                   "setting_signals": ["contemporary"], "tone_signals": ["neutral"], 
                   "complexity": "moderate"}
    
    async def suggest_options(self, step_name: str, concept: str, previous_selections: Dict[str, str], 
                            available_options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get LLM suggestions for wizard step options."""
        
        # Format previous selections
        selections_text = "\n".join([f"- {k}: {v}" for k, v in previous_selections.items()])
        
        # Format available options
        options_text = "\n".join([f"- {opt['id']}: {opt['name']} - {opt.get('description', '')}" 
                                 for opt in available_options])
        
        prompt = f"""
        You are helping a user create a commercially successful book. 
        
        Book concept: "{concept}"
        
        Previous selections:
        {selections_text}
        
        Current step: {step_name}
        Available options:
        {options_text}
        
        Please:
        1. Recommend the top 3-4 most suitable options for commercial success
        2. Provide a brief reasoning for each recommendation
        3. Score each recommended option from 0-100 based on commercial potential
        
        Focus on market appeal, genre consistency, and commercial viability.
        
        Respond in JSON format:
        {{
            "recommendations": [
                {{
                    "option_id": "option_identifier",
                    "score": 85,
                    "reasoning": "Brief explanation of why this works commercially"
                }}
            ],
            "general_reasoning": "Overall reasoning for these recommendations"
        }}
        """
        
        try:
            response = await asyncio.to_thread(self.llm.invoke, prompt)
            import json
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback - return top 3 options with default scores
                return {
                    "recommendations": [
                        {"option_id": opt["id"], "score": 80, "reasoning": "Good commercial option"}
                        for opt in available_options[:3]
                    ],
                    "general_reasoning": "These options offer good commercial potential."
                }
        except Exception as e:
            logger.error(f"Error getting LLM suggestions: {e}")
            # Return fallback recommendations
            return {
                "recommendations": [
                    {"option_id": opt["id"], "score": 70, "reasoning": "Recommended option"}
                    for opt in available_options[:3]
                ],
                "general_reasoning": "Standard commercial recommendations."
            }

