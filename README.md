# Dockerized Flask App

A small Flask REST API packaged as a production-style Docker image.
Built to practice the DevOps basics: containerization, Linux, and CI.

**Stack:** Python 3.12, Flask, Gunicorn, Docker, Docker Compose, GitHub Actions

## Endpoints

| Method | Path      | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `/`       | Service info                         |
| GET    | `/health` | Health check (used by Docker)        |
| GET    | `/notes`  | List notes                           |
| POST   | `/notes`  | Add a note, body: `{"text": "..."}`  |

## Run with Docker

```bash
docker compose up --build
curl localhost:5000/health
curl -X POST localhost:5000/notes -H "Content-Type: application/json" -d '{"text":"hello"}'
curl localhost:5000/notes
```

Or without compose:

```bash
docker build -t flask-docker-app .
docker run --rm -p 5000:5000 flask-docker-app
```

## Run locally (no Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python wsgi.py
pytest -q
```

## Docker design choices

- **Multi-stage build**: dependencies are installed in a builder stage, and only the virtualenv is copied into the final image, which keeps it small.
- **Non-root user**: the container runs as `appuser` (UID 10001).
- **Gunicorn**: a production WSGI server instead of Flask's dev server.
- **HEALTHCHECK**: Docker marks the container healthy via `/health`.
- **Hardened compose**: read-only root filesystem, `no-new-privileges`, restart policy.
- **`.dockerignore`**: keeps tests, git history, and caches out of the build context.
- **Layer caching**: `requirements.txt` is copied before the source so dependency layers are reused.

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs the tests, builds the image, then starts the container and curls `/health` as a smoke test.

## Ideas to extend

- Add Postgres to `docker-compose.yml` and replace the in-memory store
- Push the image to Docker Hub or GHCR from CI
- Add a Trivy image scan step
- Deploy to a Linux VM with systemd or to a small Kubernetes cluster
