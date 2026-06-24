from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QuestionInput(BaseModel):
    question: str = Field(..., description="AWS exam question stem")
    options: list[str] = Field(default_factory=list)
    answer: str | None = None

    def render(self) -> str:
        parts = [self.question.strip()]
        if self.options:
            parts.append("\n".join(self.options))
        if self.answer:
            parts.append(f"参考答案：{self.answer}")
        return "\n\n".join(part for part in parts if part)


class QuestionRecord(QuestionInput):
    id: str | None = None


class ClassificationResult(BaseModel):
    exam_domain: str | None = None
    aws_services: list[str] = Field(default_factory=list)
    knowledge_points: list[str] = Field(default_factory=list)
    question_type: str | None = None
    difficulty: str | None = None
    keywords: list[str] = Field(default_factory=list)
    raw: str | None = None


class RetrievedChunk(BaseModel):
    content: str
    source: str = "unknown"
    score: float | None = None


class AnalysisResponse(BaseModel):
    classification: ClassificationResult
    retrieved_context: list[RetrievedChunk]
    explanation: str
    provider: dict[str, Any]
