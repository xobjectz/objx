# This file is placed in the Public Domain.
#
#


"commands"


from .default import Default
from .errors  import Errors


class Command:

    "Command"

    cmds = Default()

    @staticmethod
    def add(func):
        "add command to client."
        setattr(Command.cmds, func.__name__, func)


class Event(Default):

    "Event"

    def __init__(self):
        Default.__init__(self)
        self.result  = []

    def reply(self, txt):
        "add text to the result"
        self.result.append(txt)


def cmnd(txt, evt=None):
    "check for and run a command."
    if evt is None:
        evt = Event()
    if not txt:
        return evt
    evt.txt = txt
    evt.cmd = evt.txt.split()[0]
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as ex:
            Errors.add(ex)
    return evt
