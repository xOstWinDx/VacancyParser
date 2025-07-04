FROM python:3.12-slim
LABEL authors="ostwind"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

RUN chmod 666 /app/vacancy-parser.session*  # Даём права всем



CMD ["poetry", "run", "python", "main.py"]
