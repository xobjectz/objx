# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"working directory"


import os


from .object import Object, cdir


class Workdir(Object):

    "Workdir"

    workdir = ""


def skel():
    "create directory,"
    cdir(os.path.join(Workdir.workdir, "store", ""))


def store(pth=""):
    "return objects directory."
    return os.path.join(Workdir.workdir, "store", pth)


def strip(pth, nmr=3):
    "reduce to path with directory."
    return os.sep.join(pth.split(os.sep)[-nmr:])


def types():
    "return types stored."
    return os.listdir(Workdir.store())


def __dir__():
    return (
        'Workdir',
        'skel',
        'store',
        'strip',
        'types'
    )


__all__ = __dir__()
