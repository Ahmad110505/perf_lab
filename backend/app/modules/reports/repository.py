from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.shared.repository import BaseRepository
from app.modules.reports.models import Report
from typing import List, Tuple

class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    def get_by_project_id(self, db: Session, project_id: int, skip: int = 0, limit: int = 100) -> Tuple[List[Report], int]:
        base_stmt = select(Report).where(Report.project_id == project_id)
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = db.execute(count_stmt).scalar_one()

        stmt = base_stmt.offset(skip).limit(limit)
        items = list(db.execute(stmt).scalars().all())

        return items, total

report_repository = ReportRepository()
