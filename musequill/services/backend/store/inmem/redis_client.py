import redis
import logging
from typing import Any, Optional, Union, Dict, List
from contextlib import asynccontextmanager
import asyncio
from redis.exceptions import (
    RedisError, 
    ConnectionError, 
    TimeoutError,
    ResponseError
)

from .redis_config import RedisClientConfig  # Adjust import path as needed

logger = logging.getLogger(__name__)


class RedisClient:
    """
    Redis client wrapper that provides connection management, error handling,
    and common Redis operations with proper configuration.
    """
    
    def __init__(self, config: RedisClientConfig):
        """
        Initialize Redis client with configuration.
        
        Args:
            config: RedisClientConfig instance with Redis connection settings
        """
        self.config = config
        self._client: Optional[redis.Redis] = None
        self._connection_pool: Optional[redis.ConnectionPool] = None
        self._is_connected = False
        
    def _create_connection_pool(self) -> redis.ConnectionPool:
        """Create and return a Redis connection pool."""
        pool_kwargs = {
            'host': self.config.host,
            'port': self.config.port,
            'db': self.config.db,
            'decode_responses': self.config.decode_responses,
            'socket_timeout': self.config.socket_timeout,
            'socket_connect_timeout': self.config.socket_connect_timeout,
            'health_check_interval': self.config.health_check_interval,
            'retry_on_timeout': True,
            'retry_on_error': [ConnectionError, TimeoutError],
        }
        
        if self.config.password:
            pool_kwargs['password'] = self.config.password
            
        return redis.ConnectionPool(**pool_kwargs)
    
    def connect(self) -> None:
        """
        Establish connection to Redis server.
        
        Raises:
            ConnectionError: If unable to connect to Redis server
        """
        try:
            if not self._connection_pool:
                self._connection_pool = self._create_connection_pool()
                
            self._client = redis.Redis(connection_pool=self._connection_pool)
            
            # Test the connection
            self._client.ping()
            self._is_connected = True
            
            logger.info(
                f"Successfully connected to Redis at {self.config.host}:{self.config.port}"
            )
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._is_connected = False
            raise ConnectionError(f"Could not connect to Redis: {e}")
    
    def disconnect(self) -> None:
        """Close Redis connection and cleanup resources."""
        try:
            if self._connection_pool:
                self._connection_pool.disconnect()
                logger.info("Redis connection pool disconnected")
                
            self._client = None
            self._connection_pool = None
            self._is_connected = False
            
        except Exception as e:
            logger.error(f"Error during Redis disconnect: {e}")
    
    def is_connected(self) -> bool:
        """
        Check if Redis client is connected and responsive.
        
        Returns:
            bool: True if connected and responsive, False otherwise
        """
        if not self._is_connected or not self._client:
            return False
            
        try:
            self._client.ping()
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
            'ping_successful': False,
            'server_info': None,
            'error': None
        }
        
        try:
            if self.is_connected():
                health_info['connected'] = True
                health_info['ping_successful'] = True
                health_info['server_info'] = self._client.info('server')
            else:
                health_info['error'] = 'Not connected to Redis'
                
        except Exception as e:
            health_info['error'] = str(e)
            logger.error(f"Redis health check failed: {e}")
            
        return health_info
    
    @property
    def client(self) -> redis.Redis:
        """
        Get the underlying Redis client instance.
        
        Returns:
            redis.Redis: The Redis client instance
            
        Raises:
            ConnectionError: If not connected to Redis
        """
        if not self._client or not self.is_connected():
            raise ConnectionError("Redis client is not connected. Call connect() first.")
        return self._client
    
    # Common Redis operations with error handling
    
    def get(self, key: str) -> Optional[Union[str, bytes]]:
        """
        Get value by key.
        
        Args:
            key: Redis key
            
        Returns:
            Value associated with key or None if key doesn't exist
        """
        try:
            return self.client.get(key)
        except RedisError as e:
            logger.error(f"Redis GET error for key '{key}': {e}")
            raise
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ex: Optional[int] = None,
        px: Optional[int] = None,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """
        Set key-value pair with optional expiration and conditions.
        
        Args:
            key: Redis key
            value: Value to store
            ex: Expiration time in seconds
            px: Expiration time in milliseconds
            nx: Only set if key doesn't exist
            xx: Only set if key exists
            
        Returns:
            bool: True if operation was successful
        """
        try:
            return self.client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)
        except RedisError as e:
            logger.error(f"Redis SET error for key '{key}': {e}")
            raise
    
    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.
        
        Args:
            keys: Keys to delete
            
        Returns:
            int: Number of keys deleted
        """
        try:
            return self.client.delete(*keys)
        except RedisError as e:
            logger.error(f"Redis DELETE error for keys {keys}: {e}")
            raise
    
    def exists(self, *keys: str) -> int:
        """
        Check if keys exist.
        
        Args:
            keys: Keys to check
            
        Returns:
            int: Number of existing keys
        """
        try:
            return self.client.exists(*keys)
        except RedisError as e:
            logger.error(f"Redis EXISTS error for keys {keys}: {e}")
            raise
    
    def expire(self, key: str, time: int) -> bool:
        """
        Set expiration time for a key.
        
        Args:
            key: Redis key
            time: Expiration time in seconds
            
        Returns:
            bool: True if expiration was set
        """
        try:
            return self.client.expire(key, time)
        except RedisError as e:
            logger.error(f"Redis EXPIRE error for key '{key}': {e}")
            raise
    
    def ttl(self, key: str) -> int:
        """
        Get time to live for a key.
        
        Args:
            key: Redis key
            
        Returns:
            int: TTL in seconds (-1 if no expiration, -2 if key doesn't exist)
        """
        try:
            return self.client.ttl(key)
        except RedisError as e:
            logger.error(f"Redis TTL error for key '{key}': {e}")
            raise
    
    def keys(self, pattern: str = "*") -> List[str]:
        """
        Get all keys matching pattern.
        
        Args:
            pattern: Key pattern (default: "*")
            
        Returns:
            List of matching keys
        """
        try:
            return self.client.keys(pattern)
        except RedisError as e:
            logger.error(f"Redis KEYS error for pattern '{pattern}': {e}")
            raise
    
    def flushdb(self) -> bool:
        """
        Clear all keys from the current database.
        
        Returns:
            bool: True if successful
        """
        try:
            return self.client.flushdb()
        except RedisError as e:
            logger.error(f"Redis FLUSHDB error: {e}")
            raise
    
    # Hash operations
    
    def hget(self, name: str, key: str) -> Optional[Union[str, bytes]]:
        """Get field value from hash."""
        try:
            return self.client.hget(name, key)
        except RedisError as e:
            logger.error(f"Redis HGET error for hash '{name}', key '{key}': {e}")
            raise
    
    def hset(self, name: str, key: str, value: Any) -> int:
        """Set field value in hash."""
        try:
            return self.client.hset(name, key, value)
        except RedisError as e:
            logger.error(f"Redis HSET error for hash '{name}', key '{key}': {e}")
            raise
    
    def hgetall(self, name: str) -> Dict[str, Any]:
        """Get all fields and values from hash."""
        try:
            return self.client.hgetall(name)
        except RedisError as e:
            logger.error(f"Redis HGETALL error for hash '{name}': {e}")
            raise
    
    # List operations
    
    def lpush(self, name: str, *values: Any) -> int:
        """Push values to the left of list."""
        try:
            return self.client.lpush(name, *values)
        except RedisError as e:
            logger.error(f"Redis LPUSH error for list '{name}': {e}")
            raise
    
    def rpush(self, name: str, *values: Any) -> int:
        """Push values to the right of list."""
        try:
            return self.client.rpush(name, *values)
        except RedisError as e:
            logger.error(f"Redis RPUSH error for list '{name}': {e}")
            raise
    
    def lpop(self, name: str) -> Optional[Union[str, bytes]]:
        """Pop value from the left of list."""
        try:
            return self.client.lpop(name)
        except RedisError as e:
            logger.error(f"Redis LPOP error for list '{name}': {e}")
            raise
    
    def rpop(self, name: str) -> Optional[Union[str, bytes]]:
        """Pop value from the right of list."""
        try:
            return self.client.rpop(name)
        except RedisError as e:
            logger.error(f"Redis RPOP error for list '{name}': {e}")
            raise
    
    def lrange(self, name: str, start: int, end: int) -> List[Union[str, bytes]]:
        """Get range of values from list."""
        try:
            return self.client.lrange(name, start, end)
        except RedisError as e:
            logger.error(f"Redis LRANGE error for list '{name}': {e}")
            raise
    
    # Context manager support
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


# Factory function for easy instantiation
def create_redis_client(config: Optional[RedisClientConfig] = None) -> RedisClient:
    """
    Factory function to create and return a configured Redis client.
    
    Args:
        config: RedisClientConfig instance
        
    Returns:
        RedisClient: Configured Redis client instance
    """
    if not config:
        logger.warning('Using default Redis client config')
        config = RedisClientConfig()
    return RedisClient(config)