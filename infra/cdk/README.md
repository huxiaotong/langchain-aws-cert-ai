# CDK Deployment

This is a starter AWS CDK stack for deploying the FastAPI + LangChain app.

It creates:

- ECR repository for the application image
- ECS Fargate cluster and service
- Application Load Balancer
- CloudWatch logs
- Task role permissions to invoke Bedrock and retrieve from Bedrock Knowledge Bases

## Deploy

```bash
cd infra/cdk
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy \
  -c bedrockModelId=<your-bedrock-qwen-model-id> \
  -c bedrockKnowledgeBaseId=<your-kb-id>
```

Build and push the Docker image to the created ECR repository, then update the ECS service image tag.
