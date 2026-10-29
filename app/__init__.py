import os

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["APP_ENV"] = os.getenv("APP_ENV", "development")

    # In-memory store keeps the project dependency-free; swap for a DB later.
    notes: list[dict] = []

    @app.get("/")
    def index():
        return jsonify(
            service="flask-docker-app",
            env=app.config["APP_ENV"],
            endpoints=["/health", "/notes"],
        )

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    @app.get("/notes")
    def list_notes():
        return jsonify(notes)

    @app.post("/notes")
    def add_note():
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        if not text:
            return jsonify(error="'text' is required"), 400
        note = {"id": len(notes) + 1, "text": text}
        notes.append(note)
        return jsonify(note), 201

    return app
