import sys
import traceback


def handle_exception(exc_type, exc_value, exc_traceback):
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    traceback.print_tb(exc_traceback)


sys.excepthook = handle_exception


if __name__ == "__main__":
    raise RuntimeError("Test unhandled")
    # while True:
    #     pass
