# This file is placed in the Public Domain,
#
# pylint: disable=C,R,W0105,W0613,E0101


"objects"



from .objects import Object


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)
