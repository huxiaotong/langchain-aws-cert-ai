from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate


CLASSIFY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是 AWS 认证考试教练。请严格输出 JSON，不要输出 Markdown。",
        ),
        (
            "human",
            """分析下面 AWS 考试题，完成分类与知识点抽取。

题目：
{question}

请输出 JSON，字段如下：
- exam_domain: 认证考试领域，例如 Design Resilient Architectures
- aws_services: 涉及的 AWS 服务数组
- knowledge_points: 关键知识点数组
- question_type: 题型，例如 单选/多选/场景题/排错题
- difficulty: easy/medium/hard
- keywords: 检索关键词数组
""",
        ),
    ]
)


EXPLAIN_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是 AWS 认证考试讲师。请用中文讲解，重点帮助考生理解考点和排除干扰项。必须优先基于检索到的知识库内容，不确定时明确说明。",
        ),
        (
            "human",
            """请基于题目分析和检索到的知识库内容，给出考试向讲解。

题目：
{question}

分类与知识点：
{classification}

知识库检索结果：
{context}

请按以下结构输出：
1. 题目分类
2. 核心考点
3. 解题思路
4. 选项/干扰项判断方法
5. 需要记住的 AWS 规则
""",
        ),
    ]
)
