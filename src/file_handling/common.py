from pathlib import Path
import shutil


# helper fun
def find_latest_file(directory: Path, pattern: str) -> Path | None:
    """
    Find the latest file matching a pattern.
    """

    files = list(directory.glob(pattern))

    if not files:
        return None

    return max(files, key=lambda file: file.stat().st_mtime)


def move_file(
    source: Path,
    destination_directory: Path
) -> Path:
    """
    Move a file to another directory.
    """

    destination_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = destination_directory / source.name

    shutil.move(str(source), str(destination))

    return destination

# ------------------------------------------------------------------

# 1. First Check
def check_file_exists(file_path: Path | None) -> dict:
    """
    Check whether a file exists.
    """

    if file_path is None:
        return {
            "passed": False,
            "rule": "FILE_EXISTS",
            "file": None
        }

    return {
        "passed": file_path.exists(),
        "rule": "FILE_EXISTS",
        "file": file_path.name
    }


# 2. Second Check
def check_empty_file(file_path: Path) -> dict:
    """
    Check whether a file is empty.
    """

    return {
        "passed": file_path.stat().st_size > 0,
        "rule": "EMPTY_FILE",
        "file": file_path.name,
        "size_bytes": file_path.stat().st_size
    }

def check_file_extension(
    file_path: Path,
    expected_extension: str
) -> dict:
    """
    Check whether the file has the expected extension.
    """

    actual_extension = file_path.suffix.lower()

    return {
        "passed": actual_extension == expected_extension.lower(),
        "rule": "FILE_EXTENSION",
        "file": file_path.name,
        "expected_extension": expected_extension.lower(),
        "actual_extension": actual_extension
    }

def check_file_encoding(
        file_path: Path,
        expected_encoding: str="utf-8"
) -> dict:
    """
    Check whether the file uses the expected encoding.
    """
    try:
        with open(file_path, "r", encoding=expected_encoding) as file:
            file.readline()
            return {
            "passed": True,
            "rule": "FILE_ENCODING",
            "file": file_path.name,
            "expected_encoding": expected_encoding,
            "actual_encoding": expected_encoding
        }

    except UnicodeDecodeError:
        return {
            "passed": False,
            "rule": "FILE_ENCODING",
            "file": file_path.name,
            "expected_encoding": expected_encoding,
            "actual_encoding": "unknown"
        }