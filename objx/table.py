# This file is placed in the Public Domain.


"table"


import importlib


from .object import Object


class Table:

    mods = Object()


def load(mname):
    setattr(Table.mods, mname, importlib.import_module(mname))
    

def ondemand(mname):
    mod = getattr(Table.mods, mname, None)
    if not mod:
        load(mname)
        mod = getattr(Table.mods, mname, None)
    return mod


def __dir__():
    return (
        'Table',
        'load',
        'ondemend'
    )
