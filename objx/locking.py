# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"locks module"


import _thread


disklock   = _thread.allocate_lock()


"interfacce"


def __dir__():
    return (
        'disklock',
    )


__all__ = __dir__()
