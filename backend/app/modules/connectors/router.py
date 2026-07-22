from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.connectors.schemas import ConnectorRunResponse, ConnectorRunListResponse, TriggerSyncRequest
from app.modules.connectors.services import connector_service

router = APIRouter()

@router.post("/integrations/{integration_id}/sync", response_model=ConnectorRunResponse)
def trigger_sync(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Trigger a sync for a specific integration."""
    return connector_service.trigger_sync(db, integration_id=integration_id)

@router.get("/integrations/{integration_id}/runs", response_model=ConnectorRunListResponse)
def read_integration_runs(
    integration_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retrieve run history for a specific integration."""
    return connector_service.get_runs_by_integration(db, integration_id=integration_id, skip=skip, limit=limit)

@router.get("/connector-runs/{run_id}", response_model=ConnectorRunResponse)
def read_connector_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retrieve status of a single run."""
    return connector_service.get_run(db, run_id=run_id)
