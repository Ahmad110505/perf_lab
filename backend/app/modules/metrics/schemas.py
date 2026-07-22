from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List

class NormalizedMetricResponse(BaseModel):
    id: int
    project_id: int
    location_id: Optional[int] = None
    metric_type: str
    metric_date: date
    value: float
    unit: Optional[str] = None
    source_provider: str
    raw_metric_id: int
    
    model_config = ConfigDict(from_attributes=True)

class NormalizedMetricListResponse(BaseModel):
    items: List[NormalizedMetricResponse]
    total: int
