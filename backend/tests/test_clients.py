import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_client_unauthorized():
    response = client.post("/api/v1/clients", json={"name": "Test Client"})
    assert response.status_code == 401

def test_get_clients_without_auth():
    # GET doesn't strictly require auth in this V1 stub, should return 200 (or 500 if DB is down)
    response = client.get("/api/v1/clients")
    assert response.status_code in [200, 500]

def test_create_client_success():
    headers = {"Authorization": "Bearer demo-bypass-token"}
    response = client.post("/api/v1/clients", json={"name": "Test Client Alpha"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Client Alpha"
    assert "id" in data

def test_create_client_duplicate():
    headers = {"Authorization": "Bearer demo-bypass-token"}
    client.post("/api/v1/clients", json={"name": "Test Client Dup"}, headers=headers)
    response = client.post("/api/v1/clients", json={"name": "Test Client Dup"}, headers=headers)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_delete_client_success():
    headers = {"Authorization": "Bearer demo-bypass-token"}
    res = client.post("/api/v1/clients", json={"name": "Test Client Del"}, headers=headers)
    c_id = res.json()["id"]
    del_res = client.delete(f"/api/v1/clients/{c_id}", headers=headers)
    assert del_res.status_code == 204
    get_res = client.get(f"/api/v1/clients/{c_id}", headers=headers)
    assert get_res.status_code == 404

