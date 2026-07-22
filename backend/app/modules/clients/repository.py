from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Tuple
from app.shared.repository import BaseRepository
from app.modules.clients.models import Client

class ClientRepository(BaseRepository[Client]):
    def __init__(self):
        super().__init__(Client)

    def get_by_name(self, db: Session, name: str) -> Client | None:
        stmt = select(Client).where(Client.name == name, Client.deleted_at == None)
        return db.execute(stmt).scalars().first()
        
    def get_multi_with_count(self, db: Session, skip: int = 0, limit: int = 100) -> Tuple[List[Client], int]:
        base_stmt = select(Client).where(Client.deleted_at == None)
        
        # Count
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()
        
        # Items
        stmt = base_stmt.offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())
        
        return items, total

client_repository = ClientRepository()
