def solve_problem(parsed, retrieved_docs):
    text = parsed["problem_text"].lower()
    nums = parsed.get("numbers", [])
    topic = parsed["topic"]

    # =========================
    # PROBABILITY (DICE / COIN)
    # =========================
    if topic == "probability":
        if "dice" in text:
            total_outcomes = 6

            if "getting" in text:
                favorable = 1
                return {
                    "answer": f"{favorable}/{total_outcomes}",
                    "steps": [
                        "A fair dice has 6 equally likely outcomes",
                        "Only one outcome satisfies the event",
                        "Probability = favorable / total"
                    ]
                }

        if "coin" in text:
            total_outcomes = 2
            return {
                "answer": "1/2",
                "steps": [
                    "A fair coin has two outcomes",
                    "Probability = 1 / 2"
                ]
            }

    # =========================
    # ALGEBRA (LINEAR)
    # =========================
    if topic == "algebra":
        # Example: a + b = 7 where a = 3
        if len(nums) == 2 and "=" in text:
            total, known = nums
            unknown = total - known
            return {
                "answer": str(unknown),
                "steps": [
                    f"Given total = {total}",
                    f"Given known value = {known}",
                    f"Unknown = {total} − {known}"
                ]
            }

    # =========================
    # LINEAR ALGEBRA (2×2)
    # =========================
    if topic == "linear algebra" and len(nums) == 4:
        a, b, c, d = nums
        det = a*d - b*c
        return {
            "answer": str(det),
            "steps": [
                "Determinant of [[a,b],[c,d]] is ad − bc",
                f"= {a}×{d} − {b}×{c}",
                f"= {det}"
            ]
        }

    # =========================
    # CALCULUS (BASIC)
    # =========================
    if topic == "calculus" and "x^2" in text:
        return {
            "answer": "2x",
            "steps": [
                "Using power rule",
                "d/dx(x²) = 2x"
            ]
        }

    # =========================
    # SAFE FAILURE
    # =========================
    return {
        "answer": "Unable to solve this problem reliably.",
        "steps": [
            "Problem structure not supported",
            "Human review required"
        ]
    }
