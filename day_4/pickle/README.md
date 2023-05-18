pickle — Python object serialization

Source code: Lib/pickle.py


implements binary protocols for serializing and de-serializing a Python object structure

“Pickling”
    the process whereby a Python object hierarchy is converted into a byte stream

“unpickling”
    the inverse operation
    
    whereby a byte stream (from a binary file or bytes-like object) is converted back into an object hierarchy
    
Pickling (and unpickling)
    alternatively known
        “serialization”
        “marshalling,”
        “flattening”



Safer serialization formats
    json
    more appropriate
        processing untrusted data
