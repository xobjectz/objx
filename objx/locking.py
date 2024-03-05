# This file is placed in the Public Domain.
#
#


"lock module"


import _thread


decodelock = _thread.allocate_lock()
encodelock = _thread.allocate_lock()
disklock   = _thread.allocate_lock()
hooklock   = _thread.allocate_lock()
pathlock   = _thread.allocate_lock()
