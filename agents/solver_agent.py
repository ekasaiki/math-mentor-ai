import re
from math import sqrt

def solve_problem(parsed, docs):
    topic = parsed.get("topic", "").lower()
    text = parsed.get("problem_text", "")

    # -----------------------
    # PROBABILITY
    # -----------------------
    if topic == "probability":
        if "two coins" in text and "one head" in text:
            return {
                "answer": "1/2",
                "method": "Probability formula: favorable outcomes / total outcomes",
                "steps": [
                    "Sample space: {HH, HT, TH, TT}",
                    "Favorable outcomes: {HT, TH}",
                    "Probability = 2 / 4 = 1/2"
                ]
            }

        if "dice" in text and "prime" in text:
            return {
                "answer": "1/2",
                "method": "Prime numbers on dice",
                "steps": [
                    "Prime numbers: {2, 3, 5}",
                    "Total outcomes: 6",
                    "Probability = 3 / 6 = 1/2"
                ]
            }

    # -----------------------
    # QUADRATIC
    # -----------------------
    if topic == "algebra" and "x²" in text or "x^2" in text:
        match = re.findall(r"[-+]?\d+", text)
        if len(match) >= 3:
            a, b, c = map(int, match[:3])
            D = b*b - 4*a*c
            root1 = (-b + sqrt(D)) / (2*a)
            root2 = (-b - sqrt(D)) / (2*a)

            return {
                "answer": f"x = {root1}, {root2}",
                "method": "Quadratic formula",
                "steps": [
                    "ax² + bx + c = 0",
                    "Discriminant D = b² - 4ac",
                    "Roots = (-b ± √D) / 2a"
                ]
            }

    # -----------------------
    # FALLBACK (SAFE)
    # -----------------------
    return {
        "answer": "Unable to solve with available formulas.",
        "method": "Rule-based solver",
        "steps": ["Formula not matched"]
    }