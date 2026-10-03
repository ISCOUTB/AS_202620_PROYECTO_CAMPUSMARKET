FROM python:3.12.15-slim-bookworm
ARG CAMPUSMARKET_REVISION=development
LABEL org.opencontainers.image.source="https://github.com/ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET"
LABEL org.opencontainers.image.revision=$CAMPUSMARKET_REVISION
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 CAMPUSMARKET_UPLOAD_DIR=/app/backend/uploads
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN python -m pip install --no-cache-dir -r backend/requirements.txt
COPY backend/app backend/app
RUN useradd --uid 10001 --create-home campusmarket && mkdir -p backend/uploads && chown -R campusmarket:campusmarket backend/uploads
RUN printf '%s' "$CAMPUSMARKET_REVISION" > REVISION
USER campusmarket
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--limit-concurrency", "6", "--no-proxy-headers"]
