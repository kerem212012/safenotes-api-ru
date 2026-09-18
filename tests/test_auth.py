import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.main import app, engine


@pytest.fixture
def client() -> TestClient:
    SQLModel.metadata.drop_all(engine)
    with TestClient(app) as test_client:
        yield test_client


def token_for(client: TestClient, username: str) -> str:
    registered = client.post("/auth/register", json={"username": username, "password": "strong-pass-123"})
    assert registered.status_code == 201
    response = client.post("/auth/token", data={"username": username, "password": "strong-pass-123"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_private_notes_are_isolated(client: TestClient) -> None:
    first = token_for(client, "first-user")
    second = token_for(client, "second-user")
    created = client.post("/notes", json={"title": "Private", "body": "Only mine"}, headers={"Authorization": f"Bearer {first}"})
    assert created.status_code == 201
    assert len(client.get("/notes", headers={"Authorization": f"Bearer {first}"}).json()) == 1
    assert client.get("/notes", headers={"Authorization": f"Bearer {second}"}).json() == []


def test_protected_route_requires_valid_token(client: TestClient) -> None:
    assert client.get("/users/me").status_code == 401
    assert client.get("/users/me", headers={"Authorization": "Bearer broken"}).status_code == 401
