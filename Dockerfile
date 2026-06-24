FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY aws_cert_ai ./aws_cert_ai
COPY data ./data

EXPOSE 8000

CMD ["uvicorn", "aws_cert_ai.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
