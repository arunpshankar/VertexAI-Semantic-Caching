from vertexai.language_models import TextEmbeddingModel
from src.cache.utils import generate_md5_hash
from src.config.logging import logger
from src.config.setup import config 
from typing import Optional
from typing import Dict
from typing import Any


# Initialize the text embedding model
model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)

def get_embeddings(question: str) -> Optional[Dict[str, Any]]:
    """
    Encode a question and returns a dictionary with metadata and embedding.

    Args:
    question (str): The question to be encoded.

    Returns:
    Optional[Dict[str, Any]]: A dictionary with the embedding and metadata, or None if an error occurs.
    """
    logger.info(f"Encoding question: {question}")
    try:
        id_ = generate_md5_hash(question)
        embedding = model.get_embeddings([question])[0].values
        embedding_dict = {
            'id': id_,
            'embedding': [val for val in embedding],
            'restricts': [{'namespace': 'question', 'allow': [question]}]
        }
        return embedding_dict
    except Exception as e:
        logger.error(f"Error processing question '{question}': {e}")
        return None


if __name__ == '__main__':
    query = "As of Q2 2023, what was the subscriber base for Microsoft 365?"
    response = get_embeddings(query)
    print(response)
