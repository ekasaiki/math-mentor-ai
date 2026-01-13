# Multimodal Math Mentor AI

An end-to-end AI system that solves JEE-style math problems using
RAG, multi-agent reasoning, Human-in-the-Loop (HITL), and memory-based learning.

---

## 🚀 Features
- Text, Image (OCR), and Audio (ASR) input
- Parser → Router → Solver → Verifier → Explainer agents
- Retrieval-Augmented Generation (RAG)
- Human-in-the-Loop review
- Memory-based self learning
- Streamlit UI

---

## 🧠 Architecture
```mermaid
flowchart TD
    Input --> OCR_ASR
    OCR_ASR --> Parser
    Parser --> Router
    Router --> RAG
    RAG --> Solver
    Solver --> Verifier
    Verifier --> Explainer
    Explainer --> UI
    Verifier -->|Low confidence| HITL
    HITL --> Memory
    Solver --> Memory
