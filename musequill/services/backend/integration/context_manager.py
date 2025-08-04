#!/usr/bin/env python3
"""
LLMContextManager Integration Function

Provides a comprehensive integration function that assembles all components
and returns a fully configured LLMContextManager instance ready for use.

Key Features:
- Automatic configuration of Redis and ChromaDB backends
- LLM client setup with configurable parameters
- Pluggable ContentParser and MetadataGenerator initialization
- Error handling and validation
- Multiple configuration strategies (config file, environment, explicit)
- Health checks and connectivity validation
"""

import logging
import os
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

# Import the core components
from .llm_context_manager import LLMContextManager
from .content_parser import BookContentParser, SimpleContentParser, create_content_parser
from .metadata_generator import LLMMetadataGenerator, SimpleMetadataGenerator, MetadataPromptConfig, create_metadata_generator

# Import backend dependencies
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None

try:
    # Assuming you have an LLM client (adjust import based on your setup)
    from langchain_ollama import OllamaLLM
    OLLAMA_AVAILABLE = True
except ImportError:
    try:
        # Alternative LLM client import
        from ollama import Client as OllamaClient
        OLLAMA_AVAILABLE = True
        OllamaLLM = OllamaClient
    except ImportError:
        OLLAMA_AVAILABLE = False
        OllamaLLM = None


logger = logging.getLogger(__name__)


@dataclass
class RedisConfig:
    """Configuration for Redis backend."""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    decode_responses: bool = True
    socket_timeout: int = 30
    socket_connect_timeout: int = 30
    health_check_interval: int = 30


@dataclass
class ChromaDBConfig:
    """Configuration for ChromaDB backend."""
    host: str = "localhost"
    port: int = 8000
    collection_name: str = "book_context"
    persist_directory: Optional[str] = None
    # For local ChromaDB
    path: Optional[str] = None
    # Connection settings
    timeout: int = 30


@dataclass 
class LLMConfig:
    """Configuration for LLM client."""
    base_url: str = "http://localhost:11434"
    model_name: str = "llama3.3:70b"
    temperature: float = 0.3
    max_tokens: int = 4000
    timeout: int = 60
    # Additional parameters
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1


@dataclass
class ParserConfig:
    """Configuration for ContentParser."""
    parser_type: str = "book"  # "book" or "simple"
    preserve_structure: bool = True
    extract_key_concepts: bool = True


@dataclass
class MetadataConfig:
    """Configuration for MetadataGenerator."""
    generator_type: str = "llm"  # "llm" or "simple"
    prompt_config: MetadataPromptConfig = field(default_factory=MetadataPromptConfig)


