StringIO

    an in-memory file-like object
    object can be used as input or output to the most function that would expect a standard file object
    
when created
    it is initialized by passing a string to the constructor
    no string is passed the StringIO will start empty
    initial cursor on the file starts at zero
    
does not exist in the latest version of Python
to work with it
    import io.StringIO


# Importing the StringIO module.
from io import StringIO

# The arbitrary string.
string ='This is initial string.'

# Using the StringIO method to set
# as file object. Now we have an
# object file that we will able to
# treat just like a file.
file = StringIO(string)

# this will read the file
print(file.read())

# We can also write this file.
file.write(" Welcome to Home.")

# This will make the cursor at
# index 0.
file.seek(0)

# This will print the file after
# writing in the initial string.
print('The string after writing is:', file.read())


