from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(pdf_path: str):

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    loader = PyPDFLoader(str(pdf_file))

    documents = loader.load()

    if not documents:
        raise ValueError(
            f"No content could be extracted from: {pdf_path}"
        )

    return documents