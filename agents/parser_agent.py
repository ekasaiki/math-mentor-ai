import re

def parse_problem(text):
    text_l = text.lower()

    if any(k in text_l for k in ["dice", "coin", "probability", "card"]):
        topic = "probability"
    elif any(k in text_l for k in ["x²", "quadratic", "ax²"]):
        topic = "algebra"
    elif any(k in text_l for k in ["derivative", "limit", "maximum", "minimum"]):
        topic = "calculus"
    else:
        topic = "unknown"

    return {
        "topic": topic,
        "problem_text": text,
        "needs_clarification": topic == "unknown"
    }
