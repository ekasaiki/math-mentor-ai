import streamlit as st
from datetime import datetime

# -------- Agents --------
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# -------- RAG --------
from rag.retriever import build_vectorstore, retrieve_context

# -------- Memory --------
from memory.memory_store import save_to_memory, find_similar_by_topic


# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.write("Multimodal AI Tutor for JEE-style Math Problems")


# =============================
# Session State (IMPORTANT)
# =============================
if "final_answer" not in st.session_state:
    st.session_state.final_answer = None
    st.session_state.explanation = None
    st.session_state.confidence = None


# =============================
# Load Vector Store
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
# Input Mode
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
    try:
        from multimodal.ocr import extract_text_from_image

        image = st.file_uploader("📷 Upload image", type=["jpg", "jpeg", "png"])
        if image:
            extracted_text, confidence = extract_text_from_image(image)
            st.write(f"OCR Confidence: {confidence}")

            if confidence < 0.75:
                hitl_panel("Low OCR confidence")

            user_text = st.text_area("Extracted text (editable)", extracted_text)

    except Exception:
        st.error("OCR not supported here. Please type the problem manually.")
        user_text = st.text_area("Enter problem:", height=150)


# =============================
# AUDIO INPUT
# =============================
elif input_mode == "Audio":
    try:
        from multimodal.asr import transcribe_audio

        audio_bytes = st.audio_input("🎤 Record your math question")
        if audio_bytes:
            transcript, confidence = transcribe_audio(audio_bytes)
            st.write(f"ASR Confidence: {confidence}")

            if confidence < 0.75:
                hitl_panel("Low ASR confidence")

            user_text = st.text_area("Transcribed text (editable)", transcript)

    except Exception:
        st.error("ASR not supported here. Please type the problem manually.")
        user_text = st.text_area("Enter problem:", height=150)


# =============================
# SOLVE BUTTON
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")


if solve and user_text.strip():

    # -------- Parser Agent --------
    parsed = parse_problem(user_text)
    st.subheader("🧠 Parsed Problem")
    st.json(parsed)

    if parsed["needs_clarification"]:
        if hitl_panel("Parser detected ambiguity") != "Approve":
            st.stop()

    # -------- Intent Router --------
    route = route_intent(parsed)
    st.subheader("🧭 Intent Router")
    st.info(f"Routed to: {route}")

    # -------- Memory Lookup --------
    past_cases = find_similar_by_topic(parsed["topic"])
    if past_cases:
        st.subheader("🧠 Similar Past Problems")
        for case in past_cases:
            st.info(f"Past answer: {case['final_answer']}")

    # -------- RAG Retrieval --------
    retrieved_docs = retrieve_context(vectorstore, parsed["problem_text"])
    st.subheader("📚 Retrieved Context")

    if not retrieved_docs:
        st.warning("No relevant documents retrieved.")
        st.stop()

    for i, doc in enumerate(retrieved_docs):
        st.markdown(f"**Source {i+1}:**")
        st.info(doc)

    # -------- Solver --------
    solution = solve_problem(parsed, retrieved_docs)

    # -------- Verifier --------
    verification = verify_solution(parsed, solution)

    if verification["needs_hitl"]:
        if hitl_panel("Verifier not confident") != "Approve":
            st.stop()

    # -------- Explainer --------
    explanation = explain_solution(parsed, solution)

    # -------- Store in Session --------
    st.session_state.final_answer = solution["answer"]
    st.session_state.explanation = explanation
    st.session_state.confidence = verification["confidence"]

    # -------- Save Memory --------
    save_to_memory({
        "timestamp": str(datetime.now()),
        "original_input": user_text,
        "parsed_problem": parsed,
        "retrieved_context": retrieved_docs,
        "final_answer": solution["answer"],
        "verifier": verification
    })


# =============================
# DISPLAY RESULTS (PERSISTENT)
# =============================
if st.session_state.final_answer:

    st.divider()
    st.subheader("✅ Final Answer")
    st.success(st.session_state.final_answer)

    st.subheader("📖 Explanation")
    st.write(st.session_state.explanation)

    st.subheader("📊 Confidence")
    st.progress(st.session_state.confidence)

    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Correct"):
            st.success("Thanks! Feedback saved.")

    with c2:
        if st.button("❌ Incorrect"):
            st.warning("Thanks! Feedback saved.")

        

    
    