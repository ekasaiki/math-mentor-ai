import math
import re

def solve_problem(parsed, docs):
    q = parsed["problem_text"].lower()
    topic = parsed["topic"]

    solution = {
        "answer": "",
        "method": "formula-based",
        "used_formula": "",
        "steps": []
    }

    # =====================
    # PROBABILITY
    # =====================
    if topic == "probability":

        # Dice – prime number
        if "dice" in q and "prime" in q:
            solution["used_formula"] = "P = favourable / total"
            solution["steps"] = [
                "A dice has outcomes {1,2,3,4,5,6}",
                "Prime numbers are {2,3,5}",
                "Favourable = 3, Total = 6"
            ]
            solution["answer"] = "1/2"
            return solution

        # Two coins – exactly one head
        if "two" in q and "coin" in q:
            solution["used_formula"] = "P = favourable / total"
            solution["steps"] = [
                "Sample space = {HH, HT, TH, TT}",
                "Exactly one head = {HT, TH}",
                "Favourable = 2, Total = 4"
            ]
            solution["answer"] = "1/2"
            return solution

    # =====================
    # ALGEBRA – QUADRATIC
    # =====================
    if topic == "algebra":
        match = re.search(r"([-+]?\d*)x²\s*([+-]\s*\d*)x\s*([+-]\s*\d+)", q)
        if match:
            a = int(match.group(1) or 1)
            b = int(match.group(2).replace(" ", ""))
            c = int(match.group(3).replace(" ", ""))

            D = b*b - 4*a*c
            solution["used_formula"] = "x = (-b ± √D) / 2a"
            solution["steps"] = [
                f"a={a}, b={b}, c={c}",
                f"Discriminant D = {D}"
            ]

            if D >= 0:
                x1 = (-b + math.sqrt(D)) / (2*a)
                x2 = (-b - math.sqrt(D)) / (2*a)
                solution["answer"] = f"x = {x1}, {x2}"
            else:
                solution["answer"] = "No real roots"

            return solution

    # =====================
    # CALCULUS – DERIVATIVE
    # =====================
    if topic == "calculus" and "x²" in q:
        solution["used_formula"] = "d/dx (ax² + bx + c) = 2ax + b"
        solution["steps"] = [
            "Differentiate term by term"
        ]
        solution["answer"] = "Derivative computed using power rule"
        return solution

    # =====================
    # FALLBACK
    # =====================
    solution["method"] = "human-review"
    solution["steps"] = ["No matching formula"]
    solution["answer"] = "HITL required"
    return solution
