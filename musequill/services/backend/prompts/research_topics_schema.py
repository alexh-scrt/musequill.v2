#!/usr/bin/env python3
"""
Research Topics JSON Schema and Expected Output

This module defines the JSON schema structure for research topic generation
and provides a complete example of expected output format.
"""

RESEARCH_TOPICS_JSON_SCHEMA = """{
  "book_title": "string",
  "author": "string", 
  "research_topics": [
    {
      "category": "string",
      "topic": "string",
      "description": "string",
      "priority": "string",
      "estimated_time_hours": "number",
      "research_methods": ["string"],
      "key_questions": ["string"],
      "sources_suggested": ["string"]
    }
  ],
  "total_estimated_research_time": "number",
  "research_timeline": "string"
}"""

RESEARCH_TOPICS_EXPECTED_OUTPUT = """{
  "book_title": "The Enchanted Forest of Peter",
  "author": "Joseph Campbell",
  "research_topics": [
    {
      "category": "mythology_folklore",
      "topic": "Slavic Forest Spirits and Mythological Creatures",
      "description": "Research traditional Slavic folklore creatures that inhabit forests, including Rusalka, Baba Yaga, Domovoi, and forest spirits, focusing on their characteristics, behaviors, and cultural significance.",
      "priority": "high",
      "estimated_time_hours": 8,
      "research_methods": ["academic_sources", "folklore_collections", "cultural_websites"],
      "key_questions": [
        "What are the defining characteristics of major Slavic forest creatures?",
        "How do these creatures interact with humans in traditional stories?",
        "What cultural values do these creatures represent?",
        "How can these creatures be adapted for children aged 7-12?",
        "What are the regional variations in these folklore traditions?"
      ],
      "sources_suggested": [
        "Academic folklore journals",
        "The Golden Bough by James George Frazer",
        "Slavic mythology encyclopedias",
        "University folklore departments"
      ]
    },
    {
      "category": "natural_world",
      "topic": "Forest Ecosystems and Wildlife Behavior",
      "description": "Study forest environments, animal behaviors, and ecological relationships to create authentic natural settings and believable animal characters.",
      "priority": "medium",
      "estimated_time_hours": 6,
      "research_methods": ["scientific_sources", "nature_documentaries", "field_guides"],
      "key_questions": [
        "How do rabbits behave in forest environments?",
        "What are the predator-prey relationships in temperate forests?",
        "What sensory details make forest descriptions vivid?",
        "How do animals communicate in forest settings?",
        "What are seasonal changes in forest ecosystems?"
      ],
      "sources_suggested": [
        "National Geographic nature guides",
        "Wildlife behavior studies",
        "Forest ecology textbooks",
        "Nature documentaries"
      ]
    },
    {
      "category": "cultural_anthropology",
      "topic": "Slavic Cultural Values and Traditions",
      "description": "Understand the cultural context behind Slavic folklore to ensure respectful and accurate representation of mythological elements.",
      "priority": "high",
      "estimated_time_hours": 5,
      "research_methods": ["academic_sources", "cultural_sources", "expert_interviews"],
      "key_questions": [
        "What cultural values are embedded in Slavic folklore?",
        "How do Slavic cultures view the relationship between humans and nature?",
        "What are the moral lessons in traditional Slavic stories?",
        "How can cultural elements be presented respectfully?",
        "What are the historical contexts of these folklore traditions?"
      ],
      "sources_suggested": [
        "Cultural anthropology journals",
        "Slavic cultural centers",
        "Eastern European folklore experts",
        "Cultural history books"
      ]
    },
    {
      "category": "psychology_behavior",
      "topic": "Child Development and Coming-of-Age Psychology",
      "description": "Research psychological aspects of childhood development, courage-building, and coming-of-age journeys to create authentic character growth.",
      "priority": "medium",
      "estimated_time_hours": 4,
      "research_methods": ["academic_sources", "developmental_psychology"],
      "key_questions": [
        "How do children aged 7-12 process fear and courage?",
        "What psychological stages occur during coming-of-age journeys?",
        "How do children relate to animal characters?",
        "What challenges resonate with this age group?",
        "How do children understand moral lessons?"
      ],
      "sources_suggested": [
        "Developmental psychology textbooks",
        "Child psychology journals",
        "Educational research",
        "Children's literature analysis"
      ]
    },
    {
      "category": "linguistics",
      "topic": "Age-Appropriate Language and Dialogue",
      "description": "Study language patterns, vocabulary levels, and dialogue styles appropriate for the target age group while maintaining engaging storytelling.",
      "priority": "medium",
      "estimated_time_hours": 3,
      "research_methods": ["linguistic_analysis", "children_literature_study"],
      "key_questions": [
        "What vocabulary level is appropriate for ages 7-12?",
        "How do successful children's fantasy books handle dialogue?",
        "What sentence structures engage young readers?",
        "How can complex concepts be simplified without dumbing down?",
        "What dialogue patterns create distinct character voices?"
      ],
      "sources_suggested": [
        "Children's literature guides",
        "Educational linguistics research",
        "Award-winning children's fantasy books",
        "Reading level analysis tools"
      ]
    },
    {
      "category": "arts_crafts",
      "topic": "Traditional Slavic Arts and Symbolic Elements",
      "description": "Explore traditional Slavic arts, symbols, and craft traditions to add authentic visual and cultural details to the story.",
      "priority": "low",
      "estimated_time_hours": 3,
      "research_methods": ["cultural_sources", "art_history", "museum_resources"],
      "key_questions": [
        "What are common symbols in Slavic folk art?",
        "How are forests and nature depicted in traditional Slavic art?",
        "What colors and patterns are characteristic of Slavic traditions?",
        "How can visual elements enhance the story's atmosphere?",
        "What craft traditions relate to forest and nature themes?"
      ],
      "sources_suggested": [
        "Slavic folk art collections",
        "Cultural museums",
        "Traditional craft guides",
        "Art history resources"
      ]
    },
    {
      "category": "daily_life",
      "topic": "Historical and Traditional Forest Living",
      "description": "Research how people historically lived in and interacted with forest environments to create believable world-building details.",
      "priority": "low",
      "estimated_time_hours": 2,
      "research_methods": ["historical_sources", "anthropological_studies"],
      "key_questions": [
        "How did people traditionally survive in forest environments?",
        "What foods, tools, and shelters were used in forest settings?",
        "How did historical communities view forest creatures?",
        "What practical knowledge would forest dwellers have?",
        "How can these details enrich the story's authenticity?"
      ],
      "sources_suggested": [
        "Historical survival guides",
        "Anthropological studies",
        "Traditional knowledge books",
        "Historical documentaries"
      ]
    }
  ],
  "total_estimated_research_time": 31,
  "research_timeline": "3-4 weeks concentrated research before writing begins, with ongoing spot research during drafting phase as specific questions arise"
}"""

