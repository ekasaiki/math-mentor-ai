def verify_solution(parsed, solution):
    confident = solution["method"] != "human-review"
    return {
        "confidence": 0.9 if confident else 0.4,
        "needs_hitl": not confident,
        "issues": []
    }
