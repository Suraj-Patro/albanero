Scopes & Namespaces
-------------------
the innermost scope, which is searched first, contains the local names

the scopes of any enclosing functions, which are searched starting with the nearest enclosing scope, contains non-local, but also non-global names

the next-to-last scope contains the current module’s global names

the outermost scope (searched last) is the namespace containing built-in names


Assignments do not copy data
    bind names to objects

same is true for deletions
    del x
        removes the binding of x from the namespace referenced by the local scope

all operations that introduce new names use the local scope
import statements and function definitions bind the module or function name in the local scope



# Class Objects

Class objects support two kinds of operations
    - attribute references
    - attribute instantiation

Attribute references use the standard syntax used for all attribute references in Python: obj.name
Valid attribute names are all the names that were in the class’s namespace when the class object was created

class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

MyClass.i
MyClass.f

returning an integer and a function object, respectively

Class attributes can also be assigned to
    change the value of MyClass.i by assignment

__doc__ is also a valid attribute
    returning the docstring belonging to the class
        "A simple example class".

Class instantiation uses function notation


# Instance Objects

only operations understood by:
- attribute references

two kinds of valid attribute names
    - data attributes
    - methods

data attributes
    need not be declared; like local variables
        existence when they are first assigned to


x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter


method
    - function that “belongs to” an object
        term method is not unique to class instances
            other object types can have methods as well

Valid method names of an instance object depend on its class
all attributes of a class that are function objects
    define corresponding methods of its instances
    
x.f is a valid method reference
MyClass.f is a function reference

x.f is a method object
MyClass.f is a function object


# Method Objects

methods
    instance object is passed as the first argument of the function
        call x.f() is exactly equivalent to MyClass.f(x)
            calling a method with a list of n arguments
            equivalent to calling the corresponding function with an argument list
                created by inserting the method’s instance object before the first argument

When a non-data attribute of an instance is referenced
    instance’s class is searched
        If the name denotes a valid class attribute that is a function object
            a method object is created by packing (pointers to)
                - instance object
                - function object
                just found together in an abstract object

When the method object is called with an argument list
    new argument list is constructed from the instance object and the argument list
        function object is called with this new argument list


# Class and Instance Variables
instance variables are for data unique to each instance
class variables are for attributes and methods shared by all instances of the class


# Random Remarks

Data attributes override method attributes with the same name
    to avoid accidental name conflicts, which may cause hard-to-find bugs in large programs
        capitalizing method names
        prefixing data attribute names with a small unique string (perhaps just an underscore)
        verbs for methods
        nouns for data attributes

Data attributes may be referenced by
    - methods
    - ordinary users (“clients”) of an object
    
classes are not usable to implement pure abstract data types
nothing in Python makes it possible to enforce data hiding


Clients should use data attributes with care

first argument of a method is called self
nothing more than a convention
name self has absolutely no special meaning to Python
by not following the convention your code may be less readable to other Python programmers
also conceivable that a class browser program might be written that relies upon such a convention

Any function object that is a class attribute defines a method for instances of that class
not necessary that the function definition is textually enclosed in the class definition
assigning a function object to a local variable in the class is also ok


# Function defined outside the class
def f1(self, x, y):
    return min(x, x+y)

class C:
    f = f1

    def g(self):
        return 'hello world'

    h = g


f, g and h are all attributes of class C refer to function objects
consequently all methods of instances of C

Methods may call other methods by using method attributes of the self argument

class Bag:
    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)

Methods may reference global names in the same way as ordinary functions
global scope associated with a method is the module containing its definition
    A class is never used as a global scope
    While one rarely encounters a good reason for using global data in a method
    functions and modules imported into the global scope can be used by
        methods
        functions and classes defined in it
    Usually, the class containing the method is itself defined in this global scope
    good reasons why a method would want to reference its own class (inheritance)

Each value is an object
    therefore has a class (also called its type)
    stored as object.__class__


# Inheritance

The name BaseClassName must be defined in a scope containing the derived class definition. In place of a base class name, other arbitrary expressions are also allowed

class DerivedClassName(BaseClassName):


when the base class is defined in another module:
class DerivedClassName(modname.BaseClassName):


Method references are resolved
    corresponding class attribute is searched
    descending down the chain of base classes if necessary
    method reference is valid if this yields a function object

Derived classes may override methods of their base classes
    Because methods have no special privileges when calling other methods of the same object
    a method of a base class that calls another method defined in the same base class may end up calling a method of a derived class that overrides it
    all methods in Python are effectively virtual

An overriding method in a derived class may
    extend
    rather than simply replace the base class method of the same name

simple way to call the base class method directly
    BaseClassName.methodname(self, arguments)
        only works if the base class is accessible as BaseClassName in the global scope

Python has two built-in functions that work with inheritance:
    - isinstance()
        to check an instance’s type
            isinstance(obj, int) will be True
                only if obj.__class__ is
                    int
                    some class derived from int
    - issubclass()
        to check class inheritance
            issubclass(bool, int) is True
                bool is a subclass of int
            issubclass(float, int) is False
                float is not a subclass of int


