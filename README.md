# 📚 RAG Document AI Assistant

A high-performance **Retrieval-Augmented Generation (RAG)** system that allows users to upload documents and have context-aware conversations. This project uses **Groq** for rapid inference, **Jina AI** for high-dimensional embeddings, and **Chroma Cloud** for scalable vector storage.



## 🚀 Features
- **Instant Inference**: Powered by **Llama 3** on Groq for sub-second responses.
- **Deep Semantic Search**: Uses **Jina AI Embeddings** ($1024$ dimensions) for superior document retrieval.
- **Hybrid Storage**: Persistent vector data in **Chroma Cloud** and chat history in **Redis**.
- **Modern UI**: A clean, dark-themed dashboard built with Vanilla JavaScript and CSS.
- **Flexible File Handling**: Supports PDF, TXT, and DOCX processing.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **LLM** | Groq (Llama-3.3-70b-versatile) |
| **Embeddings** | Jina AI (jina-embeddings-v2-base-en) |
| **Vector DB** | Chroma Cloud |
| **Memory** | Redis |
| **Backend** | Flask (Python) |
| **Frontend** | HTML5 / CSS3 / JavaScript |

## 📁 Project Structure
```text
/retrival_augmentation_-_generation
├── app.py                 # Flask entry point & API routes
├── services/
│   ├── vector_db.py       # Chroma & Jina configuration
│   ├── file_handling.py   # Document loading & parsing
│   └── LLM.py             # Groq logic & RAG chain
├── static/
│   ├── style.css          # UI styles
│   └── script.js          # API calls & DOM handling
├── templates/
│   └── index.html         # Frontend structure
├── uploads/               # Local temp storage (ephemeral)
└── requirements.txt       # Dependencies
```
## ⚙️ Setup & Installation
### 1. Clone & Install

```
git clone git@github.com:bunny-ml/retrival_augmentation_-_generation.git
cd retrival_augmentation_-_generation
pip install -r requirements.txt
```
### 2. Environment Variables
Create a .env file or export the following:
```

# API Keys
GROQ_API_KEY="your_groq_key"
JINA_API_KEY="your_jina_key"

# Chroma Cloud
CHROMA_API_KEY="your_key"
CHROMA_TENANT="your_tenant_id"
CHROMA_DB="RAG"

# Redis
REDIS_HOST="your_host"
REDIS_PORT="6379"
REDIS_PASSWORD="your_password"
```
### 3. Run Locally

```
python app.py
```