# This file is placed in the Public Domain.
#
# pylint: disable=W0401,W0614


"objects"


from .object  import *
from .object  import __dir__ as __odir__
from .decoder import read
from .default import Default
from .encoder import write
from .config  import Config
from .utils   import *


def __dir__():
    return (
        'Config',
        'Default',
        'parse',
        'read',
        'strip',
        'write'
    ) + __odir__()


__all__ = __dir__()
