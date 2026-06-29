from src.validation.common import check_nulls, check_duplicates

REQUIRED_COLUMNS = ["Person"]
UNIQUE_COLUMNS = ["Person"]

def validate_users():
    results = []
    for column in REQUIRED_COLUMNS:
        results.append(
            check_nulls(
                table_name="bronze.users",
                column_name=column,
            )
        )
    
    for column in UNIQUE_COLUMNS:
        results.append(
            check_duplicates(table_name="bronze.users",
                column_name=column,
            )
        )

    return results
