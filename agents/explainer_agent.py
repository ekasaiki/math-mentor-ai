def explain_solution(parsed, solution):
    lines = []
    lines.append(f"Topic: {parsed['topic']}")
    lines.append(f"Method: {solution['method']}")
    lines.append(f"Formula: {solution['used_formula']}")
    lines.append("Steps:")
    for s in solution["steps"]:
        lines.append(f"- {s}")
    lines.append(f"Final Answer: {solution['answer']}")
    return "\n".join(lines)
