import re

def solve_problem(parsed, retrieved_docs):
    topic = parsed["topic"]
    text = parsed["problem_text"].lower()

    # ---------- PROBABILITY ----------
    if topic == "probability":

        if "dice" in text:
            if "prime" in text:
                return {
                    "answer": "Probability = 3/6 = 1/2",
                    "used_formula": "P(E) = favorable / total outcomes",
                    "method": "dice-prime"
                }

            if "3" in text:
                return {
                    "answer": "Probability = 1/6",
                    "used_formula": "P(E) = favorable / total outcomes",
                    "method": "dice-single-number"
                }

        if "coin" in text and "two" in text:
            return {
                "answer": "Probability = 2/4 = 1/2",
                "used_formula": "Sample space = {HH, HT, TH, TT}",
                "method": "two-coins"
            }

    # ---------- QUADRATIC ----------
    if topic == "algebra" and "x²" in text or "x^2" in text:
        return {
            "answer": "This is a quadratic function. Vertex form can be used.",
            "used_formula": "x = -b / (2a)",
            "method": "quadratic-analysis"
        }

    return {
        "answer": "Unable to solve with available formulas.",
        "used_formula": None,
        "method": "unsupported"
    }