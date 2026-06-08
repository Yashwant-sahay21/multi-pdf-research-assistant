from app.rag.llm import llm
from app.rag.document_classifier import (
    detect_document_type
)


def format_history(chat_history):

    if not chat_history:
        return ""

    history_text = ""

    for msg in chat_history:

        history_text += (
            f"{msg['role'].upper()}: "
            f"{msg['content']}\n"
        )

    return history_text


def ask_question(
    vectordb,
    question,
    filename=None,
    chat_history=None
):

    question_lower = question.lower().strip()

    history = format_history(
        chat_history
    )

    # =====================================
    # TITLE QUESTIONS
    # =====================================

    if "title" in question_lower:

        docs = vectordb.similarity_search(
            question,
            k=1,
            filter={"filename": filename}
            if filename else None
        )

        if docs:

            title = docs[0].metadata.get(
                "title",
                ""
            )

            if title:

                return {
                    "answer": title,
                    "sources": []
                }

    # =====================================
    # AUTHOR QUESTIONS
    # =====================================

    if "author" in question_lower:

        docs = vectordb.similarity_search(
            question,
            k=1,
            filter={"filename": filename}
            if filename else None
        )

        if docs:

            authors = docs[0].metadata.get(
                "authors",
                ""
            )

            if authors:

                return {
                    "answer": authors,
                    "sources": []
                }

    # =====================================
    # SUMMARY QUESTIONS
    # =====================================

    summary_keywords = [
        "summary",
        "summarize",
        "overview",
        "abstract"
    ]

    if any(
        keyword in question_lower
        for keyword in summary_keywords
    ):

        docs = vectordb.similarity_search(
            "abstract introduction methodology results conclusion",
            k=10,
            filter={"filename": filename}
            if filename else None
        )

        if not docs:

            return {
                "answer": "The information is not available in the document.",
                "sources": []
            }

        context = ""
        sources = []

        for doc in docs:

            page = doc.metadata.get(
                "page",
                "Unknown"
            )

            file_name = doc.metadata.get(
                "filename",
                "Unknown"
            )

            sources.append({
                "filename": file_name,
                "page": page + 1
                if isinstance(page, int)
                else page
            })

            context += (
                f"\n[Source: {file_name}, "
                f"Page {page}]\n"
            )

            context += doc.page_content
            context += "\n"

        # =====================================
        # DOCUMENT TYPE DETECTION
        # =====================================

        document_type = detect_document_type(
            context
        )

        print(
            f"DOCUMENT TYPE: "
            f"{document_type}"
        )

        # =====================================
        # RESEARCH PAPER
        # =====================================

        if document_type == "research_paper":

            prompt = f"""
You are an expert research paper assistant.

Conversation History:
{history}

Create a structured summary using ONLY the provided context.

Format:

1. Objective
2. Dataset
3. Methodology
4. Models Used
5. Results
6. Conclusion

Context:
{context}

Summary:
"""

        # =====================================
        # NOTIFICATION
        # =====================================

        elif document_type == "notification":

            prompt = f"""
You are an expert assistant.

Conversation History:
{history}

Create a structured summary using ONLY the provided context.

Format:

1. Purpose
2. Eligibility
3. Important Instructions
4. Important Dates
5. Key Rules
6. Conclusion

Context:
{context}

Summary:
"""

        # =====================================
        # RESUME
        # =====================================

        elif document_type == "resume":

            prompt = f"""
You are an expert assistant.

Conversation History:
{history}

Create a structured summary using ONLY the provided context.

Format:

1. Profile
2. Education
3. Skills
4. Experience
5. Projects
6. Certifications

Context:
{context}

Summary:
"""

        # =====================================
        # GENERAL DOCUMENT
        # =====================================

        else:

            prompt = f"""
You are an expert assistant.

Conversation History:
{history}

Create a concise structured summary using ONLY the provided context.

Context:
{context}

Summary:
"""

        response = llm.invoke(
            prompt
        )

        return {
            "answer": response.content.strip(),
            "sources": sources
        }

    # =====================================
    # NORMAL QUESTION ANSWERING
    # =====================================

    docs = vectordb.similarity_search(
        question,
        k=5,
        filter={"filename": filename}
        if filename else None
    )

    if not docs:

        return {
            "answer":
                "The information is not available in the document.",
            "sources": []
        }

    context = ""
    sources = []

    for doc in docs:

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        file_name = doc.metadata.get(
            "filename",
            "Unknown"
        )

        sources.append({
            "filename": file_name,
            "page": page + 1
            if isinstance(page, int)
            else page
        })

        context += (
            f"\n[Source: {file_name}, "
            f"Page {page}]\n"
        )

        context += doc.page_content
        context += "\n"

    prompt = f"""
You are an expert research assistant.

Conversation History:
{history}

Use ONLY the provided context.

Rules:
- Answer directly.
- Be concise but complete.
- Use conversation history to resolve references.
- Do not invent information.
- If the answer is unavailable, reply exactly:

The information is not available in the document.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(
        prompt
    )

    return {
        "answer": response.content.strip(),
        "sources": sources
    }