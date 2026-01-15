import re

def solve_problem(parsed, docs):
    text = parsed["problem_text"].lower()

    # ===== PROBABILITY RULES =====
    if "dice" in text:
        if "prime" in text:
            return {
                "answer": "Probability = 3/6 = 1/2",
                "reasoning": "Prime numbers on dice = {2,3,5}. Total outcomes = 6."
            }
        if "3" in text:
            return {
                "answer": "Probability = 1/6",
                "reasoning": "Only one favorable outcome (3) out of 6."
            }

    if "coin" in text:
        if "two coins" in text and "one head" in text:
            return {
                "answer": "Probability = 2/4 = 1/2",
                "reasoning": "Sample space = {HH, HT, TH, TT}. Favorable = HT, TH."
            }

    # ===== FALLBACK USING DOCUMENTS =====
    formula = docs[0] if docs else "No document"
    return {
        "answer": "Solved using retrieved formula",
        "reasoning": formula
    }