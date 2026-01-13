import re

def solve_problem(parsed_problem, retrieved_docs):
    problem_text = parsed_problem["problem_text"].lower()
    topic = parsed_problem["topic"]

    # -------- ALGEBRA --------
    if topic == "algebra":
        eq = re.search(r"([a-z])\s*\+\s*([a-z])\s*=\s*(\d+)", problem_text)
        val = re.search(r"where\s*([a-z])\s*=\s*(\d+)", problem_text)
        target = re.search(r"then\s*([a-z])\s*=\s*\?", problem_text)

        if eq and val and target:
            v1, v2, total = eq.groups()
            known_var, known_val = val.groups()
            target_var = target.group(1)

            total = int(total)
            known_val = int(known_val)

            return {
                "answer": f"{target_var} = {total - known_val}",
                "method": "Linear substitution"
            }

    # -------- PROBABILITY --------
    if topic == "probability":
        if "coin" in problem_text and "head" in problem_text:
            return {"answer": "1/2", "method": "Classical probability"}
        if "dice" in problem_text and "even" in problem_text:
            return {"answer": "1/2", "method": "Favorable outcomes / total"}

    # -------- CALCULUS --------
    if topic == "calculus":
        if "x^2" in problem_text or "x²" in problem_text:
            return {"answer": "2x", "method": "Power rule"}

    # -------- LINEAR ALGEBRA --------
    if topic == "linear algebra":
        nums = list(map(int, re.findall(r"-?\d+", problem_text)))
        if "determinant" in problem_text and len(nums) == 4:
            a, b, c, d = nums
            return {
                "answer": str(a*d - b*c),
                "method": "2×2 determinant"
            }

    return {
        "answer": "Unable to solve with current rules.",
        "method": "Unsupported pattern"
    }
