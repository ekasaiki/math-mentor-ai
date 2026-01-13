def route_intent(parsed_problem):
    """
    Decides which solving strategy to use based on topic.
    """

    topic = parsed_problem.get("topic", "")

    if topic == "calculus":
        return "calculus_solver"

    if topic == "algebra":
        return "algebra_solver"

    if topic == "probability":
        return "probability_solver"

    return "generic_solver"
