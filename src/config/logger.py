"""Logging configuration for the application."""

import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name: str = "worksquadbot", level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure application logger with console and file handlers.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    log_dir = os.getenv("LOG_DIR", "/app/logs")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "bot.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "worksquadbot") -> logging.Logger:
    """
    Get logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
