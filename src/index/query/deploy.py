from src.index.utils import create_endpoint
from src.index.utils import list_indexes
from src.index.utils import deploy_index
from src.config.logging import logger
from src.index.utils import match


if __name__ == '__main__':
    indexes = list_indexes()
    index_display_name = 'queries_2024_06_05_09_48_30'
    index_resource_name = match(index_display_name, indexes)

    if index_resource_name:
        logger.info(f"Found index: {index_resource_name}")
    else:
        logger.warning("Index not found.")

    index_endpoint_display_name = f'{index_display_name}_index_endpoint'
    index_endpoint_description = "Endpoint for index of query embeddings for FAANG companies' earnings reports."

    endpoint = create_endpoint(index_endpoint_display_name, index_endpoint_description)
    deploy_index(endpoint, index_resource_name, index_display_name)
