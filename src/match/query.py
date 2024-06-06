from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from src.match.utils import get_query_embedding
from src.match.utils import find_neighbors
from src.config.logging import logger
from typing import List
from typing import Dict
from typing import Any 


NUM_NEIGHBOURS = 1  # Retrieve the top matching neighbor (query)
DEPLOYED_INDEX_NAME = 'queries_2024_06_06_10_49_50'
INDEX_ENDPOINT_ID = '5044159126003777536'

def retrieve_top_match(api_response: List[Dict[str, Any]]) :
    top_match = {}

    try:
        for match in api_response[0]:  # Access the first (and possibly only) list of matches
            top_match['confidence'] = round(1 - match.distance, 4)
            for restrict in match.restricts:
                if restrict.name == 'question':
                    # Assuming that the desired content is always the first token in 'allow_tokens'
                    top_match['query'] = restrict.allow_tokens[0]
    except IndexError as e:
        logger.error(f"Error accessing elements in the API response: Index out of range - {e}")
    except KeyError as e:
        logger.error(f"Key error in accessing API safety response data; possibly malformed response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred - {e}")

    return top_match

if __name__ == "__main__":
    query = "Microsoft 365?"
    query_embedding = get_query_embedding(query)
    response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
    top_match = retrieve_top_match(response)
    print(top_match)
