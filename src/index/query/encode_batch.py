from vertexai.language_models import TextEmbeddingModel
from src.cache.utils import generate_md5_hash
from src.config.logging import logger
from src.config.setup import config
from typing import List
import pandas as pd
import jsonlines


# Initialize the model
model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)


def encode_and_save(questions: List[str], output_path: str) -> None:
    """
    Encodes questions using the embedding model and saves as JSONL.
    """
    logger.info(f"Encoding data and saving to {output_path}")
    with jsonlines.open(output_path, mode='w') as writer:
        for question in questions:
            try:
                id_ = generate_md5_hash(question)
                embedding = model.get_embeddings([question])[0].values
                new_item = {
                    'datapoint_id': id_,
                    'feature_vector': [val for val in embedding],
                    'restricts': [{'namespace': 'question', 'allow_list': [question]}]
                }
                writer.write(new_item)
            except Exception as e:
                logger.error(f"Error processing question '{question}': {e}")

    logger.info("Data encoding and saving completed")


if __name__ == '__main__':
    data_path = './data/eval/ground_truth.csv'
    df = pd.read_csv(data_path)

    questions = df['question'].tolist()

    output_path = './data/query_embeddings.json'
    encode_and_save(questions, output_path)
