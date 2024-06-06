
from src.redis.manager import write_question_and_answer
from src.cache.utils import generate_md5_hash
from src.redis.manager import read_answer
from src.config.logging import logger
from typing import Optional
from typing import Dict
from typing import Any
import time


def match(question: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve the answer to a given question from the cache, with performance metrics.

    Args:
    question (str): The question to retrieve the answer for.

    Returns:
    Optional[Dict[str, Any]]: A dictionary containing the answer and retrieval time in milliseconds,
                               or None if no answer is found.
    """
    start_time = time.time()  # Record the start time
    try:
        answer = read_answer(question)
    except Exception as e:
        logger.error(f"Failed to retrieve answer due to: {e}")
        return None

    if answer is None:
        return None
    else:
        retrieval_time = (time.time() - start_time) * 1000  # Calculate retrieval time in milliseconds
        return {'answer': answer, 'retrieval_time_ms': retrieval_time}
    

def add(question: str, answer: str) -> Optional[bool]:
    """
    Adds a question and its answer to the cache.

    Args:
    question (str): The question to be added.
    answer (str): The answer to the question.

    Returns:
    Optional[bool]: True if the operation was successful, None if it failed.
    """
    try:
        write_question_and_answer(question, answer)
        return True
    except Exception as e:
        logger.error(f"Failed to add question and answer due to: {e}")
        return None


if __name__ == '__main__':
    question = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    answer = match(question)
    if answer is None:
        print("Answer not found in cache.")
        # Assuming you might want to add a new question and answer if not found in cache
        # This is just an example usage; modify as per your real use case.
        new_answer = "The operating income for Google Cloud in Q1 of 2021 was X billion."
        added = add(question, new_answer)
        if added:
            print("New answer added to cache.")
        else:
            print("Failed to add answer to cache.")
    else:
        print(f"Answer: {answer['answer']}, Retrieved in {answer['retrieval_time_ms']:.2f} ms")
