from src.generate.llm import LLM


llm = LLM()


def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer to a given question based on the provided context leveraging LLM.

    Args:
    question (str): The question to answer.
    context (str): The context that informs the answer.

    Returns:
    str: The predicted answer.
    """
    prompt = f"""
    Based on the following context, provide a clear and concise answer to the question below:
    Context: {context}
    Question: {question}
    """
    return llm.predict(task=prompt, query=question)

if __name__ == '__main__':
    context = """We're very pleased with the ongoing momentum in Google Cloud, with revenues of $4.0 billion in the quarter reflecting strength and opportunity in both GCP and Workspace.” Q1 2021 financial highlights The following table summarizes our consolidated financial results for the quarters ended March 31, 2020 and 2021 (in millions, except for per share information and percentages; unaudited).
Segment results The following table presents our revenues and operating income (loss) (in millions; unaudited): Quarter Ended March 31, 2020 2021 Revenues: Google Services $ 38198 $ 51178 Google Cloud 2777 4047 Other Bets 135 198 Hedging gains (losses) 49 (109) Total revenues $ 41159 $ 55314 Quarter Ended March 31, 2020 2021 Operating income (loss): Google Services $ 11548 $ 19546 Google Cloud (1730) (974) Other Bets (1121) (1145) Corporate costs, unallocated (720) (990) Total income from operations $ 7977 $ 16437 We report our segment results as Google Services, Google Cloud, and Other Bets: • Google Services includes products and services such as ads, Android, Chrome, hardware, Google Maps, Google Play, Search, and YouTube.
This change in accounting estimate was effective beginning in fiscal year 2021 and the effect for the three months ended March 31, 2021, was a reduction in depreciation expense of $835 million and an increase in net income of $650 million, or $0.97 per basic and $0.95 per diluted share. Ref:[alphabet-q1-2021]
"""
    question = "What was the operating income or loss (in billions) for Google Cloud for Q1 of 2021 compared to the previous year?"
    answer = generate_answer(question, context)
    print(answer)
