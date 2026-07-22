from sqlalchemy.orm import Session
from app.modules.metrics import repository as metrics_repo
from app.modules.metrics.models import RawMetric
from app.modules.integrations.models import IntegrationProvider
from app.modules.metrics.normalizers.google_analytics import GoogleAnalyticsNormalizer
from app.modules.metrics.normalizers.google_search_console import GoogleSearchConsoleNormalizer
from app.modules.metrics.normalizers.meta import MetaNormalizer
from app.modules.metrics.normalizers.ahrefs import AhrefsNormalizer
from app.modules.metrics.normalizers.semrush import SEMrushNormalizer
from typing import Dict, Any, List

def get_normalizer(provider: str):
    if provider == IntegrationProvider.GOOGLE_ANALYTICS:
        return GoogleAnalyticsNormalizer()
    elif provider == IntegrationProvider.GOOGLE_SEARCH_CONSOLE:
        return GoogleSearchConsoleNormalizer()
    elif provider == IntegrationProvider.META:
        return MetaNormalizer()
    elif provider == IntegrationProvider.AHREFS:
        return AhrefsNormalizer()
    elif provider == IntegrationProvider.SEMRUSH:
        return SEMrushNormalizer()
    raise NotImplementedError(f"Normalizer for {provider} not implemented")

class MetricsService:
    def ingest_and_normalize(self, db: Session, run_id: int, integration_id: int, provider: str, raw_data: List[Dict[str, Any]]) -> None:
        try:
            normalizer = get_normalizer(provider)
        except NotImplementedError:
            return
        
        for payload in raw_data:
            project_id = payload.get("project_id")
            if not project_id:
                continue
                
            raw = metrics_repo.insert_raw_metric(
                db=db, 
                connector_run_id=run_id, 
                integration_id=integration_id, 
                project_id=project_id, 
                payload=payload
            )
            
            normalized = normalizer.normalize(payload)
            metrics_repo.upsert_normalized_metrics(db, raw.id, normalized)
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
