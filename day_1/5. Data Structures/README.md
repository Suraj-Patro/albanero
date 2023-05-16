Lists
-----

list.append(x)
    a[len(a):] = [x].
    Add an item to the end of the list

list.extend(iterable)
    a[len(a):] = iterable
    Extend the list by appending all the items from the iterable

list.insert(i, x)
    Insert an item at a given position
    first argument is the index of the element before which to insert
        a.insert(0, x) inserts at the front of the list
        a.insert(len(a), x) a.append(x).

list.remove(x)
    Remove the first item from the list whose value is equal to x
    raises a ValueError if there is no such item

list.pop([i])
    Remove the item at the given position in the list
    return it
    If no index is specified
        removes
        returns the last item in the list

list.clear()
    del a[:]
    Remove all items from the list

list.index(x[, start[, end]])
    Return zero-based index in the list of the first item whose value is equal to x
    Raises a ValueError if there is no such item
    
    optional arguments start and end are interpreted as slice notation
    used to limit the search to a particular subsequence of the list
    returned index is computed relative to the beginning of the full sequence rather than the start argument.

list.count(x)
    Return the number of times x appears in the list

list.sort(key=None, reverse=False)
    Sort the items of the list in place

list.reverse()
    Reverse the elements of the list in place

list.copy()
    a[:]
    Return a shallow copy of the list


## Lists as Stacks
stack.append(7)
stack.pop()


## Using Lists as Queues
lists are not efficient for FIFO
appends and pops from the end of list are fast
inserts or pops from the beginning of a list is slow
    because all of the other elements have to be shifted by one


from collections import deque
queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry arrives
queue.append("Graham")          # Graham arrives
queue.popleft()                 # The first to arrive now leaves
'Eric'
queue.popleft()                 # The second to arrive now leaves
'John'
queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])


##  List Comprehensions
squares = []
for x in range(10):
    squares.append(x**2)
squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

------------------------------------

squares = list(map(lambda x: x**2, range(10)))

------------------------------------

squares = [x**2 for x in range(10)]

------------------------------------

=====================================================================

[(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]

------------------------------------

combs = []
for x in [1,2,3]:
    for y in [3,1,4]:
        if x != y:
            combs.append((x, y))

=====================================================================

## Nested list comprehension

[ [ row[ i ] for row in matrix ] for i in range(4)]


zip()
-----

matrix = [
   [1, 2, 3, 4],
   [5, 6, 7, 8],
   [9, 10, 11, 12],
]


list( zip( *matrix ) )

[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]


del()
-----

del a[0]
del a[2:4]
del a[:]


## tuples and Sequences
immutable
accessed by:
    - uppacking
    - indexing

a = (,)
a = 1,


swap
a, b = b, a


Set
---
set()
{1}

set comprehension
{x for x in 'abracadabra' if x not in 'abc'}


## Dicts
{}
{1:2}

dict( [ ('sape', 4139), ('guido', 4127), ('jack', 4098) ] )

{'sape': 4139, 'guido': 4127, 'jack': 4098}

tel['guido'] = 4127
del tel['sape']

dict(sape=4139, guido=4127, jack=4098)


dict comprehension
{x: x**2 for x in (2, 4, 6)}


## Looping Techniques
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)

gallahad the pure
robin the brave


for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)

0 tic
1 tac
2 toe


questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
   print('What is your {0}?  It is {1}.'.format(q, a))

What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.



sorted()
--------
new sorted object
leave source unaltered


## Conditions
and
or

short circuiting

comparision among different obj are lexicographically
