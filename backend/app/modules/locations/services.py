from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.shared.service import BaseService
from app.modules.locations.repository import LocationRepository, location_repository
from app.modules.locations.schemas import LocationCreate, LocationUpdate, LocationResponse, LocationListResponse
from app.modules.locations.models import Location
from app.modules.clients.repository import client_repository
from app.modules.projects.repository import project_repository

class LocationService(BaseService[LocationRepository]):
    def __init__(self):
        super().__init__(location_repository)

    def get_location(self, db: Session, location_id: int) -> Location:
        location = self.repository.get(db, location_id)
        if not location:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        return location

    def get_locations(self, db: Session, client_id: Optional[int] = None, project_id: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, skip: int = 0, limit: int = 100) -> LocationListResponse:
        if client_id is not None:
            if not client_repository.get(db, client_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        
        if project_id is not None:
            if not project_repository.get(db, project_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        items, total = self.repository.get_multi_with_count(db, client_id=client_id, project_id=project_id, city=city, country=country, skip=skip, limit=limit)
        return LocationListResponse(
            items=[LocationResponse.model_validate(item) for item in items],
            total=total
        )

    def create_location(self, db: Session, location_in: LocationCreate, user_id: int) -> Location:
        if not client_repository.get(db, location_in.client_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        if location_in.project_id:
            project = project_repository.get(db, location_in.project_id)
            if not project:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            if project.client_id != location_in.client_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project does not belong to the specified client")
        
        obj_in = location_in.model_dump()
        obj_in["created_by"] = user_id
        
        location = self.repository.create(db, obj_in=obj_in)
        return location

    def update_location(self, db: Session, location_id: int, location_in: LocationUpdate, user_id: int) -> Location:
        location = self.get_location(db, location_id)
        
        update_data = location_in.model_dump(exclude_unset=True)
        
        if "project_id" in update_data and update_data["project_id"] is not None:
            project = project_repository.get(db, update_data["project_id"])
            if not project:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            if project.client_id != location.client_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project does not belong to the location's client")

        for field, value in update_data.items():
            setattr(location, field, value)
            
        location.updated_by = user_id
        db.commit()
        db.refresh(location)
        return location

    def delete_location(self, db: Session, location_id: int, user_id: int) -> None:
        location = self.get_location(db, location_id)
        location.updated_by = user_id
        db.commit()
        self.repository.soft_delete(db, id=location_id)

location_service = LocationService()
