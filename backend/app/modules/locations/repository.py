from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Tuple, Optional
from app.shared.repository import BaseRepository
from app.modules.locations.models import Location

class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)

    def get_multi_with_count(self, db: Session, client_id: Optional[int] = None, project_id: Optional[int] = None, city: Optional[str] = None, country: Optional[str] = None, skip: int = 0, limit: int = 100) -> Tuple[List[Location], int]:
        base_stmt = select(Location).where(Location.deleted_at == None)
        
        if client_id is not None:
            base_stmt = base_stmt.where(Location.client_id == client_id)
        if project_id is not None:
            base_stmt = base_stmt.where(Location.project_id == project_id)
        if city is not None:
            base_stmt = base_stmt.where(Location.city == city)
        if country is not None:
            base_stmt = base_stmt.where(Location.country == country)
            
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()
        
        stmt = base_stmt.offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())
        
        return items, total

location_repository = LocationRepository()
