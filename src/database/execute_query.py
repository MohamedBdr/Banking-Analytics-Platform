from sqlalchemy import text
from src.database.connection import get_engine
import os

DB_NAME = os.getenv('POSTGRES_DATABASE_NAME')

def execute_scalar(query: str):
    """
    Execute a SQL Query.
    """
    engine = get_engine(DB_NAME)

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return int(result.scalar())