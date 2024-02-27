# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"persistence"


import datetime
import os
import pathlib
import time
import _thread


from .objects import Default, Object, dump, fqn, load, search, update


"defines"


def __dir__():
    return (
        'Persist',
        'Workdir',
        'cdir',
        'fetch',
        'find',
        'fntime',
        'last',
        'long',
        'ident',
        'read',
        'skel',
        'store',
        'strip',
        'sync',
        'types',
        'whitelist',
        'write'
    )


__all__ = __dir__()


"workdir"


class Workdir(Object):

    wd = ""


def skel():
    cdir(os.path.join(Workdir.wd, "store", ""))


def store(pth=""):
    return os.path.join(Workdir.wd, "store", pth)


def types():
    return os.listdir(store())


"persist"


lock = _thread.allocate_lock()


class Persist(Object):

    classes = Object()


def whitelist(clz):
    if not clz:
        return
    name = str(clz).split()[1][1:-2]
    setattr(Persist.classes, name, clz)


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for named in Persist.classes:
        if split in named.split(".")[-1].lower():
            res = named
            break
    if "." not in res:
        for fnm in types():
            claz = fnm.split(".")[-1]
            if fnm == claz.lower():
                res = fnm
    return res


def ident(obj):
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def fetch(obj, pth):
    pth2 = store(pth)
    read(obj, pth2)
    return strip(pth)


def read(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def sync(obj, pth=None):
    if pth is None:
        pth = ident(obj)
    pth2 = store(pth)
    write(obj, pth2)
    return pth


def write(obj, pth):
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


"locate"


def find(mtc, selector=None, index=None, deleted=False):
    clz = long(mtc)
    nr = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if not deleted and '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nr += 1 
        if index is not None and nr != int(index):
            continue
        yield (fnm, obj)


def fns(mtc=""):
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    for fll in fls:
                        yield strip(os.path.join(ddd, fll))


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]


"utilities"


def cdir(pth) -> None:
    if os.path.exists(pth):
        return
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def strip(pth, nmr=3):
    return os.sep.join(pth.split(os.sep)[-nmr:])


def fntime(daystr):
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
