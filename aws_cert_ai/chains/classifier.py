from __future__ import annotations

import json
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from aws_cert_ai.chains.prompts import CLASSIFY_PROMPT
from aws_cert_ai.core.schemas import ClassificationResult


def _strip_json_markdown(raw: str) -> str:
    """Remove optional Markdown fences around model-produced JSON."""

    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        return cleaned.removeprefix("```json").removesuffix("```").strip()
    if cleaned.startswith("```"):
        return cleaned.removeprefix("```").removesuffix("```").strip()
    return cleaned


def _parse_classification(raw: str) -> ClassificationResult:
    """Parse model output into a classification object with raw fallback."""

    try:
        payload: dict[str, Any] = json.loads(_strip_json_markdown(raw))
        return ClassificationResult(**payload)
    except Exception:
        return ClassificationResult(raw=raw)


def classify_question(llm: BaseChatModel, rendered_question: str) -> ClassificationResult:
    """Classify a rendered question and extract services, topics, and keywords."""

    chain = CLASSIFY_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({"question": rendered_question})
    return _parse_classification(raw)
