import pytest
import os
import uuid
from datetime import date
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.dependencies import get_current_user_id
from app.core.database import SessionLocal
from app.modules.auth.models import User
from app.modules.projects.models import Project
from app.modules.metrics.models import NormalizedMetric, RawMetric
from app.modules.integrations.models import Integration, IntegrationProvider
from app.modules.connectors.models import ConnectorRun, RunStatus

client = TestClient(app)

@pytest.fixture
def test_user():
    db = SessionLocal()
    user = User(email=f"report_user_{uuid.uuid4()}@test.com", password_hash="dummyhash123")
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()
    return user_id

@pytest.fixture(autouse=True)
def override_auth(test_user):
    app.dependency_overrides[get_current_user_id] = lambda: test_user
    yield
    app.dependency_overrides.clear()

def create_project():
    c_res = client.post("/api/v1/clients", json={"name": f"Test Client {uuid.uuid4()}"})
    c_id = c_res.json()["id"]

    p_res = client.post("/api/v1/projects", json={
        "client_id": c_id,
        "name": f"Test Project {uuid.uuid4()}"
    })
    return p_res.json()["id"]

def test_reports_pipeline():
    p_id = create_project()
    db = SessionLocal()

    try:
        c_id = db.query(Project).filter_by(id=p_id).first().client_id

        integ = Integration(client_id=c_id, provider=IntegrationProvider.GOOGLE_ANALYTICS, name="GA Reports Test")
        db.add(integ)
        db.commit()

        run = ConnectorRun(integration_id=integ.id, status=RunStatus.SUCCESS)
        db.add(run)
        db.commit()

        raw = RawMetric(connector_run_id=run.id, integration_id=integ.id, project_id=p_id, raw_payload={})
        db.add(raw)
        db.commit()

        norm = NormalizedMetric(
            project_id=p_id,
            metric_type="pageviews",
            metric_date=date(2026, 7, 20),
            value=500.0,
            source_provider="google_analytics",
            raw_metric_id=raw.id
        )
        db.add(norm)
        db.commit()

        # 1. Create Report via POST endpoint
        post_res = client.post(f"/api/v1/projects/{p_id}/reports", json={
            "name": "July Performance Report",
            "format": "csv",
            "period_start": "2026-07-01",
            "period_end": "2026-07-31"
        })
        assert post_res.status_code == 201
        report_data = post_res.json()
        r_id = report_data["id"]
        assert report_data["status"] == "completed"
        assert report_data["file_path"] is not None

        # 2. List Reports for Project
        list_res = client.get(f"/api/v1/projects/{p_id}/reports")
        assert list_res.status_code == 200
        assert list_res.json()["total"] == 1

        # 3. Download Report CSV
        dl_res = client.get(f"/api/v1/projects/{p_id}/reports/{r_id}/download")
        assert dl_res.status_code == 200
        assert "text/csv" in dl_res.headers["content-type"]
        csv_content = dl_res.text
        assert "Metric Date,Metric Type,Value,Source Provider" in csv_content
        assert "pageviews" in csv_content
        assert "500.0" in csv_content

    finally:
        db.close()
