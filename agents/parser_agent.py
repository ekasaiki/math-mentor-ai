import re

def parse_problem(text):
    text = text.strip()

    topic = "unknown"
    if "dice" in text or "coin" in text or "probability" in text:
        topic = "probability"
    elif "determinant" in text:
        topic = "linear algebra"
    elif "find derivative" in text or "differentiate" in text:
        topic = "calculus"
    elif "=" in text:
        topic = "algebra"

    numbers = list(map(int, re.findall(r"-?\d+", text)))

    needs_clarification = len(numbers) == 0

    return {
        "problem_text": text,
        "topic": topic,
        "numbers": numbers,
        "needs_clarification": needs_clarification
    }
