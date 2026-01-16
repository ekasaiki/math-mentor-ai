import streamlit as st
from datetime import datetime

# =============================
# Import Agents
# =============================
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# =============================
# Streamlit Page Config
# =============================
st.set_page_config(
    page_title="Math Mentor AI",
    layout="wide"
)

st.title("🧠 Math Mentor AI")
st.caption("Formula-based Multimodal Math Tutor (Probability • Algebra • Calculus)")

st.divider()

# =============================
# User Input
# =============================
user_question = st.text_area(
    "Enter your math question",
    placeholder="Example: Two coins are tossed. What is the probability of getting exactly one head?",
    height=120
)

solve_btn = st.button("🚀 Solve Problem")

# =============================
# Main Pipeline
# =============================
if solve_btn and user_question.strip():

    # -------------------------
    # 1️⃣ Parser Agent
    # -------------------------
    parsed = parse_problem(user_question)

    st.subheader("🧠 Parser Agent")
    st.json(parsed)

    if parsed.get("needs_clarification"):
        st.error("Parser could not confidently identify the topic.")
        st.stop()

    # -------------------------
    # 2️⃣ Intent Router
    # -------------------------
    intent = route_intent(parsed)

    st.subheader("🧭 Intent Router")
    st.write(f"Detected topic: *{intent}*")

    # -------------------------
    # 3️⃣ Solver Agent
    # -------------------------
    solution = solve_problem(parsed, docs=[])

    st.subheader("🧮 Solver Agent")
    st.json(solution)

    # Safety check (prevents KeyError)
    if "answer" not in solution:
        st.error("Solver failed to produce an answer.")
        st.stop()

    # -------------------------
    # 4️⃣ Verifier Agent
    # -------------------------
    verification = verify_solution(parsed, solution)

    st.subheader("🔍 Verifier Agent")
    st.json(verification)

    # -------------------------
    # 5️⃣ Explainer Agent
    # -------------------------
    explanation = explain_solution(parsed, solution)

    st.subheader("📖 Explainer Agent")
    st.text(explanation)

    # -------------------------
    # Final Answer (Pinned – NO VANISH)
    # -------------------------
    st.divider()
    st.subheader("✅ Final Answer")
    st.success(solution["answer"])

    # -------------------------
    # Confidence Bar
    # -------------------------
    st.subheader("📊 Confidence")
    st.progress(verification.get("confidence", 0.5))

    # -------------------------
    # Feedback (Optional)
    # -------------------------
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        st.button("✅ Correct")

    with c2:
        st.button("❌ Incorrect")

else:
    st.info("Enter a math problem and click *Solve Problem*.")