if statemtns
------------

x = 42

if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')


for Statements
--------------
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

range()
len()

a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])


while statements
----------------
a = 1
while a < 10:
    print( a )


enumerate()
-----------
seasons = ['Spring', 'Summer', 'Fall', 'Winter']

list( enumerate(seasons) )
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

list( enumerate(seasons, start=1) )
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

same as
-------
def enumerate(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1

===============================================================================
eval()
------
dynamically evaluate arbitrary Python expressions from
    - string-based
    - compiled-code-based ( using compile() )
input


string
    - parses expression
    - compiles it to bytecode
    - evaluates it as a Python expression
    
compiled code object
    - just the evaluation step
        quite convenient if you call eval() several times with the same input
        i.e. closer to Memoization


eval(expression[, globals[, locals]])


eval("2 ** 8")      ->      256
eval("1024 + 1024")     ->      2048
eval("sum([8, 16, 32])")        ->      56

x = 100
eval("x * 2")       ->      200


code = compile("5 + 4", "<string>", "eval")
eval(code)


compile( source, filename, mode )

source
------
source code that you want to compile
accepts normal strings, byte strings, and AST objects

filename
--------
file from which the code was read
use a string-based input -> "<string>"

mode
----
specifies which kind of compiled code you want to get
process the compiled code with eval(), then this argument should be set to "eval".



You can also use exec() to dynamically execute Python code
main difference between eval() and exec()
    - eval() can only execute or evaluate expressions
    - exec() can execute any piece of Python code

exec()

===============================================================================

### break and continue Statements, and else Clauses on Loops

break statement
breaks out of the innermost enclosing for or while loop

Loop statements may have an else clause, executed
    - when the loop terminates through exhaustion of the list (with for)
    - when the condition becomes false (with while)
    - not when the loop is terminated by a break statement


for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')

output
------
2 is a prime number
3 is a prime number
4 equals 2 * 2
5 is a prime number
6 equals 2 * 3
7 is a prime number
8 equals 2 * 4
9 equals 3 * 3


When used with a loop
else clause has more in common with the else clause of a try statement
than it does that of if statements

try statement’s else clause runs when no exception occurs
loop’s else clause runs when no break occurs


continue
pass

while True:
    pass

class MyEmptyClass:
    pass

def func:
    pass


functions
---------
def fib(n):    # write Fibonacci series up to n
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

fib( 2000 )

def -> introduces funtions definition
followed by function name


symbol table

execution of a function creates a local symbol table
all variable assignments in a function store the value in the local symbol table
variable references look in:
    - local symbol table
    - local symbol tables of enclosing functions
    - global symbol table
    - table of built-in names

global variables and variables of enclosing functions cannot be directly assigned a value within a function unless:
    - for global variables, named in a global statement
    - variables of enclosing functions, named in a nonlocal statement

although they may be referenced


A function definition introduces the function name in the current symbol table
value of the function name has a type that is recognized by the interpreter as a user-defined function
This value can be assigned to another name which can then also be used as a function
    serves as a general renaming mechanism

return
------
return statement returns with a value from a function
return without an expression argument returns None
Falling off the end of a function also returns None

None
----
returned by functions with no return statement


## Default Argument Values

def func( a, b = "two", c = "three", d = "four" ):
    print(a, b, c, d)

func( 10 )
func( 10, "dirg" )
func( 10, "dirg", "hoguspdu" )
func( 10, "dirg", "hoguspdu", "njohguoeur" )


- default values are evaluated at the point of function definition in the defining scope

i = 5
def f(arg=i):
    print(arg)
i = 6
f() -> 5

default value is evaluated only once
makes a difference when the default is a mutable object such as a list, dictionary, or instances of most classes


ex: function accumulates the arguments passed to it on subsequent calls

def f(a, L=[]):
    L.append(a)
    return L

print(f(1))     ->      [1]
print(f(2))     ->      [1, 2]
print(f(3))     ->      [1, 2, 3]


default not shared between subsequent calls

def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L


## Keyword Argument
Functions can be called using keyword arguments
    of the form kwarg=value

def func( a, b = "two", c = "three", d = "four" ):
    print(a, b, c, d)

func( 10 )
func( 10, b = "dirg" )
func( 10, c = "dirg", d = "hoguspdu" )
func( 10, d = "dirg", c = "hoguspdu", b = "njohguoeur" )


keyword arguments must follow positional arguments
All the keyword arguments passed must match one of the arguments accepted by the function
    - order is not important
    - also includes non-optional arguments
No argument may receive a value more than once


## Arbitrary Argument Lists

def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])


cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")

output
======
-- Do you have any Limburger ?
-- I'm sorry, we're all out of Limburger
It's very runny, sir.
It's really very, VERY runny, sir.
----------------------------------------
shopkeeper : Michael Palin
client : John Cleese
sketch : Cheese Shop Sketch


order in which the keyword arguments are invoked
match the order in which they were provided in the function call


## Unpacking Argument Lists

reverse situation occurs when the arguments are already in a list or tuple
unpacked for a function call requiring separate positional arguments

args = [3, 6]
list( range( *args ) )      ->      [3, 4, 5]


def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)     ->      -- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !



*args, **kwargs
---------------
when used in function defintion
    pack variable arguments into 1 variable *args
when used in function call
    unpack 1 variable into multiple values


## Lambda Expressions
Small anonymous functions can be created with the lambda keyword
used wherever function objects are required
syntactically restricted to a single expression
Semantically, they are just syntactic sugar for a normal function definition
Like nested function definitions, lambda functions can reference variables from the containing scope

used to:
    - return a function from a function

def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)
f(0)        ->      42
f(1)        ->      43


    - pass a function to a function

pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort( key = lambda pair: pair[1] )        ->      [(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]


## Documentation Strings

The first line should always be a short, concise summary of the object’s purpose
should not explicitly state the object’s name or type
should begin with a capital letter and end with a period


If there are more lines in the documentation string
    second line should be blank
    visually separating the summary from the rest of the description
        following lines should be one or more paragraphs describing the object’s calling conventions, its side effects, etc.

Python parser does not strip indentation from multi-line string literals in Python
tools to process documentation have to strip indentation if desired
    first non-blank line after the first line of the string determines the amount of indentation for the entire documentation string
        We can’t use the first line
            generally adjacent to the string’s opening quotes so its indentation is not apparent in the string literal
    Whitespace “equivalent” to this indentation is then stripped from the start of all lines of the string
    Lines that are indented less should not occur, but if they occur all their leading whitespace should be stripped
    Equivalence of whitespace should be tested after expansion of tabs (to 8 spaces, normally).


def my_function():
    """Do nothing, but document it.

    No, really, it doesn't do anything.
    """
    pass

print(my_function.__doc__)
Do nothing, but document it.

    No, really, it doesn't do anything.


## Function Annotations
completely optional metadata information
about the types used by user-defined functions


def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs

f('spam')       ->
Annotations: {'ham': <class 'str'>, 'return': <class 'str'>, 'eggs': <class 'str'>}
Arguments: spam eggs
'spam and eggs'

