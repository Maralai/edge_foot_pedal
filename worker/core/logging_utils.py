import logging
import os

def configure_logging():
    log_level = os.getenv('LOG_LEVEL', 'WARNING').upper()
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=log_level
    )