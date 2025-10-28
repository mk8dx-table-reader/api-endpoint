FROM python:3.12-slim

# Metadata
LABEL org.opencontainers.image.source="https://github.com/mk8dx-table-reader/api-endpoint"

# Setup project and install dependencies
WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV HOST=0.0.0.0 PORT=8000

CMD ["sh", "-c", "uvicorn api_server:app --host ${HOST} --port ${PORT}"]
