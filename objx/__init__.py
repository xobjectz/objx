# This file is placed in the Public Domain,
#
#


""" objects library


OBJX provides an objx namespace that allows for easy json save//load
to/from disk of objects. It provides an "clean namespace" Object class
that only has dunder methods, so the namespace is not cluttered with
method names. This makes storing and reading to/from json possible.

>>> from objx import Object, dumps, loads
>>> o = Object()
>>> o.a = "b"
>>> txt = dumps(o)
>>> oo = Object()
>>> loads(oo, txt)
>>> oo
{"a": "b"}

"""


from .default import Default
from .objects import *

def __dir__():
    return (
        'Object',
        'construct',
        'dump',
        'dumps',
        'edit',
        'fmt',
        'fqn',
        'items',
        'keys',
        'load',
        'loads',
        'update',
        'values',
    )


__all__ = __dir__()
