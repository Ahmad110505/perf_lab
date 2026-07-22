from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user_id
from app.modules.clients.schemas import ClientCreate, ClientUpdate, ClientResponse, ClientListResponse
from app.modules.clients.services import client_service
from app.modules.projects.schemas import ProjectListResponse
from app.modules.projects.services import project_service
from app.modules.projects.models import ProjectStatus
from app.modules.locations.schemas import LocationListResponse
from app.modules.locations.services import location_service

router = APIRouter()

@router.get("", response_model=ClientListResponse)
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all active clients."""
    return client_service.get_clients(db, skip=skip, limit=limit)

@router.get("/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific client by ID."""
    return client_service.get_client(db, client_id=client_id)

@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Create a new client."""
    return client_service.create_client(db, client_in=client_in, user_id=current_user_id)

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_in: ClientUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Update a client."""
    return client_service.update_client(db, client_id=client_id, client_in=client_in, user_id=current_user_id)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Soft delete a client."""
    client_service.delete_client(db, client_id=client_id, user_id=current_user_id)

@router.get("/{client_id}/projects", response_model=ProjectListResponse)
def read_client_projects(
    client_id: int,
    project_status: Optional[ProjectStatus] = Query(None, alias="status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all projects for a specific client."""
    return project_service.get_projects(db, client_id=client_id, project_status=project_status, skip=skip, limit=limit)

@router.get("/{client_id}/locations", response_model=LocationListResponse)
def read_client_locations(
    client_id: int,
    city: Optional[str] = None,
    country: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all locations for a specific client."""
    return location_service.get_locations(db, client_id=client_id, city=city, country=country, skip=skip, limit=limit)
