from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.shared.service import BaseService
from app.modules.auth.repository import UserRepository, user_repository
from app.modules.auth.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.modules.auth.models import User
from app.modules.auth.security import get_password_hash, verify_password, create_access_token

class AuthService(BaseService[UserRepository]):
    def __init__(self):
        super().__init__(user_repository)

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        existing = self.repository.get_by_email(db, user_in.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        obj_in = {
            "email": user_in.email,
            "password_hash": get_password_hash(user_in.password),
            "role": "analyst"
        }
        
        user = self.repository.create(db, obj_in=obj_in)
        return user

    def authenticate_user(self, db: Session, login_req: LoginRequest) -> TokenResponse:
        user = self.repository.get_by_email(db, login_req.email)
        if not user or not verify_password(login_req.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        token = create_access_token(user.id)
        return TokenResponse(access_token=token)

auth_service = AuthService()
