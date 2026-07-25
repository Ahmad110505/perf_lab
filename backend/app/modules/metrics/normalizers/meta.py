from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class MetaNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = raw_payload.get("project_id")
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="ad_spend",
            metric_date=m_date,
            value=float(raw_payload.get("spend", 0.0)),
            unit="currency",
            source_provider=IntegrationProvider.META.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="roas",
            metric_date=m_date,
            value=float(raw_payload.get("roas", 0.0)),
            unit="ratio",
            source_provider=IntegrationProvider.META.value
        ))
        return metrics
