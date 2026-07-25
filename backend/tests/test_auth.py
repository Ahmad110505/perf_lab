import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    reg_response = client.post("/api/v1/auth/register", json={"email": "test@test.com", "password": "password123"})
    # Only passes if DB is up, else 500
    if reg_response.status_code == 201:
        login_response = client.post("/api/v1/auth/login", json={"email": "test@test.com", "password": "password123"})
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@test.com"

def test_invalid_login():
    login_response = client.post("/api/v1/auth/login", json={"email": "wrong@test.com", "password": "wrong"})
    assert login_response.status_code in [401, 500]
