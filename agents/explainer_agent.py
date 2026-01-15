def explain_solution(parsed, solution):
    return f"""
Step 1: Identify topic → {parsed['topic']}
Step 2: Apply standard formula
Step 3: Substitute values
Step 4: Final answer → {solution['answer']}

Explanation:
{solution['method']}
"""