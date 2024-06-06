from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from src.match.utils import get_query_embedding
from src.match.utils import find_neighbors
from src.config.logging import logger
from typing import List
from typing import Dict
from typing import Any 


NUM_NEIGHBOURS = 3  # Retrieve top relevant matching pages
DEPLOYED_INDEX_NAME = 'earnings_report_2024_06_06_09_32_39'
INDEX_ENDPOINT_ID = '7073945551808495616'

def retrieve_top_matches(api_response: List[Dict[str, Any]]) -> List[str]:
    """
    Extracts page contents from an API response.

    This function parses a structured API response to extract page contents specified under the 'page_content' key.
    It assumes the API response is a list of dictionaries containing lists of 'restricts' dictionaries.

    Parameters:
    api_response (List[To handle a structured API response where each item is a dictionary containing further information.

    Returns:
    List[str]: A list of strings, each representing the page content extracted from the API response.
    """
    page_contents = []

    try:
        for match in api_response[0]:  # Access the first (and possibly only) list of matches
            for restrict in match.restricts:
                if restrict.name == 'page_content':
                    # Assuming that the desired content is always the first token in 'allow_tokens'
                    page_contents.append(restrict.allow_tokens[0])
    except IndexError as e:
        logger.error(f"Error accessing elements in the API response: Index out of range - {e}")
    except KeyError as e:
        logger.error(f"Key error in accessing API safety response data; possibly malformed response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred - {e}")

    return page_contents

if __name__ == "__main__":
    query = "How many Microsoft 365 Consumer subscribers were there as of Q2 2021?"
    query_embedding = get_query_embedding(query)
    response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
    pages = retrieve_top_matches(response)
    for page in pages:
        print(page[:100])
