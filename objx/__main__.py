# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,E0402


"runtime"


import getpass
import os
import readline
import sys
import termios
import time


from .excepts import Error, debug, enable
from .handler import Client, Command, Message, cmnd, forever, parse_cmd, scan
from .objects import Default
from .workdir import Workdir, skel


"defines"


Cfg         = Default()
Cfg.mod     = "cmd,err,fnd,mod,thr"
Cfg.version = "60"
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")
Workdir.wd = Cfg.wd


names    = __file__.split(os.sep)


if names[-2] == "bin":
    Cfg.name = names[-1]
else:
    Cfg.name = names[-2]


"classes"


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


"utility"


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def wrap(func):
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


"runtime"


from . import modules


def cmd(event):
    event.reply(",".join(sorted(list(Command.cmds))))


def ver(event):
    event.reply(f"{Cfg.name.upper()} {Cfg.version}")
    

def main():
    Command.add(cmd)
    Command.add(ver)
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
    if "d" in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
        Cfg.user = getpass.getuser()
        daemon(Cfg.pidfile, "v" in Cfg.opts)
        privileges(Cfg.user)
        scan(modules, Cfg.mod, True, Cfg.dis, True)
        forever()
        return
    if "c" in Cfg.opts:
        scan(modules, Cfg.mod, True, Cfg.sets.dis, True)
        csl = Console()
        if 'z' in Cfg.opts:
            csl.threaded = False
        csl.start()
        forever()
        return
    if Cfg.otxt:
        Cfg.mod = ",".join(modules.__dir__())
        scan(modules, Cfg.mod, False, Cfg.sets.dis, False)
        return cmnd(Cfg.otxt, print)


def wrapped():
    wrap(main)
    Error.show()


if __name__ == "__main__":
    wrapped()
