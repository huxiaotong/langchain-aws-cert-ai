from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: Literal["local", "aws"] = "local"
    log_level: str = "INFO"

    llm_provider: Literal["ollama", "bedrock"] = "ollama"
    rag_provider: Literal["chroma", "bedrock_kb"] = "chroma"

    local_llm_model: str = "qwen2.5:7b"
    local_embedding_model: str = "bge-m3"
    chroma_dir: Path = Path(".vectorstore/aws_cert")
    chroma_collection: str = "aws_cert_knowledge"
    knowledge_dir: Path = Path("data/knowledge")

    aws_region: str = "us-east-1"
    bedrock_model_id: str = "qwen.qwen3-32b"
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    bedrock_knowledge_base_id: str | None = None

    temperature: float = 0.1
    top_k: int = 5


def get_settings() -> Settings:
    return Settings()
