# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E0402


"available modules"


import os


from . import __dir__


def mod(event):
    res = []
    if os.path.exists("mods"):
        import mods
        res.extend(mods.__dir__())
    res.extend(__dir__())
    event.reply(",".join(sorted(res)))
