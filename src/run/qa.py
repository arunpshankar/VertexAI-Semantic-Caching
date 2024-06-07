from src.generate.expand import QuestionVariantGenerator
from src.cache.semantic import stream_update
from src.cache.semantic import query_match
from src.cache.semantic import doc_match
from src.config.logging import logger
from src.cache.exact import match
from src.cache.exact import add
from typing import Optional 
from typing import Dict
import time


generator = QuestionVariantGenerator()

def meets_threshold(confidence: float) -> bool:
    """
    Determine if the confidence level meets the required threshold.
    
    Parameters:
        confidence (float): The confidence level of a match.

    Returns:
        bool: True if confidence is greater than 0.9, False otherwise.
    """
    return confidence > 0.9


def handle_semantic_match(question: str, closest_match: Dict[str, any], start_time: float) -> Dict[str, Optional[str]]:
    """
    Handle the case where there is a semantic match for the question.

    Parameters:
        question (str): User's question.
        closest_match (dict): Closest matching question and its metadata.
        start_time (float): Timestamp when the query processing started.

    Returns:
        dict: Details about the processed question and the match.
    """
    confidence = closest_match['confidence']
    if meets_threshold(confidence):
        query = closest_match['query']
        answer = match(query)
        if answer is not None:
            add(question, answer)
        return {
            "question": question,
            "closest_question": query,
            "match_type": "SEMANTIC",
            "confidence": confidence,
            "answer": answer,
            "execution_time": (time.time() - start_time) * 1000
        }
    else:
        return handle_native_search(question, start_time)


def handle_native_search(question: str, start_time: float) -> Dict[str, Optional[str]]:
    """
    Handle native search for a question when no semantic or exact matches are found.

    Parameters:
        question (str): User's question.
        start_time (float): Timestamp when the query processing started.

    Returns:
        dict: Details about the processed question.
    """
    try:
        answer = doc_match(question)
        stream_update(question)
        add(question, answer)
        return {
            "question": question,
            "closest_question": "NA",
            "match_type": "NATIVE",
            "confidence": "NA",
            "answer": answer,
            "execution_time": (time.time() - start_time) * 1000
        }
    except Exception as e:
        logger.error(f"Error during native search: {str(e)}")


def handle_exact_match(question: str, answer: str, start_time: float) -> Dict[str, Optional[str]]:
    """
    Handle the response for an exact match found for the question.

    Parameters:
        question (str): User's question.
        answer (str): The answer associated with the exact match.
        start_time (float): Timestamp when the query processing started.

    Returns:
        dict: Details about the question and the exact match found.
    """
    try:
        return {
            "question": question,
            "closest_question": "NA",
            "match_type": "EXACT",
            "confidence": "NA",
            "answer": answer,
            "execution_time": (time.time() - start_time) * 1000
        }
    except Exception as e:
        logger.error(f"Error handling exact match: {str(e)}")
    

def pipeline(question: str) -> Dict[str, Optional[str]]:
    """
    Processing pipeline for handling a question, searching for exact, semantic, and native matches.

    Parameters:
        question (str): User's question.

    Returns:
        dict: Results of processing the question through the pipeline.
    """
    start_time = time.time()
    try:
        answer = match(question)
        if not answer:  # No exact match found
            closest_match = query_match(question)
            if closest_match:
                return handle_semantic_match(question, closest_match, start_time)
            else:
                return handle_native_search(question, start_time)
        else:
            # Exact match found
            return handle_exact_match(question, answer, start_time)
    except Exception as e:
        logger.error(f"Error processing the question: {str(e)}")
        return {
            "question": question,
            "error": str(e),
            "execution_data": (time.time() - start_time) * 1000
        }


if __name__ == '__main__':
    # TEST 1: Test exact match - user question and relevant correct answer is already available in Redis Memorystore. 
    # Warmup query - to compensate for LLM load times.
    print('WARM UP')
    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    answer = pipeline(question)
    print(answer)
    print('-' * 100)

    # Test run 1 
    print('TEST 1')
    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    answer = pipeline(question)
    print(answer)
    print('-' * 100)

    # TEST 2: Test semantic query match - user question is semantically similar to an already asked question stored in Vertex AI Vector Store.
    # Note: The match meets confidence threshold. 
    print('TEST 2') 
    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    variant = generator.generate_variant(question)
    logger.info(f'Query variant => {variant}')
    answer = pipeline(variant)
    print(answer)
    print('-' * 100)

    # TEST 3: Test exact match after upsert 
    print('TEST 3')
    answer = pipeline(variant)
    print(answer)
    print('-' * 100)

    # TEST 4: Test semantic query match that failed to meet the confidence threshold 
    print('TEST 4')
    question = "How did Alphabet's adjustment in the estimated useful lives of servers and network equipment affect its financial results for the fourth quarter of 2023?"
    answer = pipeline(question)
    print(answer)
    print('-' * 100)
