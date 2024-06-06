from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from vertexai.preview.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from typing import List
from typing import Dict
from typing import Any 


NUM_NEIGHBOURS = 3  # Retrieve the top matching pages
DEPLOYED_INDEX_NAME = 'earnings_report_2024_06_06_07_11_43'
INDEX_ENDPOINT_ID = '2462259533381107712'

def get_query_embedding(query: str) -> List[float]:
    """Generates embeddings for a given query.

    Args:
        query (str): The query string.

    Returns:
        List[float]: The query embeddings.
    """
    model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)
    return model.get_embeddings([query])[0].values


def find_neighbors(query_embedding: List[float]):
    """
    Finds neighbors for the given query embedding and logs results.

    Args:
        query_embedding (List[float]): The query embeddings.
    """
    index_endpoint_name = f'projects/{config.PROJECT_ID}/locations/{config.REGION}/indexEndpoints/{INDEX_ENDPOINT_ID}'
    my_index_endpoint = MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_name)

    response = my_index_endpoint.find_neighbors(deployed_index_id=DEPLOYED_INDEX_NAME, 
                                                queries=[query_embedding], 
                                                num_neighbors=NUM_NEIGHBOURS, 
                                                return_full_datapoint=True)
                                                # filter=[Namespace("doc_name", ['microsoft-q2-2022']), Namespace('page_number', ['1'])])
    return response

    for match in response[0]:
        logger.info(f"Match ID: {match.id}, Distance: {match.distance}")
        for namespace in match.restricts:
            print(f'{namespace.name} >> {namespace.allow_tokens[0]}')
        logger.info('-' * 30)


def extract_page_content(api_response: List[Dict[str, Any]]) -> List[str]:
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
        logger.error("Error accessing elements in the API response: Index out of range", exc_info=True)
    except KeyError as e:
        logger.error("Key error in accessing API response data; possibly malformed response", exc_info=True)
    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
    return page_contents

if __name__ == "__main__":
    query = "How many Microsoft 365 Consumer subscribers were there as of Q2 2021?"
    query_embedding = get_query_embedding(query)
    response = find_neighbors(query_embedding)
    pages = extract_page_content(response)
    for page in pages:
        print(page[:100])
