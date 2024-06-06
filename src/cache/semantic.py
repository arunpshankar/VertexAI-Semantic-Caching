from src.match.doc import retrieve_top_matches
from src.match.query import retrieve_top_match
from src.config.logging import logger


def query_match(question: str):
    match = retrieve_top_match(question)
    print(match)


def doc_match():
    matches = retrieve_top_matches(question)
    context = '\n\n'.join(matches)
       




def add():
    pass



if __name__ == '__main__':
    question = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    answer = query_match(question)