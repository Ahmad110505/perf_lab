from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from app.shared.repository import BaseRepository
from app.modules.integrations.models import Integration, IntegrationProvider, IntegrationStatus

class IntegrationRepository(BaseRepository[Integration]):
    def __init__(self):
        super().__init__(Integration)

    def get_by_client_id(self, db: Session, client_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[Integration], int]:
        return self.get_multi_with_count(db, client_id=client_id, skip=skip, limit=limit)

    def get_by_provider(self, db: Session, client_id: int, provider: IntegrationProvider) -> Optional[Integration]:
        stmt = select(Integration).where(
            and_(Integration.client_id == client_id, Integration.provider == provider, Integration.deleted_at == None)
        )
        return db.execute(stmt).scalars().first()

    def get_multi_with_count(self, db: Session, client_id: Optional[int] = None, provider: Optional[IntegrationProvider] = None, status: Optional[IntegrationStatus] = None, skip: int = 0, limit: int = 100) -> Tuple[List[Integration], int]:
        base_stmt = select(Integration).where(Integration.deleted_at == None)
        if client_id is not None:
            base_stmt = base_stmt.where(Integration.client_id == client_id)
        if provider is not None:
            base_stmt = base_stmt.where(Integration.provider == provider)
        if status is not None:
            base_stmt = base_stmt.where(Integration.status == status)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()

        stmt = base_stmt.offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())

        return items, total

integration_repository = IntegrationRepository()
