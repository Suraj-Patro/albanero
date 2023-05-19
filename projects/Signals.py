import os
import sys
import signal
import traceback



def handler(signum, frame):
    print("handler")
    print(signum)
    print(frame)
	# print the stack frame / execution frame
	# let's us know where the code was when the signal was raised
    
    print(traceback.StackSummary)
    print(traceback.walk_stack(frame))
    traceback.print_stack(frame)
    print(traceback.extract_stack(frame))
    print(traceback.format_stack(frame))
    
    sys.exit(0)


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

# Can't handle SIGKILL
# signal.signal(signal.SIGKILL, handler)


print(f"pid: {os.getpid()}")
print("entering loop")
try:
    while True:
        pass
except Exception as e:
    print("exception detected")
    
# BaseException cathes the sys.exit(0)
# except BaseException:
#     print("base exception detected")
