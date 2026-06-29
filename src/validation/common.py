from src.database.execute_query import execute_scalar


def check_nulls(table_name: str, column_name: str) -> dict:
    """
    Check Rule if a column contains NULL values.
    """
    query = f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE "{column_name}" IS NULL
    """
    invalid_count = execute_scalar(query)
    return {
        "passed": invalid_count==0,
        "rule": "NULL_CHECK",
        "table": table_name,
        "column": column_name,
        "invalid_count": invalid_count
    }
     

def check_duplicates(table_name: str, column_name: str) -> dict:
    """
    Check Rule if a column contains duplicate values.
    """
    query = f"""
        SELECT COALESCE(SUM(duplicate_count - 1), 0)
        FROM (
            SELECT COUNT(*) AS duplicate_count
            FROM {table_name}
            GROUP BY "{column_name}"
            HAVING COUNT(*) > 1
        ) duplicates    
    """
    duplicate_count = execute_scalar(query)
    return {
        "passed": duplicate_count == 0,
        "rule": "DUPLICATE_CHECK",
        "table": table_name,
        "column": column_name,
        "invalid_count": duplicate_count,
    }