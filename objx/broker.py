# This file is placed in the Public Domain.


"broker"


import datetime
import inspect
import os


from .object import Object, fqn, items, keys, search, update


rpr = object.__repr__


class Broker:

    "Broker"

    def __init__(self):
        self.objs = Object()

    def add(self, obj):
        "add an object to the broker."
        setattr(self.objs, ident(obj), obj)

    def all(self):
        "return all objects."
        return self.objs

    def find(self, selector=None, index=None, deleted=False):
        "find objects stored in the broker."
        if selector is None:
            selector = {}
        nrs = 0
        for key, obj in items(self.objs):
            if not deleted and '__deleted__' in dir(obj):
                continue
            if selector and not search(obj, selector):
                continue
            nrs += 1
            if index is not None and nrs != int(index):
                continue
            yield (key, obj)

    def last(self, selector=None):
        "return last object saved."
        if selector is None:
            selector = {}
        result = sorted(self.find(selector))
        res = None
        if result:
            inp = result[-1]
            res = inp[0]
        return res

    def first(self):
        "return first object."
        for key in keys(self.objs):
            return getattr(self.objs, key)

    def get(self, orig):
        "return object by origin (repr)"
        return getattr(self.objs, orig, None)

    def remove(self, obj):
        "remove object from broker"
        delattr(self.objs, rpr(obj))


def fntime(daystr):
    "convert file name to it's saved time."
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def ident(obj):
    "return an id for an object."
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def __dir__():
    return (
        'Broker',
    )
