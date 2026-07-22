from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the location")
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state_or_region: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)

class LocationCreate(LocationBase):
    client_id: int = Field(..., description="The ID of the client owning this location")
    project_id: Optional[int] = Field(None, description="The optional ID of the project owning this location")

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    project_id: Optional[int] = Field(None)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state_or_region: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)

class LocationResponse(LocationBase):
    id: int
    client_id: int
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LocationListResponse(BaseModel):
    items: list[LocationResponse]
    total: int
