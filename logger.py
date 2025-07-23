import logging
from logging import getLogger, Formatter
import logging.handlers

def my_logger(name: str) -> logging.Logger:
    """
    ### Create Logger

    Args:
        - `name`: logger user name

    Returns:
        - `logging.Logger`: logger to be used
    """
    logger: logging.Logger = logging.getLogger(name=name)
    logger.setLevel(20)
    file_handler = logging.FileHandler(f"log.txt")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return logger

def err_logger(name: str) -> logging.Logger:
    """
    ### Create Logger

    Args:
        - `name`: logger user name

    Returns:
        - `logging.Logger`: logger to be used
    """
    logger: logging.Logger = getLogger(name=name)
    logger.setLevel(30)
    file_handler = logging.FileHandler(f"error_log.txt")
    file_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.setLevel((logging.DEBUG))
    logger.addHandler(file_handler)
    return logger