import streamlit as st
import requests
import uuid

import os

API_URL = os.getenv(
    "API_URL",
    "http://api:8000"
)
st.set_page_config(
    page_title="Research Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Research Assistant")
st.markdown(
    "Ask questions about your uploaded research papers."
)

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---------------------------
# Load Documents
# ---------------------------

documents = []

try:
    response = requests.get(
        f"{API_URL}/documents"
    )

    if response.status_code == 200:
        documents = response.json()

except Exception:
    st.error(
        "Unable to connect to FastAPI backend."
    )

# ---------------------------
# Sidebar
# ---------------------------

st.sidebar.header("Documents")

document_names = [
    doc["filename"]
    for doc in documents
]

selected_document = None

if document_names:

    selected_document = st.sidebar.selectbox(
        "Select Document",
        document_names
    )

else:

    st.sidebar.warning(
        "No documents available."
    )

# ---------------------------
# Upload PDF
# ---------------------------

st.sidebar.header("Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if st.sidebar.button("Upload"):

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        if response.status_code == 200:

            st.sidebar.success(
                "PDF uploaded successfully."
            )

            st.rerun()

        else:

            st.sidebar.error(
                "Upload failed."
            )

# ---------------------------
# Chat Interface
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    payload = {
        "session_id":
            st.session_state.session_id,
        "filename":
            selected_document,
        "question":
            question
    }

    try:

        response = requests.post(
            f"{API_URL}/chat",
            json=payload
        )

        result = response.json()

        answer = result.get(
            "answer",
            "No answer."
        )

        sources = result.get(
            "sources",
            []
        )

        response_text = answer

        if sources:

            response_text += "\n\n### Sources\n"

            for source in sources:

                response_text += (
                    f"- {source['filename']} "
                    f"(Page {source['page']})\n"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text
            }
        )

        with st.chat_message(
            "assistant"
        ):
            st.markdown(
                response_text
            )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )