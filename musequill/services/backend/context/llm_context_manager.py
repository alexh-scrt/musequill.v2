#!/usr/bin/env python3
"""
LLMContextManager - Core Implementation

Manages content storage and retrieval across Redis (raw/exact) and ChromaDB (vector) backends.
Supports pluggable metadata generation and content parsing modules.

Key Features:
- Constructor injection for clean dependency management
- Explicit storage control (as_vector parameter)
- Unified retrieval with automatic backend routing
- LLM-generated metadata with strict validation + fallback
- Simple concatenation results for caller assembly
"""

import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timezone
from musequill.services.backend.model import (
    BookModelType
)

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Container for retrieval results with metadata."""
    vector_results: List[str]
    exact_results: List[str] 
    total_tokens: int
    content_sources: List[Dict[str, Any]]


class MetadataGenerator(ABC):
    """Abstract interface for metadata generation modules."""
    
    @abstractmethod
    def generate_metadata(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """
        Generate metadata for content using LLM or other methods.
        
        Args:
            content: Raw content to analyze
            content_type: Hint about content type for better analysis
            book_id: Book identifier for context
            
        Returns:
            Complete metadata dictionary following universal schema
        """
        pass


class ContentParser(ABC):
    """Abstract interface for content parsing modules."""
    
    @abstractmethod
    def parse_content(self, raw_content: str, content_format: str) -> str:
        """
        Parse and normalize content from various formats.
        
        Args:
            raw_content: Original content string
            content_format: Format type (json|markdown|text)
            
        Returns:
            Parsed and normalized content string
        """
        pass


class LLMContextManager:
    """
    Core context manager for storing and retrieving content across dual backends.
    
    Supports Redis for exact/raw storage and ChromaDB for vector/semantic storage.
    Uses pluggable modules for metadata generation and content parsing.
    """
    
    def __init__(self, 
                 redis_store,
                 vector_store, 
                 metadata_generator: MetadataGenerator,
                 content_parser: ContentParser):
        """
        Initialize LLMContextManager with injected dependencies.
        
        Args:
            redis_store: Configured Redis client for exact storage
            vector_store: Configured ChromaDB client/collection for vector storage
            metadata_generator: Plugin for generating content metadata
            content_parser: Plugin for parsing content formats
        """
        self.redis_store = redis_store
        self.vector_store = vector_store
        self.metadata_generator = metadata_generator
        self.content_parser = content_parser
        
        # Fallback metadata template for error cases
        self.fallback_metadata = {
            "content_type": "unknown",
            "content_subtype": "unclassified", 
            "chapter_relevance": "all",
            "priority": "supporting",
            "quality_score": 50,
            "key_concepts": ["unprocessed"],
            "usage_context": "reference"
        }
        
        logger.info("LLMContextManager initialized with pluggable modules")
    
    async def store(self,
            book_id: str,
            content_id: str, 
            content: str, 
            metadata: BookModelType,
            as_vector: bool = False) -> bool:
        """
        Store content with explicit storage strategy control.
        
        Args:
            content_id: Unique identifier for content
            content: Raw content to store (JSON/Markdown/Text)
            metadata: Optional pre-generated metadata (if None, will generate via LLM)
            as_vector: True = ChromaDB + Redis metadata, False = Redis only
            content_type: Hint for metadata generation
            book_id: Book identifier for organization
            
        Returns:
            True if storage successful, False otherwise
        """
        try:
            # Generate metadata if not provided
            # if metadata is None:
            #     metadata = await self._generate_metadata_with_fallback(content, content_type, book_id)
            
            # # Add system-generated metadata fields
            # complete_metadata = self._enrich_metadata(metadata, content_id, content, book_id)
            
            # Parse content if needed
            parsed_content = self._parse_content(content, "text")
            
            # Execute storage strategy
            if as_vector:
                return self._store_vector_content(book_id, content_id, parsed_content, metadata)
            else:
                return self._store_raw_content(book_id, content_id, parsed_content, metadata)
                
        except Exception as e:
            logger.error(f"Failed to store content {content_id}: {e}")
            return False
    
    def retrieve(self,
                 query: Optional[str] = None,
                 exact_ids: Optional[List[str]] = None,
                 filters: Optional[Dict[str, Any]] = None,
                 token_limit: Optional[int] = None) -> RetrievalResult:
        """
        Unified retrieval with automatic backend routing.
        
        Args:
            query: Semantic search query (triggers ChromaDB vector search)
            exact_ids: List of content IDs for exact lookup (triggers Redis)
            filters: Metadata filters for both backends
            token_limit: Maximum tokens to return (applies truncation)
            
        Returns:
            RetrievalResult with vector_results, exact_results, and token info
        """
        vector_results = []
        exact_results = []
        content_sources = []
        
        try:
            # Execute vector search if query provided
            if query:
                vector_data = self._search_vector_content(query, filters)
                vector_results = [item["content"] for item in vector_data]
                content_sources.extend([{
                    "source": "vector",
                    "content_id": item.get("content_id", "unknown"),
                    "score": item.get("score", 0.0)
                } for item in vector_data])
            
            # Execute exact lookup if IDs provided  
            if exact_ids:
                exact_data = self._get_exact_content(exact_ids, filters)
                exact_results = [item["content"] for item in exact_data]
                content_sources.extend([{
                    "source": "exact", 
                    "content_id": item["content_id"],
                    "score": 1.0
                } for item in exact_data])
            
            # Apply token limit if specified
            if token_limit:
                vector_results, exact_results = self._apply_token_limit(
                    vector_results, exact_results, token_limit
                )
            
            total_tokens = self._estimate_total_tokens(vector_results + exact_results)
            
            return RetrievalResult(
                vector_results=vector_results,
                exact_results=exact_results, 
                total_tokens=total_tokens,
                content_sources=content_sources
            )
            
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return RetrievalResult([], [], 0, [])
    
    def get(self, content_id: str) -> Optional[Dict[str, Any]]:
        """
        Simple exact retrieval by content ID.
        
        Args:
            content_id: Unique content identifier
            
        Returns:
            Content dict with content and metadata, or None if not found
        """
        try:
            # Try Redis first (faster)
            redis_key = f"content:{content_id}"
            redis_data = self.redis_store.get(redis_key)
            
            if redis_data:
                return json.loads(redis_data)
            
            # Try ChromaDB if not in Redis
            vector_results = self.vector_store.get(ids=[content_id])
            if vector_results and vector_results.get("documents"):
                return {
                    "content_id": content_id,
                    "content": vector_results["documents"][0],
                    "metadata": vector_results.get("metadatas", [{}])[0]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get content {content_id}: {e}")
            return None
    
    def delete(self, content_id: str) -> bool:
        """
        Remove content from appropriate backend(s).
        
        Args:
            content_id: Unique content identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            success = True
            
            # Delete from Redis
            redis_key = f"content:{content_id}"
            self.redis_store.delete(redis_key)
            
            # Delete from ChromaDB (if exists)
            try:
                self.vector_store.delete(ids=[content_id])
            except Exception as e:
                logger.warning(f"ChromaDB deletion failed for {content_id}: {e}")
                # Don't fail overall deletion if vector delete fails
            
            logger.info(f"Content {content_id} deleted successfully")
            return success
            
        except Exception as e:
            logger.error(f"Failed to delete content {content_id}: {e}")
            return False
    
    # === PRIVATE HELPER METHODS ===
    
    async def _generate_metadata_with_fallback(self, content: str, content_type: str, book_id: str) -> Dict[str, Any]:
        """Generate metadata with strict validation and fallback."""
        try:
            # Attempt LLM metadata generation
            metadata = await self.metadata_generator.generate_metadata(content, content_type, book_id)
            
            # Strict validation
            if self._validate_metadata(metadata):
                return metadata
            else:
                logger.warning(f"Invalid metadata generated, using fallback")
                return self.fallback_metadata.copy()
                
        except Exception as e:
            logger.error(f"Metadata generation failed: {e}, using fallback")
            return self.fallback_metadata.copy()
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> bool:
        """Validate metadata against required schema."""
        required_fields = [
            "content_type", "content_subtype", "chapter_relevance", 
            "priority", "quality_score", "key_concepts", "usage_context"
        ]
        
        for field in required_fields:
            if field not in metadata:
                return False
        
        # Validate specific field constraints
        if metadata["priority"] not in ["essential", "important", "supporting"]:
            return False
            
        if not isinstance(metadata["quality_score"], (int, float)) or not (0 <= metadata["quality_score"] <= 100):
            return False
            
        return True
    
    def _enrich_metadata(self, metadata: Dict[str, Any], content_id: str, content: str, book_id: str) -> Dict[str, Any]:
        """Add system-generated metadata fields."""
        enriched = metadata.copy()
        enriched.update({
            "content_id": content_id,
            "book_id": book_id,
            "format": self._detect_format(content),
            "token_estimate": self._estimate_tokens(content),
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        return enriched
    
    def _parse_content(self, content: str, content_format: str) -> str:
        """Parse content using configured parser."""
        try:
            return self.content_parser.parse_content(content, content_format)
        except Exception as e:
            logger.warning(f"Content parsing failed: {e}, using raw content")
            return content
    
    def _store_vector_content(self, book_id:str, content_id: str, content: str, metadata: BookModelType) -> bool:
        """Store content in both ChromaDB and Redis."""
        try:
            # Store in ChromaDB for vector search
            self.vector_store.add(
                documents=[content],
                metadatas=[metadata],
                ids=[book_id, content_id]
            )
            
            # Store metadata in Redis for fast access
            redis_key = f"content:{content_id}"
            redis_data = {
                "book_id": book_id,
                "content_id": content_id,
                "content": content,
                "metadata": metadata.model_dump(),
                "storage_type": "vector"
            }
            self.redis_store.setex(redis_key, 86400, json.dumps(redis_data))  # 24h TTL
            
            logger.info(f"Vector content {content_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Vector storage failed for {content_id}: {e}")
            return False
    
    def _store_raw_content(self, book_id:str, content_id: str, content: str, metadata: BookModelType) -> bool:
        """Store content in Redis only."""
        try:
            redis_key = f"content:{content_id}"
            redis_data = {
                "book_id": book_id,
                "content_id": content_id,
                "content": content,
                "metadata": metadata.model_dump(),
                "storage_type": "raw"
            }
            self.redis_store.set(redis_key, json.dumps(redis_data))
            
            logger.info(f"Raw content {content_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Raw storage failed for {content_id}: {e}")
            return False
    
    def _search_vector_content(self, query: str, filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search ChromaDB with optional metadata filters."""
        try:
            # Convert filters to ChromaDB format if provided
            where_clause = None
            if filters:
                where_clause = self._build_chromadb_filters(filters)
            
            results = self.vector_store.query(
                query_texts=[query],
                n_results=10,  # Reasonable default
                where=where_clause
            )
            
            # Format results
            formatted_results = []
            if results.get("documents") and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "content_id": results["ids"][0][i] if results.get("ids") else f"unknown_{i}",
                        "score": 1.0 - results["distances"][0][i] if results.get("distances") else 0.8,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    def _get_exact_content(self, content_ids: List[str], filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get exact content from Redis with optional filtering."""
        results = []
        
        for content_id in content_ids:
            try:
                redis_key = f"content:{content_id}"
                redis_data = self.redis_store.get(redis_key)
                
                if redis_data:
                    data = json.loads(redis_data)
                    
                    # Apply filters if provided
                    if filters and not self._matches_filters(data.get("metadata", {}), filters):
                        continue
                    
                    results.append({
                        "content": data.get("content", ""),
                        "content_id": content_id,
                        "metadata": data.get("metadata", {})
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to retrieve {content_id}: {e}")
        
        return results
    
    def _apply_token_limit(self, vector_results: List[str], exact_results: List[str], token_limit: int) -> tuple:
        """Apply token limit by truncating results."""
        current_tokens = 0
        limited_vector = []
        limited_exact = []
        
        # Prioritize exact results first
        for content in exact_results:
            content_tokens = self._estimate_tokens(content)
            if current_tokens + content_tokens <= token_limit:
                limited_exact.append(content)
                current_tokens += content_tokens
            else:
                break
        
        # Add vector results if tokens remaining
        for content in vector_results:
            content_tokens = self._estimate_tokens(content) 
            if current_tokens + content_tokens <= token_limit:
                limited_vector.append(content)
                current_tokens += content_tokens
            else:
                break
        
        return limited_vector, limited_exact
    
    def _build_chromadb_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Convert generic filters to ChromaDB where clause format."""
        # Simple implementation - can be enhanced based on ChromaDB capabilities
        where_clause = {}
        
        for key, value in filters.items():
            if isinstance(value, list):
                where_clause[key] = {"$in": value}
            else:
                where_clause[key] = value
        
        return where_clause
    
    def _matches_filters(self, metadata: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if metadata matches provided filters."""
        for key, expected in filters.items():
            if key not in metadata:
                return False
            
            actual = metadata[key]
            
            if isinstance(expected, list):
                # Handle list filtering (e.g., chapter_relevance: [1, 3, 5])
                if isinstance(actual, list):
                    if not any(item in expected for item in actual):
                        return False
                elif actual not in expected and actual != "all":
                    return False
            else:
                if actual != expected:
                    return False
        
        return True
    
    def _detect_format(self, content: str) -> str:
        """Simple format detection."""
        content = content.strip()
        if content.startswith('{') and content.endswith('}'):
            return "json"
        elif '#' in content or '*' in content or '`' in content:
            return "markdown"
        else:
            return "text"
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 0.75 words)."""
        words = len(text.split())
        return int(words * 1.33)
    
    def _estimate_total_tokens(self, content_list: List[str]) -> int:
        """Estimate total tokens for list of content."""
        return sum(self._estimate_tokens(content) for content in content_list)