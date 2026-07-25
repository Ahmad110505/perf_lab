from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.modules.connectors.models import RunStatus

class ConnectorRunResponse(BaseModel):
    id: int
    integration_id: int
    status: RunStatus
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error_message: Optional[str] = None
    records_processed: Optional[int] = None
    retry_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TriggerSyncRequest(BaseModel):
    pass

class ConnectorRunListResponse(BaseModel):
    items: list[ConnectorRunResponse]
    total: int
    skip: int
    limit: int
