from src.config.logging import logger
from redis import StrictRedis
from redis import RedisError


# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ""


class RedisConnection:
    """Singleton class for Redis connection."""
    _instance = None

    def __new__(cls):
        """Create only one instance of the Redis connection."""
        if cls._instance is None:
            cls._instance = super(RedisConnection, cls).__new__(cls)
            try:
                cls._instance.connection = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
                logger.info("Redis connection successfully established.")
            except RedisError as e:
                logger.error(f"Failed to establish Redis connection: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        """Return the Redis connection."""
        return self._instance.connection


def write(key: str, value: str):
    """
    Write a key-value pair to Redis.

    Args:
        key (str): The key under which the value is stored.
        value (str): The value to store.
    """
    try:
        redis = RedisConnection().get_connection()
        if redis is not None:
            redis.set(key, value)
            logger.info(f"Entry {key} stored successfully.")
    except Exception as e:
        logger.error(f"Error in writing to Redis: {e}")


def read(key: str) -> str:
    """
    Retrieve data from Redis by key.

    Args:
        key (str): The key for which to retrieve the data.
    """
    try:
        redis = RedisConnection().get_connection()
        if redis is not None:
            value = redis.get(key)
            if value:
                logger.info(f"Data retrieved for {key}: {value}")
                return value
            else:
                logger.info(f"No data found for {key}")
    except Exception as e:
        logger.error(f"Error in retrieving data from Redis: {e}")
        return None

if __name__ == '__main__':
    # Test cases for Redis operations
    write('test_key', 'Hello, Redis!')
    result = read('test_key')
    assert result == 'Hello, Redis!', 'Error in Redis read/write operations'
    logger.info('All tests passed successfully.')