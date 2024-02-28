# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,W0212,W0613,W0718,E0402,E1102


"deferred exception handling"


import io
import traceback


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
