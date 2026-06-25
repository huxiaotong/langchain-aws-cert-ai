from __future__ import annotations

from langchain_core.retrievers import BaseRetriever

from aws_cert_ai.core.config import Settings
from aws_cert_ai.rag.bedrock_kb import create_bedrock_kb_retriever
from aws_cert_ai.rag.local_chroma import create_chroma_retriever


def create_retriever(settings: Settings) -> BaseRetriever:
    """Create the configured RAG retriever for local or AWS execution."""

    if settings.rag_provider == "chroma":
        return create_chroma_retriever(settings)
    if settings.rag_provider == "bedrock_kb":
        return create_bedrock_kb_retriever(settings)
    raise ValueError(f"Unsupported RAG provider: {settings.rag_provider}")
