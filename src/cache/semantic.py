from src.index.query.upsert import stream_update
from src.match.doc import retrieve_top_matches
from src.match.query import retrieve_top_match
from src.generate.qa import generate_answer
from src.config.logging import logger


def query_match(question: str):
    match = retrieve_top_match(question)
    return match


def meets_threshold(confidence: float) -> bool:
    return False

def doc_match(question: str):
    matches = retrieve_top_matches(question)
    context = '\n\n'.join(matches)
    answer = generate_answer(question, context)
    return answer


def add(question):
    stream_update(question)


if __name__ == '__main__':
    question = "What was the operating income/loss for Google Cloud for Q1 of 2021 compared to the previous year?"
    match = query_match(question)
    print(match)
    answer = doc_match(question)
    print(answer)
