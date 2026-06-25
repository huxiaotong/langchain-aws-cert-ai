from __future__ import annotations

import json

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from aws_cert_ai.chains.prompts import EXPLAIN_PROMPT
from aws_cert_ai.core.schemas import ClassificationResult, RetrievedChunk


def render_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved knowledge chunks for inclusion in the explanation prompt."""

    if not chunks:
        return "未检索到相关知识库内容。"
    return "\n\n".join(
        f"[{index}] source={chunk.source}\n{chunk.content}"
        for index, chunk in enumerate(chunks, start=1)
    )


def explain_question(
    llm: BaseChatModel,
    rendered_question: str,
    classification: ClassificationResult,
    chunks: list[RetrievedChunk],
) -> str:
    """Generate a Chinese exam-oriented explanation from question and RAG context."""

    chain = EXPLAIN_PROMPT | llm | StrOutputParser()
    return chain.invoke(
        {
            "question": rendered_question,
            "classification": json.dumps(
                classification.model_dump(exclude_none=True),
                ensure_ascii=False,
                indent=2,
            ),
            "context": render_context(chunks),
        }
    )
