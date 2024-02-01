# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"preimport"


import sys


def getmain(name):
    return getattr(sys.modules["__main__"], name, None)



from . import cmd, err, fnd, irc, log, mod, mre, pwd, rss, tdo, thr, tmr
from . import rst, udp



def __dir__():
    return (
        'cmd',
        'err',
        'fnd',
        'getmain',
        'irc',
        'log',
        'mod',
        'mre',
        'pwd',
        'rss',
        'tdo',
        'thr',
        'tmr',
        'req',
        'rst',
        'udp'
    )


__all__ = __dir__()
