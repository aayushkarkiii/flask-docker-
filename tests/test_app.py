import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_index_lists_endpoints(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "/health" in res.get_json()["endpoints"]


def test_add_and_list_notes(client):
    res = client.post("/notes", json={"text": "hello docker"})
    assert res.status_code == 201
    assert res.get_json() == {"id": 1, "text": "hello docker"}

    res = client.get("/notes")
    assert res.get_json() == [{"id": 1, "text": "hello docker"}]


def test_add_note_requires_text(client):
    res = client.post("/notes", json={"text": "   "})
    assert res.status_code == 400
