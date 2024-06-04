from src.config.logging import logger
from typing import Optional
from hashlib import md5 


def generate_md5_hash(input_string: str) -> Optional[str]:
    """
    Generate a 32-character MD5 hash for a given input string.

    Args:
        inputstring (str): The string to hash.

    Returns:
        Optional[str]: The MD5 hash of the input string, or None if an error occurs.
    """
    try:
        hash_value = md5(input_string.encode()).hexdigest()
        logger.info(f"MD5 hash generated for input: {input_string} - Hash: {hash_value}")
        return hash_value
    except Exception as e:
        logger.error(f"Error generating MD5 hash for input: {input_string} - Error: {str(e)}")
        return None


if __name__ == '__main__':
    test_queries = {
        "Same syntactic and semantic": ("financial analysis", "financial analysis"),
        "Different syntactics, same semantic": ("financial analysis", "finance analysis"),
        "Different semantics": ("stock market", "bonds market"),
    }

    for description, (q1, q2) in test_queries.items():
        hash_q1 = generate_md5_hash(q1)
        hash_q2 = generate_md5_hash(q2)
        if hash_q1 == hash_q2:
            logger.info(f"[{description}]: Queries have the same hash. q1: {q1}, q2: {q2}")
        else:
            logger.info(f"[{description}]: Queries have different hashes. q1: {q1}, hash_q1: {hash_q1}, q2: {q2}, hash_q2: {hash_q2}")
