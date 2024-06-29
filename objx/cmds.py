# This file is placed in the Public Domain.
#
# pylint: disable=R0903


"commands"


from .object import Object, construct
from .parse  import parse
from .table  import ondemand


MODNAMES = {
    "cmd": "objx.mods.cmd",
    "dmp": "objx.mods.dmp",
    "err": "objx.mods.err",
    "fnd": "objx.mods.fnd",
    "cfg": "objx.mods.irc",
    "mre": "objx.mods.irc",
    "pwd": "objx.mods.irc",
    "dpl": "objx.mods.rss",
    "nme": "objx.mods.rss",
    "rem": "objx.mods.rss",
    "res": "objx.mods.rss",
    "rss": "objx.mods.rss",
    "syn": "objx.mods.rss",
    "exp": "objx.mods.rss",
    "imp": "objx.mods.rss",
    "thr": "objx.mods.thr",
    "tmr": "objx.mods.tmr",
    "upt": "objx.mods.upt"
}


class Commands:

    "Commands"

    cmds     = Object()
    modnames = Object()
    construct(modnames, MODNAMES)


def add(func):
    "add command."
    setattr(Commands.cmds, func.__name__, func)
    if func.__module__ != "__main__":
        setattr(Commands.modnames, func.__name__, func.__module__)


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = getattr(Commands.cmds, evt.cmd, None)
    if not func:
        mname = getattr(Commands.modnames, evt.cmd, None)
        if mname:
            mod = ondemand(mname)
            getattr(mod, evt.cmd, None)
        func = getattr(Commands.cmds, evt.cmd, None)
    if func:
        func(evt)
    bot.show(evt)
    evt.ready()


def __dir__():
    return (
        'Commands',
        'add',
        'command'
    )
