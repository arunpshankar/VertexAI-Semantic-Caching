
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
from google.cloud.aiplatform_v1 import IndexDatapoint
from src.index.query.encode import get_embeddings
from src.config.logging import logger 
from src.config.setup import Config

INDEX_ID = '9163826885140938752'


def stream_update_vector_search_index(query: str) -> None:
    """Stream update an existing vector search index"""

    # Create the index instance from an existing index with stream_update enabled
    my_index = MatchingEngineIndex(index_name=INDEX_ID)
    # Encode query and get embedding
    embedding = get_embeddings(query)
    index_data_point = IndexDatapoint(embedding)
    # Upsert the datapoints to the index
    my_index.upsert_datapoints(datapoints=[index_data_point])
  

if __name__ == '__main__':
    query = 'As of Q2 2023, what was the subscriber base for Microsoft 365?'
    stream_update_vector_search_index(query)