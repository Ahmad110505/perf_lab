import pytest
from app.core.database import SessionLocal
from app.modules.projects.models import Project
from app.modules.clients.models import Client
from sqlalchemy import text

@pytest.fixture(autouse=True, scope="function")
def cleanup_test_data():
    yield
    db = SessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        db.query(Project).filter(Project.name.like("Test Project%")).delete(synchronize_session=False)
        db.query(Client).filter(Client.name.like("Test Client%")).delete(synchronize_session=False)
        db.query(Client).filter(Client.name.like("Integration Client%")).delete(synchronize_session=False)
        db.query(Client).filter(Client.name.like("Status Client%")).delete(synchronize_session=False)
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()
