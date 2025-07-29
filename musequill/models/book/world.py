from enum import Enum
from typing import List, Dict, Any, Optional


class WorldType(str, Enum):
    """Types of fictional worlds with comprehensive world-building characteristics."""
    
    # Contemporary & Realistic Worlds
    REALISTIC = "realistic"                          # Real world, no fantastical elements
    CONTEMPORARY = "contemporary"                    # Modern-day realistic settings
    HISTORICAL = "historical"                       # Past periods without fantasy elements
    ALTERNATE_HISTORY = "alternate_history"          # Real world with historical changes
    
    # Fantasy Worlds by Magic Level
    LOW_FANTASY = "low_fantasy"                     # Real world with subtle magic
    HIGH_FANTASY = "high_fantasy"                   # Completely fictional magical world
    EPIC_FANTASY = "epic_fantasy"                   # Grand-scale high fantasy with heroes
    URBAN_FANTASY = "urban_fantasy"                 # Modern world with hidden magic
    DARK_FANTASY = "dark_fantasy"                   # Fantasy with horror elements
    GRIMDARK = "grimdark"                          # Morally complex, pessimistic fantasy
    SWORD_AND_SORCERY = "sword_and_sorcery"        # Action-focused fantasy with warriors
    HEROIC_FANTASY = "heroic_fantasy"              # Classic adventure fantasy
    
    # Fantasy Subgenres by Setting
    MEDIEVAL_FANTASY = "medieval_fantasy"           # Fantasy in medieval-inspired settings
    GOTHIC_FANTASY = "gothic_fantasy"              # Dark, atmospheric fantasy
    FAIRY_TALE = "fairy_tale"                      # Traditional fairy tale worlds
    MYTHIC_FANTASY = "mythic_fantasy"              # Based on real mythology
    ARTHURIAN = "arthurian"                        # Arthurian legend-inspired worlds
    PORTAL_FANTASY = "portal_fantasy"              # Characters travel between worlds
    SECONDARY_WORLD = "secondary_world"            # Completely separate fantasy realm
    
    # Magic System Variants
    MAGICAL_REALISM = "magical_realism"            # Realistic world with accepted magic
    GASLAMP_FANTASY = "gaslamp_fantasy"            # Victorian-era fantasy
    FLINTLOCK_FANTASY = "flintlock_fantasy"        # Fantasy with early firearms
    GUNPOWDER_FANTASY = "gunpowder_fantasy"        # Fantasy with gunpowder weapons
    ARCANE_FANTASY = "arcane_fantasy"              # Magic and science coexist
    
    # Science Fiction Worlds
    SCIENCE_FICTION = "science_fiction"            # Future or alternate reality
    HARD_SCIENCE_FICTION = "hard_science_fiction"  # Scientifically accurate SF
    SOFT_SCIENCE_FICTION = "soft_science_fiction"  # Focus on social sciences
    SPACE_OPERA = "space_opera"                    # Galaxy-spanning adventure
    CYBERPUNK = "cyberpunk"                        # High-tech, low-life future
    STEAMPUNK = "steampunk"                        # Victorian-era steam technology
    DIESELPUNK = "dieselpunk"                      # 1920s-1940s diesel technology  
    BIOPUNK = "biopunk"                           # Biotechnology-focused SF
    CLOCKPUNK = "clockpunk"                       # Renaissance-era clockwork tech
    
    # Dystopian & Post-Apocalyptic
    DYSTOPIAN = "dystopian"                       # Oppressive future society
    UTOPIAN = "utopian"                           # Idealized future society
    POST_APOCALYPTIC = "post_apocalyptic"         # After civilization collapse
    POST_NUCLEAR = "post_nuclear"                 # After nuclear catastrophe
    ZOMBIE_APOCALYPSE = "zombie_apocalypse"       # Undead-overrun world
    
    # Hybrid & Experimental Worlds
    SCIENCE_FANTASY = "science_fantasy"           # Blend of SF and fantasy
    NEW_WEIRD = "new_weird"                       # Experimental weird fiction
    SLIPSTREAM = "slipstream"                     # Between genres
    PARALLEL_UNIVERSE = "parallel_universe"       # Different version of reality
    MULTIVERSE = "multiverse"                     # Multiple interconnected realities
    
    # Supernatural & Horror
    PARANORMAL = "paranormal"                     # Modern world with supernatural
    SUPERNATURAL = "supernatural"                 # Focused on supernatural beings
    GOTHIC_HORROR = "gothic_horror"               # Dark, atmospheric horror
    COSMIC_HORROR = "cosmic_horror"               # Lovecraftian cosmic dread
    OCCULT = "occult"                            # Hidden supernatural knowledge
    
    # Specialized Settings
    ANTHROPOMORPHIC = "anthropomorphic"           # Animal characters with human traits
    UNDERWATER = "underwater"                     # Aquatic civilizations
    UNDERGROUND = "underground"                   # Subterranean worlds
    FLOATING_ISLANDS = "floating_islands"         # Sky-based civilizations
    HOLLOW_EARTH = "hollow_earth"                # Inner earth civilizations
    GENERATION_SHIP = "generation_ship"           # Spaceship as entire world
    
    # Time-Based Worlds
    TIME_TRAVEL = "time_travel"                   # Stories involving time manipulation
    ALTERNATE_TIMELINE = "alternate_timeline"     # Different historical progression
    TIME_LOOP = "time_loop"                       # Repeating time scenarios
    
    # Additional World Types to reach 60+
    WEIRD_WEST = "weird_west"                     # Western with supernatural elements
    BIOPUNK_FANTASY = "biopunk_fantasy"           # Fantasy with biological magic
    CLIMATE_FICTION = "climate_fiction"           # Climate change focused worlds
    
    @property
    def display_name(self) -> str:
        """Human-readable display name for the world type."""
        name_map = {
            self.REALISTIC: "Realistic World",
            self.CONTEMPORARY: "Contemporary",
            self.HISTORICAL: "Historical",
            self.ALTERNATE_HISTORY: "Alternate History",
            self.LOW_FANTASY: "Low Fantasy",
            self.HIGH_FANTASY: "High Fantasy", 
            self.EPIC_FANTASY: "Epic Fantasy",
            self.URBAN_FANTASY: "Urban Fantasy",
            self.DARK_FANTASY: "Dark Fantasy",
            self.GRIMDARK: "Grimdark Fantasy",
            self.SWORD_AND_SORCERY: "Sword and Sorcery",
            self.HEROIC_FANTASY: "Heroic Fantasy",
            self.MEDIEVAL_FANTASY: "Medieval Fantasy",
            self.GOTHIC_FANTASY: "Gothic Fantasy",
            self.FAIRY_TALE: "Fairy Tale",
            self.MYTHIC_FANTASY: "Mythic Fantasy",
            self.ARTHURIAN: "Arthurian Fantasy",
            self.PORTAL_FANTASY: "Portal Fantasy",
            self.SECONDARY_WORLD: "Secondary World",
            self.MAGICAL_REALISM: "Magical Realism",
            self.GASLAMP_FANTASY: "Gaslamp Fantasy",
            self.FLINTLOCK_FANTASY: "Flintlock Fantasy",
            self.GUNPOWDER_FANTASY: "Gunpowder Fantasy",
            self.ARCANE_FANTASY: "Arcane Fantasy",
            self.SCIENCE_FICTION: "Science Fiction",
            self.HARD_SCIENCE_FICTION: "Hard Science Fiction",
            self.SOFT_SCIENCE_FICTION: "Soft Science Fiction",
            self.SPACE_OPERA: "Space Opera",
            self.CYBERPUNK: "Cyberpunk",
            self.STEAMPUNK: "Steampunk",
            self.DIESELPUNK: "Dieselpunk",
            self.BIOPUNK: "Biopunk",
            self.CLOCKPUNK: "Clockpunk",
            self.DYSTOPIAN: "Dystopian",
            self.UTOPIAN: "Utopian",
            self.POST_APOCALYPTIC: "Post-Apocalyptic",
            self.POST_NUCLEAR: "Post-Nuclear",
            self.ZOMBIE_APOCALYPSE: "Zombie Apocalypse",
            self.SCIENCE_FANTASY: "Science Fantasy",
            self.NEW_WEIRD: "New Weird",
            self.SLIPSTREAM: "Slipstream",
            self.PARALLEL_UNIVERSE: "Parallel Universe",
            self.MULTIVERSE: "Multiverse",
            self.PARANORMAL: "Paranormal",
            self.SUPERNATURAL: "Supernatural",
            self.GOTHIC_HORROR: "Gothic Horror",
            self.COSMIC_HORROR: "Cosmic Horror",
            self.OCCULT: "Occult",
            self.ANTHROPOMORPHIC: "Anthropomorphic",
            self.UNDERWATER: "Underwater",
            self.UNDERGROUND: "Underground",
            self.FLOATING_ISLANDS: "Floating Islands",
            self.HOLLOW_EARTH: "Hollow Earth",
            self.GENERATION_SHIP: "Generation Ship",
            self.TIME_TRAVEL: "Time Travel",
            self.ALTERNATE_TIMELINE: "Alternate Timeline",
            self.TIME_LOOP: "Time Loop",
            self.WEIRD_WEST: "Weird West",
            self.BIOPUNK_FANTASY: "Biopunk Fantasy",
            self.CLIMATE_FICTION: "Climate Fiction",
        }
        return name_map.get(self, self.value.replace("_", " ").title())

    @property
    def description(self) -> str:
        """Detailed description of the world type and its characteristics."""
        desc_map = {
            self.REALISTIC: "A world that mirrors our reality with no supernatural or fantastical elements. Stories focus on human relationships, contemporary issues, and realistic scenarios within recognizable settings.",
            
            self.CONTEMPORARY: "Modern-day settings in the real world, often featuring current technology, social issues, and cultural contexts that readers can immediately relate to.",
            
            self.HISTORICAL: "Set in past time periods without fantasy elements, requiring extensive research into historical accuracy, period-appropriate technology, customs, and social structures.",
            
            self.ALTERNATE_HISTORY: "Our world with key historical events changed, exploring 'what if' scenarios where different outcomes led to alternate timelines and societies.",
            
            self.LOW_FANTASY: "The real world with subtle magical or supernatural elements that exist on the margins, often hidden from most people or dismissed as myth.",
            
            self.HIGH_FANTASY: "Completely fictional worlds with their own geography, cultures, magic systems, and often non-human races. Magic is prevalent and accepted as part of reality.",
            
            self.EPIC_FANTASY: "Grand-scale fantasy featuring world-threatening conflicts, chosen heroes, ancient prophecies, and sweeping narratives that span continents and affect entire civilizations.",
            
            self.URBAN_FANTASY: "Modern urban settings where magic and supernatural creatures exist hidden within contemporary society, blending the mundane with the mystical.",
            
            self.DARK_FANTASY: "Fantasy worlds with horror elements, moral ambiguity, and often disturbing or frightening supernatural elements that create an atmosphere of dread.",
            
            self.GRIMDARK: "Morally complex fantasy worlds where heroes are flawed, violence has consequences, and happy endings are rare. Focuses on realistic human nature in fantastic settings.",
            
            self.SWORD_AND_SORCERY: "Action-oriented fantasy focusing on individual warriors and adventurers, emphasizing combat, magic, and personal conflicts over grand world-spanning plots.",
            
            self.HEROIC_FANTASY: "Traditional adventure fantasy featuring noble heroes, clear good vs. evil conflicts, and quests to save kingdoms or worlds from dark forces.",
            
            self.MEDIEVAL_FANTASY: "Fantasy worlds based on medieval European societies, featuring knights, castles, feudalism, and period-appropriate technology enhanced with magical elements.",
            
            self.GOTHIC_FANTASY: "Dark, atmospheric fantasy with elements of horror, often set in decaying castles, haunted landscapes, and featuring brooding atmospheres and psychological elements.",
            
            self.FAIRY_TALE: "Worlds based on traditional folk tales and fairy stories, often featuring magic, talking animals, enchanted forests, and moral lessons.",
            
            self.MYTHIC_FANTASY: "Fantasy based on real-world mythologies, reimagining ancient gods, heroes, and legendary creatures in new narratives while respecting source traditions.",
            
            self.ARTHURIAN: "Fantasy inspired by Arthurian legend, featuring knights of the Round Table, the quest for the Holy Grail, and themes of chivalry and honor.",
            
            self.PORTAL_FANTASY: "Stories where characters travel from our world to a fantasy realm through magical portals, doors, or other transitions between realities.",
            
            self.SECONDARY_WORLD: "Completely separate fantasy realms with no connection to Earth, featuring unique geography, cultures, magic systems, and often non-human species.",
            
            self.MAGICAL_REALISM: "Realistic worlds where magical events are treated as natural and accepted parts of everyday life, often used to explore deeper truths about reality.",
            
            self.GASLAMP_FANTASY: "Fantasy set in Victorian-era inspired worlds, featuring gas lighting, industrial revolution technology, and often combining scientific advancement with magic.",
            
            self.FLINTLOCK_FANTASY: "Fantasy worlds with early firearms technology, typically Renaissance or colonial era inspired, where magic coexists with gunpowder weapons.",
            
            self.GUNPOWDER_FANTASY: "Fantasy incorporating various forms of gunpowder weapons and military technology, exploring how magic and firearms interact in warfare and society.",
            
            self.ARCANE_FANTASY: "Worlds where magic and science blend together, creating new disciplines like magical engineering or alchemical technology that serves both mystical and practical purposes.",
            
            self.SCIENCE_FICTION: "Futuristic or alternate reality worlds featuring advanced technology, space travel, artificial intelligence, and scientific concepts as central elements.",
            
            self.HARD_SCIENCE_FICTION: "Science fiction that emphasizes scientific accuracy and technical details, grounding fantastical elements in real or plausible scientific principles.",
            
            self.SOFT_SCIENCE_FICTION: "Science fiction focused more on social sciences and human relationships, using technology as a backdrop rather than a central technical focus.",
            
            self.SPACE_OPERA: "Galaxy-spanning science fiction adventures featuring interstellar travel, alien civilizations, space battles, and epic conflicts across multiple worlds.",
            
            self.CYBERPUNK: "High-tech, low-life futures featuring advanced computer technology, virtual reality, corporate dominance, and social decay in urban environments.",
            
            self.STEAMPUNK: "Victorian-era alternate history where steam power has advanced to create fantastic machines, airships, and mechanical devices in a retro-futuristic setting.",
            
            self.DIESELPUNK: "1920s-1940s inspired alternate history featuring diesel technology, art deco aesthetics, and the social tensions of the interwar and World War II periods.",
            
            self.BIOPUNK: "Science fiction focused on biotechnology, genetic engineering, and biological sciences, exploring the implications of advanced life sciences on society.",
            
            self.CLOCKPUNK: "Renaissance-era alternate history featuring elaborate clockwork mechanisms and early mechanical technology as the basis for fantastic inventions.",
            
            self.DYSTOPIAN: "Oppressive future societies where individual freedom is suppressed, often serving as warnings about political and social trends.",
            
            self.UTOPIAN: "Idealized future societies that have solved major human problems, though often revealing hidden costs or contradictions in apparent perfection.",
            
            self.POST_APOCALYPTIC: "Worlds after the collapse of modern civilization, focusing on survival, rebuilding, and the human condition in the aftermath of catastrophe.",
            
            self.POST_NUCLEAR: "Specific post-apocalyptic scenarios dealing with the aftermath of nuclear war, radiation, and the struggle to rebuild from atomic devastation.",
            
            self.ZOMBIE_APOCALYPSE: "Worlds overrun by undead creatures, focusing on survival horror, the breakdown of social order, and human nature under extreme stress.",
            
            self.SCIENCE_FANTASY: "Hybrid genre combining science fiction technology with fantasy magic, often set in space or futuristic settings with mystical elements.",
            
            self.NEW_WEIRD: "Experimental fiction that subverts traditional genre expectations, combining elements of fantasy, horror, and science fiction in innovative ways.",
            
            self.SLIPSTREAM: "Genre-blending fiction that exists between categories, often featuring surreal or slightly fantastic elements in otherwise realistic settings.",
            
            self.PARALLEL_UNIVERSE: "Stories involving alternate versions of our reality where different choices or events have led to dramatically different worlds.",
            
            self.MULTIVERSE: "Narratives spanning multiple interconnected realities, exploring infinite possibilities and the connections between different versions of existence.",
            
            self.PARANORMAL: "Modern world settings featuring supernatural elements like ghosts, vampires, werewolves, and psychic phenomena as part of hidden reality.",
            
            self.SUPERNATURAL: "Worlds focused on beings and forces beyond natural explanation, including spirits, demons, angels, and other entities from beyond the physical realm.",
            
            self.GOTHIC_HORROR: "Dark, atmospheric horror featuring ancient curses, haunted locations, psychological terror, and often Victorian or medieval settings.",
            
            self.COSMIC_HORROR: "Horror emphasizing humanity's insignificance in the face of vast, incomprehensible cosmic forces and alien intelligences beyond human understanding.",
            
            self.OCCULT: "Worlds involving hidden supernatural knowledge, secret societies, magical practices, and esoteric wisdom accessible only to initiates.",
            
            self.ANTHROPOMORPHIC: "Worlds populated by animal characters with human characteristics, intelligence, and society, often used for allegory or social commentary.",
            
            self.UNDERWATER: "Civilizations and stories set in aquatic environments, featuring underwater cities, marine life, and unique challenges of aquatic existence.",
            
            self.UNDERGROUND: "Subterranean worlds featuring cave civilizations, underground cities, and the unique ecosystem and challenges of life beneath the surface.",
            
            self.FLOATING_ISLANDS: "Sky-based civilizations living on floating landmasses, featuring aerial transportation, unique weather phenomena, and height-based social structures.",
            
            self.HOLLOW_EARTH: "Worlds set inside the Earth featuring inner civilizations, unique physics, and often prehistoric or fantastical creatures in underground realms.",
            
            self.GENERATION_SHIP: "Spacecraft that serve as entire worlds for populations traveling between stars over generations, exploring closed societies and long-term survival.",
            
            self.TIME_TRAVEL: "Worlds where time manipulation is possible, exploring paradoxes, alternate timelines, and the consequences of changing past events.",
            
            self.ALTERNATE_TIMELINE: "Realities where history diverged at specific points, creating different technological, social, or political developments from our timeline.",
            
            self.TIME_LOOP: "Scenarios where characters experience repeating time periods, exploring themes of destiny, change, and the nature of causality.",
            
            self.WEIRD_WEST: "Western frontier settings with supernatural or fantastical elements, combining cowboy culture with magic, monsters, or otherworldly phenomena.",
            
            self.BIOPUNK_FANTASY: "Fantasy worlds where magic is expressed through biological manipulation, living architecture, and organic technology rather than traditional spellcasting.",
            
            self.CLIMATE_FICTION: "Contemporary or near-future worlds dealing with climate change and environmental catastrophe, exploring humanity's relationship with nature and the consequences of ecological destruction."
        }
        return desc_map.get(self, f"A fictional world of type {self.display_name}")

    @property
    def world_building_complexity(self) -> str:
        """Indicates the level of world-building complexity required."""
        complexity_map = {
            # Low Complexity - based on existing reality
            self.REALISTIC: "Low",
            self.CONTEMPORARY: "Low", 
            self.HISTORICAL: "Medium",
            
            # Medium Complexity - some new elements
            self.ALTERNATE_HISTORY: "Medium",
            self.LOW_FANTASY: "Medium",
            self.URBAN_FANTASY: "Medium",
            self.MAGICAL_REALISM: "Medium",
            self.PARANORMAL: "Medium",
            self.SUPERNATURAL: "Medium",
            self.TIME_TRAVEL: "Medium",
            self.ALTERNATE_TIMELINE: "Medium",
            self.TIME_LOOP: "Medium",
            self.WEIRD_WEST: "Medium",
            self.BIOPUNK_FANTASY: "High", 
            self.CLIMATE_FICTION: "Medium",
            
            # High Complexity - extensive new world creation
            self.HIGH_FANTASY: "High",
            self.EPIC_FANTASY: "Very High",
            self.SECONDARY_WORLD: "Very High",
            self.SPACE_OPERA: "Very High",
            self.HARD_SCIENCE_FICTION: "High",
            self.SOFT_SCIENCE_FICTION: "High",
            self.SCIENCE_FICTION: "High",
            self.MULTIVERSE: "Very High",
            self.GENERATION_SHIP: "High",
            
            # Variable Complexity - depends on implementation
            self.DARK_FANTASY: "High",
            self.GRIMDARK: "High", 
            self.SWORD_AND_SORCERY: "Medium",
            self.HEROIC_FANTASY: "Medium",
            self.MEDIEVAL_FANTASY: "Medium",
            self.GOTHIC_FANTASY: "Medium",
            self.FAIRY_TALE: "Low",
            self.MYTHIC_FANTASY: "Medium",
            self.ARTHURIAN: "Medium",
            self.PORTAL_FANTASY: "High",
            self.GASLAMP_FANTASY: "Medium",
            self.FLINTLOCK_FANTASY: "Medium",
            self.GUNPOWDER_FANTASY: "Medium",
            self.ARCANE_FANTASY: "High",
            self.CYBERPUNK: "High",
            self.STEAMPUNK: "High",
            self.DIESELPUNK: "High",
            self.BIOPUNK: "High",
            self.CLOCKPUNK: "High",
            self.DYSTOPIAN: "Medium",
            self.UTOPIAN: "Medium",
            self.POST_APOCALYPTIC: "Medium",
            self.POST_NUCLEAR: "Medium",
            self.ZOMBIE_APOCALYPSE: "Medium",
            self.SCIENCE_FANTASY: "High",
            self.NEW_WEIRD: "High",
            self.SLIPSTREAM: "Medium",
            self.PARALLEL_UNIVERSE: "High",
            self.GOTHIC_HORROR: "Medium",
            self.COSMIC_HORROR: "High",
            self.OCCULT: "Medium",
            self.ANTHROPOMORPHIC: "Medium",
            self.UNDERWATER: "High",
            self.UNDERGROUND: "High",
            self.FLOATING_ISLANDS: "High",
            self.HOLLOW_EARTH: "High",
        }
        return complexity_map.get(self, "Medium")

    @property
    def key_elements(self) -> List[str]:
        """Essential elements that define this world type."""
        elements_map = {
            self.REALISTIC: ["authentic settings", "believable characters", "real-world problems", "contemporary issues"],
            
            self.CONTEMPORARY: ["modern technology", "current social issues", "urban environments", "realistic dialogue"],
            
            self.HISTORICAL: ["period accuracy", "historical events", "authentic customs", "period-appropriate technology"],
            
            self.ALTERNATE_HISTORY: ["point of divergence", "changed historical outcomes", "butterfly effects", "altered technology"],
            
            self.LOW_FANTASY: ["subtle magic", "hidden supernatural", "real-world base", "mystery elements"],
            
            self.HIGH_FANTASY: ["magic systems", "non-human races", "original geography", "fantasy creatures"],
            
            self.EPIC_FANTASY: ["world-threatening conflicts", "chosen heroes", "ancient prophecies", "multiple kingdoms", "heroic journey", "magical elements"],
            
            self.URBAN_FANTASY: ["modern city settings", "hidden magical world", "supernatural creatures", "technology-magic interaction"],
            
            self.DARK_FANTASY: ["horror elements", "moral ambiguity", "disturbing imagery", "psychological tension", "fantasy elements", "supernatural horror"],
            
            self.GRIMDARK: ["moral complexity", "realistic consequences", "flawed heroes", "political intrigue"],
            
            self.SWORD_AND_SORCERY: ["warrior protagonists", "personal conflicts", "magic and combat", "adventure focus"],
            
            self.HEROIC_FANTASY: ["noble heroes", "clear morality", "quests and adventures", "good vs evil"],
            
            self.MEDIEVAL_FANTASY: ["feudal society", "knights and castles", "medieval technology", "court intrigue", "fantasy elements", "magical creatures"],
            
            self.GOTHIC_FANTASY: ["atmospheric settings", "psychological horror", "decaying architecture", "supernatural dread"],
            
            self.FAIRY_TALE: ["magical elements", "moral lessons", "archetypal characters", "enchanted settings"],
            
            self.MYTHIC_FANTASY: ["mythological beings", "ancient legends", "cultural authenticity", "epic themes", "supernatural elements", "mythical creatures"],
            
            self.ARTHURIAN: ["chivalric code", "Round Table", "quest for Grail", "knights and honor", "magical elements", "legendary tales"],
            
            self.PORTAL_FANTASY: ["world transitions", "fish-out-of-water", "contrasting realities", "dimensional travel", "magical portals", "fantasy realms"],
            
            self.SECONDARY_WORLD: ["complete world creation", "unique cultures", "original languages", "independent history"],
            
            self.MAGICAL_REALISM: ["accepted magical events", "symbolic elements", "realistic base", "cultural themes"],
            
            self.GASLAMP_FANTASY: ["Victorian aesthetics", "industrial technology", "gas-powered devices", "period fashion"],
            
            self.FLINTLOCK_FANTASY: ["early firearms", "Renaissance technology", "gunpowder magic", "military tactics"],
            
            self.GUNPOWDER_FANTASY: ["firearms integration", "magical ammunition", "siege warfare", "military innovation"],
            
            self.ARCANE_FANTASY: ["magic-science fusion", "alchemical technology", "magical engineering", "hybrid systems"],
            
            self.SCIENCE_FICTION: ["advanced technology", "scientific concepts", "future societies", "technological impact"],
            
            self.HARD_SCIENCE_FICTION: ["scientific accuracy", "technical details", "plausible technology", "physics-based science"],
            
            self.SOFT_SCIENCE_FICTION: ["social sciences focus", "human relationships", "technology as backdrop", "future societal change"],
            
            self.SPACE_OPERA: ["interstellar travel", "alien civilizations", "space battles", "galactic politics", "advanced technology"],
            
            self.CYBERPUNK: ["virtual reality", "corporate dystopia", "cyber hacking culture", "urban digital decay"],
            
            self.STEAMPUNK: ["steam technology", "Victorian era", "mechanical devices", "advanced brass and gears"],
            
            self.DIESELPUNK: ["diesel technology", "art deco style", "wartime aesthetics", "advanced industrial power"],
            
            self.BIOPUNK: ["genetic engineering", "biotech corporations", "organic technology", "advanced life sciences"],
            
            self.CLOCKPUNK: ["clockwork mechanisms", "Renaissance setting", "mechanical precision", "advanced gear systems"],
            
            self.DYSTOPIAN: ["oppressive government", "surveillance state", "individual vs system", "social control"],
            
            self.UTOPIAN: ["perfect society", "solved problems", "hidden costs", "social harmony"],
            
            self.POST_APOCALYPTIC: ["civilizational collapse", "survival themes", "resource scarcity", "rebuilding society"],
            
            self.POST_NUCLEAR: ["radiation effects", "atomic devastation", "mutant creatures", "nuclear winter"],
            
            self.ZOMBIE_APOCALYPSE: ["undead creatures", "survival horror", "social breakdown", "group dynamics"],
            
            self.SCIENCE_FANTASY: ["magic and technology", "space settings", "mystical forces", "advanced genre blending"],
            
            self.NEW_WEIRD: ["experimental elements", "genre subversion", "surreal imagery", "innovative narrative"],
            
            self.SLIPSTREAM: ["reality blending", "subtle strangeness", "genre ambiguity", "surreal elements"],
            
            self.PARALLEL_UNIVERSE: ["alternate realities", "dimensional travel", "reality variants", "choice consequences"],
            
            self.MULTIVERSE: ["infinite realities", "reality connections", "cosmic scope", "universal themes"],
            
            self.PARANORMAL: ["supernatural beings", "psychic abilities", "hidden world", "modern setting"],
            
            self.SUPERNATURAL: ["ghostly entities", "spiritual forces", "otherworldly beings", "mystical phenomena"],
            
            self.GOTHIC_HORROR: ["atmospheric dread", "psychological terror", "dark architecture", "ancient curses"],
            
            self.COSMIC_HORROR: ["cosmic entities", "human insignificance", "unknowable forces", "existential dread"],
            
            self.OCCULT: ["hidden knowledge", "secret societies", "magical practices", "esoteric wisdom"],
            
            self.ANTHROPOMORPHIC: ["animal characters", "human traits", "social allegory", "cultural commentary"],
            
            self.UNDERWATER: ["aquatic civilizations", "marine life", "underwater physics", "ocean exploration"],
            
            self.UNDERGROUND: ["subterranean cities", "cave systems", "unique ecosystems", "underground culture"],
            
            self.FLOATING_ISLANDS: ["aerial civilization", "sky travel", "weather systems", "height-based society"],
            
            self.HOLLOW_EARTH: ["inner world", "unique physics", "prehistoric elements", "underground exploration"],
            
            self.GENERATION_SHIP: ["closed society", "multi-generational travel", "ship as world", "destination goals"],
            
            self.TIME_TRAVEL: ["temporal mechanics", "paradoxes", "causality", "timeline changes"],
            
            self.ALTERNATE_TIMELINE: ["historical divergence", "different development", "timeline comparison", "alternate outcomes"],
            
            self.TIME_LOOP: ["repeating time", "cycle breaking", "incremental change", "temporal prison"],
            
            self.WEIRD_WEST: ["frontier setting", "supernatural elements", "cowboy culture", "western mythology"],
            
            self.BIOPUNK_FANTASY: ["biological magic", "living architecture", "organic technology", "evolutionary themes"],
            
            self.CLIMATE_FICTION: ["environmental themes", "climate change", "ecological disaster", "sustainability"],
        }
        return elements_map.get(self, ["unique setting", "distinctive atmosphere", "thematic elements"])

    @property
    def required_research_areas(self) -> List[str]:
        """Areas of research needed for authentic world-building."""
        research_map = {
            self.REALISTIC: ["contemporary culture", "social issues", "local customs"],
            self.CONTEMPORARY: ["current events", "modern technology", "urban planning"],
            self.HISTORICAL: ["historical periods", "customs and traditions", "period technology", "social structures"],
            self.ALTERNATE_HISTORY: ["historical events", "causality", "technology development", "social consequences"],
            self.LOW_FANTASY: ["folklore and mythology", "occult traditions", "urban legends"],
            self.HIGH_FANTASY: ["mythology", "medieval societies", "linguistics", "ecology"],
            self.EPIC_FANTASY: ["world mythology", "political systems", "military tactics", "ancient cultures"],
            self.URBAN_FANTASY: ["city planning", "modern mythology", "supernatural folklore", "urban subcultures"],
            self.DARK_FANTASY: ["horror tropes", "psychological horror", "gothic architecture", "medieval periods"],
            self.GRIMDARK: ["medieval warfare", "political systems", "historical atrocities", "moral philosophy"],
            self.SWORD_AND_SORCERY: ["ancient civilizations", "combat techniques", "adventure stories", "mythology"],
            self.HEROIC_FANTASY: ["heroic myths", "quest narratives", "medieval romance", "moral philosophy"],
            self.MEDIEVAL_FANTASY: ["medieval history", "feudal systems", "castle architecture", "chivalric code"],
            self.GOTHIC_FANTASY: ["gothic architecture", "Victorian era", "supernatural folklore", "psychological horror"],
            self.FAIRY_TALE: ["folk tales", "cultural traditions", "symbolic meanings", "moral philosophy"],
            self.MYTHIC_FANTASY: ["world mythologies", "cultural anthropology", "religious systems", "ancient history"],
            self.ARTHURIAN: ["Arthurian legends", "medieval Britain", "chivalric romance", "Celtic mythology"],
            self.PORTAL_FANTASY: ["dimensional theory", "cultural contrast", "adventure narratives", "coming-of-age"],
            self.SECONDARY_WORLD: ["linguistics", "cultural anthropology", "geography", "political systems"],
            self.MAGICAL_REALISM: ["cultural traditions", "symbolic meaning", "Latin American literature", "social issues"],
            self.GASLAMP_FANTASY: ["Victorian era", "industrial revolution", "gas lighting technology", "period fashion"],
            self.FLINTLOCK_FANTASY: ["Renaissance period", "early firearms", "military history", "exploration age"],
            self.GUNPOWDER_FANTASY: ["military technology", "siege warfare", "gunpowder history", "tactical evolution"],
            self.ARCANE_FANTASY: ["alchemy", "natural philosophy", "scientific method", "magical traditions"],
            self.SCIENCE_FICTION: ["scientific principles", "future technology", "space exploration", "social trends"],
            self.HARD_SCIENCE_FICTION: ["physics", "engineering", "space technology", "scientific method"],
            self.SOFT_SCIENCE_FICTION: ["social sciences", "psychology", "anthropology", "future societies"],
            self.SPACE_OPERA: ["astronomy", "space travel", "alien cultures", "galactic politics"],
            self.CYBERPUNK: ["computer technology", "corporate culture", "urban decay", "virtual reality"],
            self.STEAMPUNK: ["Victorian era", "steam technology", "industrial revolution", "mechanical engineering"],
            self.DIESELPUNK: ["1920s-1940s history", "diesel technology", "art deco", "wartime culture"],
            self.BIOPUNK: ["genetics", "biotechnology", "medical science", "bioethics"],
            self.CLOCKPUNK: ["Renaissance period", "clockwork mechanisms", "mechanical engineering", "precision crafts"],
            self.DYSTOPIAN: ["totalitarian systems", "surveillance technology", "social control", "political theory"],
            self.UTOPIAN: ["political philosophy", "social engineering", "economics", "human nature"],
            self.POST_APOCALYPTIC: ["survival techniques", "social collapse", "resource management", "rebuilding"],
            self.POST_NUCLEAR: ["nuclear physics", "radiation effects", "fallout shelter", "atomic age"],
            self.ZOMBIE_APOCALYPSE: ["epidemiology", "survival tactics", "group psychology", "social breakdown"],
            self.SCIENCE_FANTASY: ["physics and magic", "space exploration", "mystical traditions", "genre conventions"],
            self.NEW_WEIRD: ["experimental literature", "surrealism", "genre theory", "innovative narrative"],
            self.SLIPSTREAM: ["literary theory", "reality perception", "genre boundaries", "surreal elements"],
            self.PARALLEL_UNIVERSE: ["quantum physics", "multiverse theory", "alternate history", "dimensional theory"],
            self.MULTIVERSE: ["cosmology", "quantum mechanics", "infinite possibilities", "reality theory"],
            self.PARANORMAL: ["supernatural folklore", "psychic phenomena", "urban legends", "modern mythology"],
            self.SUPERNATURAL: ["religious traditions", "spiritual beliefs", "ghost lore", "mystical experiences"],
            self.GOTHIC_HORROR: ["gothic literature", "psychological horror", "Victorian gothic", "atmospheric writing"],
            self.COSMIC_HORROR: ["astronomy", "existential philosophy", "Lovecraftian lore", "cosmic insignificance"],
            self.OCCULT: ["esoteric traditions", "magical practices", "secret societies", "mystical knowledge"],
            self.ANTHROPOMORPHIC: ["animal behavior", "social structures", "cultural allegory", "fable traditions"],
            self.UNDERWATER: ["marine biology", "underwater technology", "ocean exploration", "aquatic physics"],
            self.UNDERGROUND: ["geology", "cave systems", "subterranean life", "mining techniques"],
            self.FLOATING_ISLANDS: ["atmospheric science", "meteorology", "aerial physics", "cloud formation"],
            self.HOLLOW_EARTH: ["geology", "underground ecosystems", "exploration literature", "earth sciences"],
            self.GENERATION_SHIP: ["space travel", "closed ecosystems", "multi-generational sociology", "spacecraft design"],
            self.TIME_TRAVEL: ["temporal physics", "causality", "paradox theory", "time concepts"],
            self.ALTERNATE_TIMELINE: ["historical analysis", "causality chains", "technological development", "social evolution"],
            self.TIME_LOOP: ["temporal mechanics", "psychology", "repetition theory", "cycle narratives"],
            self.WEIRD_WEST: ["western history", "frontier life", "supernatural folklore", "cowboy culture"],
            self.BIOPUNK_FANTASY: ["biology", "genetics", "organic architecture", "evolutionary theory"],
            self.CLIMATE_FICTION: ["climate science", "environmental policy", "ecological systems", "sustainability"],
        }
        return research_map.get(self, ["general world-building", "cultural research", "historical context"])

    @property
    def common_themes(self) -> List[str]:
        """Common themes and motifs associated with this world type."""
        themes_map = {
            self.REALISTIC: ["human relationships", "personal growth", "social issues", "everyday struggles"],
            self.CONTEMPORARY: ["modern life", "technology impact", "urban alienation", "current events"],
            self.HISTORICAL: ["period authenticity", "social change", "cultural tradition", "historical significance"],
            self.ALTERNATE_HISTORY: ["consequences of change", "what if scenarios", "historical inevitability", "butterfly effects"],
            self.LOW_FANTASY: ["hidden wonders", "magic in mundane", "belief vs skepticism", "wonder and mystery"],
            self.HIGH_FANTASY: ["good vs evil", "heroic journey", "power and responsibility", "coming of age"],
            self.EPIC_FANTASY: ["destiny and prophecy", "sacrifice for greater good", "power corruption", "world-changing events"],
            self.URBAN_FANTASY: ["hidden world", "ancient vs modern", "power in shadows", "dual identity"],
            self.DARK_FANTASY: ["corruption of power", "moral ambiguity", "horror of the unknown", "psychological terror"],
            self.GRIMDARK: ["moral complexity", "war's true cost", "power corruption", "survival ethics"],
            self.SWORD_AND_SORCERY: ["personal adventure", "individual heroism", "treasure and glory", "survival"],
            self.HEROIC_FANTASY: ["noble heroism", "clear morality", "triumph of good", "chivalric ideals"],
            self.MEDIEVAL_FANTASY: ["honor and duty", "feudal loyalty", "courtly love", "social hierarchy"],
            self.GOTHIC_FANTASY: ["decay and corruption", "past haunting present", "psychological horror", "atmosphere of dread"],
            self.FAIRY_TALE: ["moral lessons", "transformation", "justice prevails", "magic and wonder"],
            self.MYTHIC_FANTASY: ["archetypal stories", "cultural wisdom", "eternal themes", "spiritual journey"],
            self.ARTHURIAN: ["chivalric code", "noble sacrifice", "quest for perfection", "tragic idealism"],
            self.PORTAL_FANTASY: ["fish out of water", "personal growth", "world comparison", "homecoming"],
            self.SECONDARY_WORLD: ["cultural exploration", "world-building showcase", "epic scope", "complete immersion"],
            self.MAGICAL_REALISM: ["accepted impossibility", "cultural identity", "social commentary", "symbolic truth"],
            self.GASLAMP_FANTASY: ["progress vs tradition", "industrial change", "Victorian values", "scientific wonder"],
            self.FLINTLOCK_FANTASY: ["technological change", "military evolution", "exploration age", "cultural contact"],
            self.GUNPOWDER_FANTASY: ["military innovation", "tactical revolution", "siege warfare", "power balance"],
            self.ARCANE_FANTASY: ["knowledge and power", "science vs magic", "technological fusion", "intellectual pursuit"],
            self.SCIENCE_FICTION: ["technological impact", "future possibilities", "human adaptation", "scientific ethics"],
            self.HARD_SCIENCE_FICTION: ["scientific accuracy", "technological plausibility", "problem solving", "rational thinking"],
            self.SOFT_SCIENCE_FICTION: ["human nature", "social change", "relationship focus", "emotional truth"],
            self.SPACE_OPERA: ["galactic scope", "heroic adventure", "alien contact", "cosmic destiny"],
            self.CYBERPUNK: ["corporate control", "technology alienation", "individual vs system", "digital identity"],
            self.STEAMPUNK: ["Victorian optimism", "mechanical wonder", "class conflict", "industrial progress"],
            self.DIESELPUNK: ["war and peace", "technological power", "social upheaval", "industrial might"],
            self.BIOPUNK: ["genetic identity", "bioethics", "human enhancement", "life manipulation"],
            self.CLOCKPUNK: ["precision and craft", "mechanical beauty", "Renaissance humanism", "artistic technology"],
            self.DYSTOPIAN: ["oppression vs freedom", "individual resistance", "social control", "warning message"],
            self.UTOPIAN: ["perfect society", "human potential", "social harmony", "hidden costs"],
            self.POST_APOCALYPTIC: ["survival", "rebuilding civilization", "human resilience", "environmental message"],
            self.POST_NUCLEAR: ["atomic age fears", "radiation horror", "cold war anxiety", "technological hubris"],
            self.ZOMBIE_APOCALYPSE: ["social breakdown", "group dynamics", "survival ethics", "human nature"],
            self.SCIENCE_FANTASY: ["genre blending", "magic and technology", "cosmic adventure", "unlimited possibility"],
            self.NEW_WEIRD: ["genre subversion", "experimental narrative", "strange beauty", "reality questioning"],
            self.SLIPSTREAM: ["reality fluidity", "subtle strangeness", "genre boundaries", "perception questions"],
            self.PARALLEL_UNIVERSE: ["infinite possibilities", "choice consequences", "reality variants", "identity questions"],
            self.MULTIVERSE: ["cosmic scope", "infinite realities", "universal connections", "existence meaning"],
            self.PARANORMAL: ["hidden truth", "supernatural mystery", "psychic abilities", "otherworldly contact"],
            self.SUPERNATURAL: ["spiritual realm", "afterlife mystery", "ghostly presence", "mystical experience"],
            self.GOTHIC_HORROR: ["psychological terror", "atmospheric dread", "past sins", "decay and corruption"],
            self.COSMIC_HORROR: ["human insignificance", "unknowable universe", "existential dread", "cosmic indifference"],
            self.OCCULT: ["hidden knowledge", "secret power", "mystical tradition", "esoteric wisdom"],
            self.ANTHROPOMORPHIC: ["social allegory", "cultural commentary", "human nature", "behavioral satire"],
            self.UNDERWATER: ["environmental exploration", "alien beauty", "pressure adaptation", "oceanic mystery"],
            self.UNDERGROUND: ["hidden civilization", "earth mysteries", "claustrophobia", "buried secrets"],
            self.FLOATING_ISLANDS: ["freedom and height", "aerial beauty", "weather mastery", "sky kingdoms"],
            self.HOLLOW_EARTH: ["inner world mystery", "prehistoric wonder", "exploration spirit", "earth secrets"],
            self.GENERATION_SHIP: ["journey vs destination", "closed society", "generational change", "cosmic voyage"],
            self.TIME_TRAVEL: ["causality", "temporal paradox", "historical change", "time responsibility"],
            self.ALTERNATE_TIMELINE: ["historical what-if", "change consequences", "timeline comparison", "alternate development"],
            self.TIME_LOOP: ["repetition and change", "learning cycle", "temporal prison", "incremental progress"],
            self.WEIRD_WEST: ["frontier justice", "supernatural mystery", "cultural clash", "lawless freedom"],
            self.BIOPUNK_FANTASY: ["evolution and adaptation", "natural vs artificial", "biological harmony", "organic growth"],
            self.CLIMATE_FICTION: ["environmental responsibility", "survival adaptation", "ecological balance", "future consequences"],
        }
        return themes_map.get(self, ["adventure", "discovery", "conflict", "transformation"])

    @classmethod 
    def from_string(cls, value: str) -> 'WorldType':
        """Create WorldType from string with fuzzy matching."""
        value_lower = value.lower().strip()
        
        # Direct value matching
        try:
            return cls(value_lower)
        except ValueError:
            pass
        
        # Fuzzy matching with common synonyms and variations
        # Order matters - more specific matches should come first
        mappings = {
            # Multi-word specific matches first
            "magic realism": cls.MAGICAL_REALISM,
            "magical realism": cls.MAGICAL_REALISM,
            "real world": cls.REALISTIC,
            "realistic fiction": cls.REALISTIC,
            "fantasy world": cls.HIGH_FANTASY,
            "hard sf": cls.HARD_SCIENCE_FICTION,
            "hard sci-fi": cls.HARD_SCIENCE_FICTION,
            "soft sf": cls.SOFT_SCIENCE_FICTION,
            "soft sci-fi": cls.SOFT_SCIENCE_FICTION,
            "sci-fi": cls.SCIENCE_FICTION,
            "science fiction": cls.SCIENCE_FICTION,
            "what if": cls.ALTERNATE_HISTORY,
            "alt history": cls.ALTERNATE_HISTORY,
            "space opera": cls.SPACE_OPERA,
            "time travel": cls.TIME_TRAVEL,
            "other world": cls.PORTAL_FANTASY,
            "gas lamp": cls.GASLAMP_FANTASY,
            "perfect world": cls.UTOPIAN,
            "end times": cls.POST_APOCALYPTIC,
            "inner earth": cls.HOLLOW_EARTH,
            "center earth": cls.HOLLOW_EARTH,
            "talking animals": cls.ANTHROPOMORPHIC,
            
            # Single word matches
            "real": cls.REALISTIC,
            "modern": cls.CONTEMPORARY,
            "present day": cls.CONTEMPORARY,
            "current": cls.CONTEMPORARY,
            "past": cls.HISTORICAL,
            "period": cls.HISTORICAL,
            "historical fiction": cls.HISTORICAL,
            "alternate": cls.ALTERNATE_HISTORY,
            "subtle magic": cls.LOW_FANTASY,
            "hidden magic": cls.LOW_FANTASY,
            "low": cls.LOW_FANTASY,
            "high": cls.HIGH_FANTASY,
            "secondary world fantasy": cls.SECONDARY_WORLD,
            "epic": cls.EPIC_FANTASY,
            "grand fantasy": cls.EPIC_FANTASY,
            "city fantasy": cls.URBAN_FANTASY,
            "modern fantasy": cls.URBAN_FANTASY,
            "dark": cls.DARK_FANTASY,
            "horror fantasy": cls.DARK_FANTASY,
            "grim": cls.GRIMDARK,
            "sword": cls.SWORD_AND_SORCERY,
            "barbarian": cls.SWORD_AND_SORCERY,
            "heroic": cls.HEROIC_FANTASY,
            "knight": cls.MEDIEVAL_FANTASY,
            "medieval": cls.MEDIEVAL_FANTASY,
            "gothic": cls.GOTHIC_FANTASY,
            "fairy": cls.FAIRY_TALE,
            "folk tale": cls.FAIRY_TALE,
            "myth": cls.MYTHIC_FANTASY,
            "mythology": cls.MYTHIC_FANTASY,
            "arthur": cls.ARTHURIAN,
            "camelot": cls.ARTHURIAN,
            "portal": cls.PORTAL_FANTASY,
            "victorian fantasy": cls.GASLAMP_FANTASY,
            "musket": cls.FLINTLOCK_FANTASY,
            "gunpowder": cls.GUNPOWDER_FANTASY,
            "arcane": cls.ARCANE_FANTASY,
            "magitech": cls.ARCANE_FANTASY,
            "future": cls.SCIENCE_FICTION,
            "galactic": cls.SPACE_OPERA,
            "cyber": cls.CYBERPUNK,
            "steam": cls.STEAMPUNK,
            "victorian": cls.STEAMPUNK,
            "diesel": cls.DIESELPUNK,
            "bio": cls.BIOPUNK,
            "genetic": cls.BIOPUNK,
            "clock": cls.CLOCKPUNK,
            "clockwork": cls.CLOCKPUNK,
            "oppressive": cls.DYSTOPIAN,
            "totalitarian": cls.DYSTOPIAN,
            "apocalypse": cls.POST_APOCALYPTIC,
            "nuclear": cls.POST_NUCLEAR,
            "atomic": cls.POST_NUCLEAR,
            "zombie": cls.ZOMBIE_APOCALYPSE,
            "undead": cls.ZOMBIE_APOCALYPSE,
            "sci-fantasy": cls.SCIENCE_FANTASY,
            "weird": cls.NEW_WEIRD,
            "experimental": cls.NEW_WEIRD,
            "slip": cls.SLIPSTREAM,
            "parallel": cls.PARALLEL_UNIVERSE,
            "alternate reality": cls.PARALLEL_UNIVERSE,
            "multi": cls.MULTIVERSE,
            "many worlds": cls.MULTIVERSE,
            "ghost": cls.PARANORMAL,
            "vampire": cls.PARANORMAL,
            "psychic": cls.PARANORMAL,
            "spirit": cls.SUPERNATURAL,
            "otherworldly": cls.SUPERNATURAL,
            "lovecraft": cls.COSMIC_HORROR,
            "cosmic": cls.COSMIC_HORROR,
            "eldritch": cls.COSMIC_HORROR,
            "secret": cls.OCCULT,
            "mystical": cls.OCCULT,
            "animal": cls.ANTHROPOMORPHIC,
            "furry": cls.ANTHROPOMORPHIC,
            "ocean": cls.UNDERWATER,
            "aquatic": cls.UNDERWATER,
            "sea": cls.UNDERWATER,
            "cave": cls.UNDERGROUND,
            "subterranean": cls.UNDERGROUND,
            "sky": cls.FLOATING_ISLANDS,
            "aerial": cls.FLOATING_ISLANDS,
            "flying": cls.FLOATING_ISLANDS,
            "spaceship": cls.GENERATION_SHIP,
            "ship": cls.GENERATION_SHIP,
            "time": cls.TIME_TRAVEL,
            "temporal": cls.TIME_TRAVEL,
            "loop": cls.TIME_LOOP,
            "repeat": cls.TIME_LOOP,
            "western": cls.WEIRD_WEST,
            "cowboy": cls.WEIRD_WEST,
            "frontier": cls.WEIRD_WEST,
            "biological": cls.BIOPUNK_FANTASY,
            "organic": cls.BIOPUNK_FANTASY,
            "climate": cls.CLIMATE_FICTION,
            "environmental": cls.CLIMATE_FICTION,
            "space": cls.SPACE_OPERA,
        }
        
        # Check for partial matches, starting with most specific
        # Special handling for "magic realism" vs "realism" conflict
        if "magic" in value_lower and "realism" in value_lower:
            return cls.MAGICAL_REALISM
            
        for keyword, world_type in mappings.items():
            if keyword in value_lower:
                return world_type
        
        raise ValueError(f"Unknown world type: {value}")

    @classmethod
    def get_fantasy_types(cls) -> List['WorldType']:
        """Get all fantasy-related world types."""
        return [
            cls.LOW_FANTASY, cls.HIGH_FANTASY, cls.EPIC_FANTASY, cls.URBAN_FANTASY,
            cls.DARK_FANTASY, cls.GRIMDARK, cls.SWORD_AND_SORCERY, cls.HEROIC_FANTASY,
            cls.MEDIEVAL_FANTASY, cls.GOTHIC_FANTASY, cls.FAIRY_TALE, cls.MYTHIC_FANTASY,
            cls.ARTHURIAN, cls.PORTAL_FANTASY, cls.SECONDARY_WORLD, cls.MAGICAL_REALISM,
            cls.GASLAMP_FANTASY, cls.FLINTLOCK_FANTASY, cls.GUNPOWDER_FANTASY, cls.ARCANE_FANTASY,
            cls.WEIRD_WEST, cls.BIOPUNK_FANTASY
        ]

    @classmethod
    def get_science_fiction_types(cls) -> List['WorldType']:
        """Get all science fiction-related world types."""
        return [
            cls.SCIENCE_FICTION, cls.HARD_SCIENCE_FICTION, cls.SOFT_SCIENCE_FICTION,
            cls.SPACE_OPERA, cls.CYBERPUNK, cls.STEAMPUNK, cls.DIESELPUNK,
            cls.BIOPUNK, cls.CLOCKPUNK, cls.SCIENCE_FANTASY
        ]

    @classmethod
    def get_realistic_types(cls) -> List['WorldType']:
        """Get all realistic/contemporary world types."""
        return [
            cls.REALISTIC, cls.CONTEMPORARY, cls.HISTORICAL, cls.ALTERNATE_HISTORY,
            cls.CLIMATE_FICTION
        ]

    @classmethod
    def get_high_complexity_types(cls) -> List['WorldType']:
        """Get world types that require extensive world-building."""
        return [world_type for world_type in cls if world_type.world_building_complexity in ["High", "Very High"]]

    @classmethod
    def get_by_theme(cls, theme: str) -> List['WorldType']:
        """Get world types that commonly explore a specific theme."""
        theme_lower = theme.lower()
        matching_types = []
        
        for world_type in cls:
            if any(theme_lower in common_theme.lower() for common_theme in world_type.common_themes):
                matching_types.append(world_type)
        
        return matching_types

    def get_world_building_checklist(self) -> Dict[str, List[str]]:
        """Get a comprehensive world-building checklist for this world type."""
        base_checklist = {
            "Geography & Environment": [
                "Physical landscape and terrain",
                "Climate and weather patterns", 
                "Natural resources and ecology",
                "Key locations and landmarks"
            ],
            "Cultures & Societies": [
                "Social structures and hierarchies",
                "Cultural values and beliefs",
                "Languages and communication",
                "Customs and traditions"
            ],
            "Politics & Governance": [
                "Government systems",
                "Laws and justice systems",
                "International relations",
                "Conflicts and alliances"
            ],
            "Economics & Technology": [
                "Economic systems",
                "Trade and commerce",
                "Technology level",
                "Transportation methods"
            ],
            "History & Timeline": [
                "Major historical events",
                "Important figures",
                "Cultural evolution",
                "Timeline consistency"
            ]
        }
        
        # Add world-type specific elements
        if self in [self.HIGH_FANTASY, self.EPIC_FANTASY, self.SECONDARY_WORLD]:
            base_checklist["Magic Systems"] = [
                "Magic rules and limitations",
                "Magical creatures and beings",
                "Magical institutions",
                "Magic's role in society"
            ]
            base_checklist["Races & Species"] = [
                "Non-human species",
                "Inter-species relations",
                "Racial abilities and traits",
                "Species distribution"
            ]
        
        elif self in self.get_science_fiction_types():
            base_checklist["Technology & Science"] = [
                "Scientific principles",
                "Technological advancement",
                "Space travel capabilities",
                "Communication systems"
            ]
            if self == self.SPACE_OPERA:
                base_checklist["Alien Civilizations"] = [
                    "Alien species design",
                    "Alien cultures and societies",
                    "Inter-species relations",
                    "Galactic politics"
                ]
        
        elif self in [self.URBAN_FANTASY, self.PARANORMAL]:
            base_checklist["Hidden World"] = [
                "Supernatural concealment",
                "Human-supernatural relations",
                "Supernatural governance",
                "Discovery consequences"
            ]
        
        elif self == self.HISTORICAL:
            base_checklist["Historical Accuracy"] = [
                "Period-appropriate technology",
                "Social customs of the era",
                "Historical figure integration",
                "Authentic dialogue and language"
            ]
        
        return base_checklist

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return f"WorldType.{self.name}"