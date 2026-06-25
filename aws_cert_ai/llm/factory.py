from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from aws_cert_ai.core.config import Settings
from aws_cert_ai.llm.bedrock_qwen import create_bedrock_qwen
from aws_cert_ai.llm.local_qwen import create_local_qwen


def create_chat_model(settings: Settings) -> BaseChatModel:
    """Create the configured chat model provider for local or AWS execution."""

    if settings.llm_provider == "ollama":
        return create_local_qwen(settings)
    if settings.llm_provider == "bedrock":
        return create_bedrock_qwen(settings)
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
