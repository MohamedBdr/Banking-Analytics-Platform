from sqlalchemy import text
from dotenv import load_dotenv
from src.database.connection import get_engine
import os

load_dotenv()

DB_NAME = os.getenv('POSTGRES_DATABASE_NAME')
SCHEMAS = ["bronze", "silver", "gold", "audit"]


def create_schemas():
    engine = get_engine(DB_NAME)

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")

        for schema in SCHEMAS:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            print(f"Schema created/exists: {schema}")


if __name__ == "__main__":
    create_schemas()
