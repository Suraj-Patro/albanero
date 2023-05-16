# this is the first comment
spam = 1  # and this is the second comment
          # ... and now a third!
text = "# This is not a comment because it's inside quotes."


2 + 2
50 - 5*6
(50 - 5*6) / 4
8 / 5

8 // 5
8 % 5
5 ** 2


last printed expression is assigned to the variable _
a = 10
a
a + _


In the interactive interpreter
the output string is enclosed in quotes and special characters are escaped with backslashes
While this might sometimes look different from the input (the enclosing quotes could change), the two strings are equivalent

string is enclosed in double quotes if the string contains a single quote and no double quotes
otherwise it is enclosed in single quotes

print() function produces a more readable output
by omitting the enclosing quotes
by printing escaped and special characters

'"Isn\'t," they said.'
"\"Yes,\" they said."

to avoid \ be interpreted as escape sequence, use raw strings
s = r'D:\path\to\file'


multiple lines String literals
"""..."""
'''...'''

End of lines are automatically included in the string
possible to prevent this by adding a \ at the end of the line

print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")

Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to


string concat
-------------
break long strings

'Py' 'thon' -> python

('Put several strings within parentheses '
...         'to have them joined together.')
        'Put several strings within parentheses to have them joined together.'


only works with two literals though, not with variables or expressions
to concatenate variables or a variable and a literal, use +
+
---
"hgdsil" + "dhsgi;bip"
"nshgile" + 9
"hydgloyls" + True

String Repeatation *
--------------------
"nho" * 3 -> "nhonhonho"

3 * 'un' + 'ium'
'unununium'


Strings
-------

Indexing
--------
s[1]
accessing index out of range is not allowed

Slicing
-------
return a new string

s[0:5]
s[ :5]
s[0: ]
s[ : ]

slicing index out of range is not allowed

Strings are immutable
so no assignment possible

s[0] = 1
s[0:3] = 'jgu'
wouldn't work

len()


Lists
-----
can have elements of same/different type
mutable

indexing
slicing -> return a new list ( shallow copy )

concatenation
[1,2] + [3,4] -> [1,2,3,4]

.append()

Assignment to Slice
-------------------
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']       ->      ['a', 'b', 'c', 'd', 'e', 'f', 'g']
letters[2:5] = ['C', 'D', 'E']      ->      ['a', 'b', 'C', 'D', 'E', 'f', 'g']
letters[2:5] = []       ->      ['a', 'b', 'f', 'g']
letters[:] = []     ->      []

len()
nested lists


Fibonancci Series
-----------------
a, b = 0, 1
while a < 1000:
    print(a, end=',')
    a, b = b, a+b

