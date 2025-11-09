# 🧠 SHL GenAI Assessment Recommendation System

An intelligent **Assessment Recommendation Engine** that simplifies hiring assessment selection by understanding **natural language job descriptions**.  
Built with **FastAPI**, **Sentence Transformers**, and a **Streamlit frontend**, this project recommends the most relevant **SHL Individual Test Solutions** based on any input text.

---

## 🚀 Features

- 🔍 **Semantic Understanding** — Uses Sentence-BERT embeddings to understand job context.  
- 🤖 **Smart Recommendations** — Suggests 5–10 relevant SHL assessments ranked by similarity.  
- 🌐 **REST API** — FastAPI-based API with `/health` and `/recommend` endpoints.  
- 💻 **Interactive Web App** — Streamlit UI for testing and visualization.  
- ☁️ **Cloud Deployment** — Fully containerized with Docker and deployed on Google Cloud Run.  

---

## 🏗️ Architecture

```text
Input Query / Job Description
            ↓
Sentence Embedding (LLM - MiniLM)
            ↓
Vector Similarity Search
            ↓
Top N Relevant Assessments
            ↓
JSON Response / Web UI Display
