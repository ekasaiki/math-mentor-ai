def explain_solution(parsed, solution):
    steps = solution.get("steps", [])

    if not steps:
        return "No detailed explanation available."

    explanation = []
    explanation.append("### 🧠 Step-by-Step Explanation\n")

    for i, step in enumerate(steps, start=1):
        explanation.append(f"**Step {i}:** {step}")

    explanation.append(f"\n### ✅ Final Answer\n**{solution['answer']}**")

    return "\n\n".join(explanation)
