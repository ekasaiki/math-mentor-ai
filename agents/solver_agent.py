
import re

def extract_numbers(text):
    return list(map(int, re.findall(r"-?\d+", text)))

def solve_problem(parsed, retrieved_docs):
    topic = parsed["topic"].lower()
    question = parsed["problem_text"].lower()
    docs = " ".join(retrieved_docs).lower()

    # ==========================
    # PROBABILITY (Dice, Coin, Cards)
    # ==========================
    if topic == "probability" and "probability =" in docs:

        total = None
        if "dice" in question and "dice = 6" in docs:
            total = 6
        elif "coin" in question and "coin = 2" in docs:
            total = 2
        elif "card" in question and "cards = 52" in docs:
            total = 52

        if total:
            favorable = 1
            return {
                "answer": f"{favorable}/{total}",
                "steps": [
                    f"Total outcomes = {total}",
                    f"Favorable outcomes = {favorable}",
                    f"Probability = {favorable}/{total}"
                ]
            }

    # ==========================
    # ALGEBRA (Linear equations)
    # ==========================
    if topic == "algebra" and "b = c - a" in docs:
        nums = extract_numbers(question)
        if len(nums) >= 2:
            c, a = nums[0], nums[1]
            b = c - a
            return {
                "answer": f"b = {b}",
                "steps": [
                    f"Given a + b = {c}",
                    f"Given a = {a}",
                    f"b = {c} - {a} = {b}"
                ]
            }

    # ==========================
    # LINEAR ALGEBRA (Determinant)
    # ==========================
    if topic == "linear algebra" and "determinant = ad - bc" in docs:
        nums = extract_numbers(question)
        if len(nums) == 4:
            a, b, c, d = nums
            det = a*d - b*c
            return {
                "answer": str(det),
                "steps": [
                    f"Matrix = [[{a},{b}],[{c},{d}]]",
                    f"Determinant = ({a}×{d}) − ({b}×{c}) = {det}"
                ]
            }

    # ==========================
    # CALCULUS (Derivatives)
    # ==========================
    if topic == "calculus" and "d/dx" in docs:
        if "x^2" in question:
            return {
                "answer": "2x",
                "steps": [
                    "Using power rule",
                    "d/dx (x²) = 2x"
                ]
            }

    # ==========================
    # FALLBACK (HITL)
    # ==========================
    return {
        "answer": "Unable to solve with available knowledge.",
        "steps": ["No matching formula found in retrieved documents."]
    }
