from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.modules.auth.services import auth_service
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return auth_service.register_user(db, user_in=user_in)

@router.post("/login", response_model=TokenResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a token."""
    return auth_service.authenticate_user(db, login_req=login_req)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retrieve the currently authenticated user."""
    return current_user
