from sqlalchemy import Column, String, BigInteger, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.shared.models import Base, AuditMixin

class Location(Base, AuditMixin):
    __tablename__ = "locations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    client_id = Column(BigInteger, ForeignKey("clients.id", ondelete="CASCADE"), index=True, nullable=False)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="SET NULL"), index=True, nullable=True)
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state_or_region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
