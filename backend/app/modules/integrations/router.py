from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.integrations.schemas import IntegrationCreate, IntegrationUpdate, IntegrationResponse, IntegrationListResponse
from app.modules.integrations.services import integration_service
from app.modules.integrations.models import IntegrationProvider, IntegrationStatus

router = APIRouter()

@router.get("", response_model=IntegrationListResponse)
def read_integrations(
    client_id: Optional[int] = None,
    provider: Optional[IntegrationProvider] = None,
    integration_status: Optional[IntegrationStatus] = Query(None, alias="status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retrieve all integrations."""
    return integration_service.get_integrations(db, client_id=client_id, provider=provider, status=integration_status, skip=skip, limit=limit)

@router.get("/{integration_id}", response_model=IntegrationResponse)
def read_integration(integration_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Retrieve a specific integration by ID."""
    return integration_service.get_integration(db, integration_id=integration_id)

@router.post("", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
def create_integration(integration_in: IntegrationCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Create a new integration."""
    return integration_service.create_integration(db, integration_in=integration_in)

@router.put("/{integration_id}", response_model=IntegrationResponse)
def update_integration(integration_id: int, integration_in: IntegrationUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Update an integration."""
    return integration_service.update_integration(db, integration_id=integration_id, integration_in=integration_in)

@router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_integration(integration_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Soft delete an integration."""
    integration_service.delete_integration(db, integration_id=integration_id)

@router.patch("/{integration_id}/status", response_model=IntegrationResponse)
def update_integration_status(
    integration_id: int, 
    new_status: IntegrationStatus = Query(...),
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """Update the status of an integration."""
    return integration_service.update_status(db, integration_id=integration_id, new_status=new_status)
