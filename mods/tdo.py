# This file is placed in the Public Domain.


"todo list"


import time


from objx.broker import fntime
from objx.client import laps
from objx.object import Object
from objx.run    import broker


class NoDate(Exception):

    "no matching date"


class Todo(Object): # pylint: disable=R0903

    "Todo"

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


def dne(event):
    "flag todo as done."
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in broker.find(selector, match="Todo"):
        nmr += 1
        obj.__deleted__ = True
        broker.add(obj, fnm)
        event.reply('ok')
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    "add todo."
    if not event.rest:
        nmr = 0
        for fnm, obj in broker.all('todo'):
            lap = laps(time.time()-fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    broker.add(obj)
    event.reply('ok')
