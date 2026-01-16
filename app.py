import streamlit as st
from datetime import datetime

# =============================
# IMPORT AGENTS
# =============================
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# =============================
# RAG
# =============================
from rag.retriever import retrieve_context

# =============================
# MULTIMODAL
# =============================
from multimodal.ocr import extract_text_from_image
from multimodal.asr import transcribe_audio

# =============================
# MEMORY
# =============================
from memory.memory_store import save_to_memory, find_similar_by_topic


# =============================
# STREAMLIT CONFIG
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.write("Reliable Multimodal Math Mentor (RAG + Agents + HITL + Memory)")


# =============================
# HITL PANEL
# =============================
def hitl_panel(reason):
    st.warning(f"🧑‍⚖️ HITL Triggered: {reason}")
    decision = st.radio(
        "Human Review Required:",
        ["Approve", "Edit and Re-run", "Reject"],
        key=f"hitl_{reason}"
    )
    return decision


# =============================
# INPUT MODE
# =============================
input_mode = st.radio(
    "Choose input type:",
    ["Text", "Image", "Audio"]
)

st.divider()
user_text = ""


# =============================
# TEXT INPUT
# =============================
if input_mode == "Text":
    user_text = st.text_area("✍️ Type your math question", height=150)


# =============================
# IMAGE INPUT
# =============================
elif input_mode == "Image":
    image = st.file_uploader("📷 Upload image (JPG / PNG)", type=["jpg", "jpeg", "png"])

    if image:
        extracted_text, confidence = extract_text_from_image(image)
        st.write(f"OCR Confidence: {confidence}")

        if confidence < 0.75:
            decision = hitl_panel("Low OCR confidence")
            if decision == "Edit and Re-run":
                extracted_text = st.text_area("Edit OCR text:", extracted_text)

        user_text = st.text_area("Extracted text (editable)", extracted_text)


# =============================
# AUDIO INPUT
# =============================
elif input_mode == "Audio":
    audio_bytes = st.audio_input("🎤 Record your math question")

    if audio_bytes:
        transcript, confidence = transcribe_audio(audio_bytes)
        st.write(f"ASR Confidence: {confidence}")

        if confidence < 0.75:
            decision = hitl_panel("Low ASR confidence")
            if decision == "Edit and Re-run":
                transcript = st.text_area("Edit transcript:", transcript)

        user_text = st.text_area("Transcribed text (editable)", transcript)


# =============================
# SOLVE BUTTON
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")


# =============================
# MAIN PIPELINE
# =============================
if solve and user_text.strip():

    # -----------------------------
    # 1️⃣ PARSER AGENT
    # -----------------------------
    parsed = parse_problem(user_text)
    st.subheader("🧠 Parser Agent")
    st.json(parsed)

    if parsed["needs_clarification"]:
        decision = hitl_panel("Parser detected ambiguity")
        if decision != "Approve":
            st.stop()

    # -----------------------------
    # 2️⃣ INTENT ROUTER AGENT
    # -----------------------------
    route = route_intent(parsed)
    st.subheader("🧭 Intent Router Agent")
    st.info(f"Routed to topic: {route}")

    # -----------------------------
    # 3️⃣ MEMORY LOOKUP
    # -----------------------------
    past = find_similar_by_topic(parsed["topic"])
    if past:
        st.subheader("🧠 Memory (Similar Problems)")
        for p in past[:2]:
            st.info(f"Past Answer: {p['final_answer']}")

    # -----------------------------
    # 4️⃣ RAG RETRIEVAL
    # -----------------------------
    retrieved_docs = retrieve_context(parsed["problem_text"])

    st.subheader("📚 Retrieved Documents (RAG)")
    if not retrieved_docs:
        st.warning("No documents retrieved")
    else:
        for d in retrieved_docs:
            st.markdown(f"*Source:* {d['source']}")
            st.code(d["content"][:800])

    # -----------------------------
    # 5️⃣ SOLVER AGENT
    # -----------------------------
    solution = solve_problem(parsed, retrieved_docs)
    st.subheader("🧮 Solver Agent")
    st.success(solution["answer"])

    # -----------------------------
    # 6️⃣ VERIFIER AGENT
    # -----------------------------
    verification = verify_solution(parsed, solution)
    st.subheader("✅ Verifier Agent")
    st.progress(verification["confidence"])

    if verification["needs_hitl"]:
        decision = hitl_panel("Verifier not confident")
        if decision != "Approve":
            st.stop()

    # -----------------------------
    # 7️⃣ EXPLAINER AGENT
    # -----------------------------
    explanation = explain_solution(parsed, solution)
    st.subheader("📖 Explainer Agent")
    st.write(explanation)

    # -----------------------------
    # 8️⃣ SAVE TO MEMORY
    # -----------------------------
    save_to_memory({
        "timestamp": str(datetime.now()),
        "original_input": user_text,
        "parsed_problem": parsed,
        "retrieved_context": retrieved_docs,
        "final_answer": solution["answer"],
        "confidence": verification["confidence"]
    })

    # -----------------------------
    # 9️⃣ FEEDBACK (HITL)
    # -----------------------------
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Correct"):
            save_to_memory({"final_answer": solution["answer"], "feedback": "correct"})
            st.success("Feedback saved")

    with c2:
        if st.button("❌ Incorrect"):
            save_to_memory({"final_answer": solution["answer"], "feedback": "incorrect"})
            st.warning("Feedback saved")