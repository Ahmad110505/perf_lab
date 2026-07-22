from app.worker.celery_app import celery_app
from app.core.database import SessionLocal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
import traceback

from app.modules.connectors.repository import connector_run_repository
from app.modules.integrations.repository import integration_repository
from app.modules.connectors.models import RunStatus
from app.modules.integrations.models import IntegrationStatus
from app.modules.connectors.registry import get_connector_for_provider
from app.modules.connectors.exceptions import TransientSyncError, TerminalSyncError

@celery_app.task(bind=True, max_retries=5)
def run_sync_job(self, run_id: int):
    db: Session = SessionLocal()
    try:
        run = connector_run_repository.get(db, id=run_id)
        if not run:
            return
            
        integration = integration_repository.get(db, id=run.integration_id)
        if not integration:
            return

        run.status = RunStatus.RUNNING
        if not run.started_at:
            run.started_at = datetime.now(timezone.utc)
        
        run.retry_count = self.request.retries
        db.commit()

        try:
            ConnectorClass = get_connector_for_provider(integration.provider)
            connector = ConnectorClass(config=integration.config or {}, credentials_ref=integration.credentials_ref)
            
            connector.authenticate()
            raw_data = connector.fetch_data()
            
            processed = 0
            # Process Metrics via Sync Pipeline
            from app.modules.metrics.services import metrics_service
            metrics_service.ingest_and_normalize(
                db=db,
                run_id=run.id,
                integration_id=integration.id,
                provider=integration.provider,
                raw_data=raw_data
            )
            processed = len(raw_data)

            run.status = RunStatus.SUCCESS
            run.records_processed = processed
            run.finished_at = datetime.now(timezone.utc)
            
            integration.status = IntegrationStatus.CONNECTED
            integration.last_synced_at = datetime.now(timezone.utc)
            db.commit()
            
        except TransientSyncError as e:
            db.rollback()
            run = connector_run_repository.get(db, id=run_id)
            if self.request.retries >= self.max_retries:
                run.status = RunStatus.FAILED
                run.error_message = f"Max retries exhausted. Last error: {str(e)}"
                run.finished_at = datetime.now(timezone.utc)
                
                integration = integration_repository.get(db, id=run.integration_id)
                integration.status = IntegrationStatus.ERROR
                db.commit()
                return
            else:
                db.commit()
                raise self.retry(exc=e, countdown=2 ** self.request.retries)
                
        except TerminalSyncError as e:
            db.rollback()
            run = connector_run_repository.get(db, id=run_id)
            integration = integration_repository.get(db, id=run.integration_id)
            
            run.status = RunStatus.FAILED
            run.error_message = f"Terminal error: {str(e)}"
            run.finished_at = datetime.now(timezone.utc)
            integration.status = IntegrationStatus.ERROR
            db.commit()
            return

        except Exception as e:
            db.rollback()
            run = connector_run_repository.get(db, id=run_id)
            integration = integration_repository.get(db, id=run.integration_id)
            
            run.status = RunStatus.FAILED
            run.error_message = f"Unhandled error: {str(e)}"
            run.finished_at = datetime.now(timezone.utc)
            integration.status = IntegrationStatus.ERROR
            db.commit()
            return
            
    finally:
        db.close()

@celery_app.task
def calculate_dashboard_summaries():
    db: Session = SessionLocal()
    try:
        from app.modules.projects.repository import project_repository
        from app.modules.projects.models import ProjectStatus
        from app.modules.dashboard.services import dashboard_builder
        
        projects, total = project_repository.get_multi_with_count(db, status=ProjectStatus.active, limit=1000)
        for p in projects:
            dashboard_builder.build_summary_for_project(db, p.id)
    finally:
        db.close()
