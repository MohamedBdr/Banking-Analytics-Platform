from src.idempotency.users import validate_users_idempotency
from src.logging.logger import logger


def run_idempotency_validations():
    """
    Run all idempotency validation rules.
    """

    results = []
    validation_failed = False

    latest_files = {}

    # Users
    user_results, latest_files["users"] = validate_users_idempotency()
    results.extend(user_results)

    # Cards
    # card_results, latest_files["cards"] = validate_cards_idempotency()
    # results.extend(card_results)

    # Transactions
    # transaction_results, latest_files["transactions"] = validate_transactions_idempotency()
    # results.extend(transaction_results)

    for result in results:

        if result["passed"]:

            logger.info(
                f"Idempotency Validation Passed: {result['rule']} | "
                f"File: {result['file']}"
            )

        else:

            validation_failed = True

            logger.warning(
                f"Idempotency Validation Failed: {result['rule']} | "
                f"File: {result['file']}"
            )

    return validation_failed, latest_files