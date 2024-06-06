from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from vertexai.preview.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from typing import List


def get_query_embedding(query: str) -> List[float]:
    """Generates embeddings for a given query.

    Args:
        query (str): The query string.

    Returns:
        List[float]: The query embeddings.
    """
    model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)
    return model.get_embeddings([query])[0].values


def find_neighbors(query_embedding: List[float], deployed_index_name: str, index_endpoint_id: str, num_neighbors: int):
    """
    Finds neighbors for the given query embedding and logs results.

    Args:
        query_embedding (List[float]): The query embeddings.
        deployed_index_name (str): The name of the deployed index.
        index_endpoint_id (str): The ID of the index endpoint.
        num_neighbors (int): The number of neighbors to return.
    """
    try:
        index_endpoint_name = f'projects/{config.PROJECT_ID}/locations/{config.REGION}/indexEndpoints/{index_endpoint_id}'
        my_index_endpoint = MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_name)

        response = my_index_endpoint.find_neighbors(deployed_index_id=deployed_index_name, 
                                                    queries=[query_embedding], 
                                                    num_neighbors=num_neighbors, 
                                                    return_full_datapoint=True)
        logger.info("Neighbors found successfully.")
        return response
    except Exception as e:
        logger.error(f"Failed to find neighbors: {e}")
        return None
