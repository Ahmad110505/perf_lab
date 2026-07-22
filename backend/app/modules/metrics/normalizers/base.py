from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import date
from pydantic import BaseModel

class NormalizedMetricInput(BaseModel):
    project_id: int
    location_id: int | None = None
    metric_type: str
    metric_date: date
    value: float
    unit: str | None = None
    source_provider: str
    
class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        pass
