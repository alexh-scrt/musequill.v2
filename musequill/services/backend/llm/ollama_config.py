"""
Configuration management for the ollama client
"""

from pydantic import Field
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class OllamaConfig(BaseSettings):
    """Configuration settings for the ollama client."""
    

    # Ollama Embeddings settings (UPDATED SECTION)
    base_url: str = Field(
        default="http://localhost:11434",
        validation_alias="OLLAMA_BASE_URL",
        description="Ollama server base URL"
    )

    model_name: str = Field(
        default="llama3.3:70b",
        validation_alias="OLLAMA_MODEL_NAME",
        description="Ollama model"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )