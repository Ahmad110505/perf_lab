from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.models import Base, AuditMixin

class User(Base, AuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="analyst", nullable=False)
