TARGET_JSON_SCHEMA = """{
  "title": "string",
  "author": "string",
  "blueprint": {
    "phase_1": {
      "commercial_viability": "string",
      "target_market": {
        "primary": "string",
        "secondary": "string"
      },
      "competitive_positioning": "string",
      "unique_value_proposition": "string",
      "publishing_path": "string"
    },
    "phase_2": {
      "core_premise": {
        "logline": "string",
        "central_question": "string",
        "core_conflict": "string"
      },
      "structural_framework": {
        "act_structure": "string",
        "key_plot_points": [
          {
            "name": "string",
            "description": "string",
            "word_count_target": "number"
          }
        ],
        "character_arc_milestones": [
          {
            "stage": "string",
            "description": "string"
          }
        ],
        "pacing_strategy": "string"
      },
      "chapter_architecture": {
        "estimated_chapter_count": "number",
        "average_chapter_length": "number",
        "chapter_function_matrix": [
          {
            "chapter": "number",
            "plot_function": "string",
            "character_function": "string"
          }
        ]
      }
    },
    "phase_3": {
      "protagonist_blueprint": {
        "core_personality_traits": ["string"],
        "character_arc_framework": {
          "beginning": "string",
          "middle": "string",
          "end": "string"
        },
        "voice_and_dialogue_style": "string",
        "internal_conflict_engine": "string"
      },
      "supporting_character_ecosystem": {
        "antagonist_profile": "string",
        "ally_mentor_roles": ["string"],
        "character_relationship_web": [
          {
            "character": "string",
            "relationship": "string"
          }
        ]
      },
      "narrative_voice_strategy": {
        "pov_implementation": "string",
        "narrative_distance": "string",
        "voice_consistency_guidelines": "string"
      }
    },
    "phase_4": {
      "setting_development": {
        "world_type_implementation": "string",
        "technology_integration": "string",
        "cultural_and_social_systems": "string",
        "sensory_world_building": "string"
      },
      "research_action_plan": {
        "primary_research_areas": ["string"],
        "research_timeline": "string",
        "fact_checking_systems": "string",
        "expert_consultation_needs": "string"
      },
      "consistency_management": {
        "world_bible_creation": ["string"],
        "setting_detail_database": "string"
      }
    },
    "phase_5": {
      "pre_writing_phase": {
        "weeks": "string",
        "detailed_outline_creation": "string",
        "character_profiles_completion": "string",
        "world_building_documentation": "string",
        "research_completion": "string"
      },
      "drafting_phase": {
        "weeks": "string",
        "daily_writing_targets": "number",
        "weekly_milestones": ["string"],
        "chapter_writing_order": "string",
        "draft_quality_expectations": "string"
      },
      "revision_strategy": {
        "macro_revision": "string",
        "micro_revision": "string",
        "line_editing": "string",
        "final_polish": "string"
      },
      "quality_control_checkpoints": {
        "25_percent_review": "string",
        "50_percent_review": "string",
        "75_percent_review": "string",
        "completion_review": "string"
      }
    },
    "phase_6": {
      "writing_style_execution": {
        "sentence_structure_patterns": "string",
        "vocabulary_guidelines": "string",
        "paragraph_construction": "string",
        "dialogue_implementation": "string"
      },
      "tone_maintenance_system": {
        "emotional_baseline": "string",
        "tonal_shifts": "string",
        "genre_conventions": "string",
        "audience_alignment": "string"
      },
      "quality_assurance_checklist": {
        "style_consistency_markers": ["string"],
        "tone_verification_points": ["string"],
        "voice_authentication": ["string"]
      }
    },
    "phase_7": {
      "market_positioning": {
        "genre_classification": "string",
        "comp_title_analysis": [
          {
            "title": "string",
            "author": "string",
            "similarity": "string"
          }
        ],
        "target_reader_profile": {
          "age_range": "string",
          "interests": ["string"],
          "reading_level": "string"
        },
        "marketing_hooks": ["string"]
      },
      "publishing_readiness": {
        "manuscript_requirements": "string",
        "query_letter_elements": ["string"],
        "self_publishing_checklist": ["string"],
        "beta_reader_strategy": "string"
      },
      "launch_strategy_framework": {
        "pre_launch_timeline": "string",
        "launch_week_tactics": ["string"],
        "post_launch_growth": ["string"]
      }
    }
  }
}"""


