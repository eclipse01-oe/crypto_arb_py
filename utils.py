"helper functions for the arb finder"

import logging
from config import LOG_FILE, LOG_LEVEL

def setup_logger():
    """
    Sets up a custom logger for the bot.
    """
    logger = logging.getLogger('ArbitrageBot')
    logger.setLevel(LOG_LEVEL)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(LOG_FILE)

    # Set levels for handlers
    c_handler.setLevel(LOG_LEVEL)
    f_handler.setLevel(LOG_LEVEL)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers: # Prevent adding duplicate handlers if called multiple times
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

# Initialize the logger
Logger = setup_logger()
