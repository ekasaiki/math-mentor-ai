def explain_solution(parsed, solution):
    return "\n".join([f"- {step}" for step in solution.get("steps", [])])

