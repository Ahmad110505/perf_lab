from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
import traceback

from app.modules.connectors.repository import connector_run_repository
from app.modules.connectors.models import ConnectorRun, RunStatus
from app.modules.integrations.repository import integration_repository
from app.modules.integrations.models import IntegrationStatus
from app.modules.connectors.registry import get_connector_for_provider

from app.worker.tasks import run_sync_job

class ConnectorService:
    def trigger_sync(self, db: Session, integration_id: int) -> ConnectorRun:
        integration = integration_repository.get(db, id=integration_id)
        if not integration or integration.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
            
        if integration.status != IntegrationStatus.CONNECTED and integration.status != IntegrationStatus.PENDING and integration.status != IntegrationStatus.ERROR:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integration is not in a connectable state")
            
        run = connector_run_repository.create(db, obj_in={"integration_id": integration_id, "status": RunStatus.QUEUED})
        
        # Enqueue the background task via Celery
        run_sync_job.delay(run.id)
        
        db.refresh(run)
        return run

    def get_runs_by_integration(self, db: Session, integration_id: int, skip: int = 0, limit: int = 100) -> dict:
        items, total = connector_run_repository.get_by_integration_id(db, integration_id=integration_id, skip=skip, limit=limit)
        return {"items": items, "total": total, "skip": skip, "limit": limit}
        
    def get_run(self, db: Session, run_id: int) -> ConnectorRun:
        run = connector_run_repository.get(db, id=run_id)
        if not run or run.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Connector run not found")
        return run

    def get_failed_runs(self, db: Session, skip: int = 0, limit: int = 100) -> dict:
        items = db.query(ConnectorRun).filter(ConnectorRun.status == RunStatus.FAILED, ConnectorRun.deleted_at.is_(None)).offset(skip).limit(limit).all()
        total = db.query(ConnectorRun).filter(ConnectorRun.status == RunStatus.FAILED, ConnectorRun.deleted_at.is_(None)).count()
        return {"items": items, "total": total, "skip": skip, "limit": limit}

    def retry_run(self, db: Session, run_id: int) -> ConnectorRun:
        run = self.get_run(db, run_id)
        if run.status != RunStatus.FAILED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only failed runs can be retried")
            
        return self.trigger_sync(db, run.integration_id)

connector_service = ConnectorService()
