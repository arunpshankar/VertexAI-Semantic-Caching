from src.config.logging import logger
from src.generate.llm import LLM
from typing import Optional


class QuestionVariantGenerator:
    """
    A class to generate semantic variants of search questions using an LLM model.
    """
    
    def __init__(self):
        """
        Initialize the QuestionVariantGenerator with an instance of LLM.
        """
        self.llm = LLM()

    def generate_variant(self, question: str) -> Optional[str]:
        """
        Generate a semantic variant of a given search question.

        Parameters:
        question (str): The original search question.

        Returns:
        Optional[str]: A semantic variant of the provided question or None if an error occurs.
        """
        prompt = f"""
        Given a user's question targeting specific PDF files, create a semantic variant of the original question.
        Use the provided question below to generate the variant. Return only the variant without any formatting or explanation.
        Question: {question}
        """
        try:
            return self.llm.predict(task=prompt, query=question)
        except Exception as e:
            logger.error(f"Error when generating variant: {e}", exc_info=True)
            return None


if __name__ == '__main__':
    generator = QuestionVariantGenerator()
    query = 'How many additional stocks did the Board of Directors of Alphabet authorize to repurchase in Q1 of 2021?'
    response = generator.generate_variant(query)
    if response:
        logger.info(f"Generated Variant: {response}")
    else:
        logger.error("Failed to generate a variant.")
