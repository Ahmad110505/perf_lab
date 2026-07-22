from sqlalchemy import String, BigInteger, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.shared.models import Base, AuditMixin

class Location(Base, AuditMixin):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("clients.id"), index=True, nullable=False)
    project_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("projects.id"), index=True, nullable=True)
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state_or_region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
