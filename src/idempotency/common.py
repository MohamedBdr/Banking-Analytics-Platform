import hashlib
from pathlib import Path
from sqlalchemy import text
from src.database.connection import get_engine


# ------------------------------------------------------------------
# Helper Functions

def is_file_processed(file_name: str) -> bool:
    """
    Check whether a file has already been processed.
    """

    engine = get_engine()

    with engine.begin() as conn:

        return conn.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM audit.processed_files
                    WHERE file_name = :file_name
                )
            """),
            {
                "file_name": file_name
            }
        ).scalar_one()


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate the SHA-256 hash of a file.

    Args:
        file_path: Path to the file.

    Returns:
        SHA-256 hash as a hexadecimal string.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def is_file_hash_processed(file_hash: str) -> bool:
    """
    Check whether a file hash has already been processed.

    Args:
        file_hash: SHA-256 hash of the file.

    Returns:
        True if the hash already exists, otherwise False.
    """

    engine = get_engine()

    with engine.begin() as conn:

        return conn.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM audit.processed_files
                    WHERE file_hash = :file_hash
                )
            """),
            {
                "file_hash": file_hash
            }
        ).scalar_one()


def mark_file_processed(
    file_name: str,
    file_hash: str,
    run_id: int
) -> None:
    """
    Register a successfully processed file.
    """

    engine = get_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO audit.processed_files (
                    file_name,
                    file_hash,
                    run_id
                )

                VALUES (
                    :file_name,
                    :file_hash,
                    :run_id
                )
            """),
            {
                "file_name": file_name,
                "file_hash": file_hash,
                "run_id": run_id
            }
        )


# ------------------------------------------------------------------
# Rules

def check_duplicate_file(file_name: str) -> dict:
    """
    Check whether the file has already been processed.
    """

    processed = is_file_processed(file_name)

    return {
        "passed": not processed,
        "rule": "DUPLICATE_FILE",
        "file": file_name
    }


def check_duplicate_file_hash(file_path: Path) -> dict:
    """
    Check whether a file with the same content
    has already been processed.
    """

    file_hash = calculate_file_hash(file_path)

    processed = is_file_hash_processed(file_hash)

    return {
        "passed": not processed,
        "rule": "DUPLICATE_FILE_HASH",
        "file": file_path.name,
        "file_hash": file_hash
    }