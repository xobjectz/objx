NAME

::

    OBJX - objects library


SYNOPSIS

::

    >>> from objx import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> loads(dumps(o))
    <objx.objects.Object object at 0x7ff59c9c9a50>
    >>> str(o)
    "{'a': 'b'}"


DESCRIPTION

::

    OBJX contains all the python3 code to program objects in a functional
    way. It provides a base Object class that has only dunder methods, all
    methods are factored out into functions with the objects as the first
    argument. It is called Object Programming (OP), OOP without the
    oriented.

    OBJX  allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.

    OBJX is Public Domain.


AUTHOR

::

    xobjectz <objx@proton.me>


COPYRIGHT

::

    OBJX is Public Domain.
