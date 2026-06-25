from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QuestionInput(BaseModel):
    """User-provided AWS exam question payload."""

    question: str = Field(..., description="AWS exam question stem")
    options: list[str] = Field(default_factory=list)
    answer: str | None = None

    def render(self) -> str:
        """Render the question, options, and optional answer into one prompt string."""

        parts = [self.question.strip()]
        if self.options:
            parts.append("\n".join(self.options))
        if self.answer:
            parts.append(f"参考答案：{self.answer}")
        return "\n\n".join(part for part in parts if part)


class QuestionRecord(QuestionInput):
    """Question payload with an optional stable identifier for batch input."""

    id: str | None = None


class ClassificationResult(BaseModel):
    """Structured classification and knowledge-point extraction result."""

    exam_domain: str | None = None
    aws_services: list[str] = Field(default_factory=list)
    knowledge_points: list[str] = Field(default_factory=list)
    question_type: str | None = None
    difficulty: str | None = None
    keywords: list[str] = Field(default_factory=list)
    raw: str | None = None


class RetrievedChunk(BaseModel):
    """A knowledge chunk retrieved from the configured RAG backend."""

    content: str
    source: str = "unknown"
    score: float | None = None


class AnalysisResponse(BaseModel):
    """Full response returned by the analysis pipeline and API."""

    classification: ClassificationResult
    retrieved_context: list[RetrievedChunk]
    explanation: str
    provider: dict[str, Any]
