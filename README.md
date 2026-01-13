# 🧠 Multimodal Math Mentor AI

A reliable AI Math Mentor built as part of an **AI Engineer Assignment**.  
The system solves **JEE-style math problems** using **RAG + Multi-Agent System + HITL + Memory**.

---

## 🚀 Features
- ✍️ Text input
- 📷 Image input (OCR)
- 🎤 Audio input (ASR)
- 🧠 Parser, Intent Router, Solver, Verifier, Explainer agents
- 📚 Retrieval-Augmented Generation (RAG)
- 👨‍⚖️ Human-in-the-Loop (HITL)
- 🧠 Memory & self-learning

---

## 🧩 Supported Math Scope
- Algebra
- Probability
- Basic Calculus (limits, derivatives)
- Linear Algebra basics  
(JEE-level difficulty)

---

## 🏗️ Architecture
```mermaid
flowchart TD
    A[User Input: Text / Image / Audio] --> B[OCR / ASR]
    B --> C[Parser Agent]
    C --> D[Intent Router]
    D --> E[RAG Retriever]
    E --> F[Solver Agent]
    F --> G[Verifier Agent]
    G -->|Approved| H[Explainer Agent]
    G -->|Uncertain| I[HITL]
    H --> J[Memory Store]
⚠️ Multimodal Support Note
This application fully supports Text, Image, and Audio inputs.

Due to cloud environment limitations:

OCR / ASR dependencies may vary across platforms

When extraction confidence is low, HITL is triggered

Users can manually edit extracted text before solving

The complete multimodal pipeline works locally and is production-ready.

▶️ Run Locally
bash
Copy code
pip install -r requirements.txt
streamlit run app.py
Open:

arduino
Copy code
http://localhost:8501
🌐 Deployment
The application is deployed using Streamlit Cloud.

📦 Deliverables
✅ GitHub Repository

✅ README (setup + run)

✅ Architecture Diagram (Mermaid)

✅ .env.example

✅ Deployed App Link

🧠 Learning & Memory
The system stores:

Original input

Parsed structure

Retrieved context

Final answer

Verifier confidence

User feedback

These are reused for similar future problems.

yaml
Copy code

👉 **Save the file (Ctrl + S)**

---

# ✅ 2️⃣ `.env.example` (MANDATORY)

Create / open **`.env.example`** and add:

```env
ENV=production
Save it.