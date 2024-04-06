# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E1102


"errors"


import io
import traceback


class Errors:

    "Errors"

    errors = []

    @staticmethod
    def add(exc):
        "add an exception"
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

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
        txt = str(Errors.format(exc))
        print(txt)

    @staticmethod
    def show():
        "show exceptions"
        for exc in Errors.errors:
            Errors.out(exc)


"interface"


def __dir__():
    return (
        'Errors',
    )


__all__ = __dir__()
