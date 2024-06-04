from vertexai.preview.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from google.cloud import aiplatform
from typing import Dict
from typing import List
import jsonlines


NUM_NEIGHBOURS = 3 # Retrieve the top matching page

FILE_PATH = './data/data.jsonl'
DEPLOYED_INDEX_ID = 'earnings_report'
INDEX_ENDPOINT_ID = '1487511689032105984'


def read_jsonl(file_path: str) -> Dict[str, dict]:
    """Reads a JSONL file and returns a dictionary with 'id' as the key.

    Args:
        file_path (str): Path to the JSONL file.

    Returns:
        Dict[str, dict]: A dictionary of the data.
    """
    data_dict = {}
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            data_dict[obj['id']] = {k: v for k, v in obj.items() if k != 'id'}
    return data_dict


def get_query_embedding(query: str) -> List[float]:
    """Generates embeddings for a given query.

    Args:
        query (str): The query string.

    Returns:
        List[float]: The query embeddings.
    """
    model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)
    return model.get_embeddings([query])[0].values


def find_neighbors(query_embedding: List[float], data_dict: Dict[str, dict]):
    """Finds neighbors for the given query embedding and logs results.

    Args:
        query_embedding (List[float]): The query embeddings.
        data_dict (Dict[str, dict]): Dictionary containing data items.
    """
    index_endpoint_name = f'projects/{config.PROJECT_ID}/locations/{config.REGION}/indexEndpoints/{INDEX_ENDPOINT_ID}'
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_name)

    response = my_index_endpoint.find_neighbors(deployed_index_id=DEPLOYED_INDEX_ID, 
                                                queries=[query_embedding], 
                                                num_neighbors=NUM_NEIGHBOURS)

    for match in response[0]:
        logger.info(f"Match ID: {match.id}, Distance: {match.distance}")
        item = data_dict[match.id]
        logger.info(f"Document: {item['doc_name']}, Page: {item['page_number']}")
        #logger.info(item['page_content'])
        logger.info('-' * 30)


def main():
    data_dict = read_jsonl(FILE_PATH)
    query = "How many Microsoft 365 Consumer subscribers were there as of Q2 2021?"
    query_embedding = get_query_embedding(query)
    find_neighbors(query_embedding, data_dict)


if __name__ == "__main__":
    main()
