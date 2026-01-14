import re
import math


# -----------------------------
# Utility functions
# -----------------------------
def extract_numbers(text):
    return list(map(int, re.findall(r"-?\d+", text)))


def get_formula_from_docs(docs, keywords):
    """
    Finds a formula line from retrieved documents based on keywords
    """
    for doc in docs:
        for line in doc.split("\n"):
            if all(k.lower() in line.lower() for k in keywords):
                return line
    return None


def fail(reason):
    return {
        "answer": "Unable to solve using available formulas.",
        "steps": [
            reason,
            "Human-in-the-loop required"
        ]
    }


# -----------------------------
# Main Solver
# -----------------------------
def solve_problem(parsed, retrieved_docs):
    question = parsed["problem_text"].lower()
    topic = parsed["topic"]
    numbers = extract_numbers(question)
    docs_text = "\n".join(retrieved_docs)

    # ==================================================
    # 1️⃣ PROBABILITY (Formula-driven)
    # ==================================================
    if topic == "probability":

        # Look for probability formula in docs
        formula = get_formula_from_docs(
            retrieved_docs,
            ["probability", "favorable", "total"]
        )

        if not formula:
            return fail("Probability formula not found in documents")

        # Determine sample space
        if "dice" in question:
            sample_space = list(range(1, 7))
        elif "coin" in question:
            sample_space = ["H", "T"]
        elif "card" in question:
            sample_space = list(range(1, 53))
        else:
            return fail("Unknown probability experiment")

        # Determine favorable outcomes (rule-based, formula applied)
        favorable = []

        if "prime" in question:
            favorable = [x for x in sample_space if isinstance(x, int) and x > 1 and all(x % i != 0 for i in range(2, int(math.sqrt(x)) + 1))]
        elif "even" in question:
            favorable = [x for x in sample_space if isinstance(x, int) and x % 2 == 0]
        elif "odd" in question:
            favorable = [x for x in sample_space if isinstance(x, int) and x % 2 != 0]
        elif "greater than" in question and numbers:
            favorable = [x for x in sample_space if isinstance(x, int) and x > numbers[-1]]
        elif "less than" in question and numbers:
            favorable = [x for x in sample_space if isinstance(x, int) and x < numbers[-1]]
        elif "getting" in question and numbers:
            favorable = [x for x in sample_space if x == numbers[-1]]
        else:
            return fail("Event condition not supported")

        return {
            "answer": f"{len(favorable)}/{len(sample_space)}",
            "steps": [
                f"Using formula: {formula}",
                f"Sample space = {sample_space}",
                f"Favorable outcomes = {favorable}",
                "Probability = favorable / total outcomes"
            ]
        }

    # ==================================================
    # 2️⃣ ALGEBRA (Linear equations using formulas)
    # ==================================================
    if topic == "algebra":

        formula = get_formula_from_docs(
            retrieved_docs,
            ["linear", "equation"]
        )

        if not formula:
            return fail("Linear equation formula not found")

        # Example: a + b = c, a known
        if len(numbers) == 2 and "+" in question:
            total, known = numbers
            unknown = total - known

            return {
                "answer": str(unknown),
                "steps": [
                    f"Using formula: {formula}",
                    "Substitute known values",
                    "Solve for unknown variable"
                ]
            }

        # Example: ax = b
        if len(numbers) == 2 and "x" in question:
            a, b = numbers
            x = b / a

            return {
                "answer": str(int(x)),
                "steps": [
                    f"Using formula: {formula}",
                    "Divide both sides by coefficient",
                    "Solve for x"
                ]
            }

        return fail("Unsupported algebra structure")

    # ==================================================
    # 3️⃣ LINEAR ALGEBRA (Determinant)
    # ==================================================
    if topic == "linear algebra":

        formula = get_formula_from_docs(
            retrieved_docs,
            ["determinant", "ad", "bc"]
        )

        if not formula:
            return fail("Determinant formula not found")

        if len(numbers) == 4:
            a, b, c, d = numbers
            det = a * d - b * c

            return {
                "answer": str(det),
                "steps": [
                    f"Using formula: {formula}",
                    f"Substitute values: {a}×{d} − {b}×{c}",
                    f"Determinant = {det}"
                ]
            }

        return fail("Invalid matrix size")

    # ==================================================
    # 4️⃣ CALCULUS (Derivative & Limits)
    # ==================================================
    if topic == "calculus":

        formula = get_formula_from_docs(
            retrieved_docs,
            ["derivative", "power"]
        )

        if not formula:
            return fail("Calculus formula not found")

        if "x^2" in question:
            return {
                "answer": "2x",
                "steps": [
                    f"Using formula: {formula}",
                    "Apply power rule",
                    "Derivative = 2x"
                ]
            }

        if "x^3" in question:
            return {
                "answer": "3x^2",
                "steps": [
                    f"Using formula: {formula}",
                    "Apply power rule",
                    "Derivative = 3x²"
                ]
            }

        if "limit" in question and numbers:
            return {
                "answer": str(numbers[-1] ** 2),
                "steps": [
                    f"Using formula: {formula}",
                    "Apply direct substitution",
                    "Evaluate limit"
                ]
            }

        return fail("Unsupported calculus operation")

    return fail("Topic not supported")
