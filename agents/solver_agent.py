import re

def solve_problem(parsed, retrieved_docs):
    text = parsed["problem_text"].lower()
    topic = parsed["topic"]

    # =========================
    # PROBABILITY MODEL
    # =========================
    if topic == "probability":

        # Total outcomes
        if "dice" in text:
            sample_space = list(range(1, 7))
        elif "coin" in text:
            sample_space = ["H", "T"]
        else:
            return fail()

        # Event condition
        favorable = []

        if "prime" in text:
            favorable = [x for x in sample_space if x in [2,3,5]]

        elif "even" in text:
            favorable = [x for x in sample_space if isinstance(x, int) and x % 2 == 0]

        elif "odd" in text:
            favorable = [x for x in sample_space if isinstance(x, int) and x % 2 == 1]

        elif "greater than" in text:
            n = int(re.findall(r"greater than (\d+)", text)[0])
            favorable = [x for x in sample_space if isinstance(x, int) and x > n]

        elif "less than" in text:
            n = int(re.findall(r"less than (\d+)", text)[0])
            favorable = [x for x in sample_space if isinstance(x, int) and x < n]

        elif "getting" in text:
            n = int(re.findall(r"getting (\d+)", text)[0])
            favorable = [x for x in sample_space if x == n]

        else:
            return fail()

        return {
            "answer": f"{len(favorable)}/{len(sample_space)}",
            "steps": [
                f"Sample space = {sample_space}",
                f"Favorable outcomes = {favorable}",
                "Probability = favorable / total outcomes"
            ]
        }

    # =========================
    # ALGEBRA (LINEAR)
    # =========================
    if topic == "algebra":
        nums = list(map(int, re.findall(r"-?\d+", text)))

        if "a + b =" in text and "a =" in text:
            total, a = nums
            b = total - a
            return {
                "answer": f"{b}",
                "steps": [
                    "Given: a + b = total",
                    "Substitute known value of a",
                    "Solve for b = total − a"
                ]
            }

        return fail()

    # =========================
    # LINEAR ALGEBRA (DETERMINANT)
    # =========================
    if topic == "linear algebra":
        nums = list(map(int, re.findall(r"-?\d+", text)))
        if len(nums) == 4:
            a, b, c, d = nums
            det = a*d - b*c
            return {
                "answer": str(det),
                "steps": [
                    "Determinant formula: ad − bc",
                    f"= {a}×{d} − {b}×{c}"
                ]
            }

    return fail()


def fail():
    return {
        "answer": "Cannot solve this problem reliably.",
        "steps": [
            "Problem structure not supported",
            "Human-in-the-loop required"
        ]
    }
