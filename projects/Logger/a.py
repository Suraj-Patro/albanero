import uuid
from logger import get_logger


LOGGER = get_logger()
# LOGGER = get_logger( str(uuid.uuid4()) )

LOGGER.debug("debug message")
LOGGER.info("info message")
LOGGER.warning("warning message")
LOGGER.error("error message")
LOGGER.critical("critical message")



import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    LOGGER.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

if __name__ == "__main__":
    raise RuntimeError("Test unhandled")

