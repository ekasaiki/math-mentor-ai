# 🧠 Math Mentor AI
Reliable Multimodal Math Tutor (RAG + Agents + HITL + Memory)

## 🚀 Overview
Math Mentor AI is a reliable AI tutor that solves JEE-style math problems using:
- Multimodal input (Text / Image / Audio)
- Retrieval-Augmented Generation (RAG)
- Multi-agent architecture
- Human-in-the-loop (HITL)
- Memory-based self-learning (no retraining)

## ✨ Features
- 📷 OCR for handwritten / textbook problems
- 🎤 Audio input using ASR
- 🧠 Parser → Router → Solver → Verifier → Explainer agents
- 📚 Curated math knowledge base
- 👨‍🏫 Human review when confidence is low
- 🧠 Memory reuse for similar problems

## 🧩 Architecture
```mermaid
flowchart TD
    A[Input: Text/Image/Audio] --> B[OCR / ASR]
    B --> C[Parser Agent]
    C -->|Ambiguous| H[HITL]
    C --> D[Intent Router]
    D --> E[RAG Retriever]
    E --> F[Solver Agent]
    F --> G[Verifier Agent]
    G -->|Low Confidence| H
    G --> I[Explainer Agent]
    I --> J[Final Answer]
    J --> K[Memory Store]
