# This file is placed in the Public Domain.


"log text"


import time


from objx.broker import fntime
from objx.client import laps
from objx.object import Object
from objx.run    import broker


class Log(Object): # pylint: disable=R0903

    "Log"

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    "log text."
    if not event.rest:
        nmr = 0
        for fnm, obj in broker.all('log'):
            lap = laps(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    broker.add(obj)
    event.reply('ok')
