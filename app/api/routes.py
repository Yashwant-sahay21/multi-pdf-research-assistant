from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.api.upload import router as upload_router
from app.api.documents import router as documents_router

from app.rag.rag_chain import ask_question
from app.rag.vector_store import load_vector_store

from app.chat.memory import (
    get_chat_history,
    add_message
)

from app.chat.database import (
    initialize_database
)


app = FastAPI(
    title="Research Assistant API",
    description="Multi-PDF Research Assistant using RAG, ChromaDB and Llama3",
    version="1.0.0"
)

initialize_database()

app.include_router(upload_router)
app.include_router(documents_router)

try:
    vectordb = load_vector_store()
    print("Vector database loaded successfully.")

except Exception as e:
    print(f"Failed to load vector database: {e}")
    vectordb = None


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    filename: str | None = None
    session_id: str = "default"


@app.get("/")
def root():
    return {
        "message": "Research Assistant API is running",
        "status": "online"
    }


@app.get("/health")
def health():

    if vectordb is None:
        return {
            "status": "error",
            "vector_db": "not loaded"
        }

    return {
        "status": "healthy",
        "vector_db": "loaded"
    }


@app.get("/info")
def info():
    return {
        "application": "Research Assistant API",
        "version": "1.0.0",
        "llm": "Llama3",
        "vector_store": "ChromaDB"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if vectordb is None:
        raise HTTPException(
            status_code=500,
            detail="Vector database is not loaded."
        )

    try:

        history = get_chat_history(
            request.session_id
        )

        result = ask_question(
            vectordb=vectordb,
            question=request.question,
            filename=request.filename,
            chat_history=history
        )

        add_message(
            request.session_id,
            "user",
            request.question
        )

        add_message(
            request.session_id,
            "assistant",
            result["answer"]
        )

        return {
            "session_id": request.session_id,
            "question": request.question,
            "filename": request.filename,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )