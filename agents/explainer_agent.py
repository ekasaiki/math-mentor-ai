def explain_solution(parsed, solution):
    return "\n".join(
        [f"Step {i+1}: {step}" for i, step in enumerate(solution["steps"])]
    )
