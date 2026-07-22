from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class GoogleAnalyticsNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = raw_payload.get("project_id")
        
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="sessions",
            metric_date=m_date,
            value=float(raw_payload.get("sessions", 0)),
            unit="count",
            source_provider=IntegrationProvider.GOOGLE_ANALYTICS.value
        ))
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="bounce_rate",
            metric_date=m_date,
            value=float(raw_payload.get("bounce_rate", 0.0)),
            unit="percentage",
            source_provider=IntegrationProvider.GOOGLE_ANALYTICS.value
        ))
        
        return metrics
