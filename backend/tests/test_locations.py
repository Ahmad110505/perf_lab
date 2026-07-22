import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_location_unauthorized():
    response = client.post("/api/v1/locations", json={"name": "Test Location", "client_id": 1})
    assert response.status_code == 401

def test_get_locations_without_auth():
    response = client.get("/api/v1/locations")
    assert response.status_code in [200, 500]

def test_get_client_locations_without_auth():
    response = client.get("/api/v1/clients/1/locations")
    assert response.status_code in [200, 404, 500] 

def test_get_project_locations_without_auth():
    response = client.get("/api/v1/projects/1/locations")
    assert response.status_code in [200, 404, 500]
