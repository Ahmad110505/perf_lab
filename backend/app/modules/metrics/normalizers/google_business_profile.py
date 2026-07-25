from typing import Dict, Any, List
from datetime import datetime
from app.modules.metrics.normalizers.base import BaseNormalizer, NormalizedMetricInput
from app.modules.integrations.models import IntegrationProvider

class GoogleBusinessProfileNormalizer(BaseNormalizer):
    def normalize(self, raw_payload: Dict[str, Any]) -> List[NormalizedMetricInput]:
        metrics = []
        project_id = int(raw_payload.get("project_id", 1))
        m_date = datetime.strptime(raw_payload["date"], "%Y-%m-%d").date()
        
        if "sessions" in raw_payload:
            metrics.append(NormalizedMetricInput(
                project_id=project_id,
                metric_type="sessions",
                metric_date=m_date,
                value=float(raw_payload.get("sessions", 0)),
                unit="count",
                source_provider=IntegrationProvider.GOOGLE_BUSINESS_PROFILE.value
            ))
            
        if "map_views" in raw_payload:
            metrics.append(NormalizedMetricInput(
                project_id=project_id,
                metric_type="map_views",
                metric_date=m_date,
                value=float(raw_payload.get("map_views", 0)),
                unit="count",
                source_provider=IntegrationProvider.GOOGLE_BUSINESS_PROFILE.value
            ))

        if "phone_calls" in raw_payload:
            metrics.append(NormalizedMetricInput(
                project_id=project_id,
                metric_type="phone_calls",
                metric_date=m_date,
                value=float(raw_payload.get("phone_calls", 0)),
                unit="count",
                source_provider=IntegrationProvider.GOOGLE_BUSINESS_PROFILE.value
            ))
        
        return metrics
