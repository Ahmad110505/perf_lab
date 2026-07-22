import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user_id
import uuid
from app.core.database import SessionLocal
from app.modules.metrics.models import RawMetric, NormalizedMetric
from datetime import date

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth_and_celery():
    app.dependency_overrides[get_current_user_id] = lambda: 1
    
    from app.worker.celery_app import celery_app
    celery_app.conf.update(task_always_eager=True)
    
    yield
    app.dependency_overrides.clear()
    celery_app.conf.update(task_always_eager=False)

def create_integration(provider="google_analytics"):
    client_res = client.post("/api/v1/clients", json={"name": f"Test Client {uuid.uuid4()}"})
    c_id = client_res.json()["id"]

    proj_res = client.post("/api/v1/projects", json={
        "client_id": c_id,
        "name": f"Test Project {uuid.uuid4()}"
    })
    p_id = proj_res.json()["id"]

    int_res = client.post("/api/v1/integrations", json={
        "client_id": c_id,
        "name": f"Test Sync {uuid.uuid4()}",
        "provider": provider,
        "config": {"project_id": p_id}
    })
    int_id = int_res.json()["id"]
    client.patch(f"/api/v1/integrations/{int_id}/status?new_status=connected")
    return int_id, p_id

def test_metrics_pipeline():
    int_id, p_id = create_integration("google_analytics")
    
    # Run sync job
    res = client.post(f"/api/v1/integrations/{int_id}/sync")
    assert res.status_code == 200
    
    # Verify records created
    db = SessionLocal()
    try:
        raw_metrics = db.query(RawMetric).filter(RawMetric.project_id == p_id).all()
        assert len(raw_metrics) == 2
        
        normalized = db.query(NormalizedMetric).filter(NormalizedMetric.project_id == p_id).all()
        assert len(normalized) == 4
        
        # Check upsert logic
        res2 = client.post(f"/api/v1/integrations/{int_id}/sync")
        run_res2 = client.get(f"/api/v1/integrations/{int_id}/runs")
        run_data = run_res2.json()["items"][0]
        assert run_data["status"] == "success", f"Run failed: {run_data.get('error_message')}"
        
        db.commit()
        # Raw metrics should double, normalized should stay the same due to upsert
        raw_metrics_after = db.query(RawMetric).filter(RawMetric.project_id == p_id).all()
        assert len(raw_metrics_after) == 4
        
        normalized_after = db.query(NormalizedMetric).filter(NormalizedMetric.project_id == p_id).all()
        assert len(normalized_after) == 4
        
        # Test Rebuild
        db.query(NormalizedMetric).filter(NormalizedMetric.project_id == p_id).delete()
        db.commit()
        
        from app.modules.metrics.services import metrics_service
        metrics_service.rebuild_normalized_metrics(db, project_id=p_id)
        
        normalized_rebuilt = db.query(NormalizedMetric).filter(NormalizedMetric.project_id == p_id).all()
        assert len(normalized_rebuilt) == 4
        
        # Test API
        api_res = client.get(f"/api/v1/projects/{p_id}/metrics")
        assert api_res.status_code == 200
        assert api_res.json()["total"] == 4
        
    finally:
        db.close()
