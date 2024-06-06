from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from src.match.utils import get_query_embedding, find_neighbors
from src.config.logging import logger
from typing import List, Dict, Any 

NUM_NEIGHBOURS = 1  # Retrieve the top matching neighbor (query)
DEPLOYED_INDEX_NAME = 'queries_2024_06_06_10_49_50'
INDEX_ENDPOINT_ID = '5044159126003777536'

def retrieve_top_match(query: str) -> Dict[str, Any]:
    """
    Retrieves the top match from a matching engine for a given query.

    Parameters:
    query (str): The query to find a match for.

    Returns:
    Dict[str, Any]: A dictionary containing the top match with its confidence and query.
    """
    try:
        query_embedding = get_query_embedding(query)
        api_response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
        top_match = {}
        
        for match in api_response[0]:  # Assuming the first item contains the match
            top_match['confidence'] = round(1 - match.distance, 4)
            for restrict in match.restricts:
                if restrict.name == 'question':
                    top_match['query'] = restrict.allow_tokens[0]
        return top_match

    except IndexError as e:
        logger.error(f"Error accessing elements in API response: Index out of range - {e}")
    except KeyError as e:
        logger.error(f"Key error in accessing API safety response data; possibly malformed response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred - {e}")
        return {}  # Return an empty dictionary on failure


if __name__ == "__main__":
    query = "How many 365 consumer subscribers were there as of Q2 2021?"
    top_match = retrieve_top_match(query)
    print(top_match)
