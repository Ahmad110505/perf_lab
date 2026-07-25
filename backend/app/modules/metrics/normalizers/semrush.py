from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class SEMrushNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = raw_payload.get("project_id")
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="organic_keywords",
            metric_date=m_date,
            value=float(raw_payload.get("organic_keywords", 0)),
            unit="count",
            source_provider=IntegrationProvider.SEMRUSH.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="organic_traffic",
            metric_date=m_date,
            value=float(raw_payload.get("organic_traffic", 0)),
            unit="count",
            source_provider=IntegrationProvider.SEMRUSH.value
        ))
        return metrics
