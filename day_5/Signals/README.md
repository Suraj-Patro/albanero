Signals
Interupts

https://chadrick-kwag.net/python-interrupt-sigterm-sigkill-exception-handling-experiments/
https://medium.com/@cziegler_99189/gracefully-shutting-down-async-multiprocesses-in-python-2223be384510


# Interrupt
signal.SIGINT

# Termination
signal.SIGTERM

# Kill
signal.SIGKILL



KeyBoardInterrupt cannot be catched by try..except Exception

KeyboardInterrupt not a subclass of Exception


try:
    print("entering loop")
    while True:
        pass
except KeyboardInterrupt:
    print("keyboardinterrupt detected")
except Exception as e:
    print("exception catched")



signal package also allows to handle keyboard interrupts through SIGINT
SIGINT signal handler comes first than except KeyboardInterrupt


import signal, sys

def int_handler(signum, frame):
    print("sigint handler")
    sys.exit(0)


signal.signal(signal.SIGINT, int_handler)

try:
    print("entering loop")
    while True:
        pass
except KeyboardInterrupt:
    print("keyboardinterrupt detected")
except Exception as e:
    print("exception catched")



exception KeyboardInterrupt
    Raised when the user hits the interrupt key
        normally Control-C
        Delete

During execution, a check for interrupts is made regularly
    exception KeyboardInterrupt inherits from BaseException
    to not be accidentally caught by code that catches Exception
    prevent the interpreter from exiting.


SIGTERM handler works when terminated from outside



import signal, sys, os

def term_handler(signum, frame):
    print("sig term handler")
    sys.exit(0)


signal.signal(signal.SIGTERM, term_handler)


print(f"pid: {os.getpid()}")
print("entering loop")
try:
    while True:
        pass
except Exception as e:
    print("exception detected")
except BaseException:
    print("base exception detected")


