from src.file_handling.common import find_latest_file, check_file_exists,\
      check_empty_file, check_file_extension, check_file_encoding
from src.file_handling.config import DATA_PATH
from pathlib import Path


FILE_PATTERN = "*users.csv"
EXPECTED_EXTENSION = ".csv"
EXPECTED_ENCODING = "utf-8"


def validate_users_file():
    """
    Run file handling rules for users file.
    """
    results = []

    latest_file = find_latest_file(
        directory=Path(DATA_PATH),
        pattern=FILE_PATTERN
    )

    results.append(
        check_file_exists(latest_file)
    )
    
    if latest_file is not None:
        results.append(check_empty_file(latest_file))
        results.append(
            check_file_extension(
                file_path=latest_file,
                expected_extension=EXPECTED_EXTENSION
            )
        )
        results.append(
            check_file_encoding(
                file_path=latest_file,
                expected_encoding=EXPECTED_ENCODING
            )
        )        

    return results