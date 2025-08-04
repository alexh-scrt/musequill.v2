"""
Configuration management for the chromadb client
"""

from pydantic import Field
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChromaDbConfig(BaseSettings):
    """Configuration settings for the chromadb client."""
        
    # Chroma Vector Store settings
    chroma_host: str = Field(
        default="localhost",
        validation_alias="CHROMA_HOST",
        description="Chroma database host"
    )
    chroma_port: int = Field(
        default=8000,
        validation_alias="CHROMA_PORT",
        description="Chroma database port"
    )
    chroma_collection_name: str = Field(
        default="research_collection",
        validation_alias="CHROMA_COLLECTION_NAME",
        description="Chroma collection name for storing research materials"
    )
    chroma_tenant: str = Field(
        default="default_tenant",
        validation_alias="CHROMA_TENANT",
        description="Chroma tenant name"
    )
    chroma_database: str = Field(
        default="default_database",
        validation_alias="CHROMA_DATABASE",
        description="Chroma database name"
    )
    
    # Ollama Embeddings settings (UPDATED SECTION)
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        validation_alias="OLLAMA_BASE_URL",
        description="Ollama server base URL"
    )
    embedding_model: str = Field(
        default="nomic-embed-text",
        validation_alias="OLLAMA_EMBEDDING_MODEL",
        description="Ollama embedding model (nomic-embed-text, mxbai-embed-large, all-minilm)"
    )
    # Note: Removed openai_api_key and embedding_dimensions as they're not needed for Ollama

    embedding_dimensions: int = Field(
        default=768,  # Reduced from 1024 for better Ollama performance
        validation_alias="OLLAMA_EMBEDDING_DIMENSIONS",
        description="Ollama embedding dimensions",
        ge=64,
        le=1536
    )

    # Text Processing settings
    chunk_size: int = Field(
        default=800,  # Reduced from 1000 for better Ollama performance
        validation_alias="RESEARCH_CHUNK_SIZE",
        description="Text chunk size for embedding",
        ge=100,
        le=8000
    )
    chunk_overlap: int = Field(
        default=150,  # Reduced from 200 for better Ollama performance
        validation_alias="RESEARCH_CHUNK_OVERLAP",
        description="Overlap between text chunks",
        ge=0,
        le=500
    )
    min_chunk_size: int = Field(
        default=100,
        validation_alias="MIN_CHUNK_SIZE",
        description="Minimum chunk size to store",
        ge=50,
        le=500
    )
    max_content_length: int = Field(
        default=50000,
        validation_alias="MAX_CONTENT_LENGTH",
        description="Maximum content length to process per result",
        ge=1000,
        le=200000
    )
    
    max_research_queries: int = Field(
        default=10,
        validation_alias="MAX_RESEARCH_QUERIES",
        description="Maximum number of research queries to perform",
        ge=1,
        le=20
    )

    # Processing settings (OPTIMIZED FOR OLLAMA)
    max_concurrent_queries: int = Field(
        default=2,  # Reduced from 5 for local Ollama processing
        validation_alias="MAX_CONCURRENT_RESEARCH_QUERIES",
        description="Maximum concurrent research queries",
        ge=1,
        le=10
    )
    query_retry_attempts: int = Field(
        default=3,
        validation_alias="QUERY_RETRY_ATTEMPTS",
        description="Number of retry attempts for failed queries",
        ge=1,
        le=5
    )
    retry_delay_seconds: int = Field(
        default=5,
        validation_alias="RETRY_DELAY_SECONDS",
        description="Delay between retry attempts",
        ge=1,
        le=60
    )
    rate_limit_delay: float = Field(
        default=0.5,  # Reduced from 1.0 since no external API limits
        validation_alias="RATE_LIMIT_DELAY",
        description="Delay between API calls to respect rate limits",
        ge=0.1,
        le=10.0
    )
    
    # Content Quality settings
    min_content_quality_score: float = Field(
        default=0.4,  # Slightly increased from 0.3 for better quality
        validation_alias="MIN_CONTENT_QUALITY_SCORE",
        description="Minimum quality score for content inclusion",
        ge=0.0,
        le=1.0
    )
    enable_content_filtering: bool = Field(
        default=True,
        validation_alias="ENABLE_CONTENT_FILTERING",
        description="Enable content quality filtering"
    )
    filter_duplicate_content: bool = Field(
        default=True,
        validation_alias="FILTER_DUPLICATE_CONTENT",
        description="Filter out duplicate content"
    )
    content_similarity_threshold: float = Field(
        default=0.85,
        validation_alias="CONTENT_SIMILARITY_THRESHOLD",
        description="Threshold for considering content duplicate",
        ge=0.5,
        le=1.0
    )
    
    min_source_score: float = Field(
        default=0.4,  # Reduced from 0.8 for more flexibility with local processing
        validation_alias="MIN_SOURCE_SCORE",
        description="Minimum Tavily source score to include",
        ge=0.0,
        le=1.0
    )
    
    # Storage settings (OPTIMIZED FOR OLLAMA)
    batch_size: int = Field(
        default=25,  # Reduced from 50 for more stable local processing
        validation_alias="CHROMA_BATCH_SIZE",
        description="Batch size for Chroma insertions",
        ge=1,
        le=1000
    )
    enable_metadata_indexing: bool = Field(
        default=True,
        validation_alias="ENABLE_METADATA_INDEXING",
        description="Enable metadata indexing in Chroma"
    )
    
    # Monitoring and logging
    log_search_results: bool = Field(
        default=True,
        validation_alias="LOG_SEARCH_RESULTS",
        description="Log detailed search results"
    )
    log_chunk_details: bool = Field(
        default=False,
        validation_alias="LOG_CHUNK_DETAILS",
        description="Log detailed chunk processing information"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )