from __future__ import annotations

from langchain_ollama import ChatOllama

from aws_cert_ai.core.config import Settings


def create_local_qwen(settings: Settings) -> ChatOllama:
    return ChatOllama(
        model=settings.local_llm_model,
        temperature=settings.temperature,
    )
