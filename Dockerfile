FROM python:3.11-slim

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY questionnaires/ questionnaires/
COPY fonts/ fonts/
COPY .streamlit/ .streamlit/

# Create results directory owned by appuser
RUN mkdir -p /app/results && chown -R appuser:appuser /app

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

ENTRYPOINT ["streamlit", "run", "app.py"]
