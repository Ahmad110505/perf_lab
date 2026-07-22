import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data
    assert data["status"] in ["healthy", "degraded"]
