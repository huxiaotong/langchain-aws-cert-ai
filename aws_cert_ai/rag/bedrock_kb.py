from __future__ import annotations

from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever

from aws_cert_ai.core.config import Settings


def create_bedrock_kb_retriever(settings: Settings) -> AmazonKnowledgeBasesRetriever:
    if not settings.bedrock_knowledge_base_id:
        raise ValueError("BEDROCK_KNOWLEDGE_BASE_ID is required when RAG_PROVIDER=bedrock_kb")

    return AmazonKnowledgeBasesRetriever(
        knowledge_base_id=settings.bedrock_knowledge_base_id,
        retrieval_config={
            "vectorSearchConfiguration": {
                "numberOfResults": settings.top_k,
            }
        },
        region_name=settings.aws_region,
    )
