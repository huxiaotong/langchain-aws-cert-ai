from __future__ import annotations

from pathlib import Path
from typing import Iterable

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from aws_cert_ai.core.config import Settings
from aws_cert_ai.core.schemas import RetrievedChunk


SUPPORTED_EXTENSIONS = {".md", ".txt"}


def _iter_knowledge_files(knowledge_dir: Path) -> Iterable[Path]:
    """Yield supported local knowledge files from the configured directory."""

    if not knowledge_dir.exists():
        return []
    return (
        path
        for path in knowledge_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def _load_documents(knowledge_dir: Path) -> list[Document]:
    """Load local knowledge files into LangChain document objects."""

    documents: list[Document] = []
    for path in _iter_knowledge_files(knowledge_dir):
        text = path.read_text(encoding="utf-8")
        if text.strip():
            documents.append(Document(page_content=text, metadata={"source": str(path)}))
    return documents


def _split_documents(documents: list[Document]) -> list[Document]:
    """Split source documents into overlapping chunks for vector search."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n## ", "\n### ", "\n\n", "\n", "。", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def create_embeddings(settings: Settings) -> OllamaEmbeddings:
    """Create the local embedding model used by Chroma."""

    return OllamaEmbeddings(model=settings.local_embedding_model)


def create_vectorstore(settings: Settings) -> Chroma:
    """Create a Chroma vector store using HTTP server or embedded persistence."""

    if settings.chroma_mode == "chroma_http":
        client = chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            ssl=settings.chroma_ssl,
        )
        return Chroma(
            collection_name=settings.chroma_collection,
            embedding_function=create_embeddings(settings),
            client=client,
        )

    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=create_embeddings(settings),
        persist_directory=str(settings.chroma_dir),
    )


def ingest_local_knowledge(settings: Settings) -> int:
    """Ingest local knowledge files into Chroma and return inserted chunk count."""

    documents = _load_documents(settings.knowledge_dir)
    chunks = _split_documents(documents)
    if not chunks:
        return 0
    vectorstore = create_vectorstore(settings)
    vectorstore.add_documents(chunks)
    return len(chunks)


def create_chroma_retriever(settings: Settings) -> VectorStoreRetriever:
    """Create a LangChain retriever backed by the local Chroma collection."""

    return create_vectorstore(settings).as_retriever(
        search_kwargs={"k": settings.top_k},
    )


def documents_to_chunks(documents: list[Document]) -> list[RetrievedChunk]:
    """Convert LangChain documents to API-friendly retrieved chunk objects."""

    return [
        RetrievedChunk(
            content=document.page_content,
            source=str(document.metadata.get("source", "unknown")),
        )
        for document in documents
    ]
