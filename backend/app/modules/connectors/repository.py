from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.shared.repository import BaseRepository
from app.modules.connectors.models import ConnectorRun

class ConnectorRunRepository(BaseRepository[ConnectorRun]):
    def __init__(self):
        super().__init__(ConnectorRun)

    def get_by_integration_id(self, db: Session, integration_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[ConnectorRun], int]:
        base_stmt = select(ConnectorRun).where(ConnectorRun.integration_id == integration_id, ConnectorRun.deleted_at == None)
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()

        stmt = base_stmt.order_by(ConnectorRun.created_at.desc()).offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())
        return items, total
        
    def get_latest_run_for_integration(self, db: Session, integration_id: int) -> Optional[ConnectorRun]:
        stmt = select(ConnectorRun).where(ConnectorRun.integration_id == integration_id, ConnectorRun.deleted_at == None).order_by(ConnectorRun.created_at.desc())
        return db.execute(stmt).scalars().first()

connector_run_repository = ConnectorRunRepository()
