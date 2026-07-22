from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.shared.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id, getattr(self.model, "deleted_at", None) == None)
        return db.execute(stmt).scalars().first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).where(getattr(self.model, "deleted_at", None) == None).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, *, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, *, id: int) -> Optional[ModelType]:
        obj = self.get(db=db, id=id)
        if obj and hasattr(obj, "deleted_at"):
            from datetime import datetime, timezone
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
        return obj
