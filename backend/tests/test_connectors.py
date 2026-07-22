import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user_id
import uuid

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user_id] = lambda: 1
    yield
    app.dependency_overrides.clear()

def create_integration(provider="procore", status="connected"):
    client_res = client.post("/api/v1/clients", json={"name": f"Test Client {uuid.uuid4()}"})
    c_id = client_res.json()["id"]

    int_res = client.post("/api/v1/integrations", json={
        "client_id": c_id,
        "name": f"Test Sync {uuid.uuid4()}",
        "provider": provider
    })
    int_id = int_res.json()["id"]
    
    client.patch(f"/api/v1/integrations/{int_id}/status?new_status={status}")
    return int_id

def test_sync_unauthorized():
    app.dependency_overrides.clear()
    res = client.post("/api/v1/integrations/1/sync")
    assert res.status_code == 401
    app.dependency_overrides[get_current_user_id] = lambda: 1

def test_sync_bad_integration():
    res = client.post("/api/v1/integrations/9999/sync")
    assert res.status_code == 404

def test_sync_bad_status():
    int_id = create_integration(status="error")
    res = client.post(f"/api/v1/integrations/{int_id}/sync")
    assert res.status_code == 400

@patch("app.modules.connectors.providers.procore.ProcoreConnector.fetch_data")
def test_sync_success(mock_fetch):
    mock_fetch.return_value = [{"procore_id": 99, "name": "Mocked"}]
    int_id = create_integration(status="connected")
    
    res = client.post(f"/api/v1/integrations/{int_id}/sync")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["records_processed"] == 1
    assert data["error_message"] is None
    
    int_res = client.get(f"/api/v1/integrations/{int_id}")
    assert int_res.json()["last_synced_at"] is not None

@patch("app.modules.connectors.providers.procore.ProcoreConnector.fetch_data")
def test_sync_failure(mock_fetch):
    mock_fetch.side_effect = Exception("Network timeout")
    int_id = create_integration(status="connected")
    
    res = client.post(f"/api/v1/integrations/{int_id}/sync")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "failed"
    assert data["error_message"] == "Network timeout"
    
    int_res = client.get(f"/api/v1/integrations/{int_id}")
    assert int_res.json()["status"] == "error"
