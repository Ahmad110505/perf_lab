import os
os.environ["MYSQL_PORT"] = "3307"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer demo-bypass-token"}

res_metrics_1 = client.get("/api/v1/projects/1/metrics", headers=headers)
print("Project 1 Metrics response:", res_metrics_1.status_code, res_metrics_1.json())

res_dash_1 = client.get("/api/v1/projects/1/dashboard", headers=headers)
print("Project 1 Dashboard response:", res_dash_1.status_code, res_dash_1.json())

# Trigger sync for Integration #329
res_sync = client.post("/api/v1/integrations/329/sync", headers=headers)
print("Sync Integration 329 response:", res_sync.status_code, res_sync.json())

res_metrics_1_after = client.get("/api/v1/projects/1/metrics", headers=headers)
print("Project 1 Metrics after sync:", res_metrics_1_after.status_code, len(res_metrics_1_after.json().get("items", [])))
