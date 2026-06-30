from sqlalchemy import text
from src.database.connection import get_engine

def get_table_schema(schema_name: str, table_name: str) -> dict:
    """
    Fetch actual schema (columns + data types) from Database.
    """

    engine = get_engine()

    query = text("""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = :schema_name
          AND table_name = :table_name
        ORDER BY ordinal_position;
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {
                "schema_name": schema_name,
                "table_name": table_name
            }
        ).fetchall()

    schema = {}

    for row in result:
        schema[row.column_name] = row.data_type

    return schema



