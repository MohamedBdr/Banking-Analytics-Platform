from src.validation.common import check_nulls, check_duplicates
from src.validation.schema import validate_schema

REQUIRED_COLUMNS = ["Person"]
UNIQUE_COLUMNS = ["Person"]

EXPECTED_SCHEMA = {
    "Person": "text",
    "Current Age": "text",
    "Retirement Age": "text",
    "Birth Year": "text",
    "Birth Month": "text",
    "Gender": "text",
    "Address": "text",
    "Apartment": "text",
    "City": "text",
    "State": "text",
    "Zipcode": "text",
    "Latitude": "text",
    "Longitude": "text",
    "Per Capita Income - Zipcode": "text",
    "Yearly Income - Person": "text",
    "Total Debt": "text",
    "FICO Score": "text",
    "Num Credit Cards": "text",
    "source_file": "character varying",
    "load_timestamp": "timestamp without time zone"
}

def validate_users_data():
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

def validate_users_schema():
    return validate_schema(
        schema_name="bronze",
        table_name="users",
        expected_schema=EXPECTED_SCHEMA
    )
