from sqlalchemy import text
from dotenv import load_dotenv
from src.database.connection import get_engine
import os

load_dotenv()

DB_DEFAULT = "postgres"
DB_NAME = os.getenv('POSTGRES_DATABASE_NAME')

def create_database():
    engine = get_engine(DB_DEFAULT)

    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")

        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": DB_NAME}
        ).scalar()

        if not exists:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"✅ {DB_NAME} Database Created successfully!")
        else:
            print("ℹ️ DB Database Already Exists!")


if __name__ == "__main__":
    create_database()