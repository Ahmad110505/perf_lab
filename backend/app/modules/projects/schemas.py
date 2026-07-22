from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime, date
from typing import Optional
from app.modules.projects.models import ProjectStatus

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the project")
    status: ProjectStatus = Field(default=ProjectStatus.active)
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ProjectCreate(ProjectBase):
    client_id: int = Field(..., description="The ID of the client owning this project")

    @model_validator(mode='after')
    def validate_dates(self) -> 'ProjectCreate':
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @model_validator(mode='after')
    def validate_dates(self) -> 'ProjectUpdate':
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self

class ProjectResponse(ProjectBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
