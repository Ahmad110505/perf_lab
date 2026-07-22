from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Dict, Any, List

class DashboardSummaryResponse(BaseModel):
    id: int
    project_id: int
    kpi_type: str
    period_start: date
    period_end: date
    aggregated_value: Dict[str, Any]
    last_calculated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DashboardResponse(BaseModel):
    items: List[DashboardSummaryResponse]
    is_stale: bool
    total: int
