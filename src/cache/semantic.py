from src.index.query.upsert import stream_update
from src.match.doc import retrieve_top_matches
from src.match.query import retrieve_top_match
from src.generate.qa import generate_answer
from src.config.logging import logger
from typing import Optional


def query_match(question: str) -> Optional[str]:
    """
    Retrieve the top match for a given question.
    
    Args:
        question (str): The question to query.

    Returns:
        Optional[str]: The top matching document or None if no match found.
    """
    try:
        match = retrieve_top_match(question)
        if match:
            logger.info(f"Top match found: {match}")
        else:
            logger.info("No match found.")
        return match
    except Exception as e:
        logger.error(f"Failed to retrieve top match: {e}", exc_info=True)
        return None


def doc_match(question: str) -> str:
    """
    Generate an answer from top document matches.
    
    Args:
        question (str): The question to answer.

    Returns:
        str: The generated answer.
    """
    try:
        matches = retrieve_top_matches(question)
        if not matches:
            logger.warning("No matches found for document matching.")
            return "No relevant documents found."
        
        context = '\n\n'.join(matches)
        answer = generate_answer(question, context)
        logger.info("Answer generated successfully.")
        return answer
    except Exception as e:
        logger.error(f"Error in generating answer: {e}", exc_info=True)
        return "Failed to generate an answer due to internal error."


def add(question: str) -> None:
    """
    Add a new question to the stream for updating.
    
    Args:
        question (str): The question to add.
    """
    try:
        stream_update(question)
        logger.info(f"Question added to stream: {question}")
    except Exception as e:
        logger.error(f"Failed to add question: {e}")


if __name__ == '__main__':
    question = "What was the operating income/loss for Google Cloud for Q1 of 2021 compared to the previous year?"
    try:
        match = query_match(question)
        print(match)
        answer = doc_match(question)
        print(answer)
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {e}", exc_info=True)
