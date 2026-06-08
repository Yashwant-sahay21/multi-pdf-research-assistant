from pathlib import Path

from langchain_community.vectorstores import Chroma

from app.rag.embeddings import embedding_model


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "research_documents"


def create_vector_store(chunks):

    if not chunks:
        raise ValueError("No chunks provided.")

    Path(CHROMA_PATH).mkdir(
        parents=True,
        exist_ok=True
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME
    )

    return vectordb


def load_vector_store():

    if not Path(CHROMA_PATH).exists():
        raise FileNotFoundError(
            "Chroma database not found. Run ingest.py first."
        )

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME
    )

    return vectordb