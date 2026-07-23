from fastapi import APIRouter, Depends, status, Query
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

@router.post("/integrations/{integration_id}/action")
def execute_integration_action(
    integration_id: int,
    action: str = Query("query_keywords"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Execute a provider-specific action for an integration."""
    return connector_service.execute_provider_action(db, integration_id=integration_id, action=action)

@router.get("/connector-runs/failed", response_model=ConnectorRunListResponse)
def list_failed_runs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """List all failed connector runs."""
    return connector_service.get_failed_runs(db=db, skip=skip, limit=limit)

@router.post("/connector-runs/{run_id}/retry", response_model=ConnectorRunResponse)
def retry_failed_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retry a failed connector run."""
    return connector_service.retry_run(db=db, run_id=run_id)

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