# Multiple Inheritance
Python supports a form of multiple inheritance as well
class definition with multiple base classes looks

class DerivedClassName( Base1, Base2, Base3 ):
    <statement-1>
    .
    .
    .
    <statement-N>

search for attributes inherited from a parent class
    - depth-first
    - left-to-right
    - not searching twice in the same class where there is an overlap in the hierarchy
    
if an attribute is not found in DerivedClassName
    searched for in Base1
        (recursively) in the base classes of Base1
    if not found there, it was searched for in Base2, and so on


slightly more complex than that
method resolution order
    changes dynamically to support cooperative calls to super()
        approach is known in some other multiple-inheritance languages
            call-next-method
                more powerful than
                    super call
                        found in single-inheritance languages


Dynamic ordering is necessary
    because all cases of multiple inheritance
        exhibit one or more diamond relationships
            where at least one of the parent classes can be accessed through multiple paths from the bottommost class

all classes inherit from object, so any case of multiple inheritance provides more than one path to reach object

To keep the base classes from being accessed more than once
    dynamic algorithm linearizes the search order
        in a way that preserves the left-to-right ordering specified in each class
            that calls each parent only once
            monotonic
                meaning that a class can be subclassed without affecting the precedence order of its parents

Taken together, these properties make it possible to design reliable and extensible classes with multiple inheritance


# Private Variables

“Private” instance variables that cannot be accessed except from inside an object don’t exist in Python

convention that is followed by most Python code
    name prefixed with an underscore (e.g. _spam) should be treated as a non-public part of the API (whether it is a function, a method or a data member)
    considered an implementation detail and subject to change without notice
    
## name mangling

Any identifier of the form __spam (at least two leading underscores, at most one trailing underscore)
    is textually replaced with _classname__spam
        where classname is the current class name with leading underscore(s) stripped
            This mangling is done without regard to the syntactic position of the identifier
                as long as it occurs within the definition of a class

Name mangling is helpful
    for letting subclasses override methods without breaking intraclass method calls

class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)

The above example would work even if MappingSubclass were to introduce a __update identifier
    since it is replaced with
        _Mapping__update in the Mapping class
        _MappingSubclass__update in the MappingSubclass class

mangling rules are designed mostly to avoid accidents
possible to access or modify a variable that is considered private
useful in special circumstances, such as in the debugger


code passed to exec() or eval() does not consider the classname of the invoking class to be the current class
similar to the effect of the global statement
    effect of which is likewise restricted to code that is byte-compiled together
same restriction applies to
    getattr()
    setattr()
    delattr()
    __dict__ directly


# Odds and Ends

Instance method objects have attributes

m.__self__ is the instance object with the method m()
m.__func__ is the function object corresponding to the method m()


# Iterators
iter()
    function returns an iterator object
        that defines the method __next__()
            which accesses elements in the container one at a time
            When there are no more elements, __next__() raises a StopIteration exception
                which tells the for loop to terminate

call the __next__() method using the next() built-in function; this example shows how it all works:

s = 'abc'
it = iter(s)
it      ->      <iterator object at 0x00A1DB50>
next(it)        ->      'a'
next(it)        ->      'b'
next(it)        ->      'c'
next(it)        ->      StopIteration


to add iterator behavior to your classes
    Define an __iter__() method which returns an object with a __next__() method
    If the class defines __next__(), then __iter__() can just return self


class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]


# Generators

simple and powerful tool for creating iterators
written like regular functions
    use the yield statement whenever they want to return data
    Each time next() is called on it
        generator resumes where it left off
            it remembers all the data values
            which statement was last executed

def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

Anything that can be done with generators can also be done with class-based iterators

generators are compact because
    __iter__() and __next__() methods are created automatically


local variables and execution state are automatically saved between calls
    make function easier to write
        much more clear than an approach using instance variables like self.index and self.data
        

easy to create iterators with no more effort than writing a regular function.
    - automatic method creation
    - saving program state
    - when generators terminate, they automatically raise StopIteration
\

# Generator Expressions

syntax similar to list comprehensions
parentheses instead of square brackets
for situations where the generator is used right away by an enclosing function

more compact but less versatile than full generator definitions
tend to be more memory friendly than equivalent list comprehensions


sum(i*i for i in range(10))     ->      285


xvec = [10, 20, 30]
yvec = [7, 5, 3]
sum(x*y for x,y in zip(xvec, yvec))     ->      260


from math import pi, sin
sine_table = {x: sin(x*pi/180) for x in range(0, 91)}


unique_words = set(word  for line in page  for word in line.split())


valedictorian = max( (student.gpa, student.name) for student in graduates )


data = 'golf'
list( data[i] for i in range( len(data) - 1, -1, -1 ) )
['f', 'l', 'o', 'g']
