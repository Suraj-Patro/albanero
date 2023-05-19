import os
import sys
import time
import signal
import weakref
import traceback
import threading
from projects.Logger.logger import get_logger


LOGGER = get_logger()


def error(n):
    raise Exception(f"Exception in TID: {n}" )


def run(n):
    if n % 2 == 0:
        try:
            error(n)
        except Exception as e:
            # LOGGER.error("Uncaught exception", exc_info=e)
            LOGGER.error(e)
        return
    else:
        for i in range(5):        
            LOGGER.info(f"TID: {n} \t Running...")
            time.sleep(10)


def main():
    for i in range(5):
        p = threading.Thread(target = run, args=(i,))
        cache[i] = p
        cache[i].start()

    time.sleep(20)
    error(10)

    for p in cache.values():
        p.join()
    
    LOGGER.info('main process exiting..')



def handler(signum, frame):
    LOGGER.info(f"Signal Handler.    PID: {os.getpid()}")
    sys.exit(0)
    # # if os.getpid() == main_pid:
    # #     for p in cache.values():
    # #         LOGGER.info(f"Child Process with PID: { p.pid }")
    # #         p.terminate()
    # #         LOGGER.info(f"Child Process with PID: { p.pid } Terminated.")
    # # else:
    # #     LOGGER.info(f"Stack Trace of Child Process with PID: {os.getpid()}.")
    # #     # traceback.print_stack(frame)

    #     sys.exit(0)


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    LOGGER.info(f"Exception Handler.    PID: {os.getpid()}")
    if issubclass(exc_type, KeyboardInterrupt):
        return
    # sys.__excepthook__(exc_type, exc_value, exc_traceback)
    # traceback.print_tb(exc_traceback)
    # LOGGER.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    LOGGER.error(exc_value)
    return

sys.excepthook = handle_exception


if __name__ == '__main__':
    # LOGGER.info(f"Main PID: {os.getpid()}")

    main_pid = os.getpid()
    cache = weakref.WeakValueDictionary()
    
    main()
