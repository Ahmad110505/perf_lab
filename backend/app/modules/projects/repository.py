from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from typing import List, Tuple, Optional
from app.shared.repository import BaseRepository
from app.modules.projects.models import Project, ProjectStatus

class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)

    def get_by_name_and_client(self, db: Session, name: str, client_id: int) -> Project | None:
        stmt = select(Project).where(
            and_(Project.name == name, Project.client_id == client_id, Project.deleted_at == None)
        )
        return db.execute(stmt).scalar_first()

    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[Project], int]:
        return self.get_multi_with_count(db, client_id=client_id, skip=skip, limit=limit)

    def get_multi_with_count(self, db: Session, client_id: Optional[int] = None, status: Optional[ProjectStatus] = None, skip: int = 0, limit: int = 100) -> Tuple[List[Project], int]:
        base_stmt = select(Project).where(Project.deleted_at == None)
        
        if client_id is not None:
            base_stmt = base_stmt.where(Project.client_id == client_id)
        if status is not None:
            base_stmt = base_stmt.where(Project.status == status)
            
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()
        
        stmt = base_stmt.offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())
        
        return items, total

project_repository = ProjectRepository()
