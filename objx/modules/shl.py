# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0611,W0613


"main"


import getpass
import os
import readline
import sys
import time


from .. import Cfg, Client, Message, enable, parse_cmd, skel, wrap
from .. import debug, forever, scan, modules, wrap


Cfg.mod = "cmnd,mod,dis,ena"


class Console(Client):

    def announce(self, txt):
        pass

    def callback(self, evt):
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Message()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def doshl():
    enable(print)
    skel()
    parse_cmd(Cfg, " ".join(sys.argv[1:]))
    readline.redisplay()
    if 'a' in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} {Cfg.opts.upper()} started {dte}")
    if "h" in Cfg.opts:
        from . import __doc__ as txt
        print(txt)
        return
    scan(modules, Cfg.mod, True, Cfg.sets.dis, True)
    csl = Console()
    if 'z' in Cfg.opts:
        csl.threaded = False
    csl.start()
    wrap(forever)


def shl(event):
    wrap(doshl)
