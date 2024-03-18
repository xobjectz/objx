# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"locks"


import _thread


disklock = _thread.allocate_lock()
