import logging
from logging.handlers import RotatingFileHandler
from src.config.settings import (
    LOG_LEVEL,
    LOG_FILE,
    MAX_LOG_SIZE,
    BACKUP_COUNT,
)

# logger for (info, warning, error, critical)
logger = logging.getLogger("etl_pipeline")
logger.setLevel(LOG_LEVEL)

# Log Format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File Handler
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT
)
file_handler.setFormatter(formatter)

# One Handler inserted if it used many
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
