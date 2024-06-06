from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from src.match.utils import get_query_embedding, find_neighbors
from src.config.logging import logger
from typing import List


NUM_NEIGHBOURS = 3
DEPLOYED_INDEX_NAME = 'earnings_report_2024_06_06_09_32_39'
INDEX_ENDPOINT_ID = '7073945551808495616'

def retrieve_top_matches(query: str) -> List[str]:
    """
    Retrieves top matches from a matching engine for a given query.

    Parameters:
    query (str): The query to find matches for.

    Returns:
    List[str]: A list of page contents extracted from the top matches.
    """
    try:
        query_embedding = get_query_embedding(query)
        api_response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
        page_contents = []
        
        for match in api_response[0]:  # Assuming the first item contains the matches
            for restrict in match.restricts:
                if restrict.name == 'page_content':
                    # Assuming the desired content is in 'allow_tokens'
                    page_contents.append(restrict.allow_tokens[0])
        return page_contents

    except IndexError as e:
        logger.error(f"Error accessing elements in API response: Index out of range - {e}")
    except KeyError as e:
        logger.error(f"Key error in accessing API safety response data; possibly malformed response - {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred - {e}")
        return []  # Return empty list on failure


if __name__ == "__main__":
    query = "How many Microsoft 365 Consumer subscribers were there as of Q2 2021?"
    pages = retrieve_top_matches(query)
    for page in pages:
        print(page[:100])  # Display the first 100 characters of each page content
