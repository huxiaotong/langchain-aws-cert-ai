from __future__ import annotations

from fastapi import FastAPI

from aws_cert_ai.chains.pipeline import analyze_question
from aws_cert_ai.core.config import get_settings
from aws_cert_ai.core.schemas import AnalysisResponse, QuestionInput


app = FastAPI(title="AWS Certification Question Analysis AI")


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health and active provider configuration."""

    settings = get_settings()
    return {
        "status": "ok",
        "app_env": settings.app_env,
        "llm_provider": settings.llm_provider,
        "rag_provider": settings.rag_provider,
    }


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: QuestionInput) -> AnalysisResponse:
    """Analyze one AWS certification question through the LangChain pipeline."""

    return analyze_question(get_settings(), payload)
