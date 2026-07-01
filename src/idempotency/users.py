from pathlib import Path

from src.file_handling.common import find_latest_file
from src.file_handling.config import DATA_PATH
from src.idempotency.common import (
    check_duplicate_file,
    check_duplicate_file_hash
)


FILE_PATTERN = "*users.csv"

def validate_users_idempotency():
    """
    Run idempotency rules for users file .
    """

    results = []

    latest_file = find_latest_file(
        directory=Path(DATA_PATH),
        pattern=FILE_PATTERN
    )

    if latest_file is not None:

        results.append(
            check_duplicate_file(latest_file.name)
        )

        results.append(
            check_duplicate_file_hash(latest_file)
        )

    return results, latest_file