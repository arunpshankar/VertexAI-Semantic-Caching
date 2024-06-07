from src.cache.semantic import query_match
from src.cache.semantic import doc_match
from src.config.logging import logger 
from src.cache.exact import match
import time 


def pipeline(question: str) -> dict:
    # Start timing the execution
    start_time = time.time()

    # Try to get an exact match from the cache
    answer = match(question)
    if not answer:  # No exact match found
        # Query for a similar question match
        query_variant = query_match(question)
        if query_variant:
            return {
                "question": question,
                "query_variant": query_variant,  # semantic match variant
                "match_type": "SEMANTIC",
                "answer": query_variant,
                "execution_time": (time.time() - start_time) * 1000  # in milliseconds
            }
        else:
            return {
                "question": question,
                "query_variant": "NA",  # no variant found
                "match_type": "NO_MATCH",
                "answer": "NA",
                "execution_index": (time.time() - start_time) * 1000  # in milliseconds
            }
    else:
        # Exact match found
        return {
            "question": question,
            "query_variant": "NA",  # not applicable
            "match_type": "EXACT",
            "answer": answer,
            "execution_time": (time.time() - start_time) * 1000  # in milliseconds
        }

if __name__ == '__main__':
    question = "What was the operating income or loss (in billions) for Google Author Insights for Q1 of 2021 compared to the previous year?"
    result = pipeline(question)
    print(result)