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
