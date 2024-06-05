from src.index.utils import upload_file_to_bucket
from src.index.utils import get_timestamp
from src.index.utils import create_bucket
from src.config.logging import logger
from src.config.setup import config
from google.cloud import aiplatform


# Constants
DIMENSIONS = 768  # Maps to Text-Gecko model's output dimensions
APPROXIMATE_NEIGHBORS_COUNT = 5
DISTANCE_MEASURE_TYPE = 'COSINE_DISTANCE'
SOURCE_FILE = './data/embeddings.json'
DESTINATION_BLOB_NAME = 'embeddings/embeddings.json'
DESCRIPTION = "Index of document page embeddings for streamlined analysis of FAANG companies' earnings reports."

def create_index(bucket_name: str) -> None:
    """
    Create an index using Vertex AI Vector Search.

    Args:
        bucket_name (str): Name of the bucket where embeddings are stored.
    """
    timestamp = get_timestamp()
    display_name = f'earnings_report_{timestamp}'
    bucket_uri = f'gs://{bucket_name}'
    embeddings_remote_uri = f'{bucket_uri}/embeddings'

    try:
        aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=display_name,
            description=DESCRIPTION,
            contents_delta_uri=embeddings_remote_uri,
            dimensions=DIMENSIONS,
            approximate_neighbors_count=APPROXIMATE_NEIGHBORS_COUNT,
            distance_measure_type=DISTANCE_MEASURE_TYPE
        )
    except Exception as e:
        logger.error("Failed to create the index: %s", e)


if __name__ == "__main__":
    bucket = config.BUCKET

    # Ensure the bucket exists
    create_bucket(bucket, config.REGION, config.PROJECT_ID)

    # Upload the embeddings file
    upload_file_to_bucket(bucket, SOURCE_FILE, DESTINATION_BLOB_NAME)

    # Create the index
    create_index(bucket)