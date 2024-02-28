# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"handler"


import inspect
import io
import queue
import threading
import traceback
import _thread


from .excepts import Errors
from .objects import Default, Object, keys, spl, values
from .persist import Persist


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""
        self.type    = "event"

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result


class Handler:

    def __init__(self):
        self.cbs = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True

    def callback(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        try:
            func(evt)
        except Exception as ex:
            Errors.add(ex)
        evt.ready()

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt):
        self.queue.put_nowait(evt)

    def register(self, typ, cbs):
        setattr(self.cbs, typ, cbs)

    def start(self):
        self.loop()

    def stop(self):
        self.stopped.set()


class Client(Handler):

    cmds = Object()

    def __init__(self):
        Handler.__init__(self)
        self.register("command", self.command)

    @staticmethod
    def add(func):
        setattr(Client.cmds, func.__name__, func)

    def announce(self, txt):
        self.raw(txt)

    def command(self, evt):
        parse_cmd(evt)
        func = getattr(Client.cmds, evt.cmd, None)
        if func:
            try:
                func(evt)
            except Exception as exc:
                Errors.add(exc)
        self.show(evt)
        evt.ready()

    def forever():
        while 1:
            try:
                time.sleep(1.0)
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def raw(self, txt):
        pass

    def say(self, channel, txt):
        self.raw(txt)

    @staticmethod
    def scan(mod):
        for _key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Client.add(cmd)

    def show(self, evt):
        for txt in evt.result:
            self.say(evt.channel, txt)


"utilities"


def cmnd(txt, out):
    clt = Client()
    clt.raw = out
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    clt.command(evn)
    evn.wait()
    return evn


def init(pkg, modstr, disable="", wait=False):
    mds = []
    for modname in spl(modstr):
        if modname in spl(disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        if "init" in dir(module):
            module.init()
    return mds


def parse_cmd(obj, txt=None):
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


def scan(pkg, modstr, disable=""):
    mds = []
    for modname in spl(modstr):
        if modname in spl(disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        Client.scan(module)
        Persist.scan(module)
