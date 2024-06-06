from vertexai.language_models import TextGenerationModel
from src.config.logging import logger
from src.config.setup import config

# Constants
MODEL_NAME = 'text-unicorn@001'
MAX_OUTPUT_TOKENS = 1024
QUERY = "What is the greatest movie ever made?"


def parse_query_response(response):
    """
    Parses the response string into a list of query variations.

    Parameters:
    response (str): The response string containing query variations separated by a pipe (|).

    Returns:
    list: A list of query variations.
    """
    # Splitting the response string by pipe and trimming any leading/trailing whitespace from each element
    query_variations = [variation.strip() for variation in response.split('|')]
    return query_variations


def generate_query_variations(query):
    """
    Generates variations of a given search query using a pretrained language model.

    Parameters:
    query (str): The original search query.

    Returns:
    str: A string containing variations of the query separated by a pipe (|).
    """
    try:
        prompt = f"Given a user's search query targeting specific PDF files, create three variations of the original query. Use the provided query below to generate the variants.\n\nQuery:\n{query}\n\nReturn the expanded queries as a string, separated by a pipe (|), without linebreaks."
        model = TextGenerationModel.from_pretrained(MODEL_NAME)
        response = model.predict(prompt, max_output_tokens=MAX_OUTPUT_TOKENS)
        return response.text
    except Exception as e:
        logger.error(f"Error in generate_query_variations: {e}")
        raise

if __name__ == '__main__':
    query = 'How many additional stocks did the Board of Directors of Alphabet authorize to repurchase in Q1 of 2021?'
    response = generate_query_variations(query)
    query_variations = parse_query_response(response)

    for variation in query_variations:
        logger.info(variation)
