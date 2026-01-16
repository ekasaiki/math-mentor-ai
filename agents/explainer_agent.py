def explain_solution(parsed, solution):
    lines = []
    lines.append(f"Topic identified: {parsed['topic']}")

    if solution.get("used_formula"):
        lines.append(f"Formula used: {solution['used_formula']}")

    lines.append(f"Method: {solution.get('method', 'N/A')}")
    lines.append(f"Final Answer: {solution['answer']}")

    return "\n".join(lines)