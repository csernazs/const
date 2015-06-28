
const
=====

_Define constants and enums for Python, the easy way_

Examples
--------


While enums are available since python 3.4, they still need to be specified in this way:

```python
from enum import Enum
class Color(Enum):
    red = 1
    green = 2
    blue = 3
```

Having a value assigned to each constant seems boring for me, so here is my idea:

```python
from const import const

class Color:
    COLOR_RED, COLOR_GREEN, COLOR_BLUE = const("DASH")


print Color.COLOR_RED   # will print 'color-red'
print Color.COLOR_GREEN # will print 'color-green'
print Color.COLOR_BLUE  # will print 'color-blue'

```

Details
-------

How does `const()` work? It looks at the caller's frame, it finds the
_UNPACK_SEQUENCE_ command, then it finds the names of the variables on the
left-hand side, then it returns a list which has the same amount of
elements with the strings returned by the result of naming.

The parameter of the `const()` specifies how the naming should be done for
the variables:

*   DASH makes the string lower case and converts each underscore char to dash
*   NUMBER0 returns numbers in sequence, starting with 0
*   NUMBER1 returns numbers in sequence, starting with 1
*   SAME does nothing with the variable name (returns it as a string)

Custom namings
--------------

Additional naming styles can be added by using the `@naming` decorator:

```python
from const import naming, const

@naming("LOWERCASE")
def lowercase_naming(idx, value): # receives the index of the variable and its name
    return value.lower() # returns the value which will be stored


A, B, C = const("LOWERCASE")
print A # will print 'a'
print B # will print 'b'
print C # will print 'c'
```

And also, it can accept any callable which takes these two parameters (so if
you prefer, you can give the function reference to it).


Restrictions
------------

This code relies heavily on stack frames. The code it uses examines the
parent frame.  This might not work for each and every python interpreter.

Llocal variables do not have their names so it's not possible to use
`const()` with local variables.


