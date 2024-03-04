# This file is placed in the Public Domain.
#
# ruff: noqa: F401


"modules"


import importlib
import os


modules = []


def __dir__():
    return sorted(modules)


def import_pkg(dname, pname=""):
    modules = []
    for pth in os.listdir(dname):
        if pth.startswith("__"):
            continue
        if not pth.endswith(".py"):
            continue
        name = pth[:-3]
        if pname:
            name = f"{pname}.{name}"
        mod = importlib.import_module(name)
        modules.append(name)


import_pkg(os.path.dirname(__file__), "mods")
