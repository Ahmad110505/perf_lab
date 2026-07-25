from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
import redis

router = APIRouter(tags=["health"])

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """Health check monitoring database and redis status."""
    db_status = "healthy"
    redis_status = "healthy"
    
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    try:
        r = redis.Redis.from_url(settings.REDIS_URL, socket_timeout=2)
        r.ping()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"

    overall = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"
    
    return {
        "status": overall,
        "database": db_status,
        "redis": redis_status
    }
