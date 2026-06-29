from src.validation.users import validate_users
from src.logging.logger import logger

def run_validations():
    results = []
    validation_failed = False

    results.extend(validate_users())

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