reprlib module
    provides a version of repr()
    customized for abbreviated displays of large or deeply nested containers
    
import reprlib
reprlib.repr(set('supercalifragilisticexpialidocious'))
"{'a', 'c', 'd', 'e', 'f', 'g', ...}"


pprint module
    offers more sophisticated control over printing both built-in and user defined objects
    in readable way by the interpreter
    When the result is longer than one line
        “pretty printer” adds line breaks
        indentation to more clearly reveal data structure
        
import pprint
t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
    'yellow'], 'blue']]]

pprint.pprint(t, width=30)
[[[['black', 'cyan'],
   'white',
   ['green', 'red']],
  [['magenta', 'yellow'],
   'blue']]]


textwrap module
    formats paragraphs of text to fit a given screen width
    
import textwrap
doc = """The wrap() method is just like fill() except that it returns
a list of strings instead of one big string with newlines to separate
the wrapped lines."""

print(textwrap.fill(doc, width=40))



wrap() method
    like fill()
    except returns a list of strings
    instead of one big string with newlines
    to separate the wrapped lines

locale module
    accesses a database of culture specific data formats
    grouping attribute of locale’s format function
        provides a direct way of formatting numbers with group separators
        
import locale
locale.setlocale(locale.LC_ALL, 'English_United States.1252')
'English_United States.1252'
conv = locale.localeconv()          # get a mapping of conventions
x = 1234567.8
locale.format("%d", x, grouping=True)
'1,234,567'
locale.format_string("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], x), grouping=True)
'$1,234,567.80'
