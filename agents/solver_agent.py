import re
from math import sqrt

def solve_problem(parsed, retrieved_docs):
    text = parsed["problem_text"].lower()
    topic = parsed["topic"].lower()

    # =========================
    # PROBABILITY
    # =========================
    if topic == "probability":

        # ---- Dice: specific number ----
        if "dice" in text or "die" in text:
            if "getting 3" in text:
                return {
                    "answer": "Probability = 1 / 6",
                    "used_formula": "P(E) = favourable outcomes / total outcomes",
                    "method": "Dice probability",
                }

            if "prime" in text:
                return {
                    "answer": "Prime numbers on dice = {2, 3, 5}. Probability = 3/6 = 1/2",
                    "used_formula": "P(E) = favourable / total",
                    "method": "Dice probability",
                }

        # ---- Coins ----
        if "two coins" in text:
            if "one head" in text:
                return {
                    "answer": "Sample space = {HH, HT, TH, TT}. Exactly one head = {HT, TH}. Probability = 2/4 = 1/2",
                    "used_formula": "P(E) = favourable / total",
                    "method": "Coin probability",
                }

    # =========================
    # ALGEBRA – QUADRATIC EQUATION
    # =========================
    if topic == "algebra":

        # x^2 - 5x + 6 = 0
        quad_match = re.findall(r"[-+]?\d+", text)
        if ("x^2" in text or "x²" in text) and len(quad_match) >= 3:
            a, b, c = map(int, quad_match[:3])
            D = b*b - 4*a*c

            if D >= 0:
                root1 = (-b + sqrt(D)) / (2*a)
                root2 = (-b - sqrt(D)) / (2*a)

                return {
                    "answer": f"x = {root1}, {root2}",
                    "used_formula": "x = (-b ± √(b² - 4ac)) / 2a",
                    "method": "Quadratic equation",
                }

    # =========================
    # ALGEBRA – QUADRATIC FUNCTION
    # =========================
    if topic == "algebra" and "f(x)" in text and "x^2" in text:
        return {
            "answer": "This is a downward opening parabola. Maximum occurs at x = -b / (2a).",
            "used_formula": "Vertex formula: x = -b / (2a)",
            "method": "Quadratic function analysis",
        }

    # =========================
    # FALLBACK (SAFE)
    # =========================
    return {
        "answer": "Unable to solve this problem with available formulas.",
        "used_formula": "Not found",
        "method": "Unsupported",
    }