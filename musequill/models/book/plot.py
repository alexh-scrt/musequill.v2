from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union


class PlotType(str, Enum):
    """Comprehensive plot archetypes and story structures for book generation."""
    
    # Classic Archetypal Plots (Christopher Booker's Seven Basic Plots + expansions)
    OVERCOMING_THE_MONSTER = "overcoming_the_monster"
    RAGS_TO_RICHES = "rags_to_riches"
    THE_QUEST = "the_quest"
    VOYAGE_AND_RETURN = "voyage_and_return"
    COMEDY = "comedy"
    TRAGEDY = "tragedy"
    REBIRTH = "rebirth"
    
    # Genre-Specific Plot Types
    MYSTERY_INVESTIGATION = "mystery_investigation"
    ROMANCE_LOVE_STORY = "romance_love_story"
    COMING_OF_AGE = "coming_of_age"
    REVENGE = "revenge"
    REDEMPTION = "redemption"
    SACRIFICE = "sacrifice"
    SURVIVAL = "survival"
    FISH_OUT_OF_WATER = "fish_out_of_water"
    
    # Thriller & Suspense Plots
    CONSPIRACY = "conspiracy"
    CHASE = "chase"
    ESCAPE = "escape"
    HEIST = "heist"
    KIDNAPPING = "kidnapping"
    ASSASSINATION = "assassination"
    ESPIONAGE = "espionage"
    TICKING_CLOCK = "ticking_clock"
    CAT_AND_MOUSE = "cat_and_mouse"
    
    # Science Fiction Plots
    FIRST_CONTACT = "first_contact"
    TIME_TRAVEL = "time_travel"
    DYSTOPIAN_REBELLION = "dystopian_rebellion"
    TECHNOLOGICAL_UPRISING = "technological_uprising"
    SPACE_EXPLORATION = "space_exploration"
    ALIEN_INVASION = "alien_invasion"
    COLONIZATION = "colonization"
    GENETIC_ENHANCEMENT = "genetic_enhancement"
    VIRTUAL_REALITY = "virtual_reality"
    
    # Fantasy Plots
    CHOSEN_ONE = "chosen_one"
    MAGICAL_AWAKENING = "magical_awakening"
    DARK_LORD_RISING = "dark_lord_rising"
    PORTAL_WORLD = "portal_world"
    ANCIENT_PROPHECY = "ancient_prophecy"
    LOST_KINGDOM = "lost_kingdom"
    MAGICAL_ARTIFACT = "magical_artifact"
    DRAGON_SLAYING = "dragon_slaying"
    FAIRY_TALE_RETELLING = "fairy_tale_retelling"
    
    # Horror Plots
    HAUNTED_HOUSE = "haunted_house"
    POSSESSION = "possession"
    CURSED_OBJECT = "cursed_object"
    MONSTER_HUNT = "monster_hunt"
    APOCALYPTIC_HORROR = "apocalyptic_horror"
    PSYCHOLOGICAL_BREAKDOWN = "psychological_breakdown"
    CULT_HORROR = "cult_horror"
    BODY_HORROR = "body_horror"
    VIRAL_OUTBREAK = "viral_outbreak"
    SUPERNATURAL_HORROR = "supernatural_horror"
    
    # Romance Plots
    ENEMIES_TO_LOVERS = "enemies_to_lovers"
    FORBIDDEN_LOVE = "forbidden_love"
    SECOND_CHANCE_ROMANCE = "second_chance_romance"
    FAKE_RELATIONSHIP = "fake_relationship"
    MARRIAGE_OF_CONVENIENCE = "marriage_of_convenience"
    LOVE_TRIANGLE = "love_triangle"
    STAR_CROSSED_LOVERS = "star_crossed_lovers"
    WORKPLACE_ROMANCE = "workplace_romance"
    HOLIDAY_ROMANCE = "holiday_romance"
    
    # Mystery & Crime Plots
    LOCKED_ROOM_MYSTERY = "locked_room_mystery"
    SERIAL_KILLER = "serial_killer"
    COLD_CASE = "cold_case"
    WITNESS_PROTECTION = "witness_protection"
    UNDERCOVER_OPERATION = "undercover_operation"
    CRIME_FAMILY = "crime_family"
    POLICE_PROCEDURAL = "police_procedural"
    AMATEUR_DETECTIVE = "amateur_detective"
    LEGAL_THRILLER = "legal_thriller"
    
    # Historical Fiction Plots
    WAR_STORY = "war_story"
    POLITICAL_INTRIGUE = "political_intrigue"
    SOCIAL_REVOLUTION = "social_revolution"
    PERIOD_ROMANCE = "period_romance"
    IMMIGRANT_STORY = "immigrant_story"
    FAMILY_SAGA = "family_saga"
    CULTURAL_CLASH = "cultural_clash"
    HISTORICAL_MYSTERY = "historical_mystery"
    RISE_AND_FALL = "rise_and_fall"
    
    # Literary Fiction Plots
    CHARACTER_STUDY = "character_study"
    MIDLIFE_CRISIS = "midlife_crisis"
    FAMILY_DRAMA = "family_drama"
    RELATIONSHIP_DRAMA = "relationship_drama"
    EXISTENTIAL_JOURNEY = "existential_journey"
    SOCIAL_COMMENTARY = "social_commentary"
    GENERATIONAL_CONFLICT = "generational_conflict"
    IDENTITY_CRISIS = "identity_crisis"
    MORAL_DILEMMA = "moral_dilemma"
    
    # Young Adult Plots
    SCHOOL_STORY = "school_story"
    FIRST_LOVE = "first_love"
    TEEN_REBELLION = "teen_rebellion"
    BULLYING_STORY = "bullying_story"
    SPORTS_COMPETITION = "sports_competition"
    TALENT_COMPETITION = "talent_competition"
    PEER_PRESSURE = "peer_pressure"
    FAMILY_SECRETS = "family_secrets"
    COLLEGE_STORY = "college_story"
    
    # Adventure Plots
    TREASURE_HUNT = "treasure_hunt"
    EXPLORATION = "exploration"
    RESCUE_MISSION = "rescue_mission"
    RACE_AGAINST_TIME = "race_against_time"
    SURVIVAL_ADVENTURE = "survival_adventure"
    MARTIAL_ARTS = "martial_arts"
    PIRATE_ADVENTURE = "pirate_adventure"
    JUNGLE_ADVENTURE = "jungle_adventure"
    MOUNTAIN_CLIMBING = "mountain_climbing"
    
    # Business & Professional Plots
    CORPORATE_THRILLER = "corporate_thriller"
    STARTUP_STORY = "startup_story"
    BUSINESS_RIVALRY = "business_rivalry"
    WORKPLACE_DRAMA = "workplace_drama"
    FINANCIAL_CRISIS = "financial_crisis"
    WHISTLEBLOWER = "whistleblower"
    MERGER_ACQUISITION = "merger_acquisition"
    ENTREPRENEURIAL_JOURNEY = "entrepreneurial_journey"
    PROFESSIONAL_COMEBACK = "professional_comeback"
    
    # Contemporary Issues Plots
    ENVIRONMENTAL_CRISIS = "environmental_crisis"
    PANDEMIC_STORY = "pandemic_story"
    SOCIAL_MEDIA_DRAMA = "social_media_drama"
    TECHNOLOGY_ADDICTION = "technology_addiction"
    MENTAL_HEALTH_JOURNEY = "mental_health_journey"
    IMMIGRATION_STORY = "immigration_story"
    GENDER_IDENTITY = "gender_identity"
    RACIAL_JUSTICE = "racial_justice"
    ECONOMIC_INEQUALITY = "economic_inequality"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        names = {
            # Classic Archetypal Plots
            self.OVERCOMING_THE_MONSTER: "Overcoming the Monster",
            self.RAGS_TO_RICHES: "Rags to Riches",
            self.THE_QUEST: "The Quest",
            self.VOYAGE_AND_RETURN: "Voyage and Return",
            self.COMEDY: "Comedy",
            self.TRAGEDY: "Tragedy",
            self.REBIRTH: "Rebirth",
            
            # Genre-Specific Plot Types
            self.MYSTERY_INVESTIGATION: "Mystery Investigation",
            self.ROMANCE_LOVE_STORY: "Romance Love Story",
            self.COMING_OF_AGE: "Coming of Age",
            self.REVENGE: "Revenge",
            self.REDEMPTION: "Redemption",
            self.SACRIFICE: "Sacrifice",
            self.SURVIVAL: "Survival",
            self.FISH_OUT_OF_WATER: "Fish Out of Water",
            
            # Thriller & Suspense Plots
            self.CONSPIRACY: "Conspiracy",
            self.CHASE: "Chase",
            self.ESCAPE: "Escape",
            self.HEIST: "Heist",
            self.KIDNAPPING: "Kidnapping",
            self.ASSASSINATION: "Assassination",
            self.ESPIONAGE: "Espionage",
            self.TICKING_CLOCK: "Ticking Clock",
            self.CAT_AND_MOUSE: "Cat and Mouse",
            
            # Science Fiction Plots
            self.FIRST_CONTACT: "First Contact",
            self.TIME_TRAVEL: "Time Travel",
            self.DYSTOPIAN_REBELLION: "Dystopian Rebellion",
            self.TECHNOLOGICAL_UPRISING: "Technological Uprising",
            self.SPACE_EXPLORATION: "Space Exploration",
            self.ALIEN_INVASION: "Alien Invasion",
            self.COLONIZATION: "Colonization",
            self.GENETIC_ENHANCEMENT: "Genetic Enhancement",
            self.VIRTUAL_REALITY: "Virtual Reality",
            
            # Fantasy Plots
            self.CHOSEN_ONE: "The Chosen One",
            self.MAGICAL_AWAKENING: "Magical Awakening",
            self.DARK_LORD_RISING: "Dark Lord Rising",
            self.PORTAL_WORLD: "Portal to Another World",
            self.ANCIENT_PROPHECY: "Ancient Prophecy",
            self.LOST_KINGDOM: "Lost Kingdom",
            self.MAGICAL_ARTIFACT: "Magical Artifact",
            self.DRAGON_SLAYING: "Dragon Slaying",
            self.FAIRY_TALE_RETELLING: "Fairy Tale Retelling",
            
            # Horror Plots
            self.HAUNTED_HOUSE: "Haunted House",
            self.POSSESSION: "Possession",
            self.CURSED_OBJECT: "Cursed Object",
            self.MONSTER_HUNT: "Monster Hunt",
            self.APOCALYPTIC_HORROR: "Apocalyptic Horror",
            self.PSYCHOLOGICAL_BREAKDOWN: "Psychological Breakdown",
            self.CULT_HORROR: "Cult Horror",
            self.BODY_HORROR: "Body Horror",
            self.VIRAL_OUTBREAK: "Viral Outbreak",
            self.SUPERNATURAL_HORROR: "Supernatural Horror",
            
            # Romance Plots
            self.ENEMIES_TO_LOVERS: "Enemies to Lovers",
            self.FORBIDDEN_LOVE: "Forbidden Love",
            self.SECOND_CHANCE_ROMANCE: "Second Chance Romance",
            self.FAKE_RELATIONSHIP: "Fake Relationship",
            self.MARRIAGE_OF_CONVENIENCE: "Marriage of Convenience",
            self.LOVE_TRIANGLE: "Love Triangle",
            self.STAR_CROSSED_LOVERS: "Star-Crossed Lovers",
            self.WORKPLACE_ROMANCE: "Workplace Romance",
            self.HOLIDAY_ROMANCE: "Holiday Romance",
            
            # Mystery & Crime Plots
            self.LOCKED_ROOM_MYSTERY: "Locked Room Mystery",
            self.SERIAL_KILLER: "Serial Killer",
            self.COLD_CASE: "Cold Case",
            self.WITNESS_PROTECTION: "Witness Protection",
            self.UNDERCOVER_OPERATION: "Undercover Operation",
            self.CRIME_FAMILY: "Crime Family",
            self.POLICE_PROCEDURAL: "Police Procedural",
            self.AMATEUR_DETECTIVE: "Amateur Detective",
            self.LEGAL_THRILLER: "Legal Thriller",
            
            # Historical Fiction Plots
            self.WAR_STORY: "War Story",
            self.POLITICAL_INTRIGUE: "Political Intrigue",
            self.SOCIAL_REVOLUTION: "Social Revolution",
            self.PERIOD_ROMANCE: "Period Romance",
            self.IMMIGRANT_STORY: "Immigrant Story",
            self.FAMILY_SAGA: "Family Saga",
            self.CULTURAL_CLASH: "Cultural Clash",
            self.HISTORICAL_MYSTERY: "Historical Mystery",
            self.RISE_AND_FALL: "Rise and Fall",
            
            # Literary Fiction Plots
            self.CHARACTER_STUDY: "Character Study",
            self.MIDLIFE_CRISIS: "Midlife Crisis",
            self.FAMILY_DRAMA: "Family Drama",
            self.RELATIONSHIP_DRAMA: "Relationship Drama",
            self.EXISTENTIAL_JOURNEY: "Existential Journey",
            self.SOCIAL_COMMENTARY: "Social Commentary",
            self.GENERATIONAL_CONFLICT: "Generational Conflict",
            self.IDENTITY_CRISIS: "Identity Crisis",
            self.MORAL_DILEMMA: "Moral Dilemma",
            
            # Young Adult Plots
            self.SCHOOL_STORY: "School Story",
            self.FIRST_LOVE: "First Love",
            self.TEEN_REBELLION: "Teen Rebellion",
            self.BULLYING_STORY: "Bullying Story",
            self.SPORTS_COMPETITION: "Sports Competition",
            self.TALENT_COMPETITION: "Talent Competition",
            self.PEER_PRESSURE: "Peer Pressure",
            self.FAMILY_SECRETS: "Family Secrets",
            self.COLLEGE_STORY: "College Story",
            
            # Adventure Plots
            self.TREASURE_HUNT: "Treasure Hunt",
            self.EXPLORATION: "Exploration",
            self.RESCUE_MISSION: "Rescue Mission",
            self.RACE_AGAINST_TIME: "Race Against Time",
            self.SURVIVAL_ADVENTURE: "Survival Adventure",
            self.MARTIAL_ARTS: "Martial Arts",
            self.PIRATE_ADVENTURE: "Pirate Adventure",
            self.JUNGLE_ADVENTURE: "Jungle Adventure",
            self.MOUNTAIN_CLIMBING: "Mountain Climbing",
            
            # Business & Professional Plots
            self.CORPORATE_THRILLER: "Corporate Thriller",
            self.STARTUP_STORY: "Startup Story",
            self.BUSINESS_RIVALRY: "Business Rivalry",
            self.WORKPLACE_DRAMA: "Workplace Drama",
            self.FINANCIAL_CRISIS: "Financial Crisis",
            self.WHISTLEBLOWER: "Whistleblower",
            self.MERGER_ACQUISITION: "Merger & Acquisition",
            self.ENTREPRENEURIAL_JOURNEY: "Entrepreneurial Journey",
            self.PROFESSIONAL_COMEBACK: "Professional Comeback",
            
            # Contemporary Issues Plots
            self.ENVIRONMENTAL_CRISIS: "Environmental Crisis",
            self.PANDEMIC_STORY: "Pandemic Story",
            self.SOCIAL_MEDIA_DRAMA: "Social Media Drama",
            self.TECHNOLOGY_ADDICTION: "Technology Addiction",
            self.MENTAL_HEALTH_JOURNEY: "Mental Health Journey",
            self.IMMIGRATION_STORY: "Immigration Story",
            self.GENDER_IDENTITY: "Gender Identity",
            self.RACIAL_JUSTICE: "Racial Justice",
            self.ECONOMIC_INEQUALITY: "Economic Inequality",
        }
        return names.get(self, self.value.replace("_", " ").title())
    
    @property
    def description(self) -> str:
        """Detailed description of the plot type."""
        descriptions = {
            # Classic Archetypal Plots
            self.OVERCOMING_THE_MONSTER: "A story where the protagonist must confront and defeat a great evil, whether literal or metaphorical, that threatens them, their community, or the world. The monster represents fear, oppression, or destructive forces that must be overcome through courage, skill, and determination.",
            self.RAGS_TO_RICHES: "A transformative journey where the protagonist rises from humble or disadvantaged beginnings to achieve wealth, status, success, or fulfillment. This plot explores themes of ambition, perseverance, and the pursuit of the American Dream while examining what true success means.",
            self.THE_QUEST: "An epic journey where the protagonist embarks on a mission to find, retrieve, or accomplish something of great importance. The quest tests the hero's resolve, forces personal growth, and often involves overcoming multiple obstacles and challenges along the way.",
            self.VOYAGE_AND_RETURN: "A story of exploration and discovery where the protagonist travels to a strange, unfamiliar world or situation, experiences adventures and learns important lessons, then returns home transformed by their experience with new wisdom or perspective.",
            self.COMEDY: "A light-hearted narrative focused on humor, misunderstandings, and ultimately happy resolutions. Comedy plots often feature mistaken identities, romantic entanglements, social satire, and characters who overcome obstacles through wit and resilience rather than violence.",
            self.TRAGEDY: "A serious dramatic story that explores the downfall of the protagonist, typically due to a fatal flaw, poor decisions, or circumstances beyond their control. Tragedies examine themes of fate, mortality, and the human condition while evoking catharsis in the audience.",
            self.REBIRTH: "A story of transformation and redemption where the protagonist undergoes a profound change, often moving from a negative state to a positive one. This plot explores themes of forgiveness, second chances, and the possibility of personal renewal and growth.",
            
            # Genre-Specific Plot Types
            self.MYSTERY_INVESTIGATION: "A puzzle-driven narrative where the protagonist works to solve a crime, uncover a secret, or explain mysterious events. The plot focuses on gathering clues, interviewing suspects, and using deductive reasoning to reach the truth.",
            self.ROMANCE_LOVE_STORY: "A relationship-centered narrative that follows the development of romantic love between characters, exploring the emotional journey from attraction through obstacles to ultimate union or meaningful connection.",
            self.COMING_OF_AGE: "A bildungsroman that follows a young protagonist's psychological and moral development from youth toward adulthood, exploring themes of identity, responsibility, independence, and the transition from innocence to experience.",
            self.REVENGE: "A plot driven by the protagonist's desire for retribution against those who have wronged them or their loved ones. This narrative explores themes of justice, morality, and whether revenge truly brings satisfaction or perpetuates cycles of violence.",
            self.REDEMPTION: "A story of moral transformation where a flawed or fallen protagonist seeks to atone for past mistakes and regain their honor, self-respect, or place in society through meaningful action and personal growth.",
            self.SACRIFICE: "A narrative centered on characters making significant personal sacrifices for the greater good, their loved ones, or their principles. This plot explores themes of duty, honor, love, and the cost of doing what's right.",
            self.SURVIVAL: "A high-stakes story where characters face life-threatening situations and must use their resourcefulness, determination, and will to live to overcome extreme challenges, whether from nature, society, or other hostile forces.",
            self.FISH_OUT_OF_WATER: "A story where the protagonist finds themselves in an unfamiliar environment or situation, struggling to adapt and fit in while maintaining their identity. This plot often provides comedy and insight into different cultures or social groups.",
            
            # Thriller & Suspense Plots
            self.CONSPIRACY: "A complex plot involving secret schemes by powerful groups or individuals, where the protagonist uncovers hidden truths and faces danger from those who want to keep their activities secret. Themes include power, corruption, and paranoia.",
            self.CHASE: "A fast-paced narrative where the protagonist is pursued by antagonists, creating constant tension and momentum as they attempt to escape, evade capture, or reach safety while overcoming obstacles and making split-second decisions.",
            self.ESCAPE: "A tense story focused on characters attempting to break free from captivity, oppressive situations, or dangerous environments. The plot emphasizes ingenuity, cooperation, and the determination to regain freedom.",
            self.HEIST: "A carefully planned crime story involving the theft of valuable items, typically requiring elaborate schemes, specialized skills, and teamwork. These plots explore themes of greed, loyalty, and the thrill of outsmarting security.",
            self.KIDNAPPING: "A suspenseful plot involving the abduction of a character, exploring the psychological trauma of captivity and the desperate efforts of others to secure their safe return, often involving ransom demands or rescue attempts.",
            self.ASSASSINATION: "A plot centered around political or personal murder, involving either the planning and execution of an assassination or efforts to prevent one. These stories explore themes of power, ideology, and moral complexity.",
            self.ESPIONAGE: "A spy thriller involving intelligence gathering, double agents, and international intrigue. Characters navigate a world of deception and danger where trust is rare and betrayal is common, often serving larger political purposes.",
            self.TICKING_CLOCK: "A high-tension plot where characters race against time to prevent a catastrophe, solve a problem, or complete a mission before a deadline. The constant time pressure creates urgency and escalates stakes throughout the story.",
            self.CAT_AND_MOUSE: "A psychological thriller featuring an ongoing battle of wits between protagonist and antagonist, where each tries to outmaneuver the other through strategy, deception, and psychological manipulation.",
            
            # Science Fiction Plots
            self.FIRST_CONTACT: "A story exploring humanity's initial encounter with alien intelligence, examining the scientific, social, political, and philosophical implications of discovering we are not alone in the universe.",
            self.TIME_TRAVEL: "A narrative involving characters moving through time, exploring the consequences of altering the past or knowledge of the future, while examining themes of causality, free will, and the nature of time itself.",
            self.DYSTOPIAN_REBELLION: "A story set in an oppressive future society where protagonists fight against totalitarian control, surveillance, and social injustice, exploring themes of freedom, resistance, and the cost of defying authority.",
            self.TECHNOLOGICAL_UPRISING: "A plot where artificial intelligence, robots, or technology becomes hostile to humanity, exploring themes of technological dependence, artificial consciousness, and the relationship between creators and their creations.",
            self.SPACE_EXPLORATION: "An adventure story focusing on the discovery and colonization of new worlds, the challenges of space travel, and encounters with alien environments, examining humanity's place in the cosmos.",
            self.ALIEN_INVASION: "A conflict story where Earth faces attack from extraterrestrial forces, exploring themes of survival, unity in the face of existential threat, and what makes humanity worth defending.",
            self.COLONIZATION: "A story about establishing human settlements on other worlds, dealing with the challenges of adaptation, resource management, and the impact of human expansion on alien environments.",
            self.GENETIC_ENHANCEMENT: "A narrative exploring the modification of human genetics, examining the ethical implications of creating 'perfect' humans and the social consequences of genetic inequality.",
            self.VIRTUAL_REALITY: "A story set partially or entirely in simulated worlds, exploring the boundaries between reality and artificiality, and the psychological effects of immersive digital environments.",
            
            # Fantasy Plots
            self.CHOSEN_ONE: "A classic fantasy plot where an unlikely hero is prophesied or destined to save the world from great evil, exploring themes of destiny, responsibility, and growing into one's potential despite humble origins.",
            self.MAGICAL_AWAKENING: "A story where the protagonist discovers they possess magical abilities, learning to control their powers while navigating a world they never knew existed, often facing those who would misuse such abilities.",
            self.DARK_LORD_RISING: "An epic fantasy where an ancient evil returns to threaten the world, requiring heroes to unite against overwhelming darkness, exploring themes of good versus evil and the cost of victory.",
            self.PORTAL_WORLD: "A fantasy adventure where characters travel between our world and a magical realm, often becoming involved in the conflicts and politics of the fantasy world while trying to return home.",
            self.ANCIENT_PROPHECY: "A plot driven by foretold events that must be fulfilled or prevented, exploring themes of fate versus free will and whether the future can be changed through human action.",
            self.LOST_KINGDOM: "A quest to restore a fallen realm to its former glory, often involving the rightful heir reclaiming their throne and rebuilding what was destroyed by war, betrayal, or dark magic.",
            self.MAGICAL_ARTIFACT: "A story centered around powerful magical objects that could either save or destroy the world, exploring themes of power, corruption, and the responsibility that comes with great ability.",
            self.DRAGON_SLAYING: "A classic fantasy adventure where heroes must defeat a great dragon, representing the ultimate test of courage, skill, and heroism while often protecting innocent people.",
            self.FAIRY_TALE_RETELLING: "A modern reimagining of classic fairy tales, updating familiar stories with contemporary themes, perspectives, or twists while maintaining the core mythic elements that make them timeless.",
            
            # Horror Plots
            self.HAUNTED_HOUSE: "A supernatural horror story where characters confront ghostly presences and paranormal phenomena in a location with a dark history, exploring themes of unresolved trauma and the persistence of evil.",
            self.POSSESSION: "A terrifying narrative where characters are taken over by malevolent supernatural entities, exploring themes of loss of control, spiritual warfare, and the battle for one's soul.",
            self.CURSED_OBJECT: "A horror story where a seemingly innocent item brings misfortune, death, or supernatural torment to those who possess it, exploring themes of greed, karma, and ancient evil.",
            self.MONSTER_HUNT: "An action-horror plot where characters track and attempt to destroy a supernatural creature that threatens humanity, combining elements of adventure with terrifying encounters.",
            self.APOCALYPTIC_HORROR: "A story set during or after the end of the world, where survivors face both the collapse of civilization and supernatural threats, exploring themes of human nature under extreme stress.",
            self.PSYCHOLOGICAL_BREAKDOWN: "A psychological horror where the protagonist's mental state deteriorates, blurring the line between reality and delusion while exploring themes of madness, guilt, and the fragility of the human mind.",
            self.CULT_HORROR: "A story involving dangerous religious or occult groups that threaten individuals or society, exploring themes of fanaticism, manipulation, and the power of collective belief.",
            self.BODY_HORROR: "A disturbing narrative focusing on the grotesque transformation or violation of the human body, exploring themes of identity, mortality, and the fear of losing physical integrity.",
            self.VIRAL_OUTBREAK: "A horror story where a disease or contagion spreads rapidly, causing death or transformation, exploring themes of pandemic fear, social breakdown, and survival against biological threats.",
            self.SUPERNATURAL_HORROR: "A frightening narrative featuring otherworldly entities, paranormal phenomena, or supernatural forces that threaten characters, exploring themes of the unknown, spiritual warfare, and forces beyond human understanding.",
            
            # Romance Plots
            self.ENEMIES_TO_LOVERS: "A romantic plot where initial antagonism between characters gradually transforms into deep attraction and love, exploring themes of prejudice, misunderstanding, and the power of connection to overcome differences.",
            self.FORBIDDEN_LOVE: "A romantic story where societal, familial, or circumstantial barriers prevent characters from being together, exploring themes of sacrifice, defiance, and the strength of true love against opposition.",
            self.SECOND_CHANCE_ROMANCE: "A story where former lovers reunite and must overcome past hurts, misunderstandings, or changed circumstances to rebuild their relationship, exploring themes of forgiveness and growth.",
            self.FAKE_RELATIONSHIP: "A romantic plot where characters pretend to be in a relationship for practical reasons but gradually develop real feelings, exploring themes of authenticity, vulnerability, and unexpected love.",
            self.MARRIAGE_OF_CONVENIENCE: "A story where characters marry for practical rather than romantic reasons but slowly discover genuine affection and compatibility, exploring themes of partnership and growing love.",
            self.LOVE_TRIANGLE: "A romantic conflict where one character must choose between two potential partners, exploring themes of loyalty, compatibility, and the complexity of human attraction and emotion.",
            self.STAR_CROSSED_LOVERS: "A tragic romance where external forces or fate conspire to keep lovers apart, exploring themes of destiny, sacrifice, and love that transcends worldly concerns.",
            self.WORKPLACE_ROMANCE: "A romantic story set in professional environments where characters navigate attraction while maintaining career focus, exploring themes of ambition, professional ethics, and work-life balance.",
            self.HOLIDAY_ROMANCE: "A romance that blooms during vacation or holiday settings, often involving temporary escape from routine and the question of whether vacation love can survive return to reality.",
            
            # Mystery & Crime Plots
            self.LOCKED_ROOM_MYSTERY: "A classic mystery where a crime occurs in seemingly impossible circumstances, challenging the detective and reader to solve how the crime was committed when all logical explanations seem ruled out.",
            self.SERIAL_KILLER: "A crime story involving a murderer who follows a pattern, as law enforcement races to understand the killer's psychology and method before they strike again, exploring themes of evil and justice.",
            self.COLD_CASE: "A mystery involving long-unsolved crimes that are reopened with new evidence or perspective, exploring themes of persistence, justice delayed, and the lasting impact of unresolved trauma.",
            self.WITNESS_PROTECTION: "A thriller where characters must hide their identity to avoid retribution for testifying against criminals, exploring themes of identity, safety, and the cost of doing the right thing.",
            self.UNDERCOVER_OPERATION: "A story where law enforcement or other agents infiltrate criminal organizations, exploring the psychological toll of living a double life and the moral complexity of deception for justice.",
            self.CRIME_FAMILY: "A narrative focusing on organized crime dynasties, exploring themes of loyalty, family honor, corruption, and the conflict between personal relationships and criminal enterprise.",
            self.POLICE_PROCEDURAL: "A methodical crime story that follows standard law enforcement procedures and teamwork to solve crimes, emphasizing realistic investigation techniques and institutional cooperation.",
            self.AMATEUR_DETECTIVE: "A mystery where an ordinary person becomes involved in solving crimes, using intelligence and intuition rather than professional training, often uncovering corruption or hidden secrets.",
            self.LEGAL_THRILLER: "A story combining legal proceedings with suspense elements, exploring the courtroom as a battlefield where truth, justice, and human lives hang in the balance.",
            
            # Historical Fiction Plots
            self.WAR_STORY: "A narrative set during armed conflict, exploring the human cost of war, the bonds between soldiers, the impact on civilians, and the moral complexity of violence and survival.",
            self.POLITICAL_INTRIGUE: "A story involving the machinations of power, featuring politicians, diplomats, and others who navigate complex political landscapes while pursuing their agendas and ideals.",
            self.SOCIAL_REVOLUTION: "A narrative set during periods of major social change, exploring how individuals respond to and shape historical movements toward justice, equality, or political transformation.",
            self.PERIOD_ROMANCE: "A love story set in a specific historical era, using the customs, constraints, and culture of the time to create unique romantic challenges and opportunities.",
            self.IMMIGRANT_STORY: "A narrative following characters who leave their homeland to build new lives elsewhere, exploring themes of identity, belonging, cultural adaptation, and the pursuit of opportunity.",
            self.FAMILY_SAGA: "A multi-generational story that follows families through decades or centuries, exploring how historical events shape family dynamics and how family legacies endure or transform.",
            self.CULTURAL_CLASH: "A story exploring the meeting of different cultures, examining misunderstanding, conflict, adaptation, and the potential for mutual enrichment between different ways of life.",
            self.HISTORICAL_MYSTERY: "A mystery story set in the past, using period details and constraints to create unique investigative challenges while exploring historical events and social conditions.",
            self.RISE_AND_FALL: "A biographical or dynastic story that follows the trajectory of powerful individuals or institutions from their ascent to their eventual decline, exploring themes of ambition and hubris.",
            
            # Literary Fiction Plots
            self.CHARACTER_STUDY: "An introspective narrative that prioritizes deep exploration of character psychology, motivation, and development over external action, revealing the complexity of human nature and experience.",
            self.MIDLIFE_CRISIS: "A story focusing on characters facing the realization that their lives haven't met their expectations, exploring themes of regret, second chances, and the search for meaning in middle age.",
            self.FAMILY_DRAMA: "A complex narrative exploring family relationships, secrets, conflicts, and dynamics, often revealing how past events continue to influence present relationships and personal identity.",
            self.RELATIONSHIP_DRAMA: "A story examining the complexities of human relationships, whether romantic, familial, or platonic, exploring themes of communication, commitment, betrayal, and emotional growth.",
            self.EXISTENTIAL_JOURNEY: "A philosophical narrative where characters grapple with questions of meaning, purpose, mortality, and their place in the universe, often leading to profound personal revelation or acceptance.",
            self.SOCIAL_COMMENTARY: "A story that critiques social institutions, cultural norms, or political systems through character experiences, using narrative to explore and challenge contemporary issues and values.",
            self.GENERATIONAL_CONFLICT: "A narrative exploring the tensions between different generations, examining how changing values, technology, and social conditions create misunderstanding and conflict within families or communities.",
            self.IDENTITY_CRISIS: "A story where characters struggle to understand who they are, often triggered by major life changes, cultural displacement, or the revelation of hidden truths about their past.",
            self.MORAL_DILEMMA: "A narrative that presents characters with difficult ethical choices, exploring the complexity of right and wrong and the consequences of moral decisions in ambiguous situations.",
            
            # Young Adult Plots
            self.SCHOOL_STORY: "A narrative set in educational environments, exploring academic pressure, social hierarchies, friendships, and the unique challenges of navigating institutional life during formative years.",
            self.FIRST_LOVE: "A coming-of-age romance that explores the intensity and innocence of first romantic relationships, including the joy of discovery and the pain of heartbreak.",
            self.TEEN_REBELLION: "A story where young protagonists challenge authority figures, social expectations, or institutional rules, exploring themes of independence, identity, and the desire for autonomy.",
            self.BULLYING_STORY: "A narrative addressing the serious issue of peer harassment and its psychological impact, often following either victims finding strength or bullies learning empathy.",
            self.SPORTS_COMPETITION: "A story centered around athletic achievement, team dynamics, and competition, exploring themes of dedication, teamwork, overcoming obstacles, and personal growth through physical challenge.",
            self.TALENT_COMPETITION: "A narrative focused on artistic or intellectual competitions, exploring themes of ambition, creativity, pressure to succeed, and the balance between competition and personal fulfillment.",
            self.PEER_PRESSURE: "A story examining the influence of social groups on individual decision-making, exploring themes of conformity, authenticity, and the courage to stand up for personal values.",
            self.FAMILY_SECRETS: "A young adult narrative where protagonists discover hidden truths about their family history, exploring themes of identity, trust, and how family mysteries shape personal understanding.",
            self.COLLEGE_STORY: "A narrative exploring the transition to higher education, including academic challenges, social pressures, independence, and the process of self-discovery in a new environment.",
            
            # Adventure Plots
            self.TREASURE_HUNT: "An exciting quest to find valuable hidden objects, often involving maps, clues, and dangerous obstacles, exploring themes of greed, discovery, and the value of perseverance.",
            self.EXPLORATION: "A story of discovering unknown territories, whether geographical, scientific, or cultural, emphasizing curiosity, courage, and the human drive to push beyond known boundaries.",
            self.RESCUE_MISSION: "A high-stakes narrative where characters attempt to save others from danger, emphasizing heroism, sacrifice, and the lengths people will go to help those they care about.",
            self.RACE_AGAINST_TIME: "An adventure where characters must accomplish their goal before a deadline, creating constant tension and urgency while testing their resourcefulness and determination.",
            self.SURVIVAL_ADVENTURE: "A story where characters face natural disasters, hostile environments, or extreme conditions, emphasizing human resilience and the will to survive against overwhelming odds.",
            self.MARTIAL_ARTS: "An action-oriented narrative featuring combat skills, discipline, and philosophy, often exploring themes of honor, self-improvement, and the balance between violence and restraint.",
            self.PIRATE_ADVENTURE: "A swashbuckling story of maritime adventure, featuring themes of freedom, loyalty among outcasts, rebellion against authority, and the romantic appeal of life outside conventional society.",
            self.JUNGLE_ADVENTURE: "An exploration story set in dense wilderness, emphasizing survival skills, encounters with wildlife, and the challenge of navigating unknown and dangerous terrain.",
            self.MOUNTAIN_CLIMBING: "An adventure focused on ascending dangerous peaks, exploring themes of perseverance, respect for nature, and pushing human physical and mental limits.",
            
            # Business & Professional Plots
            self.CORPORATE_THRILLER: "A suspenseful story set in the business world, involving corporate espionage, hostile takeovers, or corruption, exploring themes of ambition, ethics, and the cost of success.",
            self.STARTUP_STORY: "A narrative following entrepreneurs building new companies, exploring themes of innovation, risk-taking, partnership dynamics, and the challenges of turning ideas into reality.",
            self.BUSINESS_RIVALRY: "A competitive story between companies or business leaders, exploring themes of competition, market strategy, personal ambition, and the fine line between healthy rivalry and destructive conflict.",
            self.WORKPLACE_DRAMA: "A story exploring office politics, professional relationships, and career advancement, examining how personal and professional lives intersect and influence each other.",
            self.FINANCIAL_CRISIS: "A narrative dealing with economic collapse or financial scandal, exploring the impact on individuals and society while examining themes of greed, responsibility, and recovery.",
            self.WHISTLEBLOWER: "A story about someone exposing corporate or governmental wrongdoing, exploring themes of courage, conscience, and the personal cost of standing up for what's right.",
            self.MERGER_ACQUISITION: "A business story involving company consolidation, exploring themes of change, power dynamics, cultural integration, and the human impact of corporate decisions.",
            self.ENTREPRENEURIAL_JOURNEY: "A narrative following the complete arc of building a business from conception to success or failure, exploring themes of vision, persistence, and innovation.",
            self.PROFESSIONAL_COMEBACK: "A story about recovering from career setbacks, exploring themes of resilience, reinvention, and the possibility of second chances in professional life.",
            
            # Contemporary Issues Plots
            self.ENVIRONMENTAL_CRISIS: "A story addressing climate change, pollution, or ecological disaster, exploring human impact on the environment and the urgent need for sustainable practices and environmental justice.",
            self.PANDEMIC_STORY: "A narrative dealing with disease outbreaks and their social impact, exploring themes of public health, social responsibility, isolation, and community resilience during health crises.",
            self.SOCIAL_MEDIA_DRAMA: "A contemporary story exploring the impact of digital communication on relationships, identity, and society, including issues like cyberbullying, privacy, and online versus offline identity.",
            self.TECHNOLOGY_ADDICTION: "A narrative examining the psychological and social effects of excessive technology use, exploring themes of connection, isolation, and finding balance in a digital world.",
            self.MENTAL_HEALTH_JOURNEY: "A sensitive story following characters dealing with psychological challenges, emphasizing recovery, support systems, and reducing stigma around mental health issues.",
            self.IMMIGRATION_STORY: "A contemporary narrative about people seeking new homes due to economic, political, or social pressures, exploring themes of belonging, identity, and the immigrant experience.",
            self.GENDER_IDENTITY: "A story exploring gender expression and identity, following characters as they navigate self-discovery, social acceptance, and the courage to live authentically.",
            self.RACIAL_JUSTICE: "A narrative addressing systemic racism and the fight for equality, exploring themes of prejudice, activism, allyship, and the ongoing struggle for civil rights.",
            self.ECONOMIC_INEQUALITY: "A story examining wealth disparity and its impact on individuals and communities, exploring themes of class conflict, opportunity, and social mobility.",
        }
        return descriptions.get(self, f"A story featuring {self.display_name.lower()} themes and narrative elements.")
    
    @property
    def complexity_level(self) -> str:
        """Complexity level for storytelling and character development."""
        simple = {
            self.COMEDY, self.FISH_OUT_OF_WATER, self.HOLIDAY_ROMANCE, 
            self.TREASURE_HUNT, self.SCHOOL_STORY, self.FIRST_LOVE,
            self.PIRATE_ADVENTURE, self.SPORTS_COMPETITION, self.RESCUE_MISSION
        }
        
        moderate = {
            self.OVERCOMING_THE_MONSTER, self.RAGS_TO_RICHES, self.THE_QUEST,
            self.VOYAGE_AND_RETURN, self.COMING_OF_AGE, self.REVENGE,
            self.SURVIVAL, self.MYSTERY_INVESTIGATION, self.ROMANCE_LOVE_STORY,
            self.CHOSEN_ONE, self.ENEMIES_TO_LOVERS, self.WORKPLACE_ROMANCE,
            self.HAUNTED_HOUSE, self.ALIEN_INVASION, self.TIME_TRAVEL
        }
        
        complex = {
            self.TRAGEDY, self.REBIRTH, self.REDEMPTION, self.SACRIFICE,
            self.CONSPIRACY, self.ESPIONAGE, self.DYSTOPIAN_REBELLION,
            self.POLITICAL_INTRIGUE, self.FAMILY_DRAMA, self.IDENTITY_CRISIS,
            self.SOCIAL_REVOLUTION, self.CULT_HORROR, self.LEGAL_THRILLER,
            self.CORPORATE_THRILLER, self.MENTAL_HEALTH_JOURNEY
        }
        
        very_complex = {
            self.CHARACTER_STUDY, self.EXISTENTIAL_JOURNEY, self.SOCIAL_COMMENTARY,
            self.MORAL_DILEMMA, self.PSYCHOLOGICAL_BREAKDOWN, self.GENERATIONAL_CONFLICT,
            self.TECHNOLOGICAL_UPRISING, self.FAMILY_SAGA, self.RISE_AND_FALL,
            self.ENVIRONMENTAL_CRISIS, self.RACIAL_JUSTICE, self.ECONOMIC_INEQUALITY
        }
        
        if self in simple:
            return "simple"
        elif self in moderate:
            return "moderate"
        elif self in complex:
            return "complex"
        else:
            return "very_complex"
    
    @property
    def typical_themes(self) -> List[str]:
        """Common themes associated with this plot type."""
        theme_map = {
            self.OVERCOMING_THE_MONSTER: ["good vs evil", "courage", "heroism", "protection"],
            self.RAGS_TO_RICHES: ["success", "transformation", "perseverance", "achievement"],
            self.THE_QUEST: ["journey", "self-discovery", "purpose", "adventure"],
            self.COMEDY: ["humor", "misunderstanding", "social satire", "happy endings"],
            self.TRAGEDY: ["fate", "downfall", "human flaws", "catharsis"],
            self.REBIRTH: ["transformation", "redemption", "second chances", "renewal"],
            self.ROMANCE_LOVE_STORY: ["love", "relationship", "emotional growth", "connection"],
            self.COMING_OF_AGE: ["growth", "identity", "responsibility", "transition"],
            self.REVENGE: ["justice", "retribution", "morality", "consequences"],
            self.SURVIVAL: ["resilience", "will to live", "resourcefulness", "endurance"],
            self.DYSTOPIAN_REBELLION: ["freedom", "resistance", "oppression", "hope"],
            self.CHOSEN_ONE: ["destiny", "responsibility", "power", "sacrifice"],
            self.ENEMIES_TO_LOVERS: ["prejudice", "understanding", "transformation", "love"],
            self.MYSTERY_INVESTIGATION: ["truth", "justice", "puzzles", "revelation"],
            self.FAMILY_DRAMA: ["relationships", "secrets", "loyalty", "forgiveness"],
            self.TIME_TRAVEL: ["causality", "consequences", "free will", "paradox"],
            self.ENVIRONMENTAL_CRISIS: ["responsibility", "sustainability", "future", "activism"],
            self.MENTAL_HEALTH_JOURNEY: ["healing", "acceptance", "support", "recovery"],
            self.EXPLORATION: ["adventure", "discovery", "curiosity", "unknown territories"],
            self.TREASURE_HUNT: ["adventure", "discovery", "greed vs purpose", "perseverance"],
            self.FORBIDDEN_LOVE: ["love", "sacrifice", "social barriers", "defiance"],
        }
        return theme_map.get(self, ["conflict", "growth", "resolution"])
    
    @property
    def target_length(self) -> str:
        """Recommended story length for this plot type."""
        short_plots = {
            self.FISH_OUT_OF_WATER, self.HOLIDAY_ROMANCE, self.FIRST_LOVE,
            self.SCHOOL_STORY, self.WORKPLACE_ROMANCE, self.RESCUE_MISSION
        }
        
        medium_plots = {
            self.OVERCOMING_THE_MONSTER, self.RAGS_TO_RICHES, self.COMEDY,
            self.COMING_OF_AGE, self.ROMANCE_LOVE_STORY, self.MYSTERY_INVESTIGATION,
            self.CHOSEN_ONE, self.ENEMIES_TO_LOVERS, self.HAUNTED_HOUSE,
            self.SURVIVAL, self.TREASURE_HUNT, self.CORPORATE_THRILLER
        }
        
        long_plots = {
            self.THE_QUEST, self.VOYAGE_AND_RETURN, self.TRAGEDY, self.REBIRTH,
            self.DYSTOPIAN_REBELLION, self.SPACE_EXPLORATION, self.FAMILY_SAGA,
            self.POLITICAL_INTRIGUE, self.SOCIAL_REVOLUTION, self.WAR_STORY
        }
        
        epic_plots = {
            self.DARK_LORD_RISING, self.APOCALYPTIC_HORROR, self.ALIEN_INVASION,
            self.TECHNOLOGICAL_UPRISING, self.RISE_AND_FALL, self.CHARACTER_STUDY,
            self.SOCIAL_COMMENTARY, self.ENVIRONMENTAL_CRISIS
        }
        
        if self in short_plots:
            return "short (40,000-60,000 words)"
        elif self in medium_plots:
            return "medium (60,000-90,000 words)"
        elif self in long_plots:
            return "long (90,000-120,000 words)"
        elif self in epic_plots:
            return "epic (120,000+ words)"
        else:
            return "medium (60,000-90,000 words)"
    
    @classmethod
    def from_string(cls, value: str) -> 'PlotType':
        """Create PlotType from string with fuzzy matching."""
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid plot type value: {value}")
        
        # Normalize input
        normalized_value = value.lower().strip().replace("-", "_").replace(" ", "_")
        
        # Direct match
        for plot in cls:
            if plot.value == normalized_value:
                return plot
        
        # Fuzzy matching
        fuzzy_matches = {
            # Classic plots
            "monster": cls.OVERCOMING_THE_MONSTER,
            "rags": cls.RAGS_TO_RICHES,
            "quest": cls.THE_QUEST,
            "voyage": cls.VOYAGE_AND_RETURN,
            "rebirth": cls.REBIRTH,
            "tragedy": cls.TRAGEDY,
            "comedy": cls.COMEDY,
            
            # Common plot variations
            "mystery": cls.MYSTERY_INVESTIGATION,
            "romance": cls.ROMANCE_LOVE_STORY,
            "love_story": cls.ROMANCE_LOVE_STORY,
            "coming_of_age": cls.COMING_OF_AGE,
            "revenge": cls.REVENGE,
            "redemption": cls.REDEMPTION,
            "sacrifice": cls.SACRIFICE,
            "survival": cls.SURVIVAL,
            "fish_out_of_water": cls.FISH_OUT_OF_WATER,
            
            # Thriller variations
            "conspiracy": cls.CONSPIRACY,
            "chase": cls.CHASE,
            "escape": cls.ESCAPE,
            "heist": cls.HEIST,
            "kidnapping": cls.KIDNAPPING,
            "spy": cls.ESPIONAGE,
            "espionage": cls.ESPIONAGE,
            "ticking_clock": cls.TICKING_CLOCK,
            
            # Sci-fi variations
            "first_contact": cls.FIRST_CONTACT,
            "time_travel": cls.TIME_TRAVEL,
            "dystopian": cls.DYSTOPIAN_REBELLION,
            "rebellion": cls.DYSTOPIAN_REBELLION,
            "space": cls.SPACE_EXPLORATION,
            "alien": cls.ALIEN_INVASION,
            "invasion": cls.ALIEN_INVASION,
            "ai": cls.TECHNOLOGICAL_UPRISING,
            "robot": cls.TECHNOLOGICAL_UPRISING,
            
            # Fantasy variations
            "chosen_one": cls.CHOSEN_ONE,
            "chosen": cls.CHOSEN_ONE,
            "prophecy": cls.ANCIENT_PROPHECY,
            "magic": cls.MAGICAL_AWAKENING,
            "magical": cls.MAGICAL_AWAKENING,
            "dragon": cls.DRAGON_SLAYING,
            "portal": cls.PORTAL_WORLD,
            "dark_lord": cls.DARK_LORD_RISING,
            "fairy_tale": cls.FAIRY_TALE_RETELLING,
            
            # Horror variations
            "haunted": cls.HAUNTED_HOUSE,
            "ghost": cls.HAUNTED_HOUSE,
            "possession": cls.POSSESSION,
            "curse": cls.CURSED_OBJECT,
            "cursed": cls.CURSED_OBJECT,
            "monster_hunt": cls.MONSTER_HUNT,
            "zombie": cls.VIRAL_OUTBREAK,
            "virus": cls.VIRAL_OUTBREAK,
            "cult": cls.CULT_HORROR,
            
            # Romance variations
            "enemies_to_lovers": cls.ENEMIES_TO_LOVERS,
            "forbidden": cls.FORBIDDEN_LOVE,
            "second_chance": cls.SECOND_CHANCE_ROMANCE,
            "fake": cls.FAKE_RELATIONSHIP,
            "marriage": cls.MARRIAGE_OF_CONVENIENCE,
            "triangle": cls.LOVE_TRIANGLE,
            "workplace": cls.WORKPLACE_ROMANCE,
            
            # Crime/Mystery variations
            "locked_room": cls.LOCKED_ROOM_MYSTERY,
            "serial": cls.SERIAL_KILLER,
            "killer": cls.SERIAL_KILLER,
            "cold_case": cls.COLD_CASE,
            "detective": cls.AMATEUR_DETECTIVE,
            "police": cls.POLICE_PROCEDURAL,
            "legal": cls.LEGAL_THRILLER,
            "court": cls.LEGAL_THRILLER,
            
            # Historical variations
            "war": cls.WAR_STORY,
            "political": cls.POLITICAL_INTRIGUE,
            "revolution": cls.SOCIAL_REVOLUTION,
            "immigrant": cls.IMMIGRANT_STORY,
            "family_saga": cls.FAMILY_SAGA,
            "period": cls.PERIOD_ROMANCE,
            
            # Literary variations
            "character": cls.CHARACTER_STUDY,
            "study": cls.CHARACTER_STUDY,
            "midlife": cls.MIDLIFE_CRISIS,
            "family": cls.FAMILY_DRAMA,
            "drama": cls.FAMILY_DRAMA,
            "existential": cls.EXISTENTIAL_JOURNEY,
            "identity": cls.IDENTITY_CRISIS,
            "moral": cls.MORAL_DILEMMA,
            
            # YA variations
            "school": cls.SCHOOL_STORY,
            "teen": cls.TEEN_REBELLION,
            "bullying": cls.BULLYING_STORY,
            "sports": cls.SPORTS_COMPETITION,
            "college": cls.COLLEGE_STORY,
            "first_love": cls.FIRST_LOVE,
            
            # Adventure variations
            "treasure": cls.TREASURE_HUNT,
            "exploration": cls.EXPLORATION,
            "rescue": cls.RESCUE_MISSION,
            "race": cls.RACE_AGAINST_TIME,
            "martial": cls.MARTIAL_ARTS,
            "pirate": cls.PIRATE_ADVENTURE,
            "jungle": cls.JUNGLE_ADVENTURE,
            "mountain": cls.MOUNTAIN_CLIMBING,
            
            # Business variations
            "corporate": cls.CORPORATE_THRILLER,
            "startup": cls.STARTUP_STORY,
            "business": cls.BUSINESS_RIVALRY,
            "financial": cls.FINANCIAL_CRISIS,
            "entrepreneur": cls.ENTREPRENEURIAL_JOURNEY,
            
            # Contemporary variations
            "environment": cls.ENVIRONMENTAL_CRISIS,
            "pandemic": cls.PANDEMIC_STORY,
            "social_media": cls.SOCIAL_MEDIA_DRAMA,
            "technology": cls.TECHNOLOGY_ADDICTION,
            "mental_health": cls.MENTAL_HEALTH_JOURNEY,
            "immigration": cls.IMMIGRATION_STORY,
            "gender": cls.GENDER_IDENTITY,
            "racial": cls.RACIAL_JUSTICE,
            "economic": cls.ECONOMIC_INEQUALITY,
        }
        
        if normalized_value in fuzzy_matches:
            return fuzzy_matches[normalized_value]
        
        # Partial matching
        for key, plot in fuzzy_matches.items():
            if key in normalized_value or normalized_value in key:
                return plot
        
        # Check if the normalized value contains any plot as a substring
        for plot in cls:
            if plot.value in normalized_value or normalized_value in plot.value:
                return plot
        
        available_plots = [plot.value for plot in cls]
        raise ValueError(
            f"Unknown plot type: '{value}'. "
            f"Available plots include: {', '.join(sorted(available_plots[:10]))}..."
        )
    
    @classmethod
    def get_plots_for_genre(cls, genre: str) -> List['PlotType']:
        """Get recommended plot types for a specific genre."""
        genre_lower = genre.lower()
        
        genre_mappings = {
            "fantasy": [
                cls.THE_QUEST, cls.CHOSEN_ONE, cls.OVERCOMING_THE_MONSTER,
                cls.MAGICAL_AWAKENING, cls.DARK_LORD_RISING, cls.ANCIENT_PROPHECY,
                cls.PORTAL_WORLD, cls.DRAGON_SLAYING, cls.LOST_KINGDOM,
                cls.MAGICAL_ARTIFACT, cls.FAIRY_TALE_RETELLING, cls.REBIRTH
            ],
            "science_fiction": [
                cls.FIRST_CONTACT, cls.TIME_TRAVEL, cls.DYSTOPIAN_REBELLION,
                cls.TECHNOLOGICAL_UPRISING, cls.SPACE_EXPLORATION, cls.ALIEN_INVASION,
                cls.COLONIZATION, cls.GENETIC_ENHANCEMENT, cls.VIRTUAL_REALITY,
                cls.THE_QUEST, cls.OVERCOMING_THE_MONSTER, cls.SURVIVAL
            ],
            "romance": [
                cls.ROMANCE_LOVE_STORY, cls.ENEMIES_TO_LOVERS, cls.FORBIDDEN_LOVE,
                cls.SECOND_CHANCE_ROMANCE, cls.FAKE_RELATIONSHIP, cls.MARRIAGE_OF_CONVENIENCE,
                cls.LOVE_TRIANGLE, cls.STAR_CROSSED_LOVERS, cls.WORKPLACE_ROMANCE,
                cls.HOLIDAY_ROMANCE, cls.FIRST_LOVE, cls.COMEDY
            ],
            "mystery": [
                cls.MYSTERY_INVESTIGATION, cls.LOCKED_ROOM_MYSTERY, cls.SERIAL_KILLER,
                cls.COLD_CASE, cls.AMATEUR_DETECTIVE, cls.POLICE_PROCEDURAL,
                cls.LEGAL_THRILLER, cls.CONSPIRACY, cls.HISTORICAL_MYSTERY
            ],
            "thriller": [
                cls.CONSPIRACY, cls.CHASE, cls.ESCAPE, cls.HEIST, cls.KIDNAPPING,
                cls.ASSASSINATION, cls.ESPIONAGE, cls.TICKING_CLOCK, cls.CAT_AND_MOUSE,
                cls.SURVIVAL, cls.CORPORATE_THRILLER, cls.LEGAL_THRILLER
            ],
            "horror": [
                cls.HAUNTED_HOUSE, cls.POSSESSION, cls.CURSED_OBJECT, cls.MONSTER_HUNT,
                cls.APOCALYPTIC_HORROR, cls.PSYCHOLOGICAL_BREAKDOWN, cls.CULT_HORROR,
                cls.BODY_HORROR, cls.VIRAL_OUTBREAK, cls.SUPERNATURAL_HORROR, cls.OVERCOMING_THE_MONSTER
            ],
            "young_adult": [
                cls.COMING_OF_AGE, cls.SCHOOL_STORY, cls.FIRST_LOVE, cls.TEEN_REBELLION,
                cls.BULLYING_STORY, cls.SPORTS_COMPETITION, cls.TALENT_COMPETITION,
                cls.FAMILY_SECRETS, cls.COLLEGE_STORY, cls.CHOSEN_ONE, cls.DYSTOPIAN_REBELLION
            ],
            "historical_fiction": [
                cls.WAR_STORY, cls.POLITICAL_INTRIGUE, cls.SOCIAL_REVOLUTION,
                cls.PERIOD_ROMANCE, cls.IMMIGRANT_STORY, cls.FAMILY_SAGA,
                cls.CULTURAL_CLASH, cls.HISTORICAL_MYSTERY, cls.RISE_AND_FALL
            ],
            "literary_fiction": [
                cls.CHARACTER_STUDY, cls.MIDLIFE_CRISIS, cls.FAMILY_DRAMA,
                cls.RELATIONSHIP_DRAMA, cls.EXISTENTIAL_JOURNEY, cls.SOCIAL_COMMENTARY,
                cls.GENERATIONAL_CONFLICT, cls.IDENTITY_CRISIS, cls.MORAL_DILEMMA,
                cls.REBIRTH, cls.TRAGEDY, cls.REDEMPTION
            ],
            "adventure": [
                cls.THE_QUEST, cls.TREASURE_HUNT, cls.EXPLORATION, cls.RESCUE_MISSION,
                cls.RACE_AGAINST_TIME, cls.SURVIVAL_ADVENTURE, cls.PIRATE_ADVENTURE,
                cls.JUNGLE_ADVENTURE, cls.MOUNTAIN_CLIMBING, cls.ESCAPE
            ],
            "crime": [
                cls.SERIAL_KILLER, cls.CRIME_FAMILY, cls.UNDERCOVER_OPERATION,
                cls.HEIST, cls.WITNESS_PROTECTION, cls.POLICE_PROCEDURAL,
                cls.LEGAL_THRILLER, cls.CONSPIRACY, cls.REVENGE
            ],
            "business": [
                cls.CORPORATE_THRILLER, cls.STARTUP_STORY, cls.BUSINESS_RIVALRY,
                cls.WORKPLACE_DRAMA, cls.FINANCIAL_CRISIS, cls.WHISTLEBLOWER,
                cls.MERGER_ACQUISITION, cls.ENTREPRENEURIAL_JOURNEY, cls.PROFESSIONAL_COMEBACK
            ],
            "dystopian": [
                cls.DYSTOPIAN_REBELLION, cls.SURVIVAL, cls.ESCAPE, cls.CONSPIRACY,
                cls.TECHNOLOGICAL_UPRISING, cls.SOCIAL_REVOLUTION, cls.SACRIFICE,
                cls.OVERCOMING_THE_MONSTER, cls.REDEMPTION
            ],
            "paranormal": [
                cls.MAGICAL_AWAKENING, cls.SUPERNATURAL_HORROR, cls.POSSESSION,
                cls.CURSED_OBJECT, cls.PORTAL_WORLD, cls.CHOSEN_ONE,
                cls.OVERCOMING_THE_MONSTER, cls.FORBIDDEN_LOVE
            ]
        }
        
        # Find matching plots
        recommended = set()
        for genre_key, plots in genre_mappings.items():
            if genre_key in genre_lower:
                recommended.update(plots)
        
        # If no specific mapping found, return general plots
        if not recommended:
            recommended = {
                cls.THE_QUEST, cls.OVERCOMING_THE_MONSTER, cls.COMING_OF_AGE,
                cls.ROMANCE_LOVE_STORY, cls.MYSTERY_INVESTIGATION, cls.SURVIVAL
            }
        
        return sorted(list(recommended), key=lambda x: x.display_name)
    
    @classmethod
    def get_plots_by_complexity(cls, complexity: str) -> List['PlotType']:
        """Get plot types filtered by complexity level."""
        return [plot for plot in cls if plot.complexity_level == complexity.lower()]
    
    @classmethod
    def get_classic_plots(cls) -> List['PlotType']:
        """Get the classic archetypal plot types."""
        return [
            cls.OVERCOMING_THE_MONSTER, cls.RAGS_TO_RICHES, cls.THE_QUEST,
            cls.VOYAGE_AND_RETURN, cls.COMEDY, cls.TRAGEDY, cls.REBIRTH
        ]
    
    @classmethod
    def get_modern_plots(cls) -> List['PlotType']:
        """Get contemporary and modern plot types."""
        return [
            cls.ENVIRONMENTAL_CRISIS, cls.PANDEMIC_STORY, cls.SOCIAL_MEDIA_DRAMA,
            cls.TECHNOLOGY_ADDICTION, cls.MENTAL_HEALTH_JOURNEY, cls.IMMIGRATION_STORY,
            cls.GENDER_IDENTITY, cls.RACIAL_JUSTICE, cls.ECONOMIC_INEQUALITY,
            cls.CORPORATE_THRILLER, cls.STARTUP_STORY, cls.VIRAL_OUTBREAK
        ]
    
    def __str__(self) -> str:
        return self.display_name


# Example usage and testing
if __name__ == "__main__":
    print("=== MuseQuill Plot Type System Demo ===\n")
    
    # Test PlotType enum
    print("1. Plot Type Examples:")
    test_plots = [
        PlotType.THE_QUEST, PlotType.ENEMIES_TO_LOVERS, 
        PlotType.DYSTOPIAN_REBELLION, PlotType.CORPORATE_THRILLER
    ]
    
    for plot in test_plots:
        print(f"  • {plot.display_name}")
        print(f"    Complexity: {plot.complexity_level}")
        print(f"    Target Length: {plot.target_length}")
        print(f"    Themes: {', '.join(plot.typical_themes)}")
        print(f"    Description: {plot.description[:100]}...")
        print()
    
    # Test string conversion
    print("2. String Conversion Examples:")
    test_strings = ["quest", "enemies to lovers", "dystopian", "corporate", "mystery"]
    for test_str in test_strings:
        try:
            plot = PlotType.from_string(test_str)
            print(f"  '{test_str}' -> {plot.display_name}")
        except ValueError as e:
            print(f"  '{test_str}' -> ERROR: {e}")
    
    # Test genre recommendations
    print("\n3. Genre-based Plot Recommendations:")
    test_genres = ["fantasy", "romance", "thriller", "business"]
    for genre in test_genres:
        plots = PlotType.get_plots_for_genre(genre)
        print(f"  {genre.title()}: {', '.join([p.display_name for p in plots[:4]])}...")
    
    # Test complexity filtering
    print("\n4. Plot Complexity Categories:")
    for complexity in ["simple", "moderate", "complex", "very_complex"]:
        plots = PlotType.get_plots_by_complexity(complexity)
        print(f"  {complexity.title()}: {len(plots)} plots")
    
    # Test classic vs modern plots
    print("\n5. Classic vs Modern Plots:")
    classic_plots = PlotType.get_classic_plots()
    modern_plots = PlotType.get_modern_plots()
    print(f"  Classic plots: {len(classic_plots)} ({', '.join([p.display_name for p in classic_plots[:3]])}...)")
    print(f"  Modern plots: {len(modern_plots)} ({', '.join([p.display_name for p in modern_plots[:3]])}...)")
    
    print("\n=== Demo Complete ===")