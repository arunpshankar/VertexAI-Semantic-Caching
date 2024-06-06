from src.index.utils import create_endpoint
from src.index.utils import list_indexes
from src.index.utils import deploy_index
from src.config.logging import logger
from src.index.utils import match
from src.config.setup import *


INDEX_DISPLAY_NAME = 'earnings_report_2024_06_06_09_32_39'
INDEX_ENDPOINT_DISPLAY_NAME = f'{INDEX_DISPLAY_NAME}_index_endpoint'
INDEX_ENDPOINT_DESCRIPTION = "Endpoint for page embeddings index of FAANG companies' earnings reports."

def run():
    """
    Deploys a search index for page emebeddings of earnings reports to an API endpoint.

    This script lists available indexes, matches a specific index based on its display name,
    and then creates and deploys an endpoint for that index if it exists.
    """
    # List all available indexes
    indexes = list_indexes()

    # Define the index to match
    index_resource_name = match(INDEX_DISPLAY_NAME, indexes)

    # Log the outcome of the index search
    if index_resource_name:
        logger.info(f"Found index: {index_resource_name}")
    else:
        logger.warning("Index not found.")
        return  # Exit if no index is found

    # Define and create an endpoint for the index
    endpoint = create_endpoint(INDEX_ENDPOINT_DISPLAY_NAME, INDEX_ENDPOINT_DESCRIPTION)

    # Deploy the index to the created endpoint
    deploy_index(endpoint, index_resource_name, INDEX_DISPLAY_NAME)


if __name__ == '__main__':
    run()