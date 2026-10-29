# syntax=docker/dockerfile:1

# ---- Builder: install dependencies into a virtualenv ----
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---- Runtime: small image, non-root user ----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_ENV=production \
    PORT=5000

RUN useradd --create-home --uid 10001 appuser

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser wsgi.py .

USER appuser
EXPOSE 5000

# Python is already in the image, so no curl needed for the healthcheck.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"PORT\",\"5000\")}/health', timeout=2)"

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --access-logfile - wsgi:app"]
