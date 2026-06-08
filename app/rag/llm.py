import os

from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3:latest",
    temperature=0,
    base_url=os.getenv(
        "OLLAMA_HOST",
        "http://host.docker.internal:11434"
    )
)