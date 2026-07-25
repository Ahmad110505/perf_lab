from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from app.modules.dashboard.models import DashboardSummary
from typing import List
from datetime import date

def upsert_summary(db: Session, project_id: int, summaries: List[dict]):
    if not summaries:
        return
        
    stmt = insert(DashboardSummary).values([
        {
            "project_id": project_id,
            "kpi_type": s["kpi_type"],
            "period_start": s["period_start"],
            "period_end": s["period_end"],
            "aggregated_value": s["aggregated_value"],
            "last_calculated_at": s["last_calculated_at"]
        }
        for s in summaries
    ])
    
    stmt = stmt.on_duplicate_key_update(
        aggregated_value=stmt.inserted.aggregated_value,
        last_calculated_at=stmt.inserted.last_calculated_at
    )
    
    db.execute(stmt)

def get_project_dashboard(db: Session, project_id: int, start_date: date | None = None, end_date: date | None = None) -> List[DashboardSummary]:
    query = db.query(DashboardSummary).filter(DashboardSummary.project_id == project_id)
    if start_date:
        query = query.filter(DashboardSummary.period_end >= start_date)
    if end_date:
        query = query.filter(DashboardSummary.period_start <= end_date)
    return query.all()
