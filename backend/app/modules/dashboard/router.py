from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user_id
from app.modules.dashboard.schemas import DashboardResponse
from app.modules.dashboard.repository import get_project_dashboard
from datetime import date, datetime, timedelta, timezone
from typing import Optional

router = APIRouter(prefix="/projects", tags=["dashboard"])

@router.get("/{project_id}/dashboard", response_model=DashboardResponse)
def read_project_dashboard(
    project_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retrieve dashboard summary for a project."""
    summaries = get_project_dashboard(
        db=db, 
        project_id=project_id, 
        start_date=start_date, 
        end_date=end_date
    )
    
    is_stale = False
    # If no data exists, it's technically stale (or just empty)
    if not summaries:
        is_stale = True
    else:
        now = datetime.now(timezone.utc)
        threshold = timedelta(hours=24)
        
        for s in summaries:
            # We assume last_calculated_at is timezone aware
            if not s.last_calculated_at or (now - s.last_calculated_at.astimezone(timezone.utc)) > threshold:
                is_stale = True
                break
            
    return {"items": summaries, "is_stale": is_stale, "total": len(summaries)}
