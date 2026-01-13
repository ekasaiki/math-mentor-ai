def parse_problem(text: str):
    text = text.lower().strip()

    topic = "algebra"
    needs_clarification = False
    variables = []
    constraints = []

    # -------- TOPIC DETECTION --------
    if any(word in text for word in ["probability", "coin", "dice"]):
        topic = "probability"

    elif any(word in text for word in ["derivative", "limit", "dx", "x^"]):
        topic = "calculus"

    elif any(word in text for word in ["determinant", "matrix"]):
        topic = "linear algebra"

    else:
        topic = "algebra"

    # -------- VARIABLE EXTRACTION (ONLY WHEN NEEDED) --------
    if topic in ["algebra", "calculus"]:
        for ch in text:
            if ch.isalpha() and ch not in variables:
                variables.append(ch)

    # -------- AMBIGUITY RULES --------
    if topic == "algebra":
        if "=" not in text:
            needs_clarification = True

    if topic == "calculus":
        if "x" not in text:
            needs_clarification = True

    # ❗ IMPORTANT: probability & linear algebra do NOT need variables
    if topic in ["probability", "linear algebra"]:
        needs_clarification = False
        variables = []

    return {
        "problem_text": text,
        "topic": topic,
        "variables": variables,
        "constraints": constraints,
        "needs_clarification": needs_clarification
    }
