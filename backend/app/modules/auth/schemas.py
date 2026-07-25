from pydantic import BaseModel, EmailStr, ConfigDict, Field, model_validator
import re
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @model_validator(mode='after')
    def validate_password_complexity(self) -> 'UserCreate':
        pw = self.password
        if not re.search(r'[A-Z]', pw):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', pw):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', pw):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[^A-Za-z0-9]', pw):
            raise ValueError("Password must contain at least one special character")
        return self

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
