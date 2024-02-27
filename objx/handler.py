# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"runtime"


import inspect
import io
import queue
import threading
import time
import traceback
import types
import _thread


from .objects import Default, Object, keys, spl, values
from .persist import Persist


"defines"


rpr = object.__repr__


"classes"


class Broker:

    objs = Object()

    @staticmethod
    def add(obj):
        setattr(Broker.objs, rpr(obj), obj)

    @staticmethod
    def all():
        return values(Broker.objs)

    @staticmethod
    def first():
        for key in keys(Broker.objs):
            return getattr(Broker.objs, key)

    @staticmethod
    def get(orig):
        return getattr(Broker.objs, orig, None)

    @staticmethod
    def remove(obj):
        delattr(Broker.objs, rpr(obj))


class Command:

    cmds = Object()

    @staticmethod
    def add(func):
        setattr(Command.cmds, func.__name__, func)


def command(evt):
    parse_cmd(evt)
    func = getattr(Command.cmds, evt.cmd, None)
    if func:
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Errors.add(exc)
    evt.ready()


class Errors:

    errors = []
    filter = []
    output = None
    shown  = []

    @staticmethod
    def add(exc):
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)


    @staticmethod
    def enable(out):
        Errors.output = out

    @staticmethod
    def format(exc):
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def out(exc):
        if Errors.output:
            txt = str(Errors.format(exc))
            Errors.output(txt)

    @staticmethod
    def show():
        for exc in Errors.errors:
            Errors.out(exc)

    @staticmethod
    def skip(txt):
        for skp in Errors.filter:
            if skp in str(txt):
                return True
        return False


def debug(txt):
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)


"handler"


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

    def show(self):
        bot = Broker.get(self.orig)
        for txt in self.result:
            bot.say(self.channel, txt)

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
        Broker.add(self)

    def callback(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        if self.threaded:
            evt._thr = launch(func, evt)
        else:
            func(evt)
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
        launch(self.loop)

    def stop(self):
        self.stopped.set()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def show(self, evt):
        for txt in evt.result:
            self.say(evt.channel, txt)

    def raw(self, txt):
        pass


"threads"


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._result   = None
        self.name      = thrname or name(func)
        self.queue     = queue.Queue()
        self.sleep     = None
        self.starttime = time.time()
        self.queue.put_nowait((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self):
        func, args = self.queue.get()
        try:
            self._result = func(*args)
        except Exception as exc:
            Errors.add(exc)
            if args and "ready" in dir(args[0]):
                args[0].ready()


def launch(func, *args, **kwargs):
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


"utilities"


def cmnd(txt, out):
    clt = Client()
    clt.raw = out
    evn = Event()
    evn.orig = object.__repr__(clt)
    evn.txt = txt
    command(evn)
    evn.wait()
    return evn


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


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


def scan(pkg, modstr, initer=False, disable="", wait=True):
    mds = []
    for modname in spl(modstr):
        if modname in spl(disable):
            continue
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for _key, cmd in inspect.getmembers(module, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Command.add(cmd)
        for _key, clz in inspect.getmembers(module, inspect.isclass):
            if not issubclass(clz, Object):
                continue
            Persist.whitelist(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
            mds.append(module)
    if wait and initer:
        for mod in mds:
            mod._thr.join()
    return mds
    