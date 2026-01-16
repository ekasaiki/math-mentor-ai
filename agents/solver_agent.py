import re
from math import sqrt

def parse_quadratic_coefficients(expr: str):
    """
    Parses ax^2 + bx + c from text like:
    x^2 - 5x + 6
    -x^2 + 4x + 1
    """
    expr = expr.replace(" ", "").replace("−", "-")

    a = re.search(r"([+-]?\d*)x\^2|([+-]?\d*)x²", expr)
    b = re.search(r"([+-]?\d+)x(?!\^)", expr)
    c = re.search(r"([+-]\d+)(?!x)", expr)

    def val(match, default=0):
        if not match:
            return default
        g = match.group(1) or match.group(2)
        if g in ["", "+"]:
            return 1
        if g == "-":
            return -1
        return int(g)

    return val(a), val(b), int(c.group(1)) if c else 0


def solve_problem(parsed, retrieved_docs):
    text = parsed["problem_text"].lower()
    topic = parsed["topic"].lower()

    # =========================
    # PROBABILITY
    # =========================
    if topic == "probability":

        if "dice" in text or "die" in text:
            if "3" in text:
                return {
                    "answer": "Probability = 1/6",
                    "used_formula": "P(E) = favourable outcomes / total outcomes",
                    "method": "Dice probability",
                }

            if "prime" in text:
                return {
                    "answer": "Prime numbers = {2,3,5}. Probability = 3/6 = 1/2",
                    "used_formula": "P(E) = favourable / total",
                    "method": "Dice probability",
                }

        if "two coins" in text and "one head" in text:
            return {
                "answer": "Sample space = {HH, HT, TH, TT}. Probability = 2/4 = 1/2",
                "used_formula": "P(E) = favourable / total",
                "method": "Coin probability",
            }

    # =========================
    # QUADRATIC EQUATION (ROOTS)
    # =========================
    if topic == "algebra" and "=" in text and ("x^2" in text or "x²" in text):

        a, b, c = parse_quadratic_coefficients(text)

        D = b*b - 4*a*c
        if D < 0:
            return {
                "answer": "No real roots",
                "used_formula": "Discriminant D = b² − 4ac",
                "method": "Quadratic equation",
            }

        r1 = (-b + sqrt(D)) / (2*a)
        r2 = (-b - sqrt(D)) / (2*a)

        return {
            "answer": f"x = {r1}, {r2}",
            "used_formula": "x = (-b ± √(b² − 4ac)) / 2a",
            "method": "Quadratic equation",
        }

    # =========================
    # QUADRATIC FUNCTION (VERTEX)
    # =========================
    if topic == "algebra" and "f(x)" in text and ("x^2" in text or "x²" in text):

        a, b, c = parse_quadratic_coefficients(text)
        xv = -b / (2*a)
        yv = a*xv*xv + b*xv + c

        nature = "maximum" if a < 0 else "minimum"

        return {
            "answer": f"Vertex at x = {xv}, y = {yv} ({nature})",
            "used_formula": "Vertex x = -b / (2a)",
            "method": "Quadratic function",
        }

    # =========================
    # FALLBACK
    # =========================
    return {
        "answer": "Unable to solve with available formulas.",
        "used_formula": "Not found",
        "method": "Unsupported",
    }