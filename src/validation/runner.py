from src.validation.users import validate_users_data, validate_users_schema
from src.logging.logger import logger

def run_schema_validations():
    """
    Run all schema validation rules.
    """

    results = []
    validation_failed = False

    # Users
    results.extend(validate_users_schema())

    # Cards
    # results.extend(validate_cards_schema())

    # Transactions
    # results.extend(validate_transactions_schema())

    for result in results:
        if result["passed"]:
            logger.info(
                f"Schema Validation Passed: {result['rule']} | "
                f"Table: {result['table']}"
            )

        else:
            validation_failed = True

            logger.warning(
                f"Schema Validation Failed: {result['rule']} | "
                f"Table: {result['table']} | "
                f"Details: {result}"
            )

    return validation_failed


def run_data_validations():
    """
    Run all data validation rules.
    """
    results = []
    validation_failed = False

    # Users
    results.extend(validate_users_data())

    # Cards
    # results.extend(validate_cards_data())

    # Transactions
    # results.extend(validate_transactions_data())

    for result in results:
        if result["passed"]:
            logger.info(
                f"Validation Passed: {result['rule']} | "
                f"Table: {result['table']} | "
                f"Column: {result['column']} | "
                f"Invalid Rows: {result['invalid_count']}"
            )
        else:
            validation_failed = True
            logger.warning(
                f"Validation Failed: {result['rule']} | "
                f"Table: {result['table']} | "
                f"Column: {result['column']} | "
                f"Invalid Rows: {result['invalid_count']}"
            )

    return validation_failed