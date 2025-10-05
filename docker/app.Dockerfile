# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.2
COPY pyproject.toml README.md ./
COPY src ./src

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY pyproject.toml README.md ./
COPY src ./src

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
