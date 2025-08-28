# enhanced_context_manager.py
from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path
from datetime import datetime

# Import the proper types from your codebase
from musequill.services.backend.writers.chapter_brief_model import GenericChapterBrief
from musequill.services.backend.model import BookModelType
from musequill.services.backend.writers.research_model import RefinedResearch

class NarrativeState:
    """Tracks the evolving state of the narrative across chapters."""
    
    def __init__(self):
        self.character_states: Dict[str, Dict] = {}
        self.plot_threads: List[Dict] = []
        self.world_changes: List[Dict] = []
        self.relationship_matrix: Dict[str, Dict] = {}
        self.active_conflicts: List[Dict] = []
        self.foreshadowing_bank: List[Dict] = []
        self.motif_evolution: Dict[str, List] = {}
        self.chapter_summaries: List[Dict] = []
        
    def update_from_chapter(self, chapter_content: str, chapter_meta: Dict, continuity_data: Dict):
        """Update narrative state based on completed chapter."""
        chapter_num = chapter_meta.get("chapter_number", 0)
        
        # Extract and update character states from continuity data (new format)
        characters_introduced = continuity_data.get("characters_introduced", [])
        characters_developed = continuity_data.get("characters_developed", [])
        all_characters = list(set(characters_introduced + characters_developed))
        
        for char in all_characters:
            if char not in self.character_states:
                self.character_states[char] = {
                    "first_appearance": chapter_num,
                    "development_arc": [],
                    "relationships": {},
                    "current_status": "active"
                }
            
            # Track character development through chapters
            self.character_states[char]["development_arc"].append({
                "chapter": chapter_num,
                "context": f"Chapter {chapter_num} appearance/development",
                "timestamp": datetime.now().isoformat(),
                "introduced": char in characters_introduced,
                "developed": char in characters_developed
            })
        
        # Update plot threads from continuity data
        new_threads = continuity_data.get("new_plot_threads", [])
        advanced_threads = continuity_data.get("plot_threads_advanced", [])
        
        for thread in new_threads:
            thread_entry = {
                "thread": thread,
                "introduced_chapter": chapter_num,
                "status": "active",
                "callbacks": continuity_data.get("callbacks_to_earlier", [])
            }
            if thread_entry not in self.plot_threads:
                self.plot_threads.append(thread_entry)
        
        # Mark advanced threads as recently active
        for thread in advanced_threads:
            for existing_thread in self.plot_threads:
                if thread.lower() in existing_thread["thread"].lower():
                    existing_thread["last_advanced"] = chapter_num
        
        # Store chapter summary with rich context
        self.chapter_summaries.append({
            "chapter": chapter_num,
            "title": chapter_meta.get("chapter_title", ""),
            "summary": chapter_meta.get("summary", ""),
            "key_events": continuity_data.get("key_events", []),
            "character_changes": all_characters,
            "new_threads": new_threads,
            "advanced_threads": advanced_threads,
            "world_changes": continuity_data.get("world_changes", []),
            "word_count": chapter_meta.get("word_count", 0)
        })
    
    def get_contextual_summary(self, target_chapter: int, max_tokens: int = 1500) -> str:
        """Generate a rich contextual summary for the target chapter."""
        
        # Get relevant character arcs
        active_chars = []
        for char_name, char_data in self.character_states.items():
            if any(entry["chapter"] < target_chapter for entry in char_data["development_arc"]):
                recent_development = [e for e in char_data["development_arc"] if e["chapter"] < target_chapter]
                if recent_development:
                    active_chars.append({
                        "name": char_name,
                        "status": char_data["current_status"],
                        "recent_chapters": [e["chapter"] for e in recent_development[-3:]]  # Last 3 appearances
                    })
        
        # Get active plot threads
        active_threads = [
            thread for thread in self.plot_threads 
            if thread["introduced_chapter"] < target_chapter and thread["status"] == "active"
        ]
        
        # Get recent chapter summaries (last 3-5 chapters)
        recent_chapters = [
            ch for ch in self.chapter_summaries 
            if ch["chapter"] < target_chapter and ch["chapter"] >= max(1, target_chapter - 5)
        ]
        
        # Construct rich summary
        context_parts = []
        
        if active_chars:
            char_summary = "**Character Status:**\n"
            for char in active_chars[:5]:  # Limit to top 5 characters
                char_summary += f"- {char['name']}: {char['status']}, appeared in chapters {char['recent_chapters']}\n"
            context_parts.append(char_summary)
        
        if active_threads:
            thread_summary = "**Active Plot Threads:**\n"
            for thread in active_threads[:5]:  # Limit to top 5 threads
                thread_summary += f"- {thread['thread']} (since Ch.{thread['introduced_chapter']})\n"
            context_parts.append(thread_summary)
        
        if recent_chapters:
            recent_summary = "**Recent Developments:**\n"
            for ch in recent_chapters[-3:]:  # Last 3 chapters
                recent_summary += f"- Ch.{ch['chapter']}: {ch['title']} - {ch['summary'][:100]}...\n"
            context_parts.append(recent_summary)
        
        full_context = "\n\n".join(context_parts)
        
        # Truncate if too long (rough token estimation: 1 token ≈ 4 characters)
        if len(full_context) > max_tokens * 4:
            full_context = full_context[:max_tokens * 4] + "..."
        
        return full_context
    
    def save_to_file(self, filepath: str):
        """Persist narrative state to JSON file."""
        data = {
            "character_states": self.character_states,
            "plot_threads": self.plot_threads,
            "world_changes": self.world_changes,
            "relationship_matrix": self.relationship_matrix,
            "active_conflicts": self.active_conflicts,
            "foreshadowing_bank": self.foreshadowing_bank,
            "motif_evolution": self.motif_evolution,
            "chapter_summaries": self.chapter_summaries,
            "last_updated": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'NarrativeState':
        """Load narrative state from JSON file."""
        if not os.path.exists(filepath):
            return cls()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        state = cls()
        state.character_states = data.get("character_states", {})
        state.plot_threads = data.get("plot_threads", [])
        state.world_changes = data.get("world_changes", [])
        state.relationship_matrix = data.get("relationship_matrix", {})
        state.active_conflicts = data.get("active_conflicts", [])
        state.foreshadowing_bank = data.get("foreshadowing_bank", [])
        state.motif_evolution = data.get("motif_evolution", {})
        state.chapter_summaries = data.get("chapter_summaries", [])
        
        return state


class EnhancedContextManager:
    """Enhanced context management for coherent chapter generation."""
    
    def __init__(self, book_id: str, base_dir: str = "manuscript"):
        self.book_id = book_id
        self.base_dir = base_dir
        self.narrative_state = NarrativeState()
        self.state_file = os.path.join(base_dir, f"narrative_state_{book_id}.json")
        
        # Load existing state if available
        if os.path.exists(self.state_file):
            self.narrative_state = NarrativeState.load_from_file(self.state_file)
    
    def build_enhanced_context_pack(
        self,
        book_model: BookModelType,
        book_summary: str,
        constraints: Dict[str, Any],
        research_corpus: RefinedResearch,
        chapter_brief: GenericChapterBrief,
        target_chapter: int,
        prior_chapter_text: Optional[str] = None,
        prior_chapter_summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """Build enhanced context pack with narrative state awareness."""
        
        # Get rich contextual summary from narrative state
        contextual_summary = self.narrative_state.get_contextual_summary(
            target_chapter, max_tokens=1500
        )
        
        # Build traditional context using proper typed objects
        traditional_context = self._build_traditional_context(
            book_model, book_summary, constraints, research_corpus, chapter_brief
        )
        
        # Enhance with narrative continuity
        enhanced_context = traditional_context.copy()
        enhanced_context.update({
            "narrative_continuity": {
                "contextual_summary": contextual_summary,
                "character_states": {
                    name: state for name, state in self.narrative_state.character_states.items()
                    if any(entry["chapter"] < target_chapter for entry in state["development_arc"])
                },
                "active_plot_threads": [
                    thread for thread in self.narrative_state.plot_threads
                    if thread["introduced_chapter"] < target_chapter and thread["status"] == "active"
                ],
                "chapter_progression": [
                    ch for ch in self.narrative_state.chapter_summaries[-5:]
                    if ch["chapter"] < target_chapter
                ]
            },
            "enhanced_research": self._select_relevant_research(
                research_corpus, chapter_brief, self.narrative_state
            )
        })
        
        return enhanced_context
    
    def update_after_chapter_completion(
        self, 
        chapter_content: str, 
        chapter_meta: Dict, 
        continuity_data: Dict
    ):
        """Update narrative state after chapter completion."""
        self.narrative_state.update_from_chapter(chapter_content, chapter_meta, continuity_data)
        self.narrative_state.save_to_file(self.state_file)
    
    def _build_traditional_context(
        self,
        book_model: BookModelType,
        book_summary: str,
        constraints: Dict[str, Any],
        research_corpus: RefinedResearch,
        chapter_brief: GenericChapterBrief
    ) -> Dict[str, Any]:
        """Build the traditional context structure using proper typed objects."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "book_model": book_model,
            "book_summary": book_summary.strip(),
            "constraints": constraints,
            "chapter_brief": chapter_brief,
            "research": research_corpus,
        }
    
    def _select_relevant_research(
        self, 
        research_corpus: RefinedResearch, 
        chapter_brief: GenericChapterBrief,
        narrative_state: NarrativeState
    ) -> Dict[str, Any]:
        """Select research most relevant to current chapter and story state."""
        
        # Get characters and locations mentioned in recent chapters
        recent_characters = set()
        recent_locations = set()
        
        for ch_summary in narrative_state.chapter_summaries[-3:]:  # Last 3 chapters
            recent_characters.update(ch_summary.get("character_changes", []))
            # Extract locations from world_changes if available
            world_changes = ch_summary.get("world_changes", [])
            for change in world_changes:
                # Extract location names from world changes if they contain location info
                if isinstance(change, str) and any(keyword in change.lower() for keyword in ['at', 'in', 'to', 'from']):
                    # This is a simple heuristic - could be more sophisticated
                    words = change.split()
                    for i, word in enumerate(words):
                        if word.lower() in ['at', 'in', 'to', 'from'] and i + 1 < len(words):
                            recent_locations.add(words[i + 1])
        
        # Add current chapter characters/locations from scenes in GenericChapterBrief
        if hasattr(chapter_brief, 'scenes') and chapter_brief.scenes:
            for scene in chapter_brief.scenes:
                # Extract character names from characters_on_stage list
                if hasattr(scene, 'characters_on_stage') and scene.characters_on_stage:
                    # Characters are in a list like ['Noah Bennett & Dr. Ava Kline']
                    for char_entry in scene.characters_on_stage:
                        # Split on '&' and clean up names
                        if '&' in char_entry:
                            chars = [c.strip() for c in char_entry.split('&')]
                            recent_characters.update(chars)
                        else:
                            recent_characters.add(char_entry.strip())
                
                # Extract location from scene
                if hasattr(scene, 'location') and scene.location:
                    recent_locations.add(scene.location)
                else:
                    recent_locations.add(chapter_brief.canon_summary)
                print('WARNIGN: MAY AFFECT THE RESULTS. REMOVE IF POLUTES')
                for x in chapter_brief.dialogue_cues:
                    recent_characters.add(x)
                for x in chapter_brief.chapter_specific_beats:
                    recent_characters.add(x)
        
        # Filter research based on RefinedResearch structure
        relevant_research = {}
        
        # Handle RefinedResearch - check if it has the expected attributes
        if hasattr(research_corpus, 'figures') and research_corpus.figures:
            # Figures are string lists in RefinedResearch
            relevant_figures = []
            for figure_info in research_corpus.figures[:10]:  # Limit to top 10
                # Check if any character name appears in the figure info
                if any(char.lower() in figure_info.lower() for char in recent_characters if char):
                    relevant_figures.append(figure_info)
            if not relevant_figures and research_corpus.figures:
                relevant_figures = research_corpus.figures[:5]  # Default to first 5
            if relevant_figures:
                relevant_research["figures"] = relevant_figures
        
        if hasattr(research_corpus, 'locales') and research_corpus.locales:
            # Locales are string lists in RefinedResearch
            relevant_locales = []
            for locale_info in research_corpus.locales[:10]:  # Limit to top 10
                # Check if any location appears in the locale info
                if any(place.lower() in locale_info.lower() for place in recent_locations if place):
                    relevant_locales.append(locale_info)
            if not relevant_locales and research_corpus.locales:
                relevant_locales = research_corpus.locales[:5]  # Default to first 5
            if relevant_locales:
                relevant_research["locales"] = relevant_locales
        
        # Keep topics for general context
        if hasattr(research_corpus, 'topics') and research_corpus.topics:
            relevant_research["topics"] = research_corpus.topics[:5]  # Limit to top 5
        
        return relevant_research
    
    def extract_chapter_context_hints(self, chapter_brief: GenericChapterBrief) -> Dict[str, Any]:
        """Extract contextual hints from the chapter brief for better context building."""
        
        context_hints = {
            "characters": set(),
            "locations": set(),
            "themes": [],
            "motifs": [],
            "beats": [],
            "constraints": {},
            "dialogue_cues": [],
            "sensory_palette": {},
            "act_context": []
        }
        
        # Extract characters from scenes
        if hasattr(chapter_brief, 'scenes') and chapter_brief.scenes:
            for scene in chapter_brief.scenes:
                if hasattr(scene, 'characters_on_stage') and scene.characters_on_stage:
                    # Handle character format like ['Noah Bennett & Dr. Ava Kline']
                    for char_entry in scene.characters_on_stage:
                        if '&' in char_entry:
                            chars = [c.strip() for c in char_entry.split('&')]
                            context_hints["characters"].update(chars)
                        else:
                            context_hints["characters"].add(char_entry.strip())
                
                # Extract locations
                if hasattr(scene, 'location') and scene.location:
                    context_hints["locations"].add(scene.location)
                
                # Extract thematic elements from scenes
                if hasattr(scene, 'thematic_element') and scene.thematic_element:
                    context_hints["themes"].append(scene.thematic_element)
                
                # Extract act context
                if hasattr(scene, 'act_context') and scene.act_context:
                    context_hints["act_context"].append(scene.act_context)
        
        # Extract narrative beats
        if hasattr(chapter_brief, 'narrative_beats') and chapter_brief.narrative_beats:
            context_hints["beats"].extend(chapter_brief.narrative_beats)
        
        if hasattr(chapter_brief, 'chapter_specific_beats') and chapter_brief.chapter_specific_beats:
            context_hints["beats"].extend(chapter_brief.chapter_specific_beats)
        
        if hasattr(chapter_brief, 'act_turning_points') and chapter_brief.act_turning_points:
            context_hints["beats"].extend(chapter_brief.act_turning_points)
        
        # Extract motifs
        if hasattr(chapter_brief, 'motifs') and chapter_brief.motifs:
            context_hints["motifs"].extend(chapter_brief.motifs)
        
        if hasattr(chapter_brief, 'act_motifs') and chapter_brief.act_motifs:
            context_hints["motifs"].extend(chapter_brief.act_motifs)
        
        # Extract dialogue cues
        if hasattr(chapter_brief, 'dialogue_cues') and chapter_brief.dialogue_cues:
            context_hints["dialogue_cues"] = chapter_brief.dialogue_cues
        
        # Extract sensory palette
        if hasattr(chapter_brief, 'sensory_palette') and chapter_brief.sensory_palette:
            palette = chapter_brief.sensory_palette
            context_hints["sensory_palette"] = {
                "sight": getattr(palette, 'sight', []),
                "sound": getattr(palette, 'sound', []),
                "smell": getattr(palette, 'smell', []),
                "touch": getattr(palette, 'touch', [])
            }
        
        # Extract constraints from the brief
        if hasattr(chapter_brief, 'constraints') and chapter_brief.constraints:
            constraints = chapter_brief.constraints
            context_hints["constraints"] = {}
            
            if hasattr(constraints, 'pov') and constraints.pov:
                context_hints["constraints"]["pov"] = {
                    "type": getattr(constraints.pov, 'type', None),
                    "rule": getattr(constraints.pov, 'rule', None)
                }
            
            if hasattr(constraints, 'tone'):
                context_hints["constraints"]["tone"] = constraints.tone
                
            if hasattr(constraints, 'pace'):
                context_hints["constraints"]["pace"] = constraints.pace
                
            if hasattr(constraints, 'safety') and constraints.safety:
                safety = constraints.safety
                context_hints["constraints"]["safety"] = {
                    "peril_level": getattr(safety, 'peril_level', None),
                    "content_warnings": getattr(safety, 'content_warnings', [])
                }
        
        # Extract meta information
        if hasattr(chapter_brief, 'meta') and chapter_brief.meta:
            meta = chapter_brief.meta
            context_hints["meta"] = {
                "theme": getattr(meta, 'theme', None),
                "logline": getattr(meta, 'logline', None),
                "act": getattr(meta, 'act', None),
                "act_description": getattr(meta, 'act_description', None)
            }
        
        # Convert sets to lists for JSON serialization
        context_hints["characters"] = list(context_hints["characters"])
        context_hints["locations"] = list(context_hints["locations"])
        
        return context_hints


def create_enhanced_context_manager(book_id: str, base_dir: str = "manuscript") -> EnhancedContextManager:
    """Factory function to create enhanced context manager."""
    return EnhancedContextManager(book_id, base_dir)