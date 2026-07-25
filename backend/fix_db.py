import os
os.environ['MYSQL_PORT'] = '3307'
os.environ['JWT_SECRET_KEY'] = 'test'
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS integrations'))
    conn.commit()
