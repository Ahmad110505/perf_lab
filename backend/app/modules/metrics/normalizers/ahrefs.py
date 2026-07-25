from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class AhrefsNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = raw_payload.get("project_id")
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="domain_rating",
            metric_date=m_date,
            value=float(raw_payload.get("domain_rating", 0)),
            unit="score",
            source_provider=IntegrationProvider.AHREFS.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="backlinks",
            metric_date=m_date,
            value=float(raw_payload.get("backlinks", 0)),
            unit="count",
            source_provider=IntegrationProvider.AHREFS.value
        ))
        return metrics
