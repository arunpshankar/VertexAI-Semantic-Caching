from src.redis.manager import RedisConnection
from src.config.logging import logger
from typing import NoReturn
from redis import Redis


def flush_redis_database() -> NoReturn:
    """
    Flush all data from the current Redis database securely and log the operation.
    
    Raises:
        ConnectionError: If there is an issue connecting to the Redis server.
        Exception: If any other issues occur during the flushing process.
    """
    try:
        redis: Redis = RedisConnection().get_connection()
        if redis is None:
            logger.error("Failed to connect to the Redis database.")
            raise ConnectionError("Failed to connect to the Redis database.")
        
        redis.flushdb()
        logger.info("All data flushed from the Redis database.")
    except ConnectionError as ce:
        logger.error(f"Connection error in flushing Redis database: {ce}")
        raise
    except Exception as e:
        logger.error(f"Error in flushing Redis database: {e}")
        raise


if __name__ == '__main__':
    logger.info("Starting the flush operation...")
    try:
        flush_redis_database()
    except Exception as e:
        logger.error(f"Failed to complete the flush operation: {e}")
