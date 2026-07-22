from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone
import traceback

from app.modules.connectors.repository import connector_run_repository
from app.modules.connectors.models import ConnectorRun, RunStatus
from app.modules.integrations.repository import integration_repository
from app.modules.integrations.models import IntegrationStatus
from app.modules.connectors.registry import get_connector_for_provider

def run_sync_job_stub(db: Session, run_id: int):
    """
    STUB JOB EXECUTION: This currently runs synchronously in the same request.
    # TODO: wire Celery/RQ so this runs asynchronously in a real background worker.
    """
    run = connector_run_repository.get(db, id=run_id)
    if not run:
        return
        
    integration = integration_repository.get(db, id=run.integration_id)
    if not integration:
        return

    run.status = RunStatus.RUNNING
    run.started_at = datetime.now(timezone.utc)
    db.commit()

    try:
        ConnectorClass = get_connector_for_provider(integration.provider)
        connector = ConnectorClass(config=integration.config or {}, credentials_ref=integration.credentials_ref)
        
        connector.authenticate()
        raw_data = connector.fetch_data()
        
        processed = 0
        for item in raw_data:
            normalized = connector.normalize(item)
            processed += 1
            
        run.status = RunStatus.SUCCESS
        run.records_processed = processed
        run.finished_at = datetime.now(timezone.utc)
        
        integration.status = IntegrationStatus.CONNECTED
        integration.last_synced_at = datetime.now(timezone.utc)
        db.commit()

    except Exception as e:
        db.rollback()
        run = connector_run_repository.get(db, id=run_id)
        integration = integration_repository.get(db, id=run.integration_id)
        
        run.status = RunStatus.FAILED
        run.error_message = str(e)
        run.finished_at = datetime.now(timezone.utc)
        integration.status = IntegrationStatus.ERROR
        db.commit()

class ConnectorService:
    def trigger_sync(self, db: Session, integration_id: int) -> ConnectorRun:
        integration = integration_repository.get(db, id=integration_id)
        if not integration or integration.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
            
        if integration.status != IntegrationStatus.CONNECTED and integration.status != IntegrationStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integration is not in a connectable state")
            
        run = connector_run_repository.create(db, obj_in={"integration_id": integration_id, "status": RunStatus.QUEUED})
        
        run_sync_job_stub(db, run.id)
        
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

connector_service = ConnectorService()
