# ---------- Build stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system build deps (only here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps into a separate folder
COPY requirements/base.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r base.txt


# ---------- Runner ----------
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy installed deps
COPY --from=builder /install /usr/local

# Copy app
COPY adoption_model.pkl model_config.json ./
COPY app/ ./app/

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]