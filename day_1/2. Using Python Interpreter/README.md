# Invoking the Interpreter
python

python3.7

which python


python m.py
python test
python test.zip

Both folder and zip should have a __main__.py


exit interpreter by adding a EOF ( End of File ) :

ctrl+d -> unix

ctrtl+z -> windows

quit()

run inline python code from shell

python -c 'a="Hello World!";print(a)'

enter interactive mode after executing a python script

python -i ex.py

useful to inspect global variables in the program

run a script as a module

python -m ex .venv


## Argument Passing
import sys
sys.argv[0]

( - ) means stdin as a scriptfile
argv[0] set to '-'
python -
import sys
sys.argv[0]

-m
argv[0] set to FULL PATH of the module
python -m m

-c
argv[0] set to '-c'
python -c 'import sys;print( sys.argv );print( sys.argv[0] )'


# The Interpreter and Its Environment
## Source Code Encoding

default utf-8

standard library only uses ASCII characters for identifiers, a convention that any portable code should follow

editor uses a font that supports all characters


special comment line should be added as the first line of the file
# -*- coding: encoding -*-

Windows-1252 encoding
# -*- coding: cp1252 -*-


One exception to the first line rule is when the source code starts with a UNIX “shebang” line
added as the second line of the file

#!/usr/bin/env python3
# -*- coding: cp1252 -*-

“shebang” line
#!/usr/bin/env python3
