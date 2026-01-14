def verify_solution(parsed, solution):
    if "unable" in solution["answer"].lower():
        return {
            "confidence": 0.3,
            "needs_hitl": True,
            "issues": ["No formula matched"]
        }

    return {
        "confidence": 0.9,
        "needs_hitl": False,
        "issues": []
    }
