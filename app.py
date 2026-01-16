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
# Optional Multimodal Imports
# =============================
IMAGE_AVAILABLE = True
AUDIO_AVAILABLE = True

try:
    from multimodal.ocr import extract_text_from_image
except Exception:
    IMAGE_AVAILABLE = False

try:
    from multimodal.asr import transcribe_audio
except Exception:
    AUDIO_AVAILABLE = False

# =============================
# Streamlit Config
# =============================
st.set_page_config(page_title="Math Mentor AI", layout="wide")
st.title("🧠 Math Mentor AI")
st.caption("Formula-based Multimodal Math Tutor (Text • Image • Audio)")
st.divider()

# =============================
# Input Mode
# =============================
input_mode = st.radio(
    "Choose input type:",
    ["Text", "Image", "Audio"],
    horizontal=True
)

user_text = ""

# =============================
# TEXT INPUT
# =============================
if input_mode == "Text":
    user_text = st.text_area(
        "✍️ Enter your math problem",
        height=120,
        placeholder="Example: Two coins are tossed. What is the probability of getting exactly one head?"
    )

# =============================
# IMAGE INPUT (OCR)
# =============================
elif input_mode == "Image":
    if not IMAGE_AVAILABLE:
        st.error("OCR is not available in this environment.")
    else:
        image = st.file_uploader("📷 Upload image", type=["png", "jpg", "jpeg"])
        if image:
            extracted_text, confidence = extract_text_from_image(image)

            st.subheader("🖼 OCR Output")
            st.write(f"Confidence: {confidence}")
            user_text = st.text_area("Extracted text (editable)", extracted_text)

# =============================
# AUDIO INPUT (ASR)
# =============================
elif input_mode == "Audio":
    if not AUDIO_AVAILABLE:
        st.error("Audio transcription is not available in this environment.")
    else:
        audio = st.audio_input("🎤 Record your math question")
        if audio:
            transcript, confidence = transcribe_audio(audio)

            st.subheader("🎧 ASR Output")
            st.write(f"Confidence: {confidence}")
            user_text = st.text_area("Transcribed text (editable)", transcript)

st.divider()
solve_btn = st.button("🚀 Solve Problem")

# =============================
# MAIN PIPELINE
# =============================
if solve_btn and user_text.strip():

    # -------------------------
    # 1️⃣ Parser Agent
    # -------------------------
    parsed = parse_problem(user_text)

    st.subheader("🧠 Parser Agent")
    st.json(parsed)

    if parsed.get("needs_clarification"):
        st.error("Parser could not clearly identify the problem.")
        st.stop()

    # -------------------------
    # 2️⃣ Intent Router
    # -------------------------
    intent = route_intent(parsed)

    st.subheader("🧭 Intent Router")
    st.success(f"Detected topic: {intent}")

    # -------------------------
    # 3️⃣ Solver Agent (FORMULA-BASED)
    # -------------------------
    solution = solve_problem(parsed, docs=[])

    st.subheader("🧮 Solver Agent")
    st.json(solution)

    if "answer" not in solution:
        st.error("Solver could not generate an answer.")
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
    # FINAL ANSWER (PINNED – NO VANISH)
    # -------------------------
    st.divider()
    st.subheader("✅ Final Answer")
    st.success(solution["answer"])

    # -------------------------
    # CONFIDENCE
    # -------------------------
    st.subheader("📊 Confidence")
    st.progress(verification.get("confidence", 0.7))

    # -------------------------
    # FEEDBACK
    # -------------------------
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)
    with c1:
        st.button("✅ Correct")
    with c2:
        st.button("❌ Incorrect")

else:
    st.info("Provide input and click *Solve Problem*.")