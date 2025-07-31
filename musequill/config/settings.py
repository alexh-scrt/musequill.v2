from pydantic import Field, field_validator
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Main application settings."""
    
    # Application settings
    APP_NAME: str = Field(default="MuseQuill", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    APP_HOST: str = Field(default="0.0.0.0", description="Application host")
    APP_PORT: int = Field(default=8000, description="Application port")
    ENVIRONMENT: str = Field(default="development", description="Environment")
    DEBUG: bool = Field(default=True, description="Debug mode")
    SECRET_KEY: str = Field(default="your-super-secret-key-change-this-in-production", description="Secret key")
    
    # LLM Provider configuration
    LLM_PROVIDER: str = Field(default="ollama", description="LLM Provider (openai, ollama)")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FORMAT: str = Field(default="json", description="Log format")
    STRUCTURED_LOGGING: bool = Field(default=True, description="Use structured logging")
    LOG_FILE_PATH: Optional[str] = Field(default="./logs/musequill.log", description="Log file path")
    LOG_MAX_FILE_SIZE: str = Field(default="100MB", description="Maximum log file size")
    LOG_BACKUP_COUNT: int = Field(default=5, description="Number of backup log files")
    
    # OpenAI settings (with OPENAI_ prefix)
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    OPENAI_DEFAULT_MODEL: str = Field(default="gpt-4o", description="Default OpenAI model")
    OPENAI_BASE_URL: str = Field(default="https://api.openai.com/v1", description="OpenAI API base URL")
    OPENAI_MAX_TOKENS: int = Field(default=4096, description="Maximum tokens per request")
    OPENAI_TEMPERATURE: float = Field(default=0.7, description="Sampling temperature")
    OPENAI_REQUEST_TIMEOUT: int = Field(default=60, description="Request timeout in seconds")
    OPENAI_MAX_RETRIES: int = Field(default=3, description="Maximum number of retries")
    
    # OpenAI model configurations
    OPENAI_PLANNING_MODEL: str = Field(default="gpt-4", description="Model for planning agent")
    OPENAI_WRITING_MODEL: str = Field(default="gpt-4o", description="Model for writing agent")
    OPENAI_CHARACTER_MODEL: str = Field(default="gpt-4", description="Model for character agent")
    OPENAI_PLOT_MODEL: str = Field(default="gpt-4", description="Model for plot agent")
    OPENAI_EDITOR_MODEL: str = Field(default="gpt-4", description="Model for editor agent")
    OPENAI_RESEARCH_MODEL: str = Field(default="gpt-3.5-turbo", description="Model for research agent")
    OPENAI_CRITIC_MODEL: str = Field(default="gpt-4", description="Model for critic agent")
    OPENAI_PROPONENT_MODEL: str = Field(default="gpt-4", description="Model for proponent agent")
    OPENAI_MEMORY_MODEL: str = Field(default="gpt-3.5-turbo", description="Model for memory management")
    
    # OpenAI cost management
    OPENAI_DAILY_BUDGET_USD: float = Field(default=100.0, description="Daily budget in USD")
    OPENAI_MONTHLY_BUDGET_USD: float = Field(default=3000.0, description="Monthly budget in USD")
    OPENAI_COST_TRACKING_ENABLED: bool = Field(default=True, description="Enable cost tracking")
    OPENAI_ALERT_THRESHOLD_PCT: float = Field(default=80.0, description="Budget alert threshold percentage")
    
    # Ollama settings (with OLLAMA_ prefix)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    OLLAMA_DEFAULT_MODEL: str = Field(default="llama3.3:70b", description="Default Ollama model")
    OLLAMA_MAX_TOKENS: int = Field(default=4096, description="Maximum tokens per request")
    OLLAMA_TEMPERATURE: float = Field(default=0.7, description="Sampling temperature")
    OLLAMA_REQUEST_TIMEOUT: int = Field(default=60, description="Request timeout in seconds")
    OLLAMA_MAX_RETRIES: int = Field(default=3, description="Maximum number of retries")
    
    # Ollama model configurations
    OLLAMA_PLANNING_MODEL: str = Field(default="llama3.3:70b", description="Model for planning agent")
    OLLAMA_WRITING_MODEL: str = Field(default="llama3.3:70b", description="Model for writing agent")
    OLLAMA_CHARACTER_MODEL: str = Field(default="llama3.3:70b", description="Model for character agent")
    OLLAMA_PLOT_MODEL: str = Field(default="llama3.3:70b", description="Model for plot agent")
    OLLAMA_EDITOR_MODEL: str = Field(default="llama3.3:70b", description="Model for editor agent")
    OLLAMA_RESEARCH_MODEL: str = Field(default="llama3.3:70b", description="Model for research agent")
    OLLAMA_CRITIC_MODEL: str = Field(default="llama3.3:70b", description="Model for critic agent")
    OLLAMA_PROPONENT_MODEL: str = Field(default="llama3.3:70b", description="Model for proponent agent")
    OLLAMA_MEMORY_MODEL: str = Field(default="llama3.3:70b", description="Model for memory management")
    
    # Ollama embedding models
    OLLAMA_EMBEDDING_MODEL: str = Field(default="nomic-embed-text:latest", description="Primary embedding model")
    OLLAMA_FALLBACK_EMBEDDING_MODEL: str = Field(default="bge-large:latest", description="Fallback embedding model")
    
    # Database configuration
    DATABASE_URL: str = Field(default="postgresql://musequill:password@localhost:5432/musequill", description="Database URL")
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    
    # Redis configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    REDIS_MAX_CONNECTIONS: int = Field(default=10, description="Redis max connections")
    REDIS_RETRY_ON_TIMEOUT: bool = Field(default=True, description="Redis retry on timeout")
    
    # Neo4j configuration
    NEO4J_URI: str = Field(default="bolt://localhost:7687", description="Neo4j URI")
    NEO4J_USER: str = Field(default="neo4j", description="Neo4j user")
    NEO4J_PASSWORD: str = Field(default="password", description="Neo4j password")
    NEO4J_DATABASE: str = Field(default="neo4j", description="Neo4j database")
    NEO4J_MAX_CONNECTION_LIFETIME: int = Field(default=3600, description="Neo4j max connection lifetime")
    
    # Vector store configuration
    VECTOR_STORE_PROVIDER: str = Field(default="pinecone", description="Vector store provider")
    PINECONE_API_KEY: Optional[str] = Field(default=None, description="Pinecone API key")
    PINECONE_ENVIRONMENT: str = Field(default="us-west1-gcp-free", description="Pinecone environment")
    PINECONE_INDEX_NAME: str = Field(default="musequill-embeddings", description="Pinecone index name")
    CHROMA_PERSIST_DIRECTORY: str = Field(default="./data/chroma", description="Chroma persist directory")
    QDRANT_URL: str = Field(default="http://localhost:6333", description="Qdrant URL")
    QDRANT_API_KEY: Optional[str] = Field(default=None, description="Qdrant API key")
    
    # Research API configuration
    TAVILY_API_KEY: Optional[str] = Field(default=None, description="Tavily API key")
    BRAVE_API_KEY: Optional[str] = Field(default=None, description="Brave API key")
    DUCKDUCKGO_ENABLED: bool = Field(default=True, description="DuckDuckGo enabled")
    RESEARCH_MAX_RESULTS: int = Field(default=10, description="Research max results")
    RESEARCH_TIMEOUT: int = Field(default=30, description="Research timeout")
    
    # File storage configuration
    STORAGE_PROVIDER: str = Field(default="local", description="Storage provider")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS secret access key")
    AWS_REGION: str = Field(default="us-east-1", description="AWS region")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, description="AWS S3 bucket")
    GCS_CREDENTIALS_PATH: Optional[str] = Field(default=None, description="GCS credentials path")
    GCS_BUCKET_NAME: Optional[str] = Field(default=None, description="GCS bucket name")
    LOCAL_STORAGE_PATH: str = Field(default="./data/storage", description="Local storage path")
    
    # Authentication configuration
    AUTH_ENABLED: bool = Field(default=True, description="Authentication enabled")
    JWT_SECRET_KEY: str = Field(default="your-jwt-secret-key", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="JWT access token expire minutes")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="JWT refresh token expire days")
    
    # CORS configuration
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:8080"], description="CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="CORS allow credentials")
    CORS_ALLOW_METHODS: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "OPTIONS"], description="CORS allow methods")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], description="CORS allow headers")
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Rate limit enabled")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, description="Rate limit requests per minute")
    RATE_LIMIT_BURST: int = Field(default=10, description="Rate limit burst")
    
    # Monitoring and metrics
    METRICS_ENABLED: bool = Field(default=True, description="Metrics enabled")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus port")
    JAEGER_ENABLED: bool = Field(default=False, description="Jaeger enabled")
    JAEGER_ENDPOINT: str = Field(default="http://localhost:14268/api/traces", description="Jaeger endpoint")
    
    # LangGraph configuration
    LANGGRAPH_CHECKPOINT_PROVIDER: str = Field(default="redis", description="LangGraph checkpoint provider")
    LANGGRAPH_STREAMING_ENABLED: bool = Field(default=True, description="LangGraph streaming enabled")
    LANGGRAPH_MAX_ITERATIONS: int = Field(default=100, description="LangGraph max iterations")
    LANGGRAPH_TIMEOUT_SECONDS: int = Field(default=300, description="LangGraph timeout seconds")
    
    # Quality control configuration
    QUALITY_ADVERSARIAL_ENABLED: bool = Field(default=True, description="Quality adversarial enabled")
    QUALITY_CONSENSUS_THRESHOLD: float = Field(default=0.8, description="Quality consensus threshold")
    QUALITY_MAX_DEBATE_ROUNDS: int = Field(default=3, description="Quality max debate rounds")
    QUALITY_JUDGE_MODEL: str = Field(default="gpt-4", description="Quality judge model")
    
    # Development settings
    RELOAD: bool = Field(default=True, description="Auto-reload enabled")
    WORKERS: int = Field(default=1, description="Number of workers")
    DEBUG_TOOLBAR: bool = Field(default=True, description="Debug toolbar enabled")
    PROFILING_ENABLED: bool = Field(default=False, description="Profiling enabled")
    
    # Testing configuration
    TEST_DATABASE_URL: str = Field(default="postgresql://musequill:password@localhost:5432/musequill_test", description="Test database URL")
    TEST_REDIS_URL: str = Field(default="redis://localhost:6379/1", description="Test Redis URL")
    MOCK_OPENAI_ENABLED: bool = Field(default=False, description="Mock OpenAI enabled")
    MOCK_EXTERNAL_APIS: bool = Field(default=True, description="Mock external APIs")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_api_key(cls, v: str) -> str:
        """Validate OpenAI API key format."""
        if not v:
            raise ValueError("OpenAI API key is required")
        if not v.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        if len(v) < 20:
            raise ValueError("OpenAI API key is too short")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        valid_envs = ["development", "testing", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v.lower()

    @field_validator("LLM_PROVIDER")
    @classmethod
    def validate_llm_provider(cls, v: str) -> str:
        """Validate LLM provider."""
        valid_providers = ["openai", "ollama"]
        if v.lower() not in valid_providers:
            raise ValueError(f"LLM provider must be one of: {valid_providers}")
        return v.lower()

    def get_openai_model_for_agent(self, agent_type: str) -> str:
        """Get the configured OpenAI model for a specific agent type."""
        model_mapping = {
            "planning": self.OPENAI_PLANNING_MODEL,
            "writing": self.OPENAI_WRITING_MODEL,
            "character": self.OPENAI_CHARACTER_MODEL,
            "plot": self.OPENAI_PLOT_MODEL,
            "editor": self.OPENAI_EDITOR_MODEL,
            "research": self.OPENAI_RESEARCH_MODEL,
            "critic": self.OPENAI_CRITIC_MODEL,
            "proponent": self.OPENAI_PROPONENT_MODEL,
            "memory": self.OPENAI_MEMORY_MODEL,
        }
        return model_mapping.get(agent_type, self.OPENAI_DEFAULT_MODEL)
    
    def get_ollama_model_for_agent(self, agent_type: str) -> str:
        """Get the configured Ollama model for a specific agent type."""
        model_mapping = {
            "planning": self.OLLAMA_PLANNING_MODEL,
            "writing": self.OLLAMA_WRITING_MODEL,
            "character": self.OLLAMA_CHARACTER_MODEL,
            "plot": self.OLLAMA_PLOT_MODEL,
            "editor": self.OLLAMA_EDITOR_MODEL,
            "research": self.OLLAMA_RESEARCH_MODEL,
            "critic": self.OLLAMA_CRITIC_MODEL,
            "proponent": self.OLLAMA_PROPONENT_MODEL,
            "memory": self.OLLAMA_MEMORY_MODEL,
        }
        return model_mapping.get(agent_type, self.OLLAMA_DEFAULT_MODEL)
    
    def get_llm_provider_model_for_agent(self, agent_type: str) -> str:
        """Get the configured model for a specific agent type based on the current LLM provider."""
        if self.LLM_PROVIDER == "openai":
            return self.get_openai_model_for_agent(agent_type)
        elif self.LLM_PROVIDER == "ollama":
            return self.get_ollama_model_for_agent(agent_type)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.LLM_PROVIDER}")

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"

    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.ENVIRONMENT == "testing"

    def get_database_url(self, for_testing: bool = False) -> str:
        """Get database URL (test or production)."""
        return self.TEST_DATABASE_URL if for_testing else self.DATABASE_URL

    def get_redis_url(self, for_testing: bool = False) -> str:
        """Get Redis URL (test or production)."""
        return self.TEST_REDIS_URL if for_testing else self.REDIS_URL


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings