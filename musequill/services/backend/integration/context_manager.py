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
import asyncio
import logging
import os
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

# Import the core components
from musequill.services.backend.context import (
    BookContentParser,
    SimpleContentParser,
    create_content_parser,
    LLMContextManager,
    llm_context_manager,
    SimpleMetadataGenerator,
    MetadataGenerator,
    create_metadata_generator,
    MetadataPromptConfig,
)


from musequill.services.backend.store.inmem import (
    RedisClient,
    create_redis_client,
)

from musequill.services.backend.store.vector import (
    ChromaDBClient,
    create_chromadb_client,
)

from musequill.services.backend.llm.ollama_client import (
    LLMService,
    create_llm_service,
)

logger = logging.getLogger(__name__)


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
    redis: RedisClient = field(default_factory=create_redis_client)
    chromadb: ChromaDBClient = field(default_factory=create_chromadb_client)
    llm: LLMService = field(default_factory=create_llm_service)
    parser: ParserConfig = field(default_factory=ParserConfig)
    metadata: MetadataConfig = field(default_factory=MetadataConfig)
    
    # Integration settings
    validate_connections: bool = True
    create_collections: bool = True
    log_level: str = "DEBUG"


class LLMContextManagerIntegration:
    """Integration helper for LLMContextManager setup and configuration."""
    
    @staticmethod
    async def create_manager(config: Optional[LLMContextManagerConfig] = None,
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
        final_config:LLMContextManagerConfig = LLMContextManagerIntegration._load_configuration(
            config, config_file, **kwargs
        )
        
        # Set up logging
        logging.basicConfig(level=getattr(logging, final_config.log_level))
        logger.info("Starting LLMContextManager integration")
        
        # Create backend clients
        redis_client = final_config.redis
        chromadb_client = final_config.chromadb
        llm_client = final_config.llm
        
        # Create parser and metadata generator
        content_parser = LLMContextManagerIntegration._create_content_parser(final_config.parser)
        metadata_generator = LLMContextManagerIntegration._create_metadata_generator(
            final_config.metadata, llm_client
        )
        
        # Validate connections if requested
        if final_config.validate_connections:
            await LLMContextManagerIntegration._validate_connections(redis_client, chromadb_client, llm_client)
        
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
    async def _validate_connections(redis_client:RedisClient, chromadb_client:ChromaDBClient, llm_client:LLMService) -> None:
        """Validate that all backend connections are working."""
        
        # Test Redis connection
        try:
            if not redis_client.is_connected():
                redis_client.connect()
            resp = redis_client.health_check()
            logger.info(f"Redis connection validated: {json.dumps(resp, indent=2)}")
        except Exception as e:
            raise ConnectionError(f"Redis connection failed: {e}")
        
        # Test ChromaDB connection
        try:
            if not chromadb_client.is_connected():
                chromadb_client.connect()
            resp = chromadb_client.health_check()
            logger.info(f"ChromaDB connection validated: {json.dumps(resp, indent=2)}")
        except Exception as e:
            raise ConnectionError(f"ChromaDB connection failed: {e}")
        
        # Test LLM connection (basic check)
        try:
            # Simple test - adjust based on your LLM client interface
            if hasattr(llm_client, 'generate'):
                # Try a simple generation
                await llm_client.initialize()
                test_response = await llm_client.generate("Capital city of USA? Respond in one word", max_tokens=10, temperature=0.1)
                if not test_response['response'] == "Washington":
                    raise ValueError("LLM is hallucinating...")
                logger.info("LLM connection validated")
            else:
                logger.info("LLM connection check skipped (no generate method)")
        except Exception as e:
            logger.warning(f"LLM connection test failed (may still work): {e}")


# === CONVENIENCE FUNCTIONS ===

async def create_llm_context_manager(config_file: Optional[str] = None, **kwargs) -> LLMContextManager:
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
    cm = await LLMContextManagerIntegration.create_manager(config_file=config_file, **kwargs)
    return cm


async def create_local_manager(chromadb_path: str = "./chromadb_data", **kwargs) -> LLMContextManager:
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
    
    cm = await LLMContextManagerIntegration.create_manager(config=config, **kwargs)
    return cm


async def create_production_manager(config_file: str, validate_all: bool = True) -> LLMContextManager:
    """
    Create LLMContextManager for production use with full validation.
    
    Args:
        config_file: Path to production configuration file
        validate_all: Whether to validate all connections
        
    Returns:
        Production-ready LLMContextManager instance
    """
    cm = await LLMContextManagerIntegration.create_manager(
        config_file=config_file,
        validate_connections=validate_all,
        log_level="WARNING"
    )
    return cm

async def main():
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

if __name__ == "__main__":
    # Example usage patterns
    asyncio.run(main())  
