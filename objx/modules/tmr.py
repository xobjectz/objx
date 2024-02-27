# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0612.W0702,E0402


"timer"


import time


from objx import Broker, Message, Timer, find, launch, sync, update
from objx.parsers import NoDate, get_day, get_hour, laps, today, to_day


"defines"


def init():
    for fnm, obj in find("timer"):
        if "time" not in obj:
            continue
        diff = float(obj.time) - time.time()
        if diff > 0:
            bot = Broker.first()
            evt = Message()
            update(evt, obj)
            evt.orig = object.__repr__(bot)
            timer = Timer(diff, evt.show)
            launch(timer.start)


MONTHS = [
    'Bo',
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
]


FORMATS = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
]


class NoDate(Exception):

    pass


"utilities"


def extract_date(daystr):
    for fmt in FORMATS:
        try:
            res = ttime.mktime(ttime.strptime(daystr, fmt))
        except ValueError:
            res = None
        if res:
            return res


def get_day(daystr):
    try:
        ymdre = re.search(r'(\d+)-(\d+)-(\d+)', daystr)
        (day, month, yea) = ymdre.groups()
    except ValueError:
        try:
            ymre = re.search(r'(\d+)-(\d+)', daystr)
            (day, month) = ymre.groups()
            yea = ttime.strftime("%Y", ttime.localtime())
        except Exception as ex:
            raise NoDate(daystr) from ex
    day = int(day)
    month = int(month)
    yea = int(yea)
    date = "%s %s %s" % (day, MONTHS[month], yea)
    return ttime.mktime(ttime.strptime(date, r"%d %b %Y"))


def get_hour(daystr):
    try:
        hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmsre.group(1)))
        hoursmin = hours  + int(hmsre.group(2)) * 60
        hmsres = hoursmin + int(hmsre.group(3))
    except AttributeError:
        pass
    except ValueError:
        pass
    try:
        hmre = re.search(r'(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmre.group(1)))
        hmsres = hours + int(hmre.group(2)) * 60
    except AttributeError:
        return 0
    except ValueError:
        return 0
    return hmsres


def get_time(txt):
    try:
        target = get_day(txt)
    except NoDate:
        target = to_day(today())
    hour =  get_hour(txt)
    if hour:
        target += hour
    return target


def laps(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    yea = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    yeas = int(nsec/yea)
    nsec -= yeas*yea
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if yeas:
        txt += f"{yeas}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def parse_time(txt):
    seconds = 0
    target = 0
    txt = str(txt)
    for word in txt.split():
        if word.startswith("+"):
            seconds = int(word[1:])
            return ttime.time() + seconds
        if word.startswith("-"):
            seconds = int(word[1:])
            return ttime.time() - seconds
    if not target:
        try:
            target = get_day(txt)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(txt)
        if hour:
            target += hour
    return target


def to_day(daystr):
    previous = ""
    line = ""
    daystr = str(daystr)
    for word in daystr.split():
        line = previous + " " + word
        previous = word
        try:
            res = extract_date(line.strip())
        except ValueError:
            res = None
        if res:
            return res
        line = ""


def today():
    return str(datetime.datetime.today()).split()[0]


"commands"


def tmr(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('timer'):
            if "time" not in obj:
                continue
            lap = float(obj.time) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {laps(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers")
        return
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply("%s is not an integer" % seconds)
                return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    event.time = target
    diff = target - time.time()
    event.reply("ok " +  laps(diff))
    event.result = []
    event.result.append(event.rest)
    timer = Timer(diff, event.show)
    update(timer, event)
    sync(timer)
    launch(timer.start)
