
import chromadb
from chromadb.config import Settings
from chromadb.api.models.Collection import Collection
from chromadb.errors import ChromaError
import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
import uuid
import time
import re
import hashlib
from contextlib import contextmanager
from urllib.parse import urlparse


from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
LANGCHAIN_AVAILABLE = True

from .chromadb_config import ChromaDbConfig  # Adjust import path as needed


logger = logging.getLogger(__name__)


@dataclass
class EmbeddingModelInfo:
    """Information about embedding models and their dimensions."""
    name: str
    dimensions: int
    description: str


class ChromaDBClient:
    """
    ChromaDB client wrapper that provides collection management, embedding operations,
    and seamless integration with Ollama embeddings.
    """
    
    # Supported embedding models and their dimensions
    EMBEDDING_MODELS = {
        'nomic-embed-text': EmbeddingModelInfo('nomic-embed-text', 768, 'Nomic Embed Text - General purpose'),
        'mxbai-embed-large': EmbeddingModelInfo('mxbai-embed-large', 1024, 'MXBAI Large - High performance'),
        'all-minilm': EmbeddingModelInfo('all-minilm', 384, 'All MiniLM - Lightweight'),
        'text-embedding-ada-002': EmbeddingModelInfo('text-embedding-ada-002', 1536, 'OpenAI Ada-002'),
        'text-embedding-3-small': EmbeddingModelInfo('text-embedding-3-small', 1536, 'OpenAI 3 Small'),
        'text-embedding-3-large': EmbeddingModelInfo('text-embedding-3-large', 3072, 'OpenAI 3 Large'),
    }
    
    def __init__(self, config: ChromaDbConfig):
        """
        Initialize ChromaDB client with configuration.
        
        Args:
            config: ChromaDbConfig instance with ChromaDB connection settings
        """
        self.config = config
        self._client: Optional[chromadb.HttpClient] = None
        self._collection: Optional[Collection] = None
        self._embeddings: Optional[OllamaEmbeddings] = None
        self._text_splitter: Optional[RecursiveCharacterTextSplitter] = None
        self._is_connected = False
        
        # Content tracking for deduplication
        self.content_hashes: set = set()
        
        # Get embedding model info
        self.embedding_model_info = self.EMBEDDING_MODELS.get(
            config.embedding_model,
            EmbeddingModelInfo(config.embedding_model, config.embedding_dimensions, 'Custom model')
        )
        
    def connect(self) -> None:
        """
        Establish connection to ChromaDB server and initialize embeddings.
        
        Raises:
            ConnectionError: If unable to connect to ChromaDB server
            RuntimeError: If Ollama embeddings are not available
        """
        try:
            # Initialize ChromaDB client
            self._client = chromadb.HttpClient(
                host=self.config.chroma_host,
                port=self.config.chroma_port,
                settings=Settings(
                    chroma_server_authn_credentials=None,
                    chroma_server_authn_provider=None
                )
            )
            
            # Test the connection
            self._client.heartbeat()
            self._is_connected = True
            
            logger.info(
                f"Successfully connected to ChromaDB at {self.config.chroma_host}:{self.config.chroma_port}"
            )
            
            # Initialize Ollama embeddings
            if LANGCHAIN_AVAILABLE:
                self._embeddings = OllamaEmbeddings(
                    model=self.config.embedding_model,
                    base_url=self.config.ollama_base_url
                )
                logger.info(f"Ollama embeddings initialized with model: {self.config.embedding_model}")
                
                # Initialize text splitter
                self._text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.config.chunk_size,
                    chunk_overlap=self.config.chunk_overlap,
                    separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
                )
                logger.info(f"Text splitter initialized with chunk_size={self.config.chunk_size}, overlap={self.config.chunk_overlap}")
            else:
                logger.warning("LangChain not available - embeddings and text splitting will need to be provided manually")
            
            # Initialize collection
            self._collection = self._get_or_create_collection()
            
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            self._is_connected = False
            raise ConnectionError(f"Could not connect to ChromaDB: {e}")
    
    def disconnect(self) -> None:
        """Close ChromaDB connection and cleanup resources."""
        try:
            self._client = None
            self._collection = None
            self._embeddings = None
            self._text_splitter = None
            self._is_connected = False
            self.content_hashes.clear()
            logger.info("ChromaDB connection closed")
            
        except Exception as e:
            logger.error(f"Error during ChromaDB disconnect: {e}")
    
    def is_connected(self) -> bool:
        """
        Check if ChromaDB client is connected and responsive.
        
        Returns:
            bool: True if connected and responsive, False otherwise
        """
        if not self._is_connected or not self._client:
            return False
            
        try:
            self._client.heartbeat()
            return True
        except Exception:
            self._is_connected = False
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check.
        
        Returns:
            Dict containing health check results
        """
        health_info = {
            'connected': False,
            'heartbeat_successful': False,
            'collection_accessible': False,
            'embedding_model': self.config.embedding_model,
            'collection_name': self.config.chroma_collection_name,
            'collection_count': None,
            'error': None
        }
        
        try:
            if self.is_connected():
                health_info['connected'] = True
                health_info['heartbeat_successful'] = True
                
                if self._collection:
                    health_info['collection_accessible'] = True
                    health_info['collection_count'] = self._collection.count()
                else:
                    health_info['error'] = 'Collection not initialized'
            else:
                health_info['error'] = 'Not connected to ChromaDB'
                
        except Exception as e:
            health_info['error'] = str(e)
            logger.error(f"ChromaDB health check failed: {e}")
            
        return health_info
    
    @property
    def client(self) -> chromadb.HttpClient:
        """
        Get the underlying ChromaDB client instance.
        
        Returns:
            chromadb.HttpClient: The ChromaDB client instance
            
        Raises:
            ConnectionError: If not connected to ChromaDB
        """
        if not self._client or not self.is_connected():
            raise ConnectionError("ChromaDB client is not connected. Call connect() first.")
        return self._client
    
    @property
    def collection(self) -> Collection:
        """
        Get the ChromaDB collection instance.
        
        Returns:
            Collection: The ChromaDB collection instance
            
        Raises:
            ConnectionError: If not connected or collection not initialized
        """
        if not self._collection:
            raise ConnectionError("ChromaDB collection is not initialized. Call connect() first.")
        return self._collection
    
    def _get_or_create_collection(self) -> Collection:
        """
        Get existing collection or create new one, handling dimension mismatches.
        
        Returns:
            Collection: ChromaDB collection instance
        """
        collection_name = self.config.chroma_collection_name
        
        try:
            # Try to get existing collection
            collection = self.client.get_collection(name=collection_name)
            
            # Check if collection metadata indicates a different embedding model
            collection_metadata = collection.metadata or {}
            stored_model = collection_metadata.get('embedding_model', 'unknown')
            stored_dims = collection_metadata.get('embedding_dimensions')
            
            expected_dims = self.embedding_model_info.dimensions
            
            # If dimensions don't match, recreate collection
            if stored_dims and stored_dims != expected_dims:
                logger.warning(
                    f"Collection '{collection_name}' expects {stored_dims}D embeddings "
                    f"(model: {stored_model}), but current model '{self.config.embedding_model}' "
                    f"produces {expected_dims}D embeddings. Recreating collection."
                )
                
                # Delete and recreate
                self.client.delete_collection(name=collection_name)
                collection = self._create_new_collection()
            else:
                logger.info(f"Using existing collection '{collection_name}' with model: {stored_model}")
            
            return collection
            
        except Exception as e:
            # Collection doesn't exist, create new one
            logger.info(f"Creating new collection '{collection_name}': {e}")
            return self._create_new_collection()
    
    def _create_new_collection(self) -> Collection:
        """Create a new ChromaDB collection with proper metadata."""
        collection_name = self.config.chroma_collection_name
        
        metadata = {
            "description": "Research materials collection",
            "embedding_model": self.config.embedding_model,
            "embedding_dimensions": self.embedding_model_info.dimensions,
            "tenant": self.config.chroma_tenant,
            "database": self.config.chroma_database,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "chunk_size": self.config.chunk_size,
            "chunk_overlap": self.config.chunk_overlap,
        }
        
        collection = self.client.create_collection(
            name=collection_name,
            metadata=metadata
        )
        
        logger.info(
            f"Created new collection '{collection_name}' for {self.config.embedding_model} "
            f"({self.embedding_model_info.dimensions}D embeddings)"
        )
        
        return collection
    
    def recreate_collection(self, force: bool = False) -> Collection:
        """
        Recreate the collection (deletes existing data).
        
        Args:
            force: If True, skip confirmation prompts
            
        Returns:
            Collection: New collection instance
        """
        collection_name = self.config.chroma_collection_name
        
        if not force:
            logger.warning(f"This will delete all data in collection '{collection_name}'")
        
        try:
            # Delete existing collection
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection: {collection_name}")
        except Exception as e:
            logger.info(f"Collection {collection_name} doesn't exist or couldn't be deleted: {e}")
        
        # Create new collection
        self._collection = self._create_new_collection()
        return self._collection
    
    # Embedding operations
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List[float]: Embedding vector
            
        Raises:
            RuntimeError: If embeddings are not available
        """
        if not self._embeddings:
            raise RuntimeError("Ollama embeddings not available. Install langchain-community.")
        
        try:
            embeddings = self._embeddings.embed_query(text)
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        if not self._embeddings:
            raise RuntimeError("Ollama embeddings not available. Install langchain-community.")
        
        try:
            embeddings = self._embeddings.embed_documents(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    # Text processing operations
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into chunks using RecursiveCharacterTextSplitter.
        
        Args:
            text: Text to split into chunks
            
        Returns:
            List[str]: List of text chunks
            
        Raises:
            RuntimeError: If text splitter is not available
        """
        if not self._text_splitter:
            raise RuntimeError("Text splitter not available. Install langchain-text-splitters.")
        
        try:
            chunks = self._text_splitter.split_text(text)
            
            # Filter chunks by minimum size
            filtered_chunks = [
                chunk for chunk in chunks 
                if len(chunk.strip()) >= self.config.min_chunk_size
            ]
            
            if self.config.log_chunk_details:
                logger.info(f"Split text into {len(filtered_chunks)} chunks (filtered from {len(chunks)})")
            
            return filtered_chunks
            
        except Exception as e:
            logger.error(f"Failed to split text: {e}")
            raise
    
    def split_documents(self, documents: List[str]) -> List[str]:
        """
        Split multiple documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List[str]: List of all chunks from all documents
        """
        all_chunks = []
        
        for i, doc in enumerate(documents):
            try:
                chunks = self.split_text(doc)
                all_chunks.extend(chunks)
                
                if self.config.log_chunk_details:
                    logger.info(f"Document {i+1}: {len(chunks)} chunks")
                    
            except Exception as e:
                logger.error(f"Failed to split document {i+1}: {e}")
                continue
        
        logger.info(f"Split {len(documents)} documents into {len(all_chunks)} total chunks")
        return all_chunks
    
    def calculate_content_quality_score(self, text: str) -> float:
        """
        Calculate content quality score for a text chunk.
        
        Args:
            text: Text chunk to evaluate
            
        Returns:
            float: Quality score between 0.0 and 1.0
        """
        if not text or not text.strip():
            return 0.0
        
        score = 0.0
        chunk_text = text.strip()
        
        # Length score (prefer substantial chunks)
        if len(chunk_text) >= self.config.min_chunk_size:
            score += 0.2
        if len(chunk_text) >= self.config.chunk_size * 0.5:
            score += 0.1
        
        # Sentence structure score
        sentences = re.split(r'[.!?]+', chunk_text)
        if len(sentences) >= 2:
            score += 0.2
        
        # Word diversity score
        words = chunk_text.lower().split()
        unique_words = set(words)
        if len(words) > 0:
            diversity_ratio = len(unique_words) / len(words)
            score += diversity_ratio * 0.2
        
        # Avoid low-content patterns
        if not re.search(r'\b(click here|subscribe|buy now|free trial)\b', chunk_text.lower()):
            score += 0.1
        
        # Check for meaningful content indicators
        if re.search(r'\b(research|study|analysis|data|evidence|conclusion)\b', chunk_text.lower()):
            score += 0.1
        
        # Sentence completion score
        if chunk_text.endswith(('.', '!', '?')):
            score += 0.1
        
        return min(1.0, score)
    
    def _get_content_hash(self, text: str) -> str:
        """Generate hash for content deduplication."""
        # Normalize text for hashing
        normalized = re.sub(r'\s+', ' ', text.strip().lower())
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def _is_duplicate_content(self, text: str, similarity_threshold: float = None) -> bool:
        """
        Check if content is duplicate based on hash and similarity.
        
        Args:
            text: Text to check
            similarity_threshold: Similarity threshold (uses config default if None)
            
        Returns:
            bool: True if content is considered duplicate
        """
        if not self.config.filter_duplicate_content:
            return False
        
        content_hash = self._get_content_hash(text)
        
        # Check exact hash match
        if content_hash in self.content_hashes:
            return True
        
        # Add to hash set for future checks
        self.content_hashes.add(content_hash)
        return False
    
    # Enhanced document operations with text processing
    
    def add_text_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
        split_documents: bool = True,
        filter_quality: bool = True,
        filter_duplicates: bool = True
    ) -> List[str]:
        """
        Add text documents with automatic chunking and quality filtering.
        
        Args:
            texts: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents (auto-generated if not provided)
            split_documents: Whether to split documents into chunks
            filter_quality: Whether to apply quality filtering
            filter_duplicates: Whether to filter duplicate content
            
        Returns:
            List[str]: Document IDs that were added
        """
        if not texts:
            return []
        
        # Process texts
        if split_documents:
            processed_texts = []
            processed_metadatas = []
            processed_ids = []
            
            for i, text in enumerate(texts):
                chunks = self.split_text(text)
                
                # Get metadata for this document
                base_metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                base_id = ids[i] if ids and i < len(ids) else str(uuid.uuid4())
                
                for j, chunk in enumerate(chunks):
                    # Apply quality filtering
                    if filter_quality:
                        quality_score = self.calculate_content_quality_score(chunk)
                        if quality_score < self.config.min_content_quality_score:
                            continue
                    
                    # Apply duplicate filtering
                    if filter_duplicates and self._is_duplicate_content(chunk):
                        continue
                    
                    # Create chunk metadata
                    chunk_metadata = base_metadata.copy()
                    chunk_metadata.update({
                        'document_index': i,
                        'chunk_index': j,
                        'chunk_size': len(chunk),
                        'quality_score': self.calculate_content_quality_score(chunk) if filter_quality else None,
                        'parent_document_id': base_id
                    })
                    
                    processed_texts.append(chunk)
                    processed_metadatas.append(chunk_metadata)
                    processed_ids.append(f"{base_id}_chunk_{j}")
            
            logger.info(f"Processed {len(texts)} documents into {len(processed_texts)} chunks")
            
        else:
            processed_texts = texts
            processed_metadatas = metadatas or [{} for _ in texts]
            processed_ids = ids or [str(uuid.uuid4()) for _ in texts]
        
        # Add processed documents
        return self.add_documents(
            documents=processed_texts,
            metadatas=processed_metadatas,
            ids=processed_ids
        )
    
    def add_research_content(
        self,
        content: str,
        source_url: str,
        title: str = "",
        research_id: str = "",
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Add research content with automatic processing and metadata enrichment.
        
        Args:
            content: Research content text
            source_url: Source URL
            title: Content title
            research_id: Research session ID
            additional_metadata: Additional metadata to include
            
        Returns:
            List[str]: Chunk IDs that were added
        """
        # Truncate content if too long
        if len(content) > self.config.max_content_length:
            content = content[:self.config.max_content_length]
            logger.warning(f"Truncated content to {self.config.max_content_length} characters")
        
        # Create base metadata
        metadata = {
            'source_url': source_url,
            'title': title,
            'research_id': research_id,
            'content_length': len(content),
            'timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            'source_domain': urlparse(source_url).geturl() if source_url else None,
        }
        
        if additional_metadata:
            metadata.update(additional_metadata)
        
        # Add with processing
        return self.add_text_documents(
            texts=[content],
            metadatas=[metadata],
            split_documents=True,
            filter_quality=self.config.enable_content_filtering,
            filter_duplicates=self.config.filter_duplicate_content
        )
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None
    ) -> List[str]:
        """
        Add documents to the collection.
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents (auto-generated if not provided)
            embeddings: Optional pre-computed embeddings
            
        Returns:
            List[str]: Document IDs that were added
        """
        if not documents:
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        # Generate embeddings if not provided
        if embeddings is None:
            if self._embeddings:
                embeddings = self.embed_texts(documents)
            else:
                raise RuntimeError("No embeddings provided and Ollama embeddings not available")
        
        # Ensure metadatas is provided
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        # Add documents in batches
        batch_size = self.config.batch_size
        added_ids = []
        
        for i in range(0, len(documents), batch_size):
            batch_end = min(i + batch_size, len(documents))
            batch_docs = documents[i:batch_end]
            batch_metas = metadatas[i:batch_end]
            batch_ids = ids[i:batch_end]
            batch_embeddings = embeddings[i:batch_end]
            
            try:
                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids,
                    embeddings=batch_embeddings
                )
                added_ids.extend(batch_ids)
                
                if self.config.log_chunk_details:
                    logger.info(f"Added batch {i//batch_size + 1}: {len(batch_docs)} documents")
                    
            except Exception as e:
                logger.error(f"Failed to add batch {i//batch_size + 1}: {e}")
                raise
        
        logger.info(f"Successfully added {len(added_ids)} documents to collection")
        return added_ids
    
    def query_documents(
        self,
        query_text: str,
        n_results: int = 10,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Query documents in the collection.
        
        Args:
            query_text: Text query to search for
            n_results: Number of results to return
            where: Metadata filter conditions
            where_document: Document content filter conditions
            include: Fields to include in results
            
        Returns:
            Dict containing query results
        """
        if include is None:
            include = ["documents", "metadatas", "distances"]
        
        try:
            # Generate query embedding
            query_embedding = None
            if self._embeddings:
                query_embedding = self.embed_text(query_text)
            
            # Perform query
            results = self.collection.query(
                query_texts=[query_text] if query_embedding is None else None,
                query_embeddings=[query_embedding] if query_embedding else None,
                n_results=n_results,
                where=where,
                where_document=where_document,
                include=include
            )
            
            if self.config.log_search_results:
                logger.info(
                    f"Query '{query_text[:50]}...' returned {len(results.get('ids', [[]])[0])} results"
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to query documents: {e}")
            raise
    
    def get_documents(
        self,
        ids: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get documents from the collection.
        
        Args:
            ids: Specific document IDs to retrieve
            where: Metadata filter conditions
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            include: Fields to include in results
            
        Returns:
            Dict containing document data
        """
        if include is None:
            include = ["documents", "metadatas"]
        
        try:
            results = self.collection.get(
                ids=ids,
                where=where,
                limit=limit,
                offset=offset,
                include=include
            )
            
            logger.info(f"Retrieved {len(results.get('ids', []))} documents")
            return results
            
        except Exception as e:
            logger.error(f"Failed to get documents: {e}")
            raise
    
    def update_documents(
        self,
        ids: List[str],
        documents: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        embeddings: Optional[List[List[float]]] = None
    ) -> None:
        """
        Update existing documents in the collection.
        
        Args:
            ids: Document IDs to update
            documents: New document texts
            metadatas: New metadata
            embeddings: New embeddings
        """
        try:
            # Generate embeddings if documents provided but embeddings not
            if documents and not embeddings and self._embeddings:
                embeddings = self.embed_texts(documents)
            
            self.collection.update(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            logger.info(f"Updated {len(ids)} documents")
            
        except Exception as e:
            logger.error(f"Failed to update documents: {e}")
            raise
    
    def delete_documents(self, ids: List[str]) -> None:
        """
        Delete documents from the collection.
        
        Args:
            ids: Document IDs to delete
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents")
            
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            raise
    
    def count_documents(self) -> int:
        """
        Get the number of documents in the collection.
        
        Returns:
            int: Number of documents
        """
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to count documents: {e}")
            raise
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        try:
            # Get all document IDs
            all_docs = self.collection.get(include=[])
            if all_docs.get('ids'):
                self.collection.delete(ids=all_docs['ids'])
                logger.info(f"Cleared {len(all_docs['ids'])} documents from collection")
            else:
                logger.info("Collection is already empty")
                
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise
    
    # Utility methods
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the ChromaDB instance.
        
        Returns:
            List[str]: Collection names
        """
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            raise
    
    # Research-specific query methods
    
    def search_research_content(
        self,
        query: str,
        research_id: Optional[str] = None,
        source_domains: Optional[List[str]] = None,
        min_quality_score: Optional[float] = None,
        n_results: int = 10
    ) -> Dict[str, Any]:
        """
        Search research content with research-specific filters.
        
        Args:
            query: Search query
            research_id: Filter by specific research session
            source_domains: Filter by source domains
            min_quality_score: Minimum quality score threshold
            n_results: Number of results to return
            
        Returns:
            Dict containing search results
        """
        where_conditions = {}
        
        if research_id:
            where_conditions['research_id'] = research_id
        
        if source_domains:
            where_conditions['source_domain'] = {"$in": source_domains}
        
        if min_quality_score is not None:
            where_conditions['quality_score'] = {"$gte": min_quality_score}
        
        return self.query_documents(
            query_text=query,
            n_results=n_results,
            where=where_conditions if where_conditions else None,
            include=["documents", "metadatas", "distances"]
        )
    
    def get_research_statistics(self, research_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about stored research content.
        
        Args:
            research_id: Optional research session ID filter
            
        Returns:
            Dict containing research statistics
        """
        try:
            # Get all documents or filter by research_id
            where_conditions = {"research_id": research_id} if research_id else None
            
            results = self.get_documents(
                where=where_conditions,
                include=["metadatas"]
            )
            
            if not results.get('metadatas'):
                return {
                    'total_chunks': 0,
                    'unique_sources': 0,
                    'research_sessions': 0,
                    'average_quality_score': 0.0,
                    'source_domains': []
                }
            
            metadatas = results['metadatas']
            
            # Calculate statistics
            total_chunks = len(metadatas)
            unique_sources = len(set(meta.get('source_url', '') for meta in metadatas if meta.get('source_url')))
            research_sessions = len(set(meta.get('research_id', '') for meta in metadatas if meta.get('research_id')))
            
            quality_scores = [
                meta.get('quality_score', 0) for meta in metadatas 
                if meta.get('quality_score') is not None
            ]
            average_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
            
            source_domains = list(set(
                meta.get('source_domain', '') for meta in metadatas 
                if meta.get('source_domain')
            ))
            
            stats = {
                'total_chunks': total_chunks,
                'unique_sources': unique_sources,
                'research_sessions': research_sessions,
                'average_quality_score': round(average_quality, 3),
                'source_domains': source_domains,
                'quality_score_distribution': {
                    'high': len([s for s in quality_scores if s >= 0.7]),
                    'medium': len([s for s in quality_scores if 0.4 <= s < 0.7]),
                    'low': len([s for s in quality_scores if s < 0.4])
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get research statistics: {e}")
            raise
    
    def cleanup_low_quality_content(self, min_quality_threshold: float = None) -> int:
        """
        Remove low-quality content based on quality scores.
        
        Args:
            min_quality_threshold: Minimum quality threshold (uses config default if None)
            
        Returns:
            int: Number of documents removed
        """
        if min_quality_threshold is None:
            min_quality_threshold = self.config.min_content_quality_score
        
        try:
            # Get all documents with quality scores
            results = self.get_documents(include=["metadatas"])
            
            if not results.get('metadatas') or not results.get('ids'):
                return 0
            
            # Find low-quality documents
            low_quality_ids = []
            for i, metadata in enumerate(results['metadatas']):
                quality_score = metadata.get('quality_score')
                if quality_score is not None and quality_score < min_quality_threshold:
                    low_quality_ids.append(results['ids'][i])
            
            # Delete low-quality documents
            if low_quality_ids:
                self.delete_documents(low_quality_ids)
                logger.info(f"Cleaned up {len(low_quality_ids)} low-quality documents")
            
            return len(low_quality_ids)
            
        except Exception as e:
            logger.error(f"Failed to cleanup low-quality content: {e}")
            raise
        """
        Get information about the current collection.
        
        Returns:
            Dict containing collection information
        """
        try:
            collection_info = {
                'name': self.collection.name,
                'count': self.collection.count(),
                'metadata': self.collection.metadata,
                'embedding_model': self.config.embedding_model,
                'embedding_dimensions': self.embedding_model_info.dimensions,
            }
            
            return collection_info
            
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise
    
    @contextmanager
    def batch_operations(self):
        """
        Context manager for batch operations (placeholder for future optimization).
        """
        try:
            yield self
        finally:
            pass
    
    # Context manager support
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# Factory function for easy instantiation
def create_chromadb_client(config: Optional[ChromaDbConfig] = None) -> ChromaDBClient:
    """
    Factory function to create and return a configured ChromaDB client.
    
    Args:
        config: ChromaDbConfig instance
        
    Returns:
        ChromaDBClient: Configured ChromaDB client instance
    """
    if not config:
        logger.warning('Using default ChromaDB config')
        config = ChromaDbConfig()
    return ChromaDBClient(config)


# Utility function for collection cleanup
def clear_and_recreate_collection(
    chroma_host: str,
    chroma_port: int,
    collection_name: str,
    embedding_model: str = "nomic-embed-text"
) -> Collection:
    """
    Utility function to clear existing ChromaDB collection and recreate it.
    
    Args:
        chroma_host: ChromaDB host
        chroma_port: ChromaDB port
        collection_name: Name of the collection to recreate
        embedding_model: Embedding model name
        
    Returns:
        Collection: New collection instance
    """
    try:
        # Create temporary client
        client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(
                chroma_server_authn_credentials=None,
                chroma_server_authn_provider=None
            )
        )
        
        # Try to delete existing collection
        try:
            client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection: {collection_name}")
        except Exception as e:
            logger.info(f"Collection {collection_name} doesn't exist or couldn't be deleted: {e}")
        
        # Get model info
        model_info = ChromaDBClient.EMBEDDING_MODELS.get(
            embedding_model,
            EmbeddingModelInfo(embedding_model, 768, 'Custom model')
        )
        
        # Create new collection with metadata
        new_collection = client.create_collection(
            name=collection_name,
            metadata={
                "description": "Research materials collection",
                "embedding_model": embedding_model,
                "embedding_dimensions": model_info.dimensions,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        )
        
        logger.info(
            f"Created new collection '{collection_name}' for {embedding_model} "
            f"({model_info.dimensions} dimensions)"
        )
        return new_collection
        
    except Exception as e:
        logger.error(f"Error recreating collection: {e}")
        raise