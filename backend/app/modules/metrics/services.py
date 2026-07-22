from sqlalchemy.orm import Session
from app.modules.metrics import repository as metrics_repo
from app.modules.metrics.models import RawMetric
from app.modules.integrations.models import IntegrationProvider
from app.modules.metrics.normalizers.google_analytics import GoogleAnalyticsNormalizer
from typing import Dict, Any, List

def get_normalizer(provider: str):
    if provider == IntegrationProvider.GOOGLE_ANALYTICS:
        return GoogleAnalyticsNormalizer()
    # Throwing NotImplementedError ensures we strictly catch unsupported providers
    raise NotImplementedError(f"Normalizer for {provider} not implemented")

class MetricsService:
    def ingest_and_normalize(self, db: Session, run_id: int, integration_id: int, provider: str, raw_data: List[Dict[str, Any]]) -> None:
        try:
            normalizer = get_normalizer(provider)
        except NotImplementedError:
            return
        
        for payload in raw_data:
            # Assuming payload contains project_id as agreed
            project_id = payload.get("project_id")
            if not project_id:
                continue
                
            # 1. Insert Raw Metric
            raw = metrics_repo.insert_raw_metric(
                db=db, 
                connector_run_id=run_id, 
                integration_id=integration_id, 
                project_id=project_id, 
                payload=payload
            )
            
            # 2. Normalize
            normalized = normalizer.normalize(payload)
            
            # 3. Upsert Normalized Metrics
            metrics_repo.upsert_normalized_metrics(db, raw.id, normalized)
            
            # Flush changes per payload to ensure IDs are available
            db.flush()

    def rebuild_normalized_metrics(self, db: Session, project_id: int | None = None) -> None:
        query = db.query(RawMetric)
        if project_id:
            query = query.filter(RawMetric.project_id == project_id)
            
        from app.modules.integrations.repository import integration_repository
            
        for raw in query.yield_per(100):
            integration = integration_repository.get(db, id=raw.integration_id)
            if not integration:
                continue
                
            try:
                normalizer = get_normalizer(integration.provider)
                normalized = normalizer.normalize(raw.raw_payload)
                metrics_repo.upsert_normalized_metrics(db, raw.id, normalized)
                db.commit()
            except NotImplementedError:
                continue

metrics_service = MetricsService()
