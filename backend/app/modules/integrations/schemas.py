from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.modules.integrations.models import IntegrationProvider, IntegrationStatus

class IntegrationBase(BaseModel):
    name: str = Field(..., max_length=100)
    provider: IntegrationProvider
    status: Optional[IntegrationStatus] = IntegrationStatus.PENDING
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Minimal config payload")
    credentials_ref: Optional[str] = Field(None, description="Reference ID to vault. Do not send raw secrets.")

class IntegrationCreate(IntegrationBase):
    client_id: int

class IntegrationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    status: Optional[IntegrationStatus] = None
    config: Optional[Dict[str, Any]] = None
    credentials_ref: Optional[str] = None
    last_synced_at: Optional[datetime] = None

class IntegrationResponse(IntegrationBase):
    id: int
    client_id: int
    last_synced_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class IntegrationListResponse(BaseModel):
    items: list[IntegrationResponse]
    total: int
    skip: int
    limit: int
