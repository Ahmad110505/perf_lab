import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.models import Base, AuditMixin
from datetime import date
from typing import Optional

class ProjectStatus(str, enum.Enum):
    active = "active"
    on_hold = "on_hold"
    completed = "completed"
    cancelled = "cancelled"

class Project(Base, AuditMixin):
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    client_id = Column(BigInteger, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.active, index=True, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
