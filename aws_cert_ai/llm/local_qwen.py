from __future__ import annotations

from langchain_ollama import ChatOllama

from aws_cert_ai.core.config import Settings


def create_local_qwen(settings: Settings) -> ChatOllama:
    """Create the local Ollama-backed Qwen chat model."""

    return ChatOllama(
        model=settings.local_llm_model,
        temperature=settings.temperature,
    )
