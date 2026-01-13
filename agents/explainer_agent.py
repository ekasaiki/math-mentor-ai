def explain_solution(parsed_problem, solution):
    topic = parsed_problem["topic"]
    answer = solution["answer"]

    if topic == "algebra":
        return (
            "Step 1: Identify the equation a + b = 7\n"
            "Step 2: Substitute a = 3\n"
            "Step 3: Solve b = 7 − 3 = 4\n\n"
            f"Final Answer: {answer}"
        )

    if topic == "probability":
        return (
            "Step 1: Count total outcomes\n"
            "Step 2: Count favorable outcomes\n"
            "Step 3: Apply P = favorable / total\n\n"
            f"Final Answer: {answer}"
        )

    if topic == "calculus":
        return (
            "Step 1: Identify the function\n"
            "Step 2: Apply Power Rule\n\n"
            f"Final Answer: {answer}"
        )

    if topic == "linear algebra":
        return (
            "Step 1: Use determinant formula ad − bc\n\n"
            f"Final Answer: {answer}"
        )

    return "Explanation not available."
