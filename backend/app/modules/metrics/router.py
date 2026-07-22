from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.metrics.schemas import NormalizedMetricListResponse
from app.modules.metrics.repository import get_normalized_metrics
from datetime import date
from typing import Optional

router = APIRouter(prefix="/projects", tags=["metrics"])

@router.get("/{project_id}/metrics", response_model=NormalizedMetricListResponse)
def read_project_metrics(
    project_id: int,
    metric_type: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retrieve normalized metrics for a project."""
    metrics = get_normalized_metrics(
        db=db, 
        project_id=project_id, 
        metric_type=metric_type, 
        start_date=start_date, 
        end_date=end_date
    )
    return {"items": metrics, "total": len(metrics)}
