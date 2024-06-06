from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from src.match.utils import get_query_embedding
from src.match.utils import find_neighbors
from src.config.logging import logger
from typing import List
from typing import Dict
from typing import Any 


NUM_NEIGHBOURS = 3  # Retrieve the top matching neighbor (query)
DEPLOYED_INDEX_NAME = 'queries_2024_06_06_09_34_29'
INDEX_ENDPOINT_ID = '3228997369940934656'

def retrieve_top_match(api_response: List[Dict[str, Any]]) :
   
    o = []


    try:
        for match in api_response[0]:  # Access the first (and possibly only) list of matches
            print(match)
            for restrict in match.restricts:
                if restrict.name == 'page_content':
                    # Assuming that the desired content is always the first token in 'allow_tokens'
                    o.append(restrict.allow_tokens[0])
    except IndexError as e:
        logger.error(f"Error accessing elements in the API response: Index out of range - {e}")
    except KeyError as e:
        logger.error(f"Key error in accessing API safety response data; possibly malformed response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred - {e}")

    return o

if __name__ == "__main__":
    query = "Microsoft 365?"
    query_embedding = get_query_embedding(query)
    print(query_embedding)
    response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
    top_match = retrieve_top_match(response)
    print(top_match)
