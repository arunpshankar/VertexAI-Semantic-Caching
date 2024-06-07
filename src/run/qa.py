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


def pipeline(question: str) -> Dict[str, Optional[str]]:
    """
    Process a query to find the best match from cache or via semantic/document match.

    Parameters:
        question (str): The question to process.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing details of the processing results.
    """
    start_time = time.time()
    try:
        answer = match(question)
        if not answer:  # No exact match found
            query_variant = query_match(question)
            if query_variant:
                confidence = query_variant['confidence']
                variant = query_variant['query']
                if meets_threshold(confidence):
                    answer = match(variant)
                    return {
                    "question": question,
                    "query_variant": variant,  # semantic match variant with high confidence meeting threshold 
                    "match_type": "SEMANTIC",
                    "confidence": confidence,
                    "answer": answer,
                    "execution_time": (time.time() - start_time) * 1000  # in milliseconds
                }
                else:
                    answer = doc_match(question)
                    return {
                    "question": question,
                    "query_variant": "NA",  # semantic match low confidence ignored 
                    "match_type": "NATIVE",
                    "confidence": "NA",
                    "answer": answer,
                    "execution_time": (time.time() - start_time) * 1000  # in milliseconds
                }
                    stream_update(question)
                    add(question, answer)
                
            else:
                answer = doc_match(question)
                return {
                    "question": question,
                    "query_variant": "NA",  # no variant found
                    "match_type": "NATIVE",
                    "confidence": "NA",
                    "answer": answer,
                    "execution_time": (time.time() - start_time) * 1000  # execution time in milliseconds
                }
                stream_update(question)
                add(question, answer)

        else:
            # Exact match found
            return {
                "question": question,
                "query_variant": "NA",  # not applicable
                "match_type": "EXACT",
                "confidence": "NA",
                "answer": answer,
                "execution_time": (time.time() - start_time) * 1000  # in milliseconds
            }
    except Exception as e:
        logger.error(f"An error occurred in processing the question: {question}. Error: {str(e)}")
        return {
            "question": question,
            "query_variant": "ERROR",
            "match_type": "ERROR",
            "confidence": "NA",
            "answer": "ERROR",
            "execution_time": (time.time() - start_time) * 1000  # in milliseconds
        }

if __name__ == '__main__':
    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    result = pipeline(question)
    print(result)
    print('-' * 100)

    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    result = pipeline(question)
    print(result)
    print('-' * 100)

    question = "What was Google's operating income (in billions) at the end of March 2021, and how did it compare to the same period of the previous year?"
    variant = generator.generate_variant(question)
    logger.info(f'Query variant => {variant}')
    result = pipeline(variant)
    print(result)
    print('-' * 100)

    result = pipeline(variant)
    print(result)
