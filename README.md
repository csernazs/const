
const
=====

_Define constants and enums for Python, the easy way._

Examples
--------

Here's the idea:

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

Permitted values
----------------

There are cases when you want to check whether the value the function
received is one of the constants defined previously in the code. Such code
usually look like:

```python
from const import const

class A:
    CONST_A, CONST_B, CONST_C = const("SAME")
    PERMITTED_CONSTANTS = {CONST_A, CONST_B, CONST_C}

    def foobar(self, param1)
        if param1 not in self.PERMITTED_CONSTANTS:
            raise ValueError("Invalid parameter specified: %r" % param1)

```


In case you need the complete list to fill the permitted values variable,
you can speciy the _prefix_ parameter as _PERMITTED_, so it will specify all
the permitted values to the first valiable.

With this, the above code would look like:

```python
from const import const, PERMITTED
class A:
    PERMITTED_CONSTANTS, CONST_A, CONST_B, CONST_C = const("SAME", PERMITTED)

    def foobar(self, param1)
        if param1 not in self.PERMITTED_CONSTANTS:
            raise ValueError("Invalid parameter specified: %r" % param1)

```

Here, the `PERMITTED_CONSTANTS` will be a set of the three constants, so the
lookup with the `in` operator will be faster (compared to `list` or `tuple`).



Restrictions
------------

This code relies heavily on stack frames. The code it uses examines the
parent frame.  This might not work for each and every python interpreter.
This library is python2 only, and works with pypy as well.

Local variables do not have their names so it's not possible to use
`const()` with local variables.


