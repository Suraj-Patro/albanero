Handling uncaught exception
https://stackoverflow.com/questions/47815850/python-sys-excepthook-on-multiprocess


import sys
import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

        traceback.TracebackException
        traceback.walk_tb(exc_traceback)
        traceback.print_tb(exc_traceback)
        traceback.format_tb(exc_traceback)
        traceback.extract_tb(exc_traceback)

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


if __name__ == "__main__":
    raise RuntimeError("Test unhandled")





import sys


def handle_exception(exc_type, exc_value, exc_traceback):
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception

if __name__ == "__main__":
    # raise RuntimeError("Test unhandled")
    while True:
        pass


