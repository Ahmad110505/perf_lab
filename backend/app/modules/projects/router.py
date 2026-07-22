from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user_id
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from app.modules.projects.services import project_service
from app.modules.projects.models import ProjectStatus
from app.modules.locations.schemas import LocationListResponse
from app.modules.locations.services import location_service

router = APIRouter()

@router.get("", response_model=ProjectListResponse)
def read_projects(
    client_id: Optional[int] = None, 
    project_status: Optional[ProjectStatus] = Query(None, alias="status"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Retrieve projects, optionally filtered by client_id and status."""
    return project_service.get_projects(db, client_id=client_id, project_status=project_status, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific project by ID."""
    return project_service.get_project(db, project_id=project_id)

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Create a new project."""
    return project_service.create_project(db, project_in=project_in, user_id=current_user_id)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_in: ProjectUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Update a project."""
    return project_service.update_project(db, project_id=project_id, project_in=project_in, user_id=current_user_id)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Soft delete a project."""
    project_service.delete_project(db, project_id=project_id, user_id=current_user_id)

@router.get("/{project_id}/locations", response_model=LocationListResponse)
def read_project_locations(
    project_id: int,
    city: Optional[str] = None,
    country: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all locations for a specific project."""
    return location_service.get_locations(db, project_id=project_id, city=city, country=country, skip=skip, limit=limit)
