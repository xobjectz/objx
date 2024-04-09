# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0201,W0718


"commands"


from objx.default import Default


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
        self.orig    = ""
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
    parse_cmd(evt, txt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as ex:
            Errors.add(ex)
    return evt


def parse_cmd(obj, txt=None):
    "parse a string for a command."
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.txt     = txt or obj.txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


"interface"


def __dir__():
    return (
        'Command',
        'Event',
        'cmnd',
        'parse_cmd'
    )


__all__ = __dir__()
