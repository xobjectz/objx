# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0718


"client"


from .command import Command
from .errors  import later
from .event   import Event
from .handler import Handler
from .utils   import parse_cmd


class Client(Handler):

    "Client class"

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    @staticmethod
    def add(func):
        "add command to client."
        setattr(Command.cmds, func.__name__, func)

    def announce(self, txt):
        "announce text."
        self.raw(txt)


    def raw(self, txt):
        "raw output."

    def say(self, _channel, txt):
        "say text in a channel."
        self.raw(txt)

    def show(self, evt):
        "show results into a channel."
        for txt in evt.result:
            self.say(evt.channel, txt)


def cmnd(txt, out):
    "do a command using the provided output function."
    clt = Client()
    clt.raw = out
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    command(clt, evn)
    evn.wait()
    return evn


def command(bot, evt):
    "check for and run a command."
    parse_cmd(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as exc:
            later(exc)
    bot.show(evt)
    evt.ready()
