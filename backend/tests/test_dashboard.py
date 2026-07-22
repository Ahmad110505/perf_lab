import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user_id
import uuid
from app.core.database import SessionLocal
from app.modules.metrics.models import NormalizedMetric, RawMetric
from app.modules.integrations.models import Integration, IntegrationProvider
from app.modules.projects.models import Project
from app.modules.dashboard.models import DashboardSummary
from app.modules.dashboard.services import dashboard_builder
from datetime import date, datetime, timedelta, timezone

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth_and_celery():
    app.dependency_overrides[get_current_user_id] = lambda: 1
    
    from app.worker.celery_app import celery_app
    celery_app.conf.update(task_always_eager=True)
    
    yield
    app.dependency_overrides.clear()
    celery_app.conf.update(task_always_eager=False)

def create_project():
    client_res = client.post("/api/v1/clients", json={"name": f"Test Client {uuid.uuid4()}"})
    c_id = client_res.json()["id"]

    proj_res = client.post("/api/v1/projects", json={
        "client_id": c_id,
        "name": f"Test Project {uuid.uuid4()}"
    })
    return proj_res.json()["id"]

def test_dashboard_builder_and_endpoint():
    p_id = create_project()
    db = SessionLocal()
    
    try:
        client_id = db.query(Project).filter_by(id=p_id).first().client_id
        
        # Bypass constraint for test simplicity on connector_run_id by adding a dummy run
        # Wait, connector_run_id is FK. I must create a run or disable FK checks temporarily.
        # It's cleaner to create a fake run.
        from app.modules.connectors.models import ConnectorRun, RunStatus
        
        integ = Integration(client_id=client_id, provider=IntegrationProvider.GOOGLE_ANALYTICS, name="GA")
        db.add(integ)
        db.commit()
        
        run = ConnectorRun(integration_id=integ.id, status=RunStatus.SUCCESS)
        db.add(run)
        db.commit()
        
        raw = RawMetric(connector_run_id=run.id, integration_id=integ.id, project_id=p_id, raw_payload={})
        db.add(raw)
        db.commit()
        
        db.add_all([
            NormalizedMetric(
                project_id=p_id,
                metric_type="sessions",
                metric_date=date(2023, 1, 1),
                value=100.0,
                source_provider="google_analytics",
                raw_metric_id=raw.id
            ),
            NormalizedMetric(
                project_id=p_id,
                metric_type="sessions",
                metric_date=date(2023, 1, 2),
                value=150.0,
                source_provider="google_analytics",
                raw_metric_id=raw.id
            )
        ])
        db.commit()
        
        # 2. Run builder
        dashboard_builder.build_summary_for_project(db, p_id)
        
        # Verify db
        summaries = db.query(DashboardSummary).filter_by(project_id=p_id).all()
        assert len(summaries) == 1
        assert summaries[0].kpi_type == "total_sessions"
        assert summaries[0].aggregated_value["value"] == 250.0
        
        # 3. Test Idempotency
        dashboard_builder.build_summary_for_project(db, p_id)
        summaries_after = db.query(DashboardSummary).filter_by(project_id=p_id).all()
        assert len(summaries_after) == 1
        
        # 4. Test API endpoint
        res = client.get(f"/api/v1/projects/{p_id}/dashboard")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 1
        assert data["is_stale"] is False
        assert data["items"][0]["aggregated_value"]["value"] == 250.0
        
        # 5. Test Stale Data Flag
        old_time = datetime.now(timezone.utc) - timedelta(hours=48)
        db.query(DashboardSummary).filter_by(project_id=p_id).update({"last_calculated_at": old_time})
        db.commit()
        
        res_stale = client.get(f"/api/v1/projects/{p_id}/dashboard")
        assert res_stale.status_code == 200
        assert res_stale.json()["is_stale"] is True
        
    finally:
        db.close()
