from fastapi import APIRouter

from app.rag.vector_store import load_vector_store

router = APIRouter()


@router.get("/documents")
def get_documents():

    vectordb = load_vector_store()

    collection = vectordb._collection

    results = collection.get()

    documents = {}

    for metadata in results["metadatas"]:

        filename = metadata.get(
            "filename",
            "Unknown"
        )

        if filename not in documents:

            documents[filename] = {
                "filename": filename,
                "title": metadata.get(
                    "title",
                    "Unknown Title"
                ),
                "authors": metadata.get(
                    "authors",
                    "Unknown Authors"
                )
            }

    return list(
        documents.values()
    )