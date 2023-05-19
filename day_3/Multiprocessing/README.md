Process-based parallelism

multiprocessing package
    offers both local and remote concurrency
    effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads
        allows the programmer to fully leverage multiple processors on a given machine
    runs on both Unix and Windows.


Pool object
    parallelizing the execution of a function across multiple input values
        distributing the input data across processes
        data parallelism
    defining such functions in a module
        child processes can successfully import that module

from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))

-------------------------------------

Process Class
-------------
similar to threading.thread


from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()


3 ways to start a process
    - spawn
        parent process starts a fresh Python interpreter process
            child process will only inherit necessary resources to run the process object’s run() method
        unnecessary file descriptors and handles from the parent process will not be inherited
        rather slow compared to using fork or forkserver
        Available on Unix and Windows
        default on Windows and macOS
    - fork
        parent process uses os.fork() to fork the Python interpreter
            child process, when it begins, is effectively identical to the parent process
        All resources of the parent are inherited by the child process
        safely forking a multithreaded process is problematic
        Available on Unix only
        default on Unix
    - forkserver
        When the program starts and selects the forkserver start method, a server process is started
            From then on, whenever a new process is needed
                parent process connects to the server and requests that it fork a new process
        fork server process is single threaded
            safe for it to use os.fork()
        No unnecessary resources are inherited
        Available on Unix platforms which support passing file descriptors over Unix pipes


On Unix
    using the spawn or forkserver start methods
        start a resource tracker process which tracks the unlinked named system resources
            named semaphores
            SharedMemory objects
        created by processes of the program
    When all processes have exited the resource tracker unlinks any remaining tracked object
    Usually there should be none, but if a process was killed by a signal there may be some “leaked” resources
        Neither leaked semaphores nor shared memory segments will be automatically unlinked until the next reboot
        problematic for both objects
        because system allows only a limited number of named semaphores
        shared memory segments occupy some space in the main memory



import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

set_start_method() should not be used more than once in the program
-------------------------------------------------------------------------------

Alternatively, you can use get_context() to obtain a context object
Context objects have the same API as the multiprocessing module
    allow one to use multiple start methods in the same program



import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()


objects related to one context may not be compatible with processes for a different context

In particular, locks created using the fork context cannot be passed to processes started using the spawn or forkserver start methods

library which wants to use a particular start method should probably use get_context() to avoid interfering with the choice of the library user

'spawn' and 'forkserver' start methods cannot currently be used with “frozen” executables
    i.e., binaries produced by packages like PyInstaller and cx_Freeze on Unix
    'fork' start method does work


# Exchanging objects between processes
2 types of communication channel between processes
    - Queues
        near clone of queue.Queue
        Queues are thread and process safe.

from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()


- Pipes
    returns a pair of connection objects connected by a pipe which by default is duplex (two-way)

from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()


    two connection objects returned by Pipe() represent the two ends of the pipe
    Each connection object has send() and recv() methods (among others)
    data in a pipe may become corrupted
        if two processes (or threads) try to read from or write to the same end of the pipe at the same time
    no risk of corruption from processes using different ends of the pipe at the same time


# Synchronization between processes

equivalents of all the synchronization primitives from threading

ensure one process prints to standard output at a time


from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()


Without using the lock output from the different processes is liable to get all mixed up



# Sharing state between processes

when doing concurrent programming
    best to avoid using shared state as far as possible
    particularly true when using multiple processes

need to use some shared data
    - Shared memory
        Data stored in a shared memory map using Value or Array

from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])


    3.1415927
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]


'd' and 'i' arguments
    used when creating num and arr are typecodes
        kind used by the array module
            'd' indicates a double precision float
            'i' indicates a signed integer


shared objects will be process and thread-safe

more flexibility in using shared memory
can use the multiprocessing.sharedctypes module
    supports the creation of arbitrary ctypes objects allocated from shared memory
    
    - Server process
        manager object returned by Manager()
            controls a server process which holds Python objects
            allows other processes to manipulate them using proxies
            support types
                list
                dict
                Namespace
                Lock
                RLock
                Semaphore
                BoundedSemaphore
                Condition
                Event
                Barrier
                Queue
                Value
                Array


from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)

{0.25: None, 1: '1', '2': 2}
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

    Server process managers are more flexible than using shared memory objects
        can be made to support arbitrary object types
    single manager can be shared by processes on different computers over a network
    
    slower than using shared memory


Using a pool of workers
-----------------------
Pool class
    pool of worker processes
    has methods which allows tasks to be offloaded to the worker processes
    methods of a pool should only ever be used by the process which created it


from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"

        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 seconds
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")


https://cuyu.github.io/python/2016/08/15/Terminate-multiprocess-in-Python-correctly-and-gracefully
