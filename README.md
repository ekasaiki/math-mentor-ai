# 🧠 Multimodal Math Mentor AI

A reliable AI-powered tutor for JEE-style math problems using
**RAG + Multi-Agent Architecture + HITL + Memory**.

---

## 🚀 Features
- Text, Image (OCR), and Audio (ASR) input
- Structured parsing of math problems
- Retrieval-Augmented Generation (RAG)
- Multi-agent reasoning pipeline
- Human-in-the-loop (HITL) for safety
- Memory-based self-learning (no retraining)

---

## 📚 Supported Math Scope
- Algebra
- Probability
- Basic Calculus (limits, derivatives)
- Linear Algebra basics  
*(JEE-level difficulty)*

---

## 🧠 Architecture

```mermaid
graph TD
A[User Input] --> B[OCR / ASR / Text]
B --> C[Parser Agent]
C -->|Ambiguous| H[HITL]
C --> D[Intent Router]
D --> E[RAG Retriever]
E --> F[Solver Agent]
F --> G[Verifier Agent]
G -->|Low confidence| H[HITL]
G --> I[Explainer Agent]
I --> J[Final Answer + Explanation]
J --> K[Memory Store]
