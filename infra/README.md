# AWS IaC Plan

This folder is reserved for the AWS deployment stack.

Recommended target architecture:

- ECS Fargate runs the FastAPI + LangChain container.
- Bedrock Qwen is used as the hosted LLM.
- Bedrock Knowledge Base or OpenSearch Serverless is used for RAG.
- S3 stores source knowledge documents.
- CloudWatch stores logs.
- IAM roles grant least-privilege access to Bedrock and knowledge sources.

The application container should not include local `data/` files. In AWS, source knowledge documents belong in S3 and should be indexed by Bedrock Knowledge Base or the selected vector backend.

Suggested first IaC implementation:

1. Create ECR repository.
2. Create ECS cluster and Fargate service.
3. Expose the API via ALB.
4. Add task role permissions for Bedrock invoke.
5. Add environment variables:
   - `APP_ENV=aws`
   - `LLM_PROVIDER=bedrock`
   - `RAG_PROVIDER=bedrock_kb`
   - `BEDROCK_MODEL_ID=...`
   - `BEDROCK_KNOWLEDGE_BASE_ID=...`

A starter CDK implementation is available in `infra/cdk`.
