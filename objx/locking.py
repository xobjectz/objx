# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"locks module"


import _thread


def __dir__():
    return (
        'disklock',
    )


disklock   = _thread.allocate_lock()
