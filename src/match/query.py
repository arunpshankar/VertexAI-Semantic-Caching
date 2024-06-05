from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from vertexai.preview.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from typing import List


NUM_NEIGHBOURS = 3  # Retrieve the top matching queries
DEPLOYED_INDEX_NAME = 'queries_2024_06_05_09_48_30'
INDEX_ENDPOINT_ID = '9216533074530009088'


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

    
    for match in response[0]:
        logger.info(f"Match ID: {match.id}, Distance: {round(1 - match.distance, 4)}")
        for namespace in match.restricts:
            print(f'{namespace.name} >> {namespace.allow_tokens[0]}')
        logger.info('-' * 30)
    


if __name__ == "__main__":
    query = "How many Microsoft 365 subscribers were there as of Q2 2023?"
    query_embedding = get_query_embedding(query)
    find_neighbors(query_embedding)
