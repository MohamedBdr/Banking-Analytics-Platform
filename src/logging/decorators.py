import time
from functools import wraps

from src.logging.logger import logger


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        logger.info(f"Started {func.__name__}")

        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)

            logger.info(f"Finished '{func.__name__}'")

            return result

        except Exception:
            logger.exception(f"Failed '{func.__name__}'")
            raise

        finally:
            duration = time.perf_counter() - start

            logger.info(f"Execution time for {func.__name__} in {duration:.2f} seconds")

    return wrapper