Asynchronous I/O
----------------

import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

asyncio.run(main())


asyncio
    library to write concurrent code using the async/await syntax
    used as a foundation for multiple Python asynchronous frameworks that provide
        high-performance network and web-servers
        database connection libraries
        distributed task queues
    
    perfect fit for
        IO-bound
        high-level structured network code
    
    provides a set of high-level APIs to
        run Python coroutines concurrently
            have full control over their execution
            
    perform network IO and IPC
    control subprocesses
    distribute tasks via queues
    synchronize concurrent code


low-level APIs for library and framework developers to
    create and manage event loops
        provide asynchronous APIs for networking, running subprocesses, handling OS signals
    implement efficient protocols using transports
    bridge callback-based libraries and code with async/await syntax

