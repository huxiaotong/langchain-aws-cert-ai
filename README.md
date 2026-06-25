# AWS 认证题目分析 AI

本项目是一个基于 LangChain 的 AWS 认证题目分析 AI。设计目标：

1. 使用 LangChain 作为 AI 应用编排层
2. 本地可以用 VS Code 开发并运行
3. 可以通过 IaC 部署到 AWS
4. 本地使用 Qwen，AWS 部署时使用 Bedrock 中的 Qwen

## 技术栈

- Python
- FastAPI
- LangChain
- 本地：Ollama Qwen + Chroma Docker service
- AWS：Bedrock Qwen + Bedrock Knowledge Base / OpenSearch
- IaC：预留 `infra/`，推荐 AWS CDK 或 Terraform

## 架构

```text
本地开发：
VS Code
  -> FastAPI / CLI
  -> LangChain
  -> Ollama Qwen
  -> Chroma Docker service
  -> data/knowledge

AWS 部署：
ECS Fargate
  -> FastAPI / LangChain
  -> Bedrock Qwen
  -> Bedrock Knowledge Base
  -> S3
```

本地的 `data/` 目录只用于本地开发和本地 Chroma ingest。AWS 部署时，知识文档应上传到 S3 并由 Bedrock Knowledge Base 同步，应用容器不打包 `data/`。

## 本地开发准备

安装 Ollama 模型：

```bash
ollama pull qwen3:0.6b
ollama pull qwen3-embedding
```

创建本地配置：

```bash
cp .env.example .env
```

## 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 启动 Chroma Docker 服务

本项目只把 Chroma 放到 Docker 中运行。Python / LangChain 应用仍然在 VS Code 和本地虚拟环境中运行，`data/knowledge/` 也保留在项目目录里，不会放进 Chroma container。

```bash
docker compose up -d chroma
```

确认 Chroma 已启动：

```bash
curl http://localhost:8000/api/v2/heartbeat
```

对应 `.env` 配置：

```env
CHROMA_MODE=chroma_http
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_SSL=false
```

Chroma 的向量数据会持久化到本机目录：

```text
.chroma_data/
```

本地 AWS 知识库仍然放在：

```text
data/knowledge/
```

如果以后想退回 Python 进程内嵌入式 Chroma，可以改成：

```env
CHROMA_MODE=chroma_embedded
CHROMA_DIR=.vectorstore/aws_cert
```

## 构建本地知识库

把 AWS 知识资料放到 `data/knowledge/`，支持 `.md` 和 `.txt`。

```bash
python -m aws_cert_ai.app.cli ingest
```

## CLI 分析题目

```bash
python -m aws_cert_ai.app.cli analyze "A company needs a highly available relational database across multiple Availability Zones. Which AWS service feature should they use?"
```

也可以传入题目文件：

```bash
python -m aws_cert_ai.app.cli analyze-file data/questions/sample_questions.jsonl
```

## 启动 API

```bash
uvicorn aws_cert_ai.app.main:app --reload --port 8000
```

健康检查：

```bash
curl http://localhost:8000/health
```

分析接口：

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"question":"A company needs automatic failover for a relational database.","options":["A. RDS Read Replica","B. RDS Multi-AZ"],"answer":"B"}'
```

JSONL 每行格式：

```json
{"id":"q1","question":"题干...","options":["A. ...","B. ..."],"answer":"B"}
```

## 项目结构

```text
aws_cert_ai/
  app/             # FastAPI 和 CLI 入口
  chains/          # LangChain 分类、检索、讲解流程
  core/            # 配置与 Schema
  llm/             # 本地 Qwen / Bedrock Qwen provider
  rag/             # Chroma / Bedrock Knowledge Base retriever
data/
  knowledge/       # 本地 AWS 知识库
  questions/       # 题目样例
infra/
  README.md        # AWS IaC 规划
```

## 切换到 AWS Provider

`.env` 示例：

```env
APP_ENV=aws
LLM_PROVIDER=bedrock
RAG_PROVIDER=bedrock_kb
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=<your-bedrock-qwen-model-id>
BEDROCK_KNOWLEDGE_BASE_ID=<your-knowledge-base-id>
```

业务代码仍然使用同一条 LangChain pipeline，只是底层 provider 从 Ollama/Chroma 切换到 Bedrock/Knowledge Base。
