Threading
    technique for decoupling tasks which are not sequentially dependent

Threads
    used to improve the responsiveness of applications that accept user input while other tasks run in the background
    use case is running I/O in parallel with computations in another thread


principal challenge of multi-threaded applications
    coordinating threads that share data or other resources
    
threading module provides a number of synchronization primitives including:
    locks
    events
    condition variables
    semaphores


While those tools are powerful
    minor design errors can result in problems that are difficult to reproduce
    
    
preferred approach to task coordination is to concentrate all access to a resource in a single thread
    then use the queue module to feed that thread with requests from other threads
    Applications using Queue objects for inter-thread communication and coordination are easier to
        design
        more readable
        more reliable




import threading, zipfile

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished background zip of:', self.infile)

background = AsyncZip('mydata.txt', 'myarchive.zip')
background.start()
print('The main program continues to run in foreground.')

background.join()    # Wait for the background task to finish
print('Main program waited until background was done.')

===============================================================================

## https://www.tutorialspoint.com/python/python_multithreading.htm

start a thread
--------------

Using thread module
------------------
thread.start_new_thread( func[, *args[, **kwargs]])
works good for both linux and windows


import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print( "%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print( "Error: unable to start thread")

while 1:
   pass


very effective for low-level threading
    thread module is very limited compared to the newer threading module


using threading
---------------
much more powerful
high-level support for threads 

threading exposes all the methods of the thread module
    - run()
        entry point for a thread
    - start()
        starts a thread by calling the run method
    - join([time])
        waits for threads to terminate
    - isAlive()
        checks whether a thread is still executing
    - getName()
        returns the name of a thread
    - setName()
        sets the name of a thread

along some additional methods
    - threading.activeCount()
        Returns the number of thread objects that are active
    - threading.currentThread()
        Returns the number of thread objects in the caller's thread control
    - threading.enumerate()
        Returns a list of all thread objects that are currently active


new thread using the threading module
    - Define a new subclass of the Thread class
    - Override the __init__(self [,args]) method to add additional arguments
    - override the run(self [,args]) method to implement what the thread should do when started
    - start a new thread by invoking the start()
        which in turn calls run() method


import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name
      print_time(self.name, 5, self.counter)
      print "Exiting " + self.name

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")
-------------------------------------------------------------------------------

Synchronizing Threads
    simple-to-implement locking mechanism that allows you to synchronize threads
    new lock is created by calling the Lock() method
        returns the new lock

acquire(blocking) method of the new lock object is used to force threads to run synchronously
    optional blocking parameter enables
        to control whether the thread waits to acquire the lock


If blocking is set to 0
    thread returns immediately with a 0 value if the lock cannot be acquired
    with a 1 if the lock was acquired

If blocking is set to 1
    thread blocks and wait for the lock to be released

release() method of the new lock object
    used to release the lock when it is no longer required


import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name
      # Get lock to synchronize threads
      threadLock.acquire()
      print_time(self.name, self.counter, 3)
      # Free lock to release next thread
      threadLock.release()

def print_time(threadName, delay, counter):
   while counter:
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"
-------------------------------------------------------------------------------


Multithreaded Priority Queue
----------------------------
Queue module
    allows to create a new queue object that can hold a specific number of items
    
methods to control the Queue
    - get()
        removes and returns an item from the queue
    - put()
        adds item to a queue
    - qsize()
        returns the number of items that are currently in the queue
    - empty()
        returns True if queue is empty
        otherwise, False
    - full()
        returns True if queue is full
        otherwise, False


import Queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print "Starting " + self.name
      process_data(self.name, self.q)
      print "Exiting " + self.name

def process_data(threadName, q):
   while not exitFlag:
      queueLock.acquire()
         if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
         else:
            queueLock.release()
         time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
   workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print "Exiting Main Thread"
