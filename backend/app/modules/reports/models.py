import enum
from sqlalchemy import Column, BigInteger, String, Enum as SQLEnum, Date, DateTime, ForeignKey
from datetime import datetime, timezone
from app.shared.models import Base

class ReportFormat(str, enum.Enum):
    CSV = "csv"
    JSON = "json"

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Report(Base):
    __tablename__ = "reports"

    id = Column(BigInteger, primary_key=True, index=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    format = Column(SQLEnum(ReportFormat), default=ReportFormat.CSV, nullable=False)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING, nullable=False, index=True)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    file_path = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
