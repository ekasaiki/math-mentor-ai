Multimodal Math Mentor AI
Reliable RAG-based Math Tutor with Agents, HITL & Memory
📌 Overview
This project implements a Reliable Multimodal Math Mentor that can solve JEE-style math problems using a structured, deterministic pipeline instead of hallucination-prone LLM guessing.
The system supports Text, Image, and Audio inputs, uses a multi-agent architecture, includes Human-in-the-Loop (HITL) safeguards, and improves over time using memory-based learning.
🎯 Key Objectives
Handle real student inputs (typed, spoken, handwritten)
Avoid hallucinations using formula-based solving
Show step-by-step explanations
Provide verifiable, explainable outputs
Demonstrate production-style AI system design
🧩 Supported Math Scope
Probability
Dice, coins, basic counting
Algebra
Quadratic equations
Quadratic functions (vertex, nature)
(Extendable)
Linear algebra basics
Calculus (limits, derivatives)
🧠 System Architecture
Copy code
Mermaid
flowchart TD
    A[User Input<br/>Text / Image / Audio] --> B[OCR / ASR]
    B --> C[Parser Agent]
    C --> D[Intent Router Agent]
    D --> E[RAG Retriever]
    E --> F[Solver Agent]
    F --> G[Verifier Agent]
    G -->|Confident| H[Explainer Agent]
    G -->|Uncertain| I[Human-in-the-Loop]
    H --> J[Memory Store]
🤖 Multi-Agent Design
Agent
Responsibility
Parser Agent
Cleans input, extracts topic, variables, ambiguity
Intent Router
Routes problem to correct math domain
Retriever (RAG)
Fetches relevant formulas & rules from KB
Solver Agent
Deterministic, formula-based computation
Verifier Agent
Checks correctness & confidence
Explainer Agent
Step-by-step student-friendly explanation

These allow evaluators to test correctness without typing.
🧠 Human-in-the-Loop (HITL)
HITL is triggered when:
OCR / ASR confidence is low
Parser detects ambiguity
Verifier confidence is low
User explicitly requests re-check
Human decisions are logged and reused as learning signals.
🧠 Memory & Self-Learning
The system stores:
Original input
Parsed structure
Retrieved documents
Final answer
Verification confidence
User feedback
Memory is used to:
Reuse known solution patterns
Improve future responses
Avoid repeating past mistakes
(No model retraining required)
📂 Project Structure
Copy code

math-mentor-ai/
│
├── app.py
├── agents/
│   ├── parser_agent.py
│   ├── intent_router.py
│   ├── solver_agent.py
│   ├── verifier_agent.py
│   └── explainer_agent.py
│
├── rag/
│   ├── retriever.py
│   └── _init_.py
│
├── multimodal/
│   ├── ocr.py
│   └── asr.py
│
├── memory/
│   └── memory_store.py
│
├── data/
│   └── math_kb/
│       ├── probability_dice.md
│       ├── probability_coins.md
│       ├── algebra_quadratic.md
│       └── calculus_basics.md
│
├── requirements.txt
├── .env.example
└── README.md

▶️ How to Run Locally
Copy code
Bash
pip install -r requirements.txt
streamlit run app.py

Open in browser:
http://localhost:8501

🌐 Deployment
The app is deployed using Streamlit Cloud.

Deployed App Link:
👉 https://math-mentor-ai-wjkgxxuqsidwzrod5xy2md.streamlit.app/

🔐 Environment Variables

.env.example
Copy code
Env
# Optional future use
# OPENAI_API_KEY=

🧪 Built-in Test Cases
The app includes predefined test cases for instant validation:
Dice → Probability of prime number
Dice → Probability of getting 3
Two coins → Exactly one head
Quadratic equation → x² − 5x + 6 = 0
Quadratic function → f(x) = −x² + 4x + 1