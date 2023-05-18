import uuid
from logger import get_logger


LOGGER = get_logger()
# LOGGER = get_logger( str(uuid.uuid4()) )

LOGGER.debug("debug message")
LOGGER.info("info message")
LOGGER.warning("warning message")
LOGGER.error("error message")
LOGGER.critical("critical message")

