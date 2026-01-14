import re

def extract_numbers(text):
    return list(map(int, re.findall(r"-?\d+", text)))

def solve_problem(parsed, retrieved_docs):
    topic = parsed["topic"].lower()
    question = parsed["problem_text"].lower()
    docs_text = " ".join(retrieved_docs).lower()

    # ==========================
    # PROBABILITY
    # ==========================
    if topic == "probability":

        # Detect entity
        if "dice" in question:
            total = 6
        elif "coin" in question:
            total = 2
        elif "card" in question:
            total = 52
        else:
            total = None

        if total:
            favorable = 1
            return {
                "answer": f"{favorable}/{total}",
                "steps": [
                    f"Total possible outcomes = {total}",
                    f"Favorable outcomes = {favorable}",
                    f"Probability = {favorable}/{total}"
                ]
            }

    # ==========================
    # ALGEBRA (Linear)
    # ==========================
    if topic == "algebra":
        nums = extract_numbers(question)
        if len(nums) >= 2 and "+" in question:
            c = nums[0]
            a = nums[1]
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
    # LINEAR ALGEBRA (2x2 determinant)
    # ==========================
    if topic == "linear algebra" and "determinant" in question:
        nums = extract_numbers(question)
        if len(nums) == 4:
            a, b, c, d = nums
            det = a * d - b * c
            return {
                "answer": str(det),
                "steps": [
                    f"Matrix = [[{a},{b}],[{c},{d}]]",
                    f"Determinant = ({a}×{d}) − ({b}×{c}) = {det}"
                ]
            }

    # ==========================
    # CALCULUS (basic derivative)
    # ==========================
    if topic == "calculus":
        if "x^2" in question or "x²" in question:
            return {
                "answer": "2x",
                "steps": [
                    "Using power rule",
                    "d/dx(x²) = 2x"
                ]
            }

    # ==========================
    # FALLBACK
    # ==========================
    return {
        "answer": "Unable to solve with available knowledge.",
        "steps": ["No applicable formula detected."]
    }
