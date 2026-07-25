from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class GoogleSearchConsoleNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = raw_payload.get("project_id")
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="clicks",
            metric_date=m_date,
            value=float(raw_payload.get("clicks", 0)),
            unit="count",
            source_provider=IntegrationProvider.GOOGLE_SEARCH_CONSOLE.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="impressions",
            metric_date=m_date,
            value=float(raw_payload.get("impressions", 0)),
            unit="count",
            source_provider=IntegrationProvider.GOOGLE_SEARCH_CONSOLE.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="ctr",
            metric_date=m_date,
            value=float(raw_payload.get("ctr", 0.0)),
            unit="percentage",
            source_provider=IntegrationProvider.GOOGLE_SEARCH_CONSOLE.value
        ))
        metrics.append(NormalizedMetricInput(
            project_id=project_id,
            metric_type="position",
            metric_date=m_date,
            value=float(raw_payload.get("position", 0.0)),
            unit="rank",
            source_provider=IntegrationProvider.GOOGLE_SEARCH_CONSOLE.value
        ))
        return metrics
