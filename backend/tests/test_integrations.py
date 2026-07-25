import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user_id

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user_id] = lambda: 1
    yield
    app.dependency_overrides.clear()

def test_create_integration_unauthorized():
    app.dependency_overrides.clear()
    response = client.post("/api/v1/integrations", json={
        "client_id": 1,
        "name": "Test",
        "provider": "procore"
    })
    assert response.status_code == 401
    app.dependency_overrides[get_current_user_id] = lambda: 1

def test_create_integration_bad_client():
    response = client.post("/api/v1/integrations", json={
        "client_id": 9999,
        "name": "Test",
        "provider": "procore"
    })
    assert response.status_code == 404

def test_create_and_duplicate_provider():
    import uuid
    client_res = client.post("/api/v1/clients", json={"name": f"Integration Client {uuid.uuid4()}"})
    assert client_res.status_code == 201
    c_id = client_res.json()["id"]

    payload = {
        "client_id": c_id,
        "name": "Procore Sync",
        "provider": "procore",
        "credentials_ref": "vault-id-12345",
        "config": {"url": "https://api.procore.com"}
    }
    res1 = client.post("/api/v1/integrations", json=payload)
    assert res1.status_code == 201
    
    data1 = res1.json()
    assert "credentials_ref" in data1
    assert data1["credentials_ref"] == "vault-id-12345"
    assert "raw_secret" not in data1
    
    res2 = client.post("/api/v1/integrations", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]

    int_id = data1["id"]
    res_del = client.delete(f"/api/v1/integrations/{int_id}")
    assert res_del.status_code == 204
    
    res_get = client.get(f"/api/v1/integrations/{int_id}")
    assert res_get.status_code == 404

def test_update_status():
    import uuid
    client_res = client.post("/api/v1/clients", json={"name": f"Status Client {uuid.uuid4()}"})
    c_id = client_res.json()["id"]

    payload = {
        "client_id": c_id,
        "name": "Autodesk Sync",
        "provider": "autodesk"
    }
    res = client.post("/api/v1/integrations", json=payload)
    int_id = res.json()["id"]

    patch_res = client.patch(f"/api/v1/integrations/{int_id}/status?new_status=error")
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "error"
