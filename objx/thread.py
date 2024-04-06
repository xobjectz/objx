# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0718


"thread"


import io
import queue
import threading
import time
import traceback
import types


class Thread(threading.Thread):

    "Thread"

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

    def join(self, timeout=1.0):
        "join this thread."
        super().join(timeout)
        return self._result

    def run(self):
        "run this thread's payload."
        func, args = self.queue.get()
        try:
            self._result = func(*args)
        except Exception as ex:
            Errors.add(ex)
            if args and "Event" in str(type(args[0])):
                args[0].ready()


class Errors:

    "Errors"

    errors = []
    filter = []
    output = None
    shown  = []

    @staticmethod
    def add(exc):
        "add an exception"
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def enable(out):
        "enable output"
        Errors.output = out

    @staticmethod
    def format(exc):
        "format an exception"
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
        "check if output function is set."
        if Errors.output is None:
            return
        txt = str(Errors.format(exc))
        Errors.output(txt)

    @staticmethod
    def show():
        "show exceptions"
        for exc in Errors.errors:
            Errors.out(exc)

    @staticmethod
    def skip(txt):
        "check for skipping exceptions"
        for skp in Errors.filter:
            if skp in str(txt):
                return True
        return False


def debug(txt):
    "debug text"
    if Errors.output and not Errors.skip(txt):
        Errors.output(txt)


def launch(func, *args, **kwargs):
    "launch a thread."
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj):
    "return a full qualified name of an object/function/module."
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


"interface"


def __dir__():
    return (
        'Errors',
        'Thread',
        'debug',
        'launch',
        'name'
    )


__all__ = __dir__()
