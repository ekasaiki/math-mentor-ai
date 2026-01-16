import streamlit as st
from datetime import datetime

# =============================
# Agents
# =============================
from agents.parser_agent import parse_problem
from agents.intent_router import route_intent
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution

# =============================
# RAG (NO LANGCHAIN)
# =============================
from rag.retriever import build_vectorstore, retrieve_context

# =============================
# Multimodal
# =============================
from multimodal.ocr import extract_text_from_image
from multimodal.asr import transcribe_audio

# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.caption("Reliable Multimodal Math Mentor (Text • Image • Audio)")

# =============================
# SESSION STATE (ANTI-VANISH)
# =============================
if "solution_data" not in st.session_state:
    st.session_state.solution_data = None

# =============================
# Load KB (cached)
# =============================
@st.cache_resource
def load_kb():
    return build_vectorstore()

kb = load_kb()

# =============================
# HITL PANEL
# =============================
def hitl_panel(reason):
    st.warning(f"🧑‍⚖️ HITL Triggered: {reason}")
    return st.radio(
        "Human Review Required:",
        ["Approve", "Edit and Re-run", "Reject"],
        key=f"hitl_{reason}"
    )

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
    user_text = st.text_area("✍️ Enter your math question", height=140)

# =============================
# IMAGE INPUT
# =============================
elif input_mode == "Image":
    image = st.file_uploader("📷 Upload image", ["jpg", "jpeg", "png"])
    if image:
        extracted_text, confidence = extract_text_from_image(image)
        st.info(f"OCR Confidence: {confidence}")
        user_text = st.text_area("Extracted text (editable)", extracted_text)

# =============================
# AUDIO INPUT
# =============================
elif input_mode == "Audio":
    audio = st.audio_input("🎤 Record your question")
    if audio:
        transcript, confidence = transcribe_audio(audio)
        st.info(f"ASR Confidence: {confidence}")
        user_text = st.text_area("Transcribed text (editable)", transcript)

# =============================
# SOLVE BUTTON
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")

# =============================
# RUN PIPELINE ONCE
# =============================
if solve and user_text.strip():

    parsed = parse_problem(user_text)

    if parsed.get("needs_clarification"):
        if hitl_panel("Parser ambiguity") != "Approve":
            st.stop()

    route = route_intent(parsed)
    retrieved_docs = retrieve_context(kb, parsed["problem_text"])
    solution = solve_problem(parsed, retrieved_docs)
    verification = verify_solution(parsed, solution)
    explanation = explain_solution(parsed, solution)

    # STORE EVERYTHING (KEY FIX)
    st.session_state.solution_data = {
        "parsed": parsed,
        "route": route,
        "retrieved_docs": retrieved_docs,
        "solution": solution,
        "verification": verification,
        "explanation": explanation
    }

# =============================
# DISPLAY RESULTS (NO VANISH)
# =============================
if st.session_state.solution_data:

    data = st.session_state.solution_data

    st.subheader("🧠 Parser Agent")
    st.json(data["parsed"])

    st.subheader("🧭 Intent Router")
    st.success(data["route"])

    st.subheader("📚 Retrieved Documents")
    if data["retrieved_docs"]:
        for i, doc in enumerate(data["retrieved_docs"]):
            st.markdown(f"*Document {i+1}*")
            st.code(doc[:800])
    else:
        st.info("No documents retrieved")

    st.subheader("🧮 Solver Agent")
    st.success(data["solution"].get("answer", "No answer"))
    st.json({
        "used_formula": data["solution"].get("used_formula", "N/A"),
        "method": data["solution"].get("method", "N/A")
    })

    st.subheader("🔍 Verifier Agent")
    st.progress(data["verification"].get("confidence", 0.5))

    st.subheader("📖 Explainer Agent")
    st.write(data["explanation"])

    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)
    with c1:
        st.button("✅ Correct")
    with c2:
        st.button("❌ Incorrect")