# Multi-PDF Research Assistant

A Retrieval-Augmented Generation (RAG) based Research Assistant that allows users to upload multiple PDF documents, ask questions, generate summaries, and maintain conversational context using Llama 3, ChromaDB, FastAPI, and Streamlit.

---

## Features

- Multi-PDF document ingestion
- Semantic search using vector embeddings
- Retrieval-Augmented Generation (RAG)
- Conversational question answering
- Persistent chat memory with SQLite
- Adaptive document summarization
- Source citation tracking
- FastAPI backend
- Streamlit frontend
- ChromaDB vector database
- Ollama-powered Llama 3 integration

---

## Tech Stack

### Backend

- FastAPI
- Python

### Frontend

- Streamlit

### RAG Pipeline

- LangChain
- ChromaDB
- HuggingFace Embeddings
- Ollama
- Llama 3

### Storage

- SQLite (Chat Memory)
- ChromaDB (Vector Store)

### Document Processing

- PyPDF
- PyMuPDF

---

## System Architecture

<img width="931" height="1401" alt="Research Assistant Architecture drawio" src="https://github.com/user-attachments/assets/2759914b-886e-4bdc-b7c5-d3c54fca509c" />



---

## Project Structure

```text
multi-pdf-research-assistant/
│
├── app/
├── frontend/
├── docs/
├── data/
│
├── requirements.txt
├── README.md
├── .gitignore
│
├── ingest.py
│
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Yashwant-sahay21/multi-pdf-research-assistant.git

cd multi-pdf-research-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download and install Ollama:

https://ollama.com

Pull Llama 3 model:

```bash
ollama pull llama3
```

Verify installation:

```bash
ollama run llama3
```

---

## Ingest Documents

Place PDFs inside the data folder and run:

```bash
python ingest.py
```

This will:

- Load PDFs
- Create chunks
- Generate embeddings
- Store vectors in ChromaDB

---

## Run FastAPI Backend

```bash
uvicorn app.api.routes:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Run Streamlit Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## API Endpoints

### Upload Document

```http
POST /upload
```

### List Documents

```http
GET /documents
```

### Chat

```http
POST /chat
```

### Health Check

```http
GET /health
```

### Application Info

```http
GET /info
```

---

## Example Questions

```text
What is the title of the paper?

Who are the authors?

Summarize the document.

What methodology was used?

What are the key findings?

Compare the results presented in the paper.
```

---

## Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Cross-Encoder Reranking
- Authentication and User Accounts
- Cloud Deployment
- PDF Annotation Support
- Export Chat History
- Citation Highlighting

---

## Screenshots

### Streamlit Interface

_Add screenshot here_

### Chat Example

_Add screenshot here_

### FastAPI Swagger

_Add screenshot here_

---

## Author

Yashwant Sahay

Machine Learning | Generative AI | Software Engineering

---

## License

MIT License
