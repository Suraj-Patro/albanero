import os
import time


def error():
    raise Exception(f"Exception in PID: {os.getpid()}" )
    # print(f"{os.getpid()}")


def work(LOGGER):
    for i in range(5):
        LOGGER.info(f"PID: {os.getpid()} \t Running...")
        time.sleep(10)


def f(LOGGER):
    raise Exception("worker exception")
    if os.getpid() % 2 == 0:
        return error()
    else:
        return work(LOGGER)
