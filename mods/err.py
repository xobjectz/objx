# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0622,E0402


"status of bots"


from objx.brokers import Broker
from objx.excepts import Errors


def err(event):
    nmr = 0
    for bot in Broker.all():
        if 'state' in dir(bot):
            event.reply(str(bot.state))
            nmr += 1
    event.reply(f"status: {nmr} errors: {len(Errors.errors)}")
    for exc in Errors.errors:
        txt = Errors.format(exc)
        for line in txt.split():
            event.reply(line)
