from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from app.modules.reports.models import ReportFormat, ReportStatus

class ReportCreate(BaseModel):
    name: str
    format: Optional[ReportFormat] = ReportFormat.CSV
    period_start: Optional[date] = None
    period_end: Optional[date] = None

class ReportResponse(BaseModel):
    id: int
    project_id: int
    created_by_user_id: int
    name: str
    format: ReportFormat
    status: ReportStatus
    period_start: Optional[date]
    period_end: Optional[date]
    file_path: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReportListResponse(BaseModel):
    items: List[ReportResponse]
    total: int
