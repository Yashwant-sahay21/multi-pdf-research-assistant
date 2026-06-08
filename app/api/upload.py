from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from app.rag.pdf_loader import load_pdf
from app.rag.chunker import split_documents
from app.rag.metadata import extract_metadata
from app.rag.vector_store import load_vector_store

router = APIRouter()

DATA_FOLDER = "data"


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    Path(DATA_FOLDER).mkdir(
        exist_ok=True
    )

    file_path = Path(DATA_FOLDER) / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    documents = load_pdf(
        str(file_path)
    )

    metadata = extract_metadata(
        documents,
        str(file_path)
    )

    chunks = split_documents(
        documents
    )

    for chunk in chunks:
        chunk.metadata.update(
            metadata
        )

    vectordb = load_vector_store()

    vectordb.add_documents(
        chunks
    )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "pages": len(documents),
        "chunks": len(chunks)
    }