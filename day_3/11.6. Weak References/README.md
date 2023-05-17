Python does automatic memory management
	reference counting for most objects
	garbage collection to eliminate cycles
	memory is freed shortly after the last reference to it has been eliminated
  
need to track objects only as long as they are being used by something else
tracking them creates a reference that makes them permanent

provides tools for tracking objects without creating a reference

When the object is no longer needed
	automatically removed from a weakref table
	garbage collector callback is triggered for weakref objects

applications include caching objects that are expensive to create



import weakref, gc
class A:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)

a = A(10)                   # create a reference
d = weakref.WeakValueDictionary()
d['primary'] = a            # does not create a reference
d['primary']                # fetch the object if it is still alive
10
del a                       # remove the one reference
gc.collect()                # run garbage collection right away
0
d['primary']                # entry was automatically removed
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    d['primary']                # entry was automatically removed
  File "C:/python37/lib/weakref.py", line 46, in __getitem__
    o = self.data[key]()
KeyError: 'primary'




KeyError meaning value garbage collected

only works on objects not primitive data types like int


===============================================================================
WeakKeyDictionary
-----------------
the dict key is the reference of weakref

WeakValueDictionary
-------------------
the dict value is the reference of weakref
