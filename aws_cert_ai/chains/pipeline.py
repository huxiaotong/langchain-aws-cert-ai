from __future__ import annotations

from langchain_core.documents import Document

from aws_cert_ai.chains.classifier import classify_question
from aws_cert_ai.chains.explainer import explain_question
from aws_cert_ai.core.config import Settings
from aws_cert_ai.core.schemas import AnalysisResponse, ClassificationResult, QuestionInput, RetrievedChunk
from aws_cert_ai.llm.factory import create_chat_model
from aws_cert_ai.rag.retriever_factory import create_retriever


def _build_retrieval_query(question: str, classification: ClassificationResult) -> str:
    terms = (
        classification.keywords
        + classification.knowledge_points
        + classification.aws_services
    )
    return f"{question}\n\n检索关键词：{' '.join(terms)}"


def _document_to_chunk(document: Document) -> RetrievedChunk:
    score = document.metadata.get("score")
    return RetrievedChunk(
        content=document.page_content,
        source=str(document.metadata.get("source", "unknown")),
        score=score if isinstance(score, float) else None,
    )


def analyze_question(settings: Settings, question_input: QuestionInput) -> AnalysisResponse:
    llm = create_chat_model(settings)
    retriever = create_retriever(settings)

    rendered_question = question_input.render()
    classification = classify_question(llm, rendered_question)
    retrieval_query = _build_retrieval_query(rendered_question, classification)
    documents = retriever.invoke(retrieval_query)
    chunks = [_document_to_chunk(document) for document in documents]
    explanation = explain_question(llm, rendered_question, classification, chunks)

    return AnalysisResponse(
        classification=classification,
        retrieved_context=chunks,
        explanation=explanation,
        provider={
            "app_env": settings.app_env,
            "llm_provider": settings.llm_provider,
            "rag_provider": settings.rag_provider,
        },
    )
