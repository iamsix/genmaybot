# -*- coding: utf-8 *-*
import sqlite3
import urllib
import json


def __init__(self):
    self.botconfig["APIkeys"]["lastfmAPIkey"] = "23caa86333d2cb2055fa82129802780a"
    with open('genmaybot.cfg', 'w') as configfile:
        self.botconfig.write(configfile)


def setlastfmuser(self, e):
    conn = sqlite3.connect('lastfm.sqlite')
    c = conn.cursor()
    result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lastfm';").fetchone()
    if not result:
        c.execute('''create table lastfm(user text UNIQUE ON CONFLICT REPLACE, lastfmuser text)''')

    c.execute("""insert into lastfm values (?,?)""", (e.nick.lower(), e.input))
    conn.commit()
    c.close()
setlastfmuser.command = "!setlastfm"


def nowplaying(self, e):
    conn = sqlite3.connect('lastfm.sqlite')
    c = conn.cursor()
    lastfmuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [e.nick]).fetchone()[0]

    if lastfmuser:
        url = "http://ws.audioscrobbler.com/2.0/?api_key=%s&limit=1&format=json&method=user.getRecentTracks&user=%s" % (self.botconfig["APIkeys"]["lastfmAPIkey"], lastfmuser)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        track = json.loads(response)
        artist = track['recenttracks']['track']['artist']['#text']
        trackname = track['recenttracks']['track']['name']
        e.output = "%s np: %s - %s" % (lastfmuser, artist, trackname)
    else:
        e.output = "You don't have a last.fm user set up"

    return e
nowplaying.command = "~np"
