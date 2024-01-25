# This file is placed in the Public Domain.
#
# pylint: disable=R,C


"""NAME

    OBJX - objects library

SYNOPSIS

    objx <cmd> [key=val] [key==val]
    objx [-a] [-c] [-d] [-v]

DESCRIPTION

    OBJX has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OBJX provides an objx namespace that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OBJX provides a demo bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can also
    copy/paste the service file and run it under systemd for 24/7 presence
    in a IRC channel.

    OBJX is Public Domain.

INSTALL

    $ pipx install objx

USAGE

    without any argument the bot does nothing

    $ objx
    $

    see list of commands

    $ objx cmd
    cfg,cmd,mre,now,pwd

    start a console

    $ objx -c 
    >

    use -v for verbose

    $ objx -cv
    SBN started CV started Sat Dec 2 17:53:24 2023
    >

    start daemon

    $ objd
    $ 

CONFIGURATION

    irc

    $ objx cfg server=<server>
    $ objx cfg channel=<channel>
    $ objx cfg nick=<nick>

    sasl

    $ objx pwd <nsvnick> <nspass>
    $ objx cfg password=<frompwd>

    rss

    $ objx rss <url>
    $ objx dpl <url> <item1,item2>
    $ objx rem <url>
    $ objx nme <url< <name>

COMMANDS

    cfg - irc configuration
    cmd - commands
    hlp - show man page
    mre - displays cached output
    now - show genocide stats
    pwd - sasl nickserv name/pass
    thr - running threads

SYSTEMD

    save the following it in /etc/systems/system/objx.service and
    replace "<user>" with the user running pipx


    [Unit]
    Description=objects library
    Requires=network-online.target
    After=network-online.target
    
    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objx
    ExecStart=/home/<user>/.local/pipx/venvs/sbn/bin/objd
    RemainAfterExit=yes
    
    [Install]
    WantedBy=multi-user.target

    then run this

    $ mkdir ~/.objx
    $ sudo systemctl enable objx --now

    default channel/server is #objx on localhost

FILES

    ~/.objx
    ~/.local/bin/objx
    ~/.local/bin/objd
    ~/.local/pipx/venvs/objx

AUTHOR

    OTP-CR-117/19 <skullbonesandnumber@gmail.com>

COPYRIGHT

    OBJX is Public Domain.

"""


def __dir__():
    return (
        "hlp",
    )


__all__ = __dir__()


def hlp(event):
    event.reply(__doc__)
