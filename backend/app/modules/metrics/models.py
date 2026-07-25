from sqlalchemy import Column, BigInteger, String, Float, Date, ForeignKey, JSON, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.shared.models import Base
from datetime import datetime, timezone

class RawMetric(Base):
    __tablename__ = "raw_metrics"
    
    id = Column(BigInteger, primary_key=True, index=True)
    connector_run_id = Column(BigInteger, ForeignKey("connector_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id = Column(BigInteger, ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    project = relationship("Project")

class NormalizedMetric(Base):
    __tablename__ = "normalized_metrics"
    
    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(BigInteger, ForeignKey("locations.id", ondelete="CASCADE"), nullable=True, index=True)
    metric_type = Column(String(100), nullable=False, index=True)
    metric_date = Column(Date, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)
    source_provider = Column(String(100), nullable=False)
    raw_metric_id = Column(BigInteger, ForeignKey("raw_metrics.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("project_id", "metric_type", "metric_date", "source_provider", name="uix_normalized_metrics_upsert"),
    )
