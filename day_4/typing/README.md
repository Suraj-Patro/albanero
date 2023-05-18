typing — Support for type hints


Python runtime does not enforce function and variable type annotations
used by third party tools such as type checkers, IDEs, linters, etc

provides runtime support for type hints

most fundamental support consists of the types
    Any
    Union
    Callable
    TypeVar
    Generic


The function below takes and returns a string and is annotated as follows:

def greeting(name: str) -> str:
    return 'Hello ' + name


Subtypes are accepted as arguments


# Type aliases
defined by assigning the type to the alias

Vector
list[float]
treated as interchangeable synonyms

Vector = list[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


# passes type checking; a list of floats qualifies as a Vector.
new_vector = scale(2.0, [1.0, -4.2, 5.4])


Type aliases are useful for simplifying complex type signatures



from collections.abc import Sequence

ConnectionOptions = dict[str, str]
Address = tuple[str, int]
Server = tuple[Address, ConnectionOptions]

def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    ...


# The static type checker will treat the previous type signature as
# being exactly equivalent to this one.
def broadcast_message(
        message: str,
        servers: Sequence[tuple[tuple[str, int], dict[str, str]]]) -> None:
    ...


None
    type hint
    special case
    replaced by type(None)


from typing import NewType

UserId = NewType('UserId', int)

ProUserId = NewType('ProUserId', UserId)


Any
    special kind of type
    static type checker will treat every type as being compatible with Any
    Any as being compatible with every type
    
    possible to perform any operation or method call on a value of type Any
    assign it to any variable


from typing import Any

a: Any = None
a = []          # OK
a = 2           # OK

s: str = ''
s = a           # OK

def foo(item: Any) -> int:
    # Passes type checking; 'item' could be any type,
    # and that type might have a 'bar' method
    item.bar()
    ...


no type checking is performed
    when assigning a value of type Any to a more precise type
