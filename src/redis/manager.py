from src.cache.utils import generate_md5_hash
from redis import StrictRedis, RedisError
from src.config.logging import logger


class RedisConnection:
    """Singleton class for Redis connection."""
    _instance = None

    def __new__(cls, host='localhost', port=6379, password='', decode_responses=True):
        """Create only one instance of the Redis connection."""
        if cls._instance is None:
            cls._instance = super(RedisConnection, cls).__new__(cls)
            try:
                cls._instance.connection = StrictRedis(
                    host=host, port=port, password=password, decode_responses=decode_responses)
                logger.info("Redis connection successfully established.")
            except RedisError as e:
                logger.error(f"Failed to establish Redis connection: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        """Return the Redis connection."""
        return self._instance.connection


def write_question_and_answer(question: str, answer: str):
    """
    Store question and its answer in Redis using a hash of the question as the key.
    """
    try:
        redis = RedisConnection().get_connection()
        question_hash = generate_md5_hash(question)
        question_key = f"question:{question_hash}"
        answer_key = f"answer:{question_hash}"

        if redis is not None:
            if not redis.exists(question_key):
                redis.set(question_key, question)
                redis.set(answer_key, answer)
                logger.info(f"Question and answer stored successfully under hash: {question_hash}")
            else:
                logger.info("This question hash already exists in the database.")
    except Exception as e:
        logger.error(f"Error in writing question and answer to Redis: {e}")


def read_answer(question: str) -> str:
    """
    Retrieve the answer from Redis using the question hash.
    """
    try:
        redis = RedisConnection().get_connection()
        question_hash = generate_md5_hash(question)
        answer_key = f"answer:{question_hash}"
        if redis is not None:
            answer = redis.get(answer_key)
            if answer:
                logger.info(f"Answer retrieved for hash {question_hash}: {answer}")
                return answer
            else:
                logger.info(f"No answer found for hash {question_hash}")
    except Exception as e:
        logger.error(f"Error in retrieving answer from Redis: {e}")
        return None


if __name__ == '__main__':
    # Example usage
    question = "What is the capital of France?"
    answer = "Paris"
    
    write_question_and_answer(question, answer)
    question_hash = generate_md5_hash(question)
    retrieved_answer = read_answer(question_hash)

    assert retrieved_answer == answer, 'Error in Redis question-answer retrieval'
    logger.info('All tests passed successfully.')
