FROM python:3.11-slim
LABEL authors="NikodemHeitzman"

RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app
RUN chown appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3\
            CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
