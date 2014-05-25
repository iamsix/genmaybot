"""Very basic version of seen for now, doesn't notice user joins/parts/nick changes yet"""
import sqlite3
import datetime


def __init__(self):
    conn = sqlite3.connect('seen.sqlite')
    c = conn.cursor()
    result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='seen';").fetchone()
    if not result:
        c.execute('create table seen('
                  'nick text UNIQUE ON CONFLICT REPLACE, '
                  'lastline text, '
                  'channel text, '
                  'ts NOT NULL default CURRENT_TIMESTAMP)')

    conn.commit()
    c.close()


def seenlineparser(self, e):
    #we only want things said in channels
    if "#" in e.source:
        conn = sqlite3.connect('seen.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO seen(nick, lastline, channel) VALUES (?,?,?)", (e.nick, e.input, e.source))
        conn.commit()
        c.close()
seenlineparser.lineparser = True


#Eventually I want to update this to also watch for joins/parts nick changes, etc.
def seen(self, e):
    if e.input.lower() == e.nick.lower():
        e.output = "Only you can find yourself."
    elif e.input.lower() == e.botnick.lower():
        e.output = "I'm right here."
    elif " " in e.input:
        e.output = "1 nick only! no spaming -.-"
    else:
        conn = sqlite3.connect('seen.sqlite')
        c = conn.cursor()
        if e.input != "*":
            result = c.execute("SELECT nick, lastline, channel, ts FROM "
                               "seen WHERE lower(nick) = lower(?)", [e.input]).fetchone()
        else:
            result = c.execute("SELECT nick, lastline, channel, ts FROM "
                               "seen ORDER BY ts DESC LIMIT 1").fetchone()
        if result:
            ago = datetime.datetime.utcnow() - datetime.datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S")
            ago = self.tools['prettytimedelta'](ago)
            if not ago:
                ago = "just now"
            else:
                ago += " ago"
            e.output = '{} was last seen saying: "{}" in {} {}'.format(result[0], result[1], result[2], ago)
        else:
            e.output = "I have never seen this {} person you speak of".format(e.input)

        c.close()
    return e

seen.command = "!seen"
