from google.cloud.aiplatform import MatchingEngineIndexEndpoint
from google.cloud.aiplatform import MatchingEngineIndex
from google.api_core.exceptions import Conflict
from src.config.logging import logger
from google.cloud import storage
from datetime import datetime
from typing import List 


def get_timestamp() -> str:
    """
    Fetches current date and time (up to seconds). 

    Returns:
        str: Timestamp string in the format 'YYYY_MM_DD_HH_MM_SS'.
    """
    try:
        now = datetime.now()
        timestamp_str = now.strftime("%Y_%m_%d_%H_%M_%S")
        return timestamp_str
    except Exception as e:  # Broad exception handling (refine for specific errors)
        logger.error(f"An error occurred while generating the timestamp: {e}")


def create_bucket(bucket_name: str, location: str, project_id: str) -> None:
    """
    Create a new bucket in Google Cloud Storage (GCS). If the bucket already exists,
    a message is logged stating that the bucket exists.

    Args:
    bucket_name (str): Name of the bucket to create.
    location (str): Location where the bucket will be created.
    project_id (str): Google Cloud project ID.
    """
    try:
        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        bucket.create(location=location)
        logger.info(f"Created bucket {bucket_name} in {location}")
    except Conflict:
        logger.info(f"Bucket {bucket_name} already exists. Proceeding with the existing bucket.")


def upload_file_to_bucket(bucket_name: str, source_file_name: str, destination_blob_name: str) -> None:
    """
    Uploads a file to the bucket.

    Args:
    bucket_name (str): Name of the bucket.
    source_file_name (str): Local path to the file.
    destination_blob_name (str): Destination path name for the file in the bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    logger.info(f"File {source_file_name} uploaded to {destination_blob_name}.")

    
def list_indexes() -> List[MatchingEngineIndex]:
    """
    List all AI Platform indexes for a specified Google Cloud project and location.

    Returns:
        List[aiplatform.MatchingEngineIndex]: A list of AI Platform index objects.
    """
    return MatchingEngineIndex.list()


def match(display_name: str, indexes: List[MatchingEngineIndex]) -> str:
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


def create_endpoint(display_name: str, description: str) -> MatchingEngineIndexEndpoint:
    """
    Create an AI Platform Matching Engine Index Endpoint.

    Args:
        display_name (str): The display name for the endpoint.
        description (str): A description of the endpoint.

    Returns:
        aiplatform.MatchingEngineIndexEndpoint: The created index endpoint object.
    """
    index_endpoint = MatchingEngineIndexEndpoint.create(
        display_name=display_name, 
        description=description, 
        public_endpoint_enabled=True
    )
    return index_endpoint


def deploy_index(endpoint: MatchingEngineIndexEndpoint, index_resource_name: str, index_display_name: str) -> None:
    """
    Deploy an index to a specified endpoint.

    Args:
        endpoint (aiplatform.MatchingEngineIndexEndpoint): The endpoint for deployment.
        index_resource_name (str): The resource name of the index.
        index_display_name (str): The display name of the index.

    Returns:
        None
    """
    tree_ah_index = MatchingEngineIndex(index_name=index_resource_name)
    endpoint.deploy_index(index=tree_ah_index, deployed_index_id=index_display_name)
   