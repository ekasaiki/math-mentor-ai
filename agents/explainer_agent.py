def explain_solution(parsed, solution):
    lines = []

    lines.append(f"Topic identified: {parsed.get('topic', 'Unknown')}")

    # SAFE access (NO KeyError ever)
    formula = solution.get("used_formula", "Formula not available")
    method = solution.get("method", "Method not specified")

    lines.append(f"Method used: {method}")
    lines.append(f"Formula applied: {formula}")
    lines.append("Steps followed logically to reach the final answer.")

    return "\n".join(lines)