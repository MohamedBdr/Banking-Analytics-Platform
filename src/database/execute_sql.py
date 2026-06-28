from pathlib import Path

from sqlalchemy import text

from src.database.connection import get_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DATABASE_NAME")


def execute_sql(sql_file: str) -> None:
    """
    Execute a SQL script.
    """

    sql_path = Path(sql_file)

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    with open(sql_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    engine = get_engine(DB_NAME)

    with engine.begin() as conn:
        conn.execute(text(sql_script))

    print(f"✅ Executed: {sql_path.name}")

