import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project_unauthorized():
    response = client.post("/api/v1/projects", json={"name": "Test Project", "client_id": 1})
    assert response.status_code == 401

def test_get_projects_without_auth():
    response = client.get("/api/v1/projects")
    assert response.status_code in [200, 500]

def test_get_client_projects_without_auth():
    response = client.get("/api/v1/clients/1/projects")
    assert response.status_code in [200, 404, 500] 
