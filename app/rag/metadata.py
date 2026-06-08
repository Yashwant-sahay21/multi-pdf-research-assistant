import os


def extract_metadata(documents, pdf_path=None):

    metadata = {
        "title": "",
        "authors": "",
        "filename": "",
        "source": ""
    }

    if pdf_path:
        metadata["filename"] = os.path.basename(pdf_path)
        metadata["source"] = pdf_path

    if not documents:
        return metadata

    first_page = documents[0].page_content

    lines = [
        line.strip()
        for line in first_page.split("\n")
        if line.strip()
    ]

    # Title

    if len(lines) >= 3:
        metadata["title"] = " ".join(lines[:3])

    # Authors

    if len(lines) >= 4:
        metadata["authors"] = lines[3]

    return metadata