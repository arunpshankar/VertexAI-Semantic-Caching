
from src.redis.manager import write_question_and_answer 
from src.redis.manager import RedisConnection
from src.redis.manager import read_answer
from src.config.logging import logger
from typing import NoReturn
import pandas as pd


def write_qa_pairs() -> NoReturn:
    """
    Reads a CSV file containing question-answer pairs and writes them to a Redis database.
    Logs and raises exceptions if connections or operations fail.
    """
    redis_conn = RedisConnection().get_connection()

    if redis_conn is None:
        logger.error("Failed to connect to the Redis database.")
        raise ConnectionError("Failed to connect to the Redis database.")

    try:
        # Read the CSV file
        df = pd.read_csv('./data/eval_ground_truth.csv')
        
        # Iterate through the DataFrame rows and write each question-answer pair to Redis
        for index, row in df.iterrows():
            question = row['question']
            answer = row['answer']
            write_question_and_answer(question, answer)
            logger.info(f"Written to Redis: {question} | {answer}")
            
    except Exception as e:
        logger.error(f"Error while writing to Redis: {e}")
        raise RuntimeError(f"Failed to write data to Redis: {e}")

if __name__ == "__main__":
    write_qa_pairs()
    
    # Test retrieval from Redis
    test_question = "What initiative did Amazon launch to support Black business owners and entrepreneurs in Q2 of 2021?"
    test_answer = read_answer(test_question)
    print("Test retrieval:", test_answer.decode('utf-8') if test_answer else "No answer found")