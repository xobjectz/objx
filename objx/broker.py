# This file is placed in the Public Domain.


"broker"


import datetime
import os
import time


from .object import Object, fqn, items, keys, search


rpr = object.__repr__


class Broker:

    "Broker"

    fqn = []

    def __init__(self):
        self.objs = Object()

    def add(self, obj):
        "add an object to the broker."
        setattr(self.objs, ident(obj), obj)
        name = fqn(obj)
        Broker.fqn.append(name)

    def all(self, fqn):
        "return all objects."
        if fqn:
            names = [x for x in keys(self.objs) if fqn in x]
            for name in names:
                yield name, getattr(self.objs, name)
            return
        return self.objs

    def find(self, selector=None, index=None, deleted=False, match=None):
        "find objects stored in the broker."
        if selector is None:
            selector = {}
        nrs = 0
        for key, obj in items(self.objs):
            if match and match not in key:
                continue
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


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for named in keys(broker.objs):
        if split in named.split(".")[-1].lower():
            res = named
            break
    if "." not in res:
        for fnm in lsstore():
            claz = fnm.split(".")[-1]
            if fnm == claz.lower():
                res = fnm
    return res



def __dir__():
    return (
        'Broker',
    )
