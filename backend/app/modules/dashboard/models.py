from sqlalchemy import Column, BigInteger, String, Date, JSON, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from app.shared.models import Base

class DashboardSummary(Base):
    __tablename__ = "dashboard_summaries"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    kpi_type = Column(String(50), nullable=False, index=True)
    period_start = Column(Date, nullable=False, index=True)
    period_end = Column(Date, nullable=False, index=True)
    aggregated_value = Column(JSON, nullable=False)
    last_calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("project_id", "kpi_type", "period_start", "period_end", name="uix_dashboard_summary"),
    )
