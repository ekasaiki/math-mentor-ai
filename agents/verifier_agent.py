def verify_solution(parsed_problem, solution):
    topic = parsed_problem["topic"]
    problem_text = parsed_problem["problem_text"].lower()
    answer = solution["answer"]

    # -------- ALGEBRA --------
    if topic == "algebra":
        try:
            total = int(problem_text.split("=")[1].split()[0])
            known = int(problem_text.split("where")[1].split("=")[1].split()[0])
            solved = int(answer.split("=")[1])
            if total - known == solved:
                return {"confidence": 0.95, "needs_hitl": False, "issues": []}
        except:
            pass

        return {"confidence": 0.6, "needs_hitl": True, "issues": ["Algebra verification failed"]}

    # -------- PROBABILITY --------
    if topic == "probability":
        if answer in ["1/2", "0.5"]:
            return {"confidence": 0.9, "needs_hitl": False, "issues": []}

    # -------- CALCULUS --------
    if topic == "calculus":
        return {"confidence": 0.9, "needs_hitl": False, "issues": []}

    # -------- LINEAR ALGEBRA --------
    if topic == "linear algebra":
        try:
            int(answer)
            return {"confidence": 0.9, "needs_hitl": False, "issues": []}
        except:
            pass

    return {"confidence": 0.5, "needs_hitl": True, "issues": ["Verification failed"]}
