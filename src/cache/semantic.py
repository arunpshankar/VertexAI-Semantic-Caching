from src.match.doc import retrieve_top_matches
from src.match.query import retrieve_top_match
from src.config.logging import logger
from src.generate.qa import generate_answer


def query_match(question: str):
    match = retrieve_top_match(question)
    return match


def doc_match(question: str):
    matches = retrieve_top_matches(question)
    context = '\n\n'.join(matches)
    answer = generate_answer(question, context)
    return answer


def add():
    pass


if __name__ == '__main__':
    question = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    match = query_match(question)
    answer = doc_match(question)
    print(answer)
