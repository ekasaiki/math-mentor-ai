def explain_solution(parsed, solution):
    explanation = []

    explanation.append(f"Topic identified: {parsed.get('topic')}")

    explanation.append(f"Method used: {solution.get('method', 'N/A')}")
    explanation.append(f"Formula used: {solution.get('used_formula', 'N/A')}")

    explanation.append("Steps:")
    for step in solution.get("steps", []):
        explanation.append(f"- {step}")

    explanation.append(f"Final Answer: {solution.get('answer')}")

    return "\n".join(explanation)
