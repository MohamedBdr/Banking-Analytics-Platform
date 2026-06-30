#####################################
# This file for Schema Validation Rules
#####################################

from src.database.metadata import get_table_schema

TYPE_MAPPING = {
    "text": "text",
    "character varying": "text",
    "varchar": "text",

    "integer": "integer",
    "int": "integer",
    "int4": "integer",

    "bigint": "bigint",
    "int8": "bigint",

    "timestamp": "timestamp",
    "timestamp without time zone": "timestamp",

    "numeric": "numeric",
    "decimal": "numeric",
}


def normalize_data_type(data_type: str) -> str:
    """
    Normalize database data types before comparison.
    """

    if data_type is None:
        return ""

    return TYPE_MAPPING.get(
        data_type.lower(),
        data_type.lower()
    )


def validate_missing_columns(
        expected_schema: dict,
        actual_schema: dict,
        table_name: str
) -> dict:
    """
    Validate that all expected columns exist.
    """
    expected_columns = set(expected_schema.keys())
    actual_columns = set(actual_schema.keys())

    missing_columns = sorted(expected_columns - actual_columns)

    return {
        "passed": len(missing_columns) == 0,
        "rule": "MISSING_COLUMNS",
        "table": table_name,
        "missing_columns": missing_columns
    }
    

def validate_extra_columns(
    expected_schema: dict,
    actual_schema: dict,
    table_name: str
) -> dict:
    """
    Validate that no unexpected columns exist.
    """

    expected_columns = set(expected_schema.keys())
    actual_columns = set(actual_schema.keys())

    extra_columns = sorted(actual_columns - expected_columns)

    return {
        "passed": len(extra_columns) == 0,
        "rule": "EXTRA_COLUMNS",
        "table": table_name,
        "extra_columns": extra_columns
    }

def validate_column_types(
    expected_schema: dict,
    actual_schema: dict,
    table_name: str
) -> dict:
    """
    Validate that column data types match the expected schema.
    """

    mismatched_columns = []

    common_columns = set(expected_schema.keys()) & set(actual_schema.keys())

    for column in common_columns:

        expected_type = normalize_data_type(expected_schema[column])
        actual_type = normalize_data_type(actual_schema[column])

        if expected_type != actual_type:
            mismatched_columns.append(
                {
                    "column": column,
                    "expected_type": expected_type,
                    "actual_type": actual_type
                }
            )

    return {
        "passed": len(mismatched_columns) == 0,
        "rule": "COLUMN_TYPES",
        "table": table_name,
        "mismatched_columns": mismatched_columns
    }

def validate_schema(
    schema_name: str,
    table_name: str,
    expected_schema: dict
) -> list:
    """
    Run all schema validation rules.
    """

    results = []

    actual_schema = get_table_schema(
        schema_name=schema_name,
        table_name=table_name
    )

    results.append(
        validate_missing_columns(
            expected_schema=expected_schema,
            actual_schema=actual_schema,
            table_name=table_name
        )
    )

    results.append(
        validate_extra_columns(
            expected_schema=expected_schema,
            actual_schema=actual_schema,
            table_name=table_name
        )
    )

    results.append(
        validate_column_types(
            expected_schema=expected_schema,
            actual_schema=actual_schema,
            table_name=table_name
        )
    )

    return results

