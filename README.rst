OBJX
####


NAME

::

    OBJX - objects


INSTALL

::

    $ pipx install objx
    $ pipx ensurepath


SYNOPSIS

::

    objx <cmd> [key=val] [key==val]
    objxd


DESCRIPTION

::

    OBJX is a python3 bot able to display rss feeds in your channel.

    OBJX comes with a cli to configure and a daemon to run in the
    background, hooking the daemon in systemd brings a 24/7 available
    bot in your channel.


COMMANDS

::

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed


CONFIGURATION

irc

::

    $ objx cfg server=<server>
    $ objx cfg channel=<channel>
    $ objx cfg nick=<nick>

sasl

::

    $ objx pwd <nsvnick> <nspass>
    $ objx cfg password=<frompwd>

rss

::

    $ objx rss <url>
    $ objx dpl <url> <item1,item2>
    $ objx rem <url>
    $ objx nme <url> <name>


SYSTEMD

save the following it in /etc/systemd/system/objx.service and
replace "<user>" with the user running pipx

::

    [Unit]
    Description=objects
    Requires=network-online.target
    After=network-online.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.objx
    ExecStart=/home/<user>/.local/pipx/venvs/objx/bin/objxd
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


then run this

::

    mkdir ~/.objx
    sudo systemctl enable objx --now


default channel/server is #objx on localhost


FILES

::

    ~/.objx
    ~/.local/bin/objx
    ~/.local/bin/objxd
    ~/.local/pipx/venvs/objxd/


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OBJX is Public Domain.
