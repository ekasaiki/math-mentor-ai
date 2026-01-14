import re
from math import prod

# ---------------------------
# Utilities
# ---------------------------
def extract_numbers(text):
    return list(map(int, re.findall(r"-?\d+", text)))

def fail(reason="Unsupported problem"):
    return {
        "answer": "Unable to solve reliably",
        "steps": [
            reason,
            "Human-in-the-loop required"
        ]
    }

# ---------------------------
# Main Solver
# ---------------------------
def solve_problem(parsed, retrieved_docs):
    text = parsed["problem_text"].lower()
    topic = parsed["topic"]
    nums = extract_numbers(text)

    # =================================================
    # 1️⃣ PROBABILITY ENGINE (Dice / Coin / Cards)
    # =================================================
    if topic == "probability":

        # ---- Sample space ----
        if "dice" in text:
            space = list(range(1, 7))
        elif "coin" in text:
            space = ["H", "T"]
        elif "card" in text:
            space = list(range(1, 53))
        else:
            return fail("Unknown probability experiment")

        # ---- Event ----
        event = []

        if "prime" in text:
            event = [x for x in space if isinstance(x, int) and x in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]]

        elif "even" in text:
            event = [x for x in space if isinstance(x, int) and x % 2 == 0]

        elif "odd" in text:
            event = [x for x in space if isinstance(x, int) and x % 2 == 1]

        elif "greater than" in text:
            n = nums[-1]
            event = [x for x in space if isinstance(x, int) and x > n]

        elif "less than" in text:
            n = nums[-1]
            event = [x for x in space if isinstance(x, int) and x < n]

        elif "getting" in text and nums:
            n = nums[-1]
            event = [x for x in space if x == n]

        else:
            return fail("Could not identify event")

        return {
            "answer": f"{len(event)}/{len(space)}",
            "steps": [
                f"Sample space = {space}",
                f"Favorable outcomes = {event}",
                "Probability = favorable / total outcomes"
            ]
        }

    # =================================================
    # 2️⃣ ALGEBRA ENGINE (Linear equations)
    # =================================================
    if topic == "algebra":

        # Example: a + b = 7, a = 3
        if "+" in text and "=" in text and len(nums) == 2:
            total, known = nums
            unknown = total - known
            return {
                "answer": str(unknown),
                "steps": [
                    "Given linear equation",
                    "Substitute known value",
                    "Solve for unknown"
                ]
            }

        # Example: 2x = 10
        if len(nums) == 2 and "x" in text:
            a, b = nums
            if "=" in text:
                return {
                    "answer": str(b // a),
                    "steps": [
                        "Given linear equation",
                        "Divide both sides by coefficient"
                    ]
                }

        return fail("Unsupported algebra structure")

    # =================================================
    # 3️⃣ LINEAR ALGEBRA ENGINE
    # =================================================
    if topic == "linear algebra":

        # Determinant 2×2
        if "determinant" in text and len(nums) == 4:
            a, b, c, d = nums
            det = a*d - b*c
            return {
                "answer": str(det),
                "steps": [
                    "Use determinant formula: ad − bc",
                    f"= {a}×{d} − {b}×{c}"
                ]
            }

        return fail("Unsupported matrix size")

    # =================================================
    # 4️⃣ CALCULUS ENGINE (Basic)
    # =================================================
    if topic == "calculus":

        if "x^2" in text:
            return {
                "answer": "2x",
                "steps": [
                    "Apply power rule",
                    "d/dx(x²) = 2x"
                ]
            }

        if "x^3" in text:
            return {
                "answer": "3x²",
                "steps": [
                    "Apply power rule",
                    "d/dx(x³) = 3x²"
                ]
            }

        if "limit" in text and nums:
            return {
                "answer": str(nums[-1] ** 2),
                "steps": [
                    "Direct substitution",
                    "Limit evaluated"
                ]
            }

        return fail("Unsupported calculus operation")

    return fail("Unknown topic")