# Research categories with descriptions
RESEARCH_CATEGORIES = {
    "mythology_folklore": "Cultural myths, legends, folklore, and traditional stories",
    "historical_context": "Time periods, historical events, social customs, daily life",
    "natural_world": "Geography, ecology, animal behavior, natural phenomena",
    "cultural_anthropology": "Social structures, belief systems, customs, traditions",
    "science_technology": "Scientific concepts, technological innovations, technical processes",
    "psychology_behavior": "Character psychology, human behavior, social dynamics",
    "linguistics": "Language patterns, dialects, communication styles",
    "arts_crafts": "Traditional arts, crafts, skills, creative practices",
    "social_political": "Government systems, political structures, social hierarchies",
    "daily_life": "Food, clothing, housing, work, entertainment, family life"
}

# Priority levels with descriptions
PRIORITY_LEVELS = {
    "high": "Essential for story authenticity and plot development",
    "medium": "Important for richness and depth but not critical for basic story",
    "low": "Nice-to-have details that could enhance but aren't necessary"
}

# Research methods with descriptions
RESEARCH_METHODS = {
    "academic_sources": "Scholarly articles, university research, peer-reviewed studies",
    "primary_sources": "Historical documents, firsthand accounts, original texts",
    "expert_interviews": "Consultations with specialists, academics, practitioners",
    "field_research": "Direct observation, site visits, hands-on experience",
    "multimedia_sources": "Documentaries, podcasts, educational videos",
    "cultural_sources": "Community resources, cultural centers, traditional practitioners",
    "online_databases": "Digital archives, specialized websites, digital libraries",
    "books_literature": "Specialized books, reference works, literary sources",
    "folklore_collections": "Compiled folklore, myth collections, traditional story anthologies",
    "nature_documentaries": "Wildlife and nature documentaries, educational videos",
    "scientific_sources": "Scientific journals, research papers, field studies",
    "cultural_websites": "Cultural organization websites, educational cultural resources",
    "developmental_psychology": "Child development research, educational psychology",
    "linguistic_analysis": "Language studies, vocabulary research, communication analysis",
    "children_literature_study": "Analysis of successful children's books and writing",
    "art_history": "Art historical sources, visual culture studies",
    "museum_resources": "Museum collections, exhibits, educational materials",
    "historical_sources": "Historical texts, period documents, historical research",
    "anthropological_studies": "Cultural anthropology research, ethnographic studies"
}