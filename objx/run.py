# This file is placed in the Public Domain.


"runtime"


import os


from .broke  import Broker
from .config import Config
from .disk   import Persist


Cfg         = Config()
Cfg.dis     = ""
Cfg.mod     = "cmd,err,mod,thr"
Cfg.opts    = ""
Cfg.name    = __file__.split(os.sep)[-2]
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.moddir  = os.path.join(Cfg.wdr, "mods")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


broker = Broker()


def __dir__():
    return (
        'Cfg',
        'broker'
    )
