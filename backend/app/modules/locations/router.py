from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.locations.schemas import LocationCreate, LocationUpdate, LocationResponse, LocationListResponse
from app.modules.locations.services import location_service

router = APIRouter()

@router.get("", response_model=LocationListResponse)
def read_locations(
    client_id: Optional[int] = None, 
    project_id: Optional[int] = None, 
    city: Optional[str] = None, 
    country: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Retrieve locations, optionally filtered."""
    return location_service.get_locations(db, client_id=client_id, project_id=project_id, city=city, country=country, skip=skip, limit=limit)

@router.get("/{location_id}", response_model=LocationResponse)
def read_location(location_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific location by ID."""
    return location_service.get_location(db, location_id=location_id)

@router.post("", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location_in: LocationCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Create a new location."""
    return location_service.create_location(db, location_in=location_in, user_id=current_user_id)

@router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, location_in: LocationUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Update a location."""
    return location_service.update_location(db, location_id=location_id, location_in=location_in, user_id=current_user_id)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """Soft delete a location."""
    location_service.delete_location(db, location_id=location_id, user_id=current_user_id)
