from pydantic import Field
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisClientConfig(BaseSettings):
    """Configuration settings for the redis client."""
    
    host: str = Field(
        default="localhost",
        validation_alias="REDIS_HOST",
        description="Redis host"
    )

    port: int = Field(
        default=16379,
        validation_alias="REDIS_PORT",
        description="Redis port"
    )

    db: int = Field(
        default=0,
        validation_alias="REDIS_DB",
        description="Redis database"
    )

    password: Optional[str] = Field(
        default=None,
        validation_alias="REDIS_PASSWORD",
        description="Redis password"
    )

    decode_responses: bool = Field(
        default=True,
        validation_alias="REDIS_DECODE_RESPONSES",
        description="Redis decode responses"
    )

    socket_timeout: int = Field(
        default=30,
        validation_alias="REDIS_SOCKET_TIMEOUT",
        description="Redis socket timeout"
    )

    socket_connect_timeout: int = Field(
        default=30,
        validation_alias="REDIS_SOCKET_CONNECT_TIMEOUT",
        description="Redis socket connect timeout"
    )

    health_check_interval: int = Field(
        default=30,
        validation_alias="REDIS_HEALTH_CHECK_INTERVAL",
        description="Redis health check interval"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )