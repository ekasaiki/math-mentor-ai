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
from rag.retriever import build_vectorstore, retrieve_context

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
# SESSION STATE (CRITICAL FIX)
# =============================
if "final_answer" not in st.session_state:
    st.session_state.final_answer = None

if "explanation" not in st.session_state:
    st.session_state.explanation = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None


# =============================
# LOAD VECTOR STORE
# =============================
@st.cache_resource
def load_vectorstore():
    return build_vectorstore()

vectorstore = load_vectorstore()


# =============================
# HITL PANEL
# =============================
def hitl_panel(reason: str):
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
# IMAGE INPUT (OCR)
# =============================
elif input_mode == "Image":
    image = st.file_uploader("📷 Upload image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if image:
        extracted_text, confidence = extract_text_from_image(image)
        st.write(f"OCR Confidence: {confidence}")

        if confidence < 0.75:
            decision = hitl_panel("Low OCR confidence")
            if decision == "Edit and Re-run":
                extracted_text = st.text_area("Edit extracted text:", extracted_text)

        user_text = st.text_area("Extracted text (editable)", extracted_text)


# =============================
# AUDIO INPUT (ASR)
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

    # -------- PARSER --------
    parsed = parse_problem(user_text)
    st.subheader("🧠 Parsed Problem")
    st.json(parsed)

    if parsed["needs_clarification"]:
        decision = hitl_panel("Parser detected ambiguity")
        if decision != "Approve":
            st.stop()

    # -------- INTENT ROUTER --------
    route = route_intent(parsed)
    st.subheader("🧭 Intent Router")
    st.info(f"Routed to: {route}")

    # -------- MEMORY LOOKUP --------
    past = find_similar_by_topic(parsed["topic"])
    if past:
        st.subheader("🧠 Similar Past Problems")
        for p in past:
            st.info(f"Past answer: {p.get('final_answer')}")

    # -------- RAG RETRIEVAL --------
    retrieved_docs = retrieve_context(vectorstore, parsed["problem_text"])
    st.subheader("📚 Retrieved Context")

    if not retrieved_docs:
        st.warning("No relevant documents retrieved.")
        st.stop()

    for i, doc in enumerate(retrieved_docs):
        st.markdown(f"*Source {i+1}:*")
        st.info(doc)

    # -------- SOLVER --------
    solution = solve_problem(parsed, retrieved_docs)

    # -------- VERIFIER --------
    verification = verify_solution(parsed, solution)

    if verification["needs_hitl"]:
        decision = hitl_panel("Verifier not confident")
        if decision != "Approve":
            st.stop()

    # -------- EXPLAINER --------
    explanation = explain_solution(parsed, solution)

    # -------- SAVE TO SESSION STATE (KEY FIX) --------
    st.session_state.final_answer = solution["answer"]
    st.session_state.explanation = explanation
    st.session_state.confidence = verification["confidence"]

    # -------- SAVE TO MEMORY --------
    save_to_memory({
        "timestamp": str(datetime.now()),
        "original_input": user_text,
        "parsed_problem": parsed,
        "retrieved_context": retrieved_docs,
        "final_answer": solution["answer"],
        "verifier": verification
    })


# =============================
# PERSISTENT DISPLAY (NO VANISH)
# =============================
if st.session_state.final_answer:
    st.subheader("✅ Final Answer")
    st.success(st.session_state.final_answer)

if st.session_state.explanation:
    st.subheader("📖 Explanation")
    st.write(st.session_state.explanation)

if st.session_state.confidence is not None:
    st.subheader("📊 Confidence")
    st.progress(st.session_state.confidence)


# =============================
# USER FEEDBACK (HITL)
# =============================
if st.session_state.final_answer:
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Correct"):
            save_to_memory({
                "timestamp": str(datetime.now()),
                "original_input": user_text,
                "final_answer": st.session_state.final_answer,
                "user_feedback": "correct"
            })
            st.success("Feedback saved.")

    with c2:
        if st.button("❌ Incorrect"):
            save_to_memory({
                "timestamp": str(datetime.now()),
                "original_input": user_text,
                "final_answer": st.session_state.final_answer,
                "user_feedback": "incorrect"
            })
            st.warning("Feedback saved.")