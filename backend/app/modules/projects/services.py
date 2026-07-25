from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.shared.service import BaseService
from app.modules.projects.repository import ProjectRepository, project_repository
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from app.modules.projects.models import Project, ProjectStatus
from app.modules.clients.repository import client_repository

class ProjectService(BaseService[ProjectRepository]):
    def __init__(self):
        super().__init__(project_repository)

    def get_project(self, db: Session, project_id: int) -> Project:
        project = self.repository.get(db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project

    def get_projects(self, db: Session, client_id: Optional[int] = None, project_status: Optional[ProjectStatus] = None, skip: int = 0, limit: int = 100) -> ProjectListResponse:
        if client_id is not None:
            client = client_repository.get(db, client_id)
            if not client:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        items, total = self.repository.get_multi_with_count(db, client_id=client_id, status=project_status, skip=skip, limit=limit)
        return ProjectListResponse(
            items=[ProjectResponse.model_validate(item) for item in items],
            total=total
        )

    def create_project(self, db: Session, project_in: ProjectCreate, user_id: int) -> Project:
        client = client_repository.get(db, project_in.client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        existing = self.repository.get_by_name_and_client(db, project_in.name, project_in.client_id)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with this name already exists for this client")
        
        obj_in = project_in.model_dump()
        obj_in["created_by"] = user_id
        
        project = self.repository.create(db, obj_in=obj_in)
        return project

    def update_project(self, db: Session, project_id: int, project_in: ProjectUpdate, user_id: int) -> Project:
        project = self.get_project(db, project_id)
        
        update_data = project_in.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = self.repository.get_by_name_and_client(db, update_data["name"], project.client_id)
            if existing and existing.id != project_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project with this name already exists for this client")
                
        new_start = update_data.get("start_date", project.start_date)
        new_end = update_data.get("end_date", project.end_date)
        if new_start and new_end and new_end < new_start:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end_date cannot be before start_date")

        for field, value in update_data.items():
            setattr(project, field, value)
            
        project.updated_by = user_id
        db.commit()
        db.refresh(project)
        return project

    def delete_project(self, db: Session, project_id: int, user_id: int) -> None:
        project = self.get_project(db, project_id)
        project.updated_by = user_id
        db.commit()
        self.repository.soft_delete(db, id=project_id)

project_service = ProjectService()
