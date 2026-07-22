import enum
from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, Enum, Text, Integer, Index
from sqlalchemy.orm import relationship
from app.shared.models import Base, AuditMixin

class RunStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class ConnectorRun(Base, AuditMixin):
    __tablename__ = "connector_runs"

    id = Column(BigInteger, primary_key=True, index=True)
    integration_id = Column(BigInteger, ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(RunStatus), default=RunStatus.QUEUED, nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    records_processed = Column(Integer, nullable=True)

    integration = relationship("Integration", backref="connector_runs")

    __table_args__ = (
        Index("ix_connector_runs_deleted_at", "deleted_at"),
    )
