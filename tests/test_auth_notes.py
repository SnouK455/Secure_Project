import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

db_file = Path("test.db")
if db_file.exists():
    db_file.unlink()

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_register_login_and_notes_crud(client: TestClient) -> None:
    register_resp = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "VeryStrong123"},
    )
    assert register_resp.status_code == 201

    login_resp = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "VeryStrong123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/notes",
        json={"title": "note", "content": "secure content"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    list_resp = client.get("/notes", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    get_resp = client.get(f"/notes/{note_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "note"

    update_resp = client.put(
        f"/notes/{note_id}",
        json={"title": "updated note"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "updated note"

    delete_resp = client.delete(f"/notes/{note_id}", headers=headers)
    assert delete_resp.status_code == 204


def test_unauthorized_access(client: TestClient) -> None:
    resp = client.get("/notes")
    assert resp.status_code == 401
