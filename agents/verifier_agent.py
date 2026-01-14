def verify_solution(parsed, solution):
    if "unable" in solution["answer"].lower():
        return {
            "confidence": 0.2,
            "needs_hitl": True,
            "issues": ["Solver could not apply a formula"]
        }

    return {
        "confidence": 0.9,
        "needs_hitl": False,
        "issues": []
    }
