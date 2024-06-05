from vertexai.language_models import TextEmbeddingModel
from src.config.logging import logger
from src.config.setup import config
from typing import Generator
from typing import Tuple
from typing import Dict 
from typing import List
from tqdm import tqdm
import jsonlines
import os


# Initialize the model
model = TextEmbeddingModel.from_pretrained(config.TEXT_EMBED_MODEL_NAME)


def get_directory_details(base_dir: str) -> Generator[Tuple[str, str, str, str], None, None]:
    """
    Recursively iterates through a given base directory and yields file details.
    """
    logger.info(f"Scanning directory: {base_dir}")
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            yield base_dir, os.path.relpath(root, base_dir), file, file_path


def read_file(file_path: str) -> str:
    """
    Reads the content of a given file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logger.info(f"File read successfully: {file_path}")
            return content
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""


def encode_and_save(data: List[Dict[str, str]], output_path: str) -> None:
    """
    Encodes text data using the embedding model and saves as JSONL.
    """
    logger.info(f"Encoding data and saving to {output_path}")
    with jsonlines.open(output_path, mode='w') as writer:
        for item in tqdm(data):
            try:
                id_, doc_name, page_number, page_content = item.values()
                doc = {}
                doc['id'] = id_
                embedding = model.get_embeddings([page_content])[0].values
                doc['embedding'] = [val for val in embedding]
                doc['restricts'] = [{'namespace': 'doc_name', 'allow_list': [doc_name]}, {'namespace': 'page_number', 'allow': [page_number]}, {'namespace': 'page_content', 'allow': [page_content]}]
                writer.write(doc)
            except Exception as e:
                logger.error(f"Error processing item {item}: {e}")

    logger.info("Data encoding and saving completed")


if __name__ == '__main__':
    data = []
    base_dir = './data/merged'

    id_ = 1
    
    for base_dir, doc_name, _, page_path in get_directory_details(base_dir):
        content = read_file(page_path)
        if content:
            page_number = os.path.basename(page_path).split('.')[0].split('_')[-1]
            item = {'id': str(id_), 'doc_name': doc_name, 'page_number': page_number, 'page_content': content}
            data.append(item)
            id_ += 1

    output_path = './data/embeddings.json'
    encode_and_save(data, output_path)