EXPECTED_OUTPUT = """
{
  "title": "The Enchanted Forest of Peter",
  "author": "Joseph Campbell",
  "blueprint": {
    "phase_1": {
      "commercial_viability": "Strong appeal in the middle-grade fantasy market. Stories with cultural roots like Slavic mythology and animal protagonists are particularly marketable due to rising interest in diverse, educational content.",
      "target_market": {
        "primary": "Children aged 7\u201312 who enjoy whimsical fantasy adventures.",
        "secondary": "Parents, teachers, and librarians seeking meaningful stories with folklore elements."
      },
      "competitive_positioning": "Competes with titles like 'The Tale of Despereaux' and 'The Spiderwick Chronicles' but stands out with its Slavic folklore integration.",
      "unique_value_proposition": "The combination of a charming animal protagonist and mythological creatures from Eastern Europe offers both entertainment and cultural education.",
      "publishing_path": "hybrid"
    },
    "phase_2": {
      "core_premise": {
        "logline": "A brave bunny ventures beyond his meadow into a magical forest, where he faces mythic creatures and returns home forever changed.",
        "central_question": "Will Peter\u2019s courage and wit be enough to overcome the enchantments and beings within the forest?",
        "core_conflict": "Peter must confront supernatural forces that test his values and bravery."
      },
      "structural_framework": {
        "act_structure": "Three acts aligned with the Hero\u2019s Journey: Departure, Initiation, and Return.",
        "key_plot_points": [
          {
            "name": "Ordinary World",
            "description": "Peter in the peaceful meadow",
            "word_count_target": 5000
          },
          {
            "name": "Call to Adventure",
            "description": "A mysterious event tempts Peter into the forest",
            "word_count_target": 3000
          },
          {
            "name": "Trials",
            "description": "Encounters with Baba Yaga, Leshy, Domovoi, Rusalka",
            "word_count_target": 25000
          },
          {
            "name": "Crisis",
            "description": "Peter faces his deepest fear",
            "word_count_target": 5000
          },
          {
            "name": "Return",
            "description": "Peter returns wiser, transformed",
            "word_count_target": 5000
          }
        ],
        "character_arc_milestones": [
          {
            "stage": "Beginning",
            "description": "Peter is curious but naive"
          },
          {
            "stage": "Middle",
            "description": "Peter is challenged and learns through trials"
          },
          {
            "stage": "End",
            "description": "Peter matures into a brave, wise figure"
          }
        ],
        "pacing_strategy": "Keep transitions brisk, shifting to new scenes or characters every 1000\u20131500 words to maintain engagement."
      },
      "chapter_architecture": {
        "estimated_chapter_count": 20,
        "average_chapter_length": 2500,
        "chapter_function_matrix": [
          {
            "chapter": 1,
            "plot_function": "Setup",
            "character_function": "Establish personality"
          },
          {
            "chapter": 5,
            "plot_function": "First major test",
            "character_function": "Reveal internal doubt"
          },
          {
            "chapter": 10,
            "plot_function": "Midpoint reversal",
            "character_function": "Growth through failure"
          },
          {
            "chapter": 15,
            "plot_function": "Climax",
            "character_function": "Prove transformation"
          },
          {
            "chapter": 20,
            "plot_function": "Return and resolution",
            "character_function": "Share gained wisdom"
          }
        ]
      }
    },
    "phase_3": {
      "protagonist_blueprint": {
        "core_personality_traits": [
          "curious",
          "charismatic",
          "brave",
          "playful"
        ],
        "character_arc_framework": {
          "beginning": "Peter is impulsive and unaware of the forest's risks.",
          "middle": "Peter struggles with fear and failure but learns through encounters.",
          "end": "Peter becomes confident, wise, and self-aware."
        },
        "voice_and_dialogue_style": "Charming, witty, and slightly na\u00efve early on; matures into clearer, confident tones.",
        "internal_conflict_engine": "Fear of insignificance; desire to prove himself."
      },
      "supporting_character_ecosystem": {
        "antagonist_profile": "The forest itself as a supernatural force, occasionally embodied in Baba Yaga\u2019s trials.",
        "ally_mentor_roles": [
          "A clever Domovoi offering riddles",
          "A kind Rusalka showing the value of empathy"
        ],
        "character_relationship_web": [
          {
            "character": "Leshy",
            "relationship": "Trickster adversary"
          },
          {
            "character": "Baba Yaga",
            "relationship": "Archetypal gatekeeper"
          },
          {
            "character": "Domovoi",
            "relationship": "Ally and wisdom guide"
          }
        ]
      },
      "narrative_voice_strategy": {
        "pov_implementation": "Descriptive third-person narration focusing on observable behavior and speech.",
        "narrative_distance": "Medium-close\u2014emotion inferred through action, not internal monologue.",
        "voice_consistency_guidelines": "Maintain light, whimsical tone even during tense scenes; avoid overt moralizing."
      }
    },
    "phase_4": {
      "setting_development": {
        "world_type_implementation": "High fantasy built from folklore-infused environments: whispering trees, glowing mushrooms, magical rivers.",
        "technology_integration": "None directly, but Enlightenment-era logic may influence creature behavior (symbolically).",
        "cultural_and_social_systems": "Forest tribes, spirits with their own customs\u2014drawn from Slavic myth.",
        "sensory_world_building": "Use rich sensory input: rustling leaves, earthy scents, glowing fog, singing water."
      },
      "research_action_plan": {
        "primary_research_areas": [
          "Slavic folklore",
          "Mythical creatures like Rusalka and Baba Yaga"
        ],
        "research_timeline": "2 weeks pre-writing, revisited at each mythological chapter",
        "fact_checking_systems": "Cross-reference regional myths from academic folklore sources.",
        "expert_consultation_needs": "Optional consultation with Eastern European folklore experts or professors."
      },
      "consistency_management": {
        "world_bible_creation": [
          "Creature behavior",
          "Magical rules",
          "Forest geography",
          "Mythological lore"
        ],
        "setting_detail_database": "Organized spreadsheet or Notion page categorizing world logic and sensory elements"
      }
    },
    "phase_5": {
      "pre_writing_phase": {
        "weeks": "Weeks 1\u20132",
        "detailed_outline_creation": "20-chapter breakdown by plot and character progression.",
        "character_profiles_completion": "Profile Peter and all mythological figures with motivations and traits.",
        "world_building_documentation": "Forest map, glossary of creatures, rule system for magic.",
        "research_completion": "Complete before drafting; allow spot-updates during writing."
      },
      "drafting_phase": {
        "weeks": "Weeks 3\u201310",
        "daily_writing_targets": 1500,
        "weekly_milestones": [
          "Complete 2 chapters per week",
          "Weekly check-in on pacing and plot integrity"
        ],
        "chapter_writing_order": "Linear, to maintain organic character progression",
        "draft_quality_expectations": "Readable first draft with complete scenes and consistent tone"
      },
      "revision_strategy": {
        "macro_revision": "Restructure any out-of-place encounters or rushed arcs.",
        "micro_revision": "Polish transitions and ensure mythological accuracy.",
        "line_editing": "Refine sentence rhythm, age-appropriate word choice.",
        "final_polish": "Proofread for flow, clarity, grammar, and formatting."
      },
      "quality_control_checkpoints": {
        "25_percent_review": "Review pacing, Peter's early arc, forest intro.",
        "50_percent_review": "Check trial sequences and plot momentum.",
        "75_percent_review": "Ensure climax builds from prior events logically.",
        "completion_review": "Read entire manuscript aloud for rhythm and tone."
      }
    },
    "phase_6": {
      "writing_style_execution": {
        "sentence_structure_patterns": "Short to medium sentences with variation for dramatic effect.",
        "vocabulary_guidelines": "Simple, vivid words; avoid idioms unfamiliar to children.",
        "paragraph_construction": "1\u20133 sentence paragraphs; break often for readability.",
        "dialogue_implementation": "Distinct speech patterns for each creature; Peter's voice evolves with maturity."
      },
      "tone_maintenance_system": {
        "emotional_baseline": "Whimsical curiosity, with wonder and subtle tension.",
        "tonal_shifts": "Tension rises during trials but defused with wit and relief.",
        "genre_conventions": "Maintain magical elements, clear moral arc, accessible danger.",
        "audience_alignment": "No intense violence; use metaphor or fantasy elements for serious themes."
      },
      "quality_assurance_checklist": {
        "style_consistency_markers": [
          "Sentence length variation",
          "Child-friendly phrasing",
          "Witty tone retention"
        ],
        "tone_verification_points": [
          "Major trials",
          "Resolution moments",
          "Opening scene"
        ],
        "voice_authentication": [
          "Peter\u2019s evolving tone",
          "Mythical character speech",
          "Narrator consistency"
        ]
      }
    },
    "phase_7": {
      "market_positioning": {
        "genre_classification": "Middle Grade Fantasy Adventure",
        "comp_title_analysis": [
          {
            "title": "The Tale of Despereaux",
            "author": "Kate DiCamillo",
            "similarity": "Animal protagonist with a moral journey"
          },
          {
            "title": "The Wildwood Chronicles",
            "author": "Colin Meloy",
            "similarity": "Mythical forest setting"
          },
          {
            "title": "East of the Sun, West of the Moon",
            "author": "Tales of the Norse",
            "similarity": "Rooted in cultural mythology"
          }
        ],
        "target_reader_profile": {
          "age_range": "7\u201312",
          "interests": [
            "Fantasy",
            "Animals",
            "Folklore",
            "Magic",
            "Adventure"
          ],
          "reading_level": "Middle grade; accessible yet challenging"
        },
        "marketing_hooks": [
          "A bunny\u2019s magical journey through Slavic myth!",
          "Like Narnia, but with Baba Yaga and a rabbit hero!",
          "Folklore meets forest magic\u2014perfect for curious young minds."
        ]
      },
      "publishing_readiness": {
        "manuscript_requirements": "40,000\u201360,000 words, 12pt font, double spaced",
        "query_letter_elements": [
          "Hook",
          "Synopsis",
          "Author bio",
          "Target audience"
        ],
        "self_publishing_checklist": [
          "Cover design",
          "Interior formatting",
          "ISBN",
          "Metadata",
          "Upload to KDP/IngramSpark"
        ],
        "beta_reader_strategy": "Gather 5\u20137 parents and educators of target readers for pre-publishing feedback."
      },
      "launch_strategy_framework": {
        "pre_launch_timeline": "6 months pre-release: mailing list, early ARC reviews, social media build-up",
        "launch_week_tactics": [
          "Virtual reading",
          "Author Q&A",
          "Discounted launch pricing",
          "Cross-promo with folklore educators"
        ],
        "post_launch_growth": [
          "Monthly themed blog posts",
          "Library outreach",
          "Folklore-based school activity kits"
        ]
      }
    }
  }
}
"""
