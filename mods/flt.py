# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"fleet"


from objx.broker import all


from objr import Client, name


def flt(event):
    try:
        event.reply(all()[int(event.args[0])])
    except (IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in all()]))


Client.add(flt)
