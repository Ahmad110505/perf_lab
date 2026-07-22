from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from app.modules.metrics.models import RawMetric, NormalizedMetric
from app.modules.metrics.normalizers.base import NormalizedMetricInput
from typing import List, Dict, Any
from datetime import date

def insert_raw_metric(db: Session, connector_run_id: int, integration_id: int, project_id: int, payload: Dict[str, Any]) -> RawMetric:
    raw = RawMetric(
        connector_run_id=connector_run_id,
        integration_id=integration_id,
        project_id=project_id,
        raw_payload=payload
    )
    db.add(raw)
    db.flush()
    return raw

def upsert_normalized_metrics(db: Session, raw_metric_id: int, metrics: List[NormalizedMetricInput]):
    if not metrics:
        return
        
    stmt = insert(NormalizedMetric).values([
        {
            "project_id": m.project_id,
            "location_id": m.location_id,
            "metric_type": m.metric_type,
            "metric_date": m.metric_date,
            "value": m.value,
            "unit": m.unit,
            "source_provider": m.source_provider,
            "raw_metric_id": raw_metric_id
        }
        for m in metrics
    ])
    
    # MySQL specific upsert logic
    stmt = stmt.on_duplicate_key_update(
        value=stmt.inserted.value,
        raw_metric_id=stmt.inserted.raw_metric_id
    )
    
    db.execute(stmt)

def get_normalized_metrics(db: Session, project_id: int, metric_type: str | None = None, start_date: date | None = None, end_date: date | None = None) -> List[NormalizedMetric]:
    query = db.query(NormalizedMetric).filter(NormalizedMetric.project_id == project_id)
    if metric_type:
        query = query.filter(NormalizedMetric.metric_type == metric_type)
    if start_date:
        query = query.filter(NormalizedMetric.metric_date >= start_date)
    if end_date:
        query = query.filter(NormalizedMetric.metric_date <= end_date)
    return query.all()
