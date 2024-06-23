# This file is placed in the Public Domain.


"auto import modules"


import importlib
import os


path = os.path.dirname(__file__)
modname = path.split(os.sep)[-1]
mods = []


for fnm in os.listdir(path):
    if fnm.startswith("__"):
        continue
    fnmm = fnm[:-3]
    mname = f"{modname}.{fnmm}"
    importlib.import_module(mname, modname)
    mods.append(fnmm)


def __dir__():
    return sorted(mods)
