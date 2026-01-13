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
# Load Vector Store (Cached)
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
# TEXT INPUT (ENABLED)
# =============================
if input_mode == "Text":
    user_text = st.text_area("✍️ Type your math question", height=150)


# =============================
# IMAGE INPUT (DISABLED FOR CLOUD)
# =============================
elif input_mode == "Image":
    from multimodal.ocr import extract_text_from_image

    image = st.file_uploader("📷 Upload image", type=["jpg", "jpeg", "png"])
    if image:
        extracted_text, confidence = extract_text_from_image(image)

        st.write(f"OCR Confidence: {confidence}")
        if confidence < 0.75:
            hitl_panel("Low OCR confidence")

        user_text = st.text_area("Extracted text (editable)", extracted_text)



# =============================
# AUDIO INPUT (DISABLED FOR CLOUD)
# =============================
elif input_mode == "Audio":
    from multimodal.asr import transcribe_audio

    audio_bytes = st.audio_input("🎤 Record your math question")
    if audio_bytes:
        transcript, confidence = transcribe_audio(audio_bytes)

        st.write(f"ASR Confidence: {confidence}")
        if confidence < 0.75:
            hitl_panel("Low ASR confidence")

        user_text = st.text_area("Transcribed text (editable)", transcript)


# =============================
# SOLVE
# =============================
st.divider()
solve = st.button("🚀 Solve Problem")


if solve and user_text.strip():

    # =============================
    # 1️⃣ PARSER AGENT
    # =============================
    parsed = parse_problem(user_text)

    st.subheader("🧠 Parsed Problem")
    st.json(parsed)

    if parsed["needs_clarification"]:
        decision = hitl_panel("Parser detected ambiguity")
        if decision != "Approve":
            st.stop()


    # =============================
    # 2️⃣ INTENT ROUTER
    # =============================
    route = route_intent(parsed)
    st.subheader("🧭 Intent Router")
    st.info(f"Routed to: {route}")


    # =============================
    # 3️⃣ MEMORY LOOKUP
    # =============================
    past_cases = find_similar_by_topic(parsed["topic"])
    if past_cases:
        st.subheader("🧠 Similar Past Problems (Memory)")
        for case in past_cases:
            st.info(f"Past answer: {case['final_answer']}")


    # =============================
    # 4️⃣ RAG RETRIEVAL
    # =============================
    retrieved_docs = retrieve_context(vectorstore, parsed["problem_text"])

    st.subheader("📚 Retrieved Context")
    if not retrieved_docs:
        st.warning("No relevant documents retrieved.")
        st.stop()

    for i, doc in enumerate(retrieved_docs):
        st.markdown(f"**Source {i+1}:**")
        st.info(doc)   # FIXED (no .page_content)


    # =============================
    # 5️⃣ SOLVER AGENT
    # =============================
    solution = solve_problem(parsed, retrieved_docs)

    st.subheader("✅ Final Answer")
    st.success(solution["answer"])


    # =============================
    # 6️⃣ VERIFIER AGENT
    # =============================
    verification = verify_solution(parsed, solution)

    st.subheader("📊 Confidence")
    st.progress(verification["confidence"])

    if verification["needs_hitl"]:
        decision = hitl_panel("Verifier not confident")
        if decision != "Approve":
            st.stop()


    # =============================
    # 7️⃣ EXPLAINER AGENT
    # =============================
    explanation = explain_solution(parsed, solution)

    st.subheader("📖 Explanation")
    st.write(explanation)


    # =============================
    # 8️⃣ SAVE TO MEMORY
    # =============================
    save_to_memory({
        "timestamp": str(datetime.now()),
        "original_input": user_text,
        "parsed_problem": parsed,
        "retrieved_context": retrieved_docs,
        "final_answer": solution["answer"],
        "verifier": verification
    })


    # =============================
    # 9️⃣ USER FEEDBACK (HITL)
    # =============================
    st.subheader("🧠 Feedback")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Correct"):
            save_to_memory({
                "timestamp": str(datetime.now()),
                "original_input": user_text,
                "parsed_problem": parsed,
                "final_answer": solution["answer"],
                "user_feedback": "correct"
            })
            st.success("Feedback saved.")

    with c2:
        if st.button("❌ Incorrect"):
            save_to_memory({
                "timestamp": str(datetime.now()),
                "original_input": user_text,
                "parsed_problem": parsed,
                "final_answer": solution["answer"],
                "user_feedback": "incorrect"
            })
            st.warning("Feedback saved.")


    # =============================
    # 🔁 USER RE-CHECK (MANDATORY)
    # =============================
    st.subheader("🔁 Request Re-check")
    if st.button("Ask Human to Re-check"):
        decision = hitl_panel("User explicitly requested re-check")
        if decision != "Approve":
            st.stop()

        

    
    