from sqlalchemy import text
from src.database.connection import get_engine

def test_connection():
    engine = get_engine()

    with engine.connect() as conn:
        version = conn.execute(text("SELECT version(); \nConnected To DB")).scalar()

    print(version)