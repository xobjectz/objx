# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0622,E0402,W0105


"status of bots"


from objr import Broker, Errors, add, tostr


def err(event):
    nmr = 0
    for bot in Broker.objs:
        if 'state' in dir(bot):
            event.reply(str(bot.state))
            nmr += 1
    event.reply(f"status: {nmr} errors: {len(Errors.errors)}")
    for exc in Errors.errors:
        txt = tostr(exc)
        for line in txt.split():
            event.reply(line)


add(err)
