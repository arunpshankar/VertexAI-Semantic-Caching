from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
from google.cloud.aiplatform_v1 import IndexDatapoint
from src.index.query.encode import get_embeddings
from src.match.utils import get_query_embedding
from src.match.query import retrieve_top_match
from src.match.utils import find_neighbors
from src.config.logging import logger 
from src.config.setup import *
import time 


NUM_NEIGHBOURS = 1  # Retrieve the top matching neighbor (query)
DEPLOYED_INDEX_NAME = 'queries_2024_06_06_10_49_50'
INDEX_ENDPOINT_ID = '5044159126003777536'
INDEX_ID = '8030608628903837696'

def stream_update(query: str) -> None:
    """
    Stream update an existing vector search index with the given query.

    Args:
        query (str): The query to encode and upsert into the vector search index.
    """
    try:
        # Create the index instance from an existing index with stream_update enabled
        my_index = MatchingEngineIndex(index_name=INDEX_ID)
        logger.info("Index instance created successfully.")

        # Encode query and get embedding
        embedding = get_embeddings(query)
        if embedding is None:
            logger.error("Failed to get embeddings; the embedding is None.")
            return
        logger.info("Query encoded into embeddings.")

        # Upsert the datapoints to the index
        index_data_point = IndexDatapoint(embedding)
        my_index.upsert_datapoints(datapoints=[index_data_point])
        logger.info("Datapoint upserted successfully.")
    
    except Exception as e:
        logger.error("Failed to update the vector search index: %s", e)

if __name__ == '__main__':
    # Start the stream update process for the vector search index
    query = 'As of Q2 2023, what was the subscriber base for Microsoft 365?'
    stream_update(query)

    # Test upsert action by performing semantic search 
    query = 'As of Q2 2023, what was the subscriber count for Microsoft 365?'
    query_embedding = get_query_embedding(query)
    response = find_neighbors(query_embedding, DEPLOYED_INDEX_NAME, INDEX_ENDPOINT_ID, NUM_NEIGHBOURS)
    top_match = retrieve_top_match(response)
    print(top_match)
