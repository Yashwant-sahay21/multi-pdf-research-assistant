from pathlib import Path

from app.rag.pdf_loader import load_pdf
from app.rag.chunker import split_documents
from app.rag.vector_store import create_vector_store
from app.rag.metadata import extract_metadata


PDF_FOLDER = "data"


def ingest_documents():

    pdf_files = list(
        Path(PDF_FOLDER).glob("*.pdf")
    )

    if not pdf_files:
        print("No PDF files found.")
        return

    all_chunks = []

    for pdf_file in pdf_files:

        print(f"\nProcessing: {pdf_file.name}")

        documents = load_pdf(str(pdf_file))

        metadata = extract_metadata(
            documents,
            str(pdf_file)
        )

        chunks = split_documents(documents)

        for chunk in chunks:
            chunk.metadata.update(metadata)

        all_chunks.extend(chunks)

        print(
            f"Pages: {len(documents)} | Chunks: {len(chunks)}"
        )

    print(f"\nTotal Chunks: {len(all_chunks)}")

    create_vector_store(all_chunks)

    print("\nIngestion Complete.")


if __name__ == "__main__":
    ingest_documents()