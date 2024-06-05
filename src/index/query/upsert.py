from src.config.logging import logger 
from src.config.setup import Config
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex

INDEX_NAME = 'queries_2024_06_05_09_48_30'


def stream_update_vector_search_index(query: str):
    """Stream update an existing vector search index"""

    # Create the index instance from an existing index with stream_update enabled
    my_index = MatchingEngineIndex(index_name=INDEX_NAME)
    # Upsert the datapoints to the index
    response = my_index.upsert_datapoints(datapoints=query)
    print(response)



if __name__ == '__main__':
    query = 'As of Q2 2023, what was the subscriber base for Microsoft 365?'
    stream_update_vector_search_index(query)

