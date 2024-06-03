# This file is placed in the Public Domain.


"broker"


import inspect


from .object import Object, fqn, keys, search


rpr = object.__repr__


class Broker:

    "Broker"

    def __init__(self):
        self.objs = Object()

    def add(self, obj):
        "add an object to the broker."
        setattr(self.objs, ident(obj), obj)

    def find(self, selector=None, index=None, deleted=False):
        "find objects stored in the broker."
        if selector is None:
            selector = {}
        for key, obj in items(self.objs):
            if not deleted and '__deleted__' in dir(obj):
                continue
            if selector and not search(obj, selector):
                continue
            nrs += 1
            if index is not None and nrs != int(index):
                continue
            yield (key, obj)

    def last(selector=None):
        "return last object saved."
        if selector is None:
            selector = {}
        result = sorted(self.find(selector), key=fntime(x[0]))
        res = None
        if result:
            inp = result[-1]
            update(obj, inp[-1])
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


class Whitelist(Object): # pylint: disable=R0903

    "Whitelist"

    classes = Object()


def scancls(mod) -> None:
    "scan module for classes."
    for key, clz in inspect.getmembers(mod, inspect.isclass):
        if key.startswith("cb"):
            continue
        if not issubclass(clz, Object):
            continue
        whitelist(clz)


def whitelist(clz):
    "add class to whitelist."
    name = str(clz).split()[1][1:-2]
    setattr(Whitelist.classes, name, clz)


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for named in Whitelist.classes:
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