@dataclass
class LLMContextManagerConfig:
    """Complete configuration for LLMContextManager."""
    redis: RedisConfig = field(default_factory=RedisConfig)
    chromadb: ChromaDBConfig = field(default_factory=ChromaDBConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    parser: ParserConfig = field(default_factory=ParserConfig)
    metadata: MetadataConfig = field(default_factory=MetadataConfig)
    
    # Integration settings
    validate_connections: bool = True
    create_collections: bool = True
    log_level: str = "INFO"


class LLMContextManagerIntegration:
    """Integration helper for LLMContextManager setup and configuration."""
    
    @staticmethod
    def create_manager(config: Optional[LLMContextManagerConfig] = None,
                      config_file: Optional[str] = None,
                      **kwargs) -> LLMContextManager:
        """
        Create a fully configured LLMContextManager instance.
        
        Args:
            config: Configuration object (takes precedence)
            config_file: Path to JSON configuration file
            **kwargs: Override specific configuration values
            
        Returns:
            Configured LLMContextManager instance
            
        Raises:
            RuntimeError: If required dependencies are missing
            ConnectionError: If backend connections fail
        """
        
        # Load configuration
        final_config = LLMContextManagerIntegration._load_configuration(
            config, config_file, **kwargs
        )
        
        # Set up logging
        logging.basicConfig(level=getattr(logging, final_config.log_level))
        logger.info("Starting LLMContextManager integration")
        
        # Validate dependencies
        LLMContextManagerIntegration._validate_dependencies()
        
        # Create backend clients
        redis_client = LLMContextManagerIntegration._create_redis_client(final_config.redis)
        chromadb_client = LLMContextManagerIntegration._create_chromadb_client(final_config.chromadb)
        llm_client = LLMContextManagerIntegration._create_llm_client(final_config.llm)
        
        # Create parser and metadata generator
        content_parser = LLMContextManagerIntegration._create_content_parser(final_config.parser)
        metadata_generator = LLMContextManagerIntegration._create_metadata_generator(
            final_config.metadata, llm_client
        )
        
        # Validate connections if requested
        if final_config.validate_connections:
            LLMContextManagerIntegration._validate_connections(redis_client, chromadb_client, llm_client)
        
        # Create and return manager
        manager = LLMContextManager(
            redis_store=redis_client,
            vector_store=chromadb_client,
            metadata_generator=metadata_generator,
            content_parser=content_parser
        )
        
        logger.info("LLMContextManager created successfully")
        return manager
    
    @staticmethod
    def _load_configuration(config: Optional[LLMContextManagerConfig],
                          config_file: Optional[str],
                          **kwargs) -> LLMContextManagerConfig:
        """Load and merge configuration from various sources."""
        
        # Start with default config
        final_config = config or LLMContextManagerConfig()
        
        # Load from config file if provided
        if config_file:
            file_config = LLMContextManagerIntegration._load_config_file(config_file)
            final_config = LLMContextManagerIntegration._merge_configs(final_config, file_config)
        
        # Load from environment variables
        env_config = LLMContextManagerIntegration._load_env_config()
        final_config = LLMContextManagerIntegration._merge_configs(final_config, env_config)
        
        # Apply kwargs overrides
        if kwargs:
            final_config = LLMContextManagerIntegration._apply_kwargs_overrides(final_config, **kwargs)
        
        return final_config
    
    @staticmethod
    def _load_config_file(config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config file {config_file}: {e}")
            return {}
    
    @staticmethod
    def _load_env_config() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {}
        
        # Redis environment variables
        if os.getenv("REDIS_HOST"):
            env_config.setdefault("redis", {})["host"] = os.getenv("REDIS_HOST")
        if os.getenv("REDIS_PORT"):
            env_config.setdefault("redis", {})["port"] = int(os.getenv("REDIS_PORT"))
        if os.getenv("REDIS_PASSWORD"):
            env_config.setdefault("redis", {})["password"] = os.getenv("REDIS_PASSWORD")
        
        # ChromaDB environment variables
        if os.getenv("CHROMADB_HOST"):
            env_config.setdefault("chromadb", {})["host"] = os.getenv("CHROMADB_HOST")
        if os.getenv("CHROMADB_PORT"):
            env_config.setdefault("chromadb", {})["port"] = int(os.getenv("CHROMADB_PORT"))
        if os.getenv("CHROMADB_COLLECTION"):
            env_config.setdefault("chromadb", {})["collection_name"] = os.getenv("CHROMADB_COLLECTION")
        
        # LLM environment variables
        if os.getenv("LLM_BASE_URL"):
            env_config.setdefault("llm", {})["base_url"] = os.getenv("LLM_BASE_URL")
        if os.getenv("LLM_MODEL"):
            env_config.setdefault("llm", {})["model_name"] = os.getenv("LLM_MODEL")
        
        return env_config
    
    @staticmethod
    def _merge_configs(base_config: LLMContextManagerConfig, override_config: Dict[str, Any]) -> LLMContextManagerConfig:
        """Merge configuration dictionaries into base config."""
        # This is a simplified merge - you might want to implement deep merging
        for section, values in override_config.items():
            if hasattr(base_config, section) and isinstance(values, dict):
                section_config = getattr(base_config, section)
                for key, value in values.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)
        
        return base_config
    
    @staticmethod
    def _apply_kwargs_overrides(config: LLMContextManagerConfig, **kwargs) -> LLMContextManagerConfig:
        """Apply keyword argument overrides to configuration."""
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
            elif "." in key:
                # Handle nested attributes like "redis.host"
                parts = key.split(".")
                obj = config
                for part in parts[:-1]:
                    if hasattr(obj, part):
                        obj = getattr(obj, part)
                    else:
                        break
                else:
                    if hasattr(obj, parts[-1]):
                        setattr(obj, parts[-1], value)
        
        return config
    
    @staticmethod
    def _validate_dependencies() -> None:
        """Validate that required dependencies are available."""
        missing_deps = []
        
        if not REDIS_AVAILABLE:
            missing_deps.append("redis")
        if not CHROMADB_AVAILABLE:
            missing_deps.append("chromadb")
        if not OLLAMA_AVAILABLE:
            missing_deps.append("ollama or langchain_ollama")
        
        if missing_deps:
            raise RuntimeError(f"Missing required dependencies: {', '.join(missing_deps)}")
    
    @staticmethod
    def _create_redis_client(config: RedisConfig) -> redis.Redis:
        """Create and configure Redis client."""
        try:
            client = redis.Redis(
                host=config.host,
                port=config.port,
                db=config.db,
                password=config.password,
                decode_responses=config.decode_responses,
                socket_timeout=config.socket_timeout,
                socket_connect_timeout=config.socket_connect_timeout,
                health_check_interval=config.health_check_interval
            )
            
            logger.info(f"Redis client created: {config.host}:{config.port}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to create Redis client: {e}")
            raise
    
    @staticmethod
    def _create_chromadb_client(config: ChromaDBConfig):
        """Create and configure ChromaDB client."""
        try:
            if config.path:
                # Local ChromaDB
                client = chromadb.PersistentClient(path=config.path)
                logger.info(f"ChromaDB client created (local): {config.path}")
            else:
                # Remote ChromaDB
                client = chromadb.HttpClient(
                    host=config.host,
                    port=config.port
                )
                logger.info(f"ChromaDB client created (remote): {config.host}:{config.port}")
            
            # Get or create collection
            try:
                collection = client.get_collection(config.collection_name)
                logger.info(f"Using existing ChromaDB collection: {config.collection_name}")
            except Exception:
                collection = client.create_collection(config.collection_name)
                logger.info(f"Created ChromaDB collection: {config.collection_name}")
            
            return collection
            
        except Exception as e:
            logger.error(f"Failed to create ChromaDB client: {e}")
            raise
    
    @staticmethod
    def _create_llm_client(config: LLMConfig):
        """Create and configure LLM client."""
        try:
            if hasattr(OllamaLLM, '__call__'):
                # LangChain Ollama client
                client = OllamaLLM(
                    model=config.model_name,
                    base_url=config.base_url,
                    temperature=config.temperature,
                    num_predict=config.max_tokens,
                    top_p=config.top_p,
                    top_k=config.top_k,
                    repeat_penalty=config.repeat_penalty
                )
            else:
                # Ollama client
                client = OllamaLLM(host=config.base_url)
            
            logger.info(f"LLM client created: {config.model_name} at {config.base_url}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to create LLM client: {e}")
            raise
    
    @staticmethod
    def _create_content_parser(config: ParserConfig):
        """Create and configure ContentParser."""
        try:
            parser = create_content_parser(
                parser_type=config.parser_type,
                preserve_structure=config.preserve_structure,
                extract_key_concepts=config.extract_key_concepts
            )
            
            logger.info(f"ContentParser created: {config.parser_type}")
            return parser
            
        except Exception as e:
            logger.error(f"Failed to create ContentParser: {e}")
            raise
    
    @staticmethod
    def _create_metadata_generator(config: MetadataConfig, llm_client):
        """Create and configure MetadataGenerator."""
        try:
            if config.generator_type == "llm":
                generator = create_metadata_generator(
                    generator_type="llm",
                    llm_client=llm_client,
                    config=config.prompt_config
                )
            else:
                generator = create_metadata_generator(generator_type="simple")
            
            logger.info(f"MetadataGenerator created: {config.generator_type}")
            return generator
            
        except Exception as e:
            logger.error(f"Failed to create MetadataGenerator: {e}")
            raise
    
    @staticmethod
    def _validate_connections(redis_client, chromadb_client, llm_client) -> None:
        """Validate that all backend connections are working."""
        
        # Test Redis connection
        try:
            redis_client.ping()
            logger.info("Redis connection validated")
        except Exception as e:
            raise ConnectionError(f"Redis connection failed: {e}")
        
        # Test ChromaDB connection
        try:
            chromadb_client.count()
            logger.info("ChromaDB connection validated")
        except Exception as e:
            raise ConnectionError(f"ChromaDB connection failed: {e}")
        
        # Test LLM connection (basic check)
        try:
            # Simple test - adjust based on your LLM client interface
            if hasattr(llm_client, 'generate'):
                # Try a simple generation
                test_response = llm_client.generate("Test", max_tokens=1, temperature=0.1)
                logger.info("LLM connection validated")
            else:
                logger.info("LLM connection check skipped (no generate method)")
        except Exception as e:
            logger.warning(f"LLM connection test failed (may still work): {e}")


# === CONVENIENCE FUNCTIONS ===

def create_llm_context_manager(config_file: Optional[str] = None, **kwargs) -> LLMContextManager:
    """
    Convenience function to create LLMContextManager with minimal configuration.
    
    Args:
        config_file: Optional path to JSON configuration file
        **kwargs: Configuration overrides (e.g., redis_host="localhost")
        
    Returns:
        Configured LLMContextManager instance
        
    Example:
        # Using defaults
        manager = create_llm_context_manager()
        
        # With custom Redis host
        manager = create_llm_context_manager(redis_host="192.168.1.100")
        
        # With config file
        manager = create_llm_context_manager(config_file="config.json")
    """
    return LLMContextManagerIntegration.create_manager(config_file=config_file, **kwargs)


def create_local_manager(chromadb_path: str = "./chromadb_data", **kwargs) -> LLMContextManager:
    """
    Create LLMContextManager with local backends (useful for development/testing).
    
    Args:
        chromadb_path: Path for local ChromaDB storage
        **kwargs: Additional configuration overrides
        
    Returns:
        LLMContextManager configured for local development
    """
    config = LLMContextManagerConfig()
    config.chromadb.path = chromadb_path
    config.validate_connections = False  # Skip connection validation for local setup
    
    return LLMContextManagerIntegration.create_manager(config=config, **kwargs)


def create_production_manager(config_file: str, validate_all: bool = True) -> LLMContextManager:
    """
    Create LLMContextManager for production use with full validation.
    
    Args:
        config_file: Path to production configuration file
        validate_all: Whether to validate all connections
        
    Returns:
        Production-ready LLMContextManager instance
    """
    return LLMContextManagerIntegration.create_manager(
        config_file=config_file,
        validate_connections=validate_all,
        log_level="WARNING"
    )


# === EXAMPLE USAGE ===

if __name__ == "__main__":
    # Example usage patterns
    
    # 1. Simple local development setup
    try:
        manager = create_local_manager()
        print("✅ Local LLMContextManager created successfully")
        
        # Test basic functionality
        result = manager.store(
            content_id="test_content",
            content="This is a test content for the Peter the Bunny book.",
            as_vector=False,
            content_type="research",
            book_id="peter_forest_001"
        )
        print(f"✅ Test storage result: {result}")
        
        # Test retrieval
        retrieved = manager.get("test_content")
        print(f"✅ Test retrieval: {retrieved is not None}")
        
    except Exception as e:
        print(f"❌ Local setup failed: {e}")
    
    # 2. Custom configuration
    try:
        manager = create_llm_context_manager(
            redis_host="localhost",
            chromadb_host="localhost",
            llm_model="llama3.3:70b"
        )
        print("✅ Custom LLMContextManager created successfully")
        
    except Exception as e:
        print(f"❌ Custom setup failed: {e}")