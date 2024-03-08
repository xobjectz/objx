# This file is placed in the Public Domain.
#
#


"locks module"


import _thread


disklock   = _thread.allocate_lock()
