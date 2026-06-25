from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from aws_cert_ai.chains.pipeline import analyze_question
from aws_cert_ai.core.config import get_settings
from aws_cert_ai.core.schemas import QuestionInput, QuestionRecord
from aws_cert_ai.rag.local_chroma import ingest_local_knowledge


def _question_from_json(data: dict[str, Any]) -> QuestionRecord:
    """Convert one JSON object from a batch file into a question record."""

    options = data.get("options") or []
    if isinstance(options, str):
        options = [options]
    return QuestionRecord(
        id=data.get("id"),
        question=str(data.get("question", "")).strip(),
        options=options,
        answer=data.get("answer"),
    )


def _print_response(response) -> None:
    """Print an analysis response in a readable CLI format."""

    print("\n=== 分类与知识点 ===")
    print(response.classification.model_dump_json(indent=2))
    print("\n=== 检索片段 ===")
    for index, chunk in enumerate(response.retrieved_context, start=1):
        print(f"[{index}] {chunk.source}")
        print(chunk.content[:500])
    print("\n=== AI 讲解 ===")
    print(response.explanation)


def command_ingest(_: argparse.Namespace) -> None:
    """Import local Markdown and text knowledge files into Chroma."""

    settings = get_settings()
    if settings.rag_provider != "chroma":
        raise SystemExit("ingest 命令只用于本地 Chroma。AWS 知识库请通过 S3/Bedrock KB 数据源同步。")
    count = ingest_local_knowledge(settings)
    if count == 0:
        print(f"没有可导入文档，请把 .md/.txt 放到 {settings.knowledge_dir}")
        return
    print(f"已导入 {count} 个知识切片到 {settings.chroma_dir}")


def command_analyze(args: argparse.Namespace) -> None:
    """Analyze a single question passed directly on the command line."""

    response = analyze_question(get_settings(), QuestionInput(question=args.question))
    _print_response(response)


def command_analyze_file(args: argparse.Namespace) -> None:
    """Analyze every non-empty JSONL record in a question file."""

    settings = get_settings()
    path = Path(args.path)
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        record = _question_from_json(json.loads(line))
        if not record.question:
            print(f"跳过第 {line_number} 行：缺少 question")
            continue
        print(f"\n\n######## Question {record.id or line_number} ########")
        response = analyze_question(settings, record)
        _print_response(response)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser and register subcommands."""

    parser = argparse.ArgumentParser(description="AWS 认证题目分析 AI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="导入本地 AWS 知识库到 Chroma")
    ingest_parser.set_defaults(func=command_ingest)

    analyze_parser = subparsers.add_parser("analyze", help="分析单道 AWS 考试题")
    analyze_parser.add_argument("question", help="题干，可包含选项")
    analyze_parser.set_defaults(func=command_analyze)

    file_parser = subparsers.add_parser("analyze-file", help="批量分析 JSONL 题目文件")
    file_parser.add_argument("path", help="JSONL 文件路径")
    file_parser.set_defaults(func=command_analyze_file)

    return parser


def main() -> None:
    """Run the CLI entrypoint."""

    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
