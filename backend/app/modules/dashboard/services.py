from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.dashboard import repository as dashboard_repo
from app.modules.metrics.models import NormalizedMetric
from datetime import datetime, timezone

class DashboardBuilderService:
    def build_summary_for_project(self, db: Session, project_id: int):
        query = db.query(
            NormalizedMetric.metric_type,
            func.sum(NormalizedMetric.value).label("total_value"),
            func.min(NormalizedMetric.metric_date).label("start_date"),
            func.max(NormalizedMetric.metric_date).label("end_date")
        ).filter(
            NormalizedMetric.project_id == project_id
        ).group_by(
            NormalizedMetric.metric_type
        )
        
        results = query.all()
        
        summaries = []
        now = datetime.now(timezone.utc)
        
        for row in results:
            if not row.start_date or not row.end_date:
                continue
                
            summaries.append({
                "kpi_type": f"total_{row.metric_type}",
                "period_start": row.start_date,
                "period_end": row.end_date,
                "aggregated_value": {"value": float(row.total_value)},
                "last_calculated_at": now
            })
            
        dashboard_repo.upsert_summary(db, project_id, summaries)
        db.commit()

dashboard_builder = DashboardBuilderService()
