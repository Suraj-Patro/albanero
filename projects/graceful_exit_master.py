import os
import sys
import time
import signal
import weakref
import traceback
import multiprocessing
from Logger.logger import get_logger

from graceful_exit_worker import f, error


LOGGER = get_logger()


def run():
    try:
        f(LOGGER)
    except Exception as e:
        # LOGGER.error("Uncaught exception", exc_info=e)
        LOGGER.error(e)
    
    return


def main():
    for i in range(5):
        p = multiprocessing.Process(target = run)
        cache[i] = p
        cache[i].start()

    time.sleep(20)
    error()

    LOGGER.info('main process exiting..')
    for p in cache.values():
        p.join()



def handler(signum, frame):
    LOGGER.info(f"Signal Handler.    PID: {os.getpid()}")
    
    if os.getpid() == main_pid:
        for p in cache.values():
            LOGGER.info(f"Child Process with PID: { p.pid }")
            p.terminate()
            LOGGER.info(f"Child Process with PID: { p.pid } Terminated.")
    else:
        LOGGER.info(f"Stack Trace of Child Process with PID: {os.getpid()}.")
        # traceback.print_stack(frame)

        sys.exit(0)


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    LOGGER.info(f"Exception Handler.    PID: {os.getpid()}")
    if issubclass(exc_type, KeyboardInterrupt):
        return
    # sys.__excepthook__(exc_type, exc_value, exc_traceback)
    # traceback.print_tb(exc_traceback)
    LOGGER.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    # LOGGER.error(exc_value)
    return

sys.excepthook = handle_exception


if __name__ == '__main__':
    LOGGER.info(f"Main PID: {os.getpid()}")

    main_pid = os.getpid()
    cache = weakref.WeakValueDictionary()
    
    main()
