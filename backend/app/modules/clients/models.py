from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.models import Base, AuditMixin

class Client(Base, AuditMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
