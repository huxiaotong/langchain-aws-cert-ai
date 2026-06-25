from __future__ import annotations

from langchain_aws import ChatBedrockConverse

from aws_cert_ai.core.config import Settings


def create_bedrock_qwen(settings: Settings) -> ChatBedrockConverse:
    """Create the AWS Bedrock-backed Qwen chat model."""

    return ChatBedrockConverse(
        model=settings.bedrock_model_id,
        region_name=settings.aws_region,
        temperature=settings.temperature,
    )
