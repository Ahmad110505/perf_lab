from sqlalchemy.orm import Session
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.auth.models import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.deleted_at == None)
        return db.execute(stmt).scalar_first()

user_repository = UserRepository()
