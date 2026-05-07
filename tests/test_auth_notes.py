import os

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test_secret_for_ci_at_least_32_bytes"

from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
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


def test_public_metadata_endpoints(client: TestClient) -> None:
    root_resp = client.get("/")
    assert root_resp.status_code == 200
    assert root_resp.json()["docs"] == "/docs"
    assert root_resp.headers["X-Content-Type-Options"] == "nosniff"
    assert root_resp.headers["Cache-Control"] == "no-store"
    assert root_resp.headers["Cross-Origin-Resource-Policy"] == "same-origin"

    robots_resp = client.get("/robots.txt")
    assert robots_resp.status_code == 200
    assert "User-agent" in robots_resp.text


def test_invalid_token_returns_unauthorized(client: TestClient) -> None:
    resp = client.get("/notes", headers={"Authorization": "Bearer not-a-valid-token"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid token"


def test_duplicate_registration_is_rejected(client: TestClient) -> None:
    payload = {"email": "user@example.com", "password": "VeryStrong123"}

    assert client.post("/auth/register", json=payload).status_code == 201
    duplicate_resp = client.post("/auth/register", json=payload)

    assert duplicate_resp.status_code == 400
    assert duplicate_resp.json()["detail"] == "Email is already registered"


def test_users_cannot_access_each_others_notes(client: TestClient) -> None:
    first_user_token = _register_and_login(client, "first@example.com")
    second_user_token = _register_and_login(client, "second@example.com")

    create_resp = client.post(
        "/notes",
        json={"title": "private", "content": "owned by first user"},
        headers={"Authorization": f"Bearer {first_user_token}"},
    )
    assert create_resp.status_code == 201
    note_id = create_resp.json()["id"]

    second_user_headers = {"Authorization": f"Bearer {second_user_token}"}
    assert client.get(f"/notes/{note_id}", headers=second_user_headers).status_code == 404
    assert client.delete(f"/notes/{note_id}", headers=second_user_headers).status_code == 404


def test_empty_note_update_is_rejected(client: TestClient) -> None:
    token = _register_and_login(client, "user@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    create_resp = client.post(
        "/notes",
        json={"title": "note", "content": "content"},
        headers=headers,
    )
    assert create_resp.status_code == 201

    update_resp = client.put(f"/notes/{create_resp.json()['id']}", json={}, headers=headers)

    assert update_resp.status_code == 400
    assert update_resp.json()["detail"] == "No fields to update"


def _register_and_login(client: TestClient, email: str) -> str:
    password = "VeryStrong123"
    register_resp = client.post("/auth/register", json={"email": email, "password": password})
    assert register_resp.status_code == 201

    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    assert login_resp.status_code == 200
    return login_resp.json()["access_token"]
