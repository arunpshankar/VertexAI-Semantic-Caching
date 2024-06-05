from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import Namespace
from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from vertexai.preview.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from typing import List


NUM_NEIGHBOURS = 3  # Retrieve the top matching pages
DEPLOYED_INDEX_NAME = 'earnings_report_2024_06_04_13_27_05'
INDEX_ENDPOINT_ID = '4519278663182581760'


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
        data_dict (Dict[str, dict]): Dictionary containing data items.
    """
    index_endpoint_name = f'projects/{config.PROJECT_ID}/locations/{config.REGION}/indexEndpoints/{INDEX_ENDPOINT_ID}'
    my_index_endpoint = MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_name)

    response = my_index_endpoint.find_neighbors(deployed_index_id=DEPLOYED_INDEX_NAME, 
                                                queries=[query_embedding], 
                                                num_neighbors=NUM_NEIGHBOURS, 
                                                return_full_datapoint=True)
                                                # filter=[Namespace("doc_name", ['microsoft-q2-2022']), Namespace('page_number', ['1'])])

    for match in response[0]:
        logger.info(f"Match ID: {match.id}, Distance: {match.distance}")
        for namespace in match.restricts:
            print(f'{namespace.name} >> {namespace.allow_tokens[0]}')
        logger.info('-' * 30)


if __name__ == "__main__":
    query = "How many Microsoft 365 Consumer subscribers were there as of Q2 2021?"
    query_embedding = get_query_embedding(query)
    find_neighbors(query_embedding)
