from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, JSON, DateTime, Enum, Index
from sqlalchemy.orm import relationship
import enum
from app.shared.models import Base, AuditMixin

class IntegrationProvider(str, enum.Enum):
    PROCORE = "procore"
    AUTODESK = "autodesk"
    GENERIC_WEBHOOK = "generic_webhook"
    GOOGLE_ANALYTICS = "google_analytics"
    GOOGLE_SEARCH_CONSOLE = "google_search_console"
    META = "meta"
    AHREFS = "ahrefs"
    SEMRUSH = "semrush"
    GOOGLE_TAG_MANAGER = "google_tag_manager"
    GOOGLE_BUSINESS_PROFILE = "google_business_profile"

class IntegrationStatus(str, enum.Enum):
    PENDING = "pending"
    CONNECTED = "connected"
    ERROR = "error"
    DISABLED = "disabled"

class Integration(Base, AuditMixin):
    __tablename__ = "integrations"

    id = Column(BigInteger, primary_key=True, index=True)
    client_id = Column(BigInteger, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(Enum(IntegrationProvider), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    status = Column(Enum(IntegrationStatus), default=IntegrationStatus.PENDING, nullable=False, index=True)
    config = Column(JSON, nullable=True)
    # We store a reference to the secret in a secure vault, NOT the raw secret string.
    credentials_ref = Column(String(255), nullable=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)

    client = relationship("Client", backref="integrations")

    __table_args__ = (
        Index("ix_integrations_client_id_provider", "client_id", "provider"),
        Index("ix_integrations_deleted_at", "deleted_at"),
    )
