# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0718


"command"


from objx import Object


class Command:

    "Command"

    cmds = Object()

    @staticmethod
    def add(func):
        "add command."
        setattr(Command.cmds, func.__name__, func)
