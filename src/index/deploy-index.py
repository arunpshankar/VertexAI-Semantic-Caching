from src.config.logging import logger
from src.config.setup import config
from google.cloud import aiplatform
from typing import List


def list_indexes() -> List[aiplatform.MatchingEngineIndex]:
    """
    List all AI Platform indexes for a specified Google Cloud project and location.

    Returns:
        List[aiplatform.MatchingEngineIndex]: A list of AI Platform index objects.
    """
    return aiplatform.MatchingEngineIndex.list()


def match(display_name: str, indexes: List[aiplatform.MatchingEngineIndex]) -> str:
    """
    Find and return the resource name of an index matching a given display name.

    Args:
        display_name (str): The display name to match.
        indexes (List[aiplatform.MatchingEngineIndex]): A list of index objects to search through.

    Returns:
        str: The resource name of the matching index, or an empty string if no match is found.
    """
    for index in indexes:
        if display_name == index.display_name:
            index_resource_name = f'projects/{index.project}/locations/{index.location}/indexes/{index.name}'
            return index_resource_name
    return ""


def create_endpoint(display_name: str, description: str) -> aiplatform.MatchingEngineIndexEndpoint:
    """
    Create an AI Platform Matching Engine Index Endpoint.

    Args:
        display_name (str): The display name for the endpoint.
        description (str): A description of the endpoint.

    Returns:
        aiplatform.MatchingEngineIndexEndpoint: The created index endpoint object.
    """
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name=display_name, 
        description=description, 
        public_endpoint_enabled=True
    )
    return index_endpoint


def deploy_index(endpoint: aiplatform.MatchingEngineIndexEndpoint, index_resource_name: str, index_display_name: str) -> None:
    """
    Deploy an index to a specified endpoint.

    Args:
        endpoint (aiplatform.MatchingEngineIndexEndpoint): The endpoint for deployment.
        index_resource_name (str): The resource name of the index.
        index_display_name (str): The display name of the index.

    Returns:
        None
    """
    tree_ah_index = aiplatform.MatchingEngineIndex(index_name=index_resource_name)
    endpoint.deploy_index(index=tree_ah_index, deployed_index_id=index_display_name)
   

if __name__ == '__main__':
    indexes = list_indexes()
    index_display_name = 'earnings_report'
    index_resource_name = match(index_display_name, indexes)

    if index_resource_name:
        logger.info(f"Found index: {index_resource_name}")
    else:
        logger.warning("Index not found.")

    index_endpoint_display_name = f'{index_display_name}_index_endpoint'
    index_endpoint_description = "Endpoint for index of vector embeddings for FAANG companies' earnings reports."

    endpoint = create_endpoint(index_endpoint_display_name, index_endpoint_description)
    deploy_index(endpoint, index_resource_name, index_display_name)
