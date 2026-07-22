from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the client")

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ClientListResponse(BaseModel):
    items: list[ClientResponse]
    total: int
