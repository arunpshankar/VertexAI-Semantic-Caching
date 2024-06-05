from src.index.utils import get_timestamp
from src.index.utils import create_bucket
from src.config.logging import logger
from src.config.setup import config
from google.cloud import aiplatform
from google.cloud import storage


def create_index(bucket_name: str) -> None:
    """
    Create an index using Vertex AI Vector Search.

    Args:
    bucket_name (str): Name of the bucket where embeddings are stored.
    """
    timestamp = get_timestamp()
    DISPLAY_NAME = f'earnings_report_{timestamp}'
    DESCRIPTION = "Index of vector embeddings for streamlined analysis of FAANG companies' earnings reports."

    BUCKET_URI = f'gs://{bucket_name}'
    EMBEDDINGS_REMOTE_URI = f'{BUCKET_URI}/embeddings'

    # Hyperparameters
    DIMENSIONS = 768  # Maps to Text-Gecko model's output dimensions 
    APPROXIMATE_NEIGHBORS_COUNT = 5 
    DISTANCE_MEASURE_TYPE = 'COSINE_DISTANCE' 

    aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=DISPLAY_NAME,
            description=DESCRIPTION,
            contents_delta_uri=EMBEDDINGS_REMOTE_URI,
            dimensions=DIMENSIONS,
            approximate_neighbors_count=APPROXIMATE_NEIGHBORS_COUNT,
            distance_measure_type=DISTANCE_MEASURE_TYPE
            )


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


if __name__ == "__main__":
    # Create a bucket
    bucket = config.BUCKET
    create_bucket(bucket, config.REGION, config.PROJECT_ID)

    # Upload a file to the bucket
    source_file = './data/embeddings.json' 
    destination_blob_name = 'embeddings/embeddings.json' 
    upload_file_to_bucket(bucket, source_file, destination_blob_name)

    # Create an index
    create_index(bucket)