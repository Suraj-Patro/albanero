import gc
import os
import sys
import time
import signal
import weakref
import traceback
import multiprocessing
from logger import get_logger

from graceful_exit_worker import f, error


LOGGER = get_logger()


class Handler:
    # KEEP_PROCESSING = True
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_exit_gracefully)
        signal.signal(signal.SIGTERM, self.signal_exit_gracefully)
        sys.excepthook = self.handle_exception
        self.logger = LOGGER
    
    def signal_exit_gracefully(self, signum, frame):
        # self.KEEP_PROCESSING = False

        if os.getpid() == main_pid:
            self.logger.info(f"Graceful Exiting Signal Main PID: {os.getpid()}")
            gc.collect()
            for p in cache.values():
                self.logger.info(f"Child Process with PID: { p.pid }")
                p.terminate()
                self.logger.info(f"Child Process with PID: { p.pid } Terminated.")
        else:
            self.logger.info(f"Graceful Exiting Signal Child PID: {os.getpid()}")
            # self.logger.info(f"Stack Trace of Child Process with PID: {os.getpid()}.")
            # traceback.print_stack(frame)
            sys.exit(0)
    

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # self.logger.info(f"Graceful Exiting Exception PID: {os.getpid()}")
        if issubclass(exc_type, KeyboardInterrupt):
            return

        if os.getpid() == main_pid:
            self.logger.info(f"Graceful Exiting Exception Main PID: {os.getpid()}")
            gc.collect()
            for p in cache.values():
                self.logger.info(f"Child Process E with PID: { p.pid }")
                p.terminate()
                self.logger.info(f"Child Process E with PID: { p.pid } Terminated.")
        else:
            self.logger.info(f"Graceful Exiting Child Exception PID: {os.getpid()}")
            # self.logger.info(f"Stack Trace of Child Process with PID: {os.getpid()}.")

        # sys.__excepthook__(exc_type, exc_value, exc_traceback)
        # traceback.print_tb(exc_traceback)
        # self.logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        self.logger.error(exc_value)

    def __enter__(self, *args):
        pass

    def __exit__(self, *args):
        pass


def run():
    # can be a contect manager or also a normal assignment as well
    with Handler():
        try:
            f(LOGGER)
        except Exception:
            sys.excepthook(*sys.exc_info())
        # f(LOGGER)
    return


def main():
    Handler()
    # error()
    for i in range(2):
        p = multiprocessing.Process(target = run)
        cache[i] = p
        cache[i].start()
    
    # error()
    time.sleep(20)
    error()

    LOGGER.info('main process exiting..')
    for p in cache.values():
        p.join()


if __name__ == '__main__':
    LOGGER.info(f"Main PID: {os.getpid()}")

    main_pid = os.getpid()
    cache = weakref.WeakValueDictionary()
    
    main()
