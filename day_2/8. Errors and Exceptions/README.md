# Syntax Errors
parsing errors

# Exceptions
Even if syntactically correct
    not unconditionally fatal

A class in an except clause is compatible with an exception if it is the same class or a base class thereof (but not the other way around — an except clause listing a derived class is not compatible with a base class). For example, the following code will print B, C, D in that order:

class B(Exception):
    pass

class C(B):
    pass

class D(C):
    pass

for cls in [B, C, D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")

Note that if the except clauses were reversed (with except B first), it would have printed B, B, B — the first matching except clause is triggered.


else clause
-----------
optional
must follow all except clauses
executed if try doesn't raise and exception


try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error:', err)


Raising Exceptoins
------------------
raise NameError('HiThere')
NameError: HiThere

raise ValueError  # shorthand for 'raise ValueError()'

try:
    raise NameError('HiThere')
except NameError:
    print('An exception flew by!')
    raise


finally
-------
define clean-up actions
must be executed under all circumstances

if an exception occurs during execution of the try clause, the exception may be handled by an except clause. If the exception is not handled by an except clause, the exception is re-raised after the finally clause has been executed.

An exception could occur during execution of an except or else clause. Again, the exception is re-raised after the finally clause has been executed.

If the try statement reaches a break, continue or return statement, the finally clause will execute just prior to the break, continue or return statement’s execution.

If a finally clause includes a return statement, the returned value will be the one from the finally clause’s return statement, not the value from the try clause’s return statement.





try
except
else
finally


context managers
----------------
with

user defined context managers
    - by functions
    - by class
        - __init__()
        - __enter__()
        - __exit__()

===========================================================
with A() as a, B() as b:
    suite

-----------------------------------------------------------

with A() as a:
    with B() as b:
        suite

===========================================================
