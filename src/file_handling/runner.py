from src.file_handling.users import validate_users_file
from src.logging.logger import logger

def run_file_validations():
    """
    Run all file validation rules.
    """

    results = []
    validation_failed = False

    # Users
    results.extend(validate_users_file())

    # Cards
    # results.extend(validate_cards_file())

    # Transactions
    # results.extend(validate_transactions_file())

    for result in results:

        if result["passed"]:

            logger.info(
                f"File Validation Passed: {result['rule']} | "
                f"File: {result['file']}"
            )

        else:

            validation_failed = True

            logger.warning(
                f"File Validation Failed: {result['rule']} | "
                f"File: {result['file']}"
            )

    return validation_failed

