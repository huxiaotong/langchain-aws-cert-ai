#!/usr/bin/env python3
from aws_cdk import App

from stacks.aws_cert_ai_stack import AwsCertAiStack


app = App()

AwsCertAiStack(
    app,
    "AwsCertAiStack",
    project_name=app.node.try_get_context("projectName") or "aws-cert-ai",
    container_port=int(app.node.try_get_context("containerPort") or 8000),
    bedrock_model_id=app.node.try_get_context("bedrockModelId") or "qwen.qwen3-32b",
    bedrock_knowledge_base_id=app.node.try_get_context("bedrockKnowledgeBaseId") or "",
)

app.synth()
