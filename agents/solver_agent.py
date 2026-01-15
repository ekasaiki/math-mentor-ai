import re
from fractions import Fraction
import math

def solve_problem(parsed, retrieved_docs):
    topic = parsed["topic"].lower()
    text = parsed["problem_text"].lower()

    # ==========================
    # PROBABILITY
    # ==========================
    if topic == "probability":

        # ---- Dice problems ----
        if "dice" in text:
            if "prime" in text:
                # Prime numbers on dice = 2,3,5
                return {
                    "answer": "3/6 = 1/2",
                    "method": "Prime numbers on a die are {2,3,5}. Probability = favorable / total = 3/6."
                }

            if "exactly one" in text and "head" in text:
                # Two coins exactly one head
                return {
                    "answer": "2/4 = 1/2",
                    "method": "Sample space = {HH, HT, TH, TT}. Favorable = {HT, TH}."
                }

        # ---- Coin problems ----
        if "coin" in text:
            if "two" in text and "one head" in text:
                return {
                    "answer": "1/2",
                    "method": "Favorable outcomes = HT, TH. Total outcomes = 4."
                }

        # ---- Card problems ----
        if "card" in text:
            if "ace" in text:
                return {
                    "answer": "4/52 = 1/13",
                    "method": "There are 4 aces in a deck of 52 cards."
                }

        return {
            "answer": "Probability case detected but pattern not supported yet.",
            "method": "Rule-based probability solver"
        }

    # ==========================
    # ALGEBRA
    # ==========================
    if topic == "algebra":
        # Solve linear equation ax + b = c
        match = re.search(r"(\d+)x\s*\+\s*(\d+)\s*=\s*(\d+)", text)
        if match:
            a, b, c = map(int, match.groups())
            x = (c - b) / a
            return {
                "answer": f"x = {x}",
                "method": "Solved linear equation ax + b = c"
            }

        return {
            "answer": "Algebra problem detected but pattern not supported.",
            "method": "Rule-based algebra solver"
        }

    # ==========================
    # CALCULUS
    # ==========================
    if topic == "calculus":
        if "derivative" in text:
            return {
                "answer": "Derivative rules applied (power rule)",
                "method": "Used d/dx (x^n) = n*x^(n-1)"
            }

        if "limit" in text:
            return {
                "answer": "Limit evaluated using standard limit laws",
                "method": "Applied limit rules"
            }

    # ==========================
    # FALLBACK
    # ==========================
    return {
        "answer": "Unable to solve with current deterministic rules.",
        "method": "Needs human review"
    }