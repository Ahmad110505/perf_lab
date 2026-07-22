import os
os.environ['MYSQL_PORT'] = '3307'
os.environ['JWT_SECRET_KEY'] = 'test'
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text("UPDATE alembic_version SET version_num='0004'"))
    conn.commit()
