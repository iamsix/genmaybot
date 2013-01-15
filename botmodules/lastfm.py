# -*- coding: utf-8 *-*
import sqlite3
import urllib
import json


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
    lastfmuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [e.nick]).fetchone()

    if lastfmuser:
        lastfmuser = lastfmuser[0]
        url = "http://ws.audioscrobbler.com/2.0/?api_key=%s&limit=1&format=json&method=user.getRecentTracks&user=%s" % (self.botconfig["APIkeys"]["lastfmAPIkey"], lastfmuser)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        track = json.loads(response)
        try:
            artist = track['recenttracks']['track'][0]['artist']['#text']
            trackname = track['recenttracks']['track'][0]['name']
            e.output = "%s np: %s - %s" % (lastfmuser, artist, trackname)
        except:
            #an exception means they are not currently playing a track
            pass
    else:
        e.output = "You don't have a last.fm user set up"

    return e
nowplaying.command = "~np"

def compare(self, e):
    conn = sqlite3.connect('lastfm.sqlite')
    c = conn.cursor()
    user1 = ""
    user2 = ""

    if len(e.input.split(" ")) == 1:
        lastfmuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [e.nick]).fetchone()
        if lastfmuser:
            user1 = lastfmuser[0]
            #first check if we're copmaring against an irc user - if there's a hit it's assumed so
            compuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [e.input]).fetchone()
            if compuser:
                user2 = compuser[0]
            else:
                user2 = e.input
        else:
            e.output = "you don't have a last.fm user set up"
    elif len(e.input.split(" ")) == 2:
        var1 = e.input.split(" ")[0]
        var2 = e.input.split(" ")[1]
        lastfmuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [var1]).fetchone()
        if lastfmuser:
            user1 = lastfmuser[0]
        else:
            user1 = var1
        lastfmuser = c.execute("SELECT lastfmuser FROM lastfm WHERE user = LOWER(?)", [var2]).fetchone()
        if lastfmuser:
            user2 = lastfmuser[0]
        else:
            user2 = var2

    if user1 and user2:
        url="http://ws.audioscrobbler.com/2.0/?api_key=%s&method=tasteometer.compare&type1=user&type2=user&value1=%s&value2=%s&format=json" % (self.botconfig["APIkeys"]["lastfmAPIkey"], user1, user2)
        response = urllib.request.urlopen(url).read().decode('utf-8')
        match = json.loads(response)
        score = match['comparison']['result']['score']
        print(score)
        artistmatches = match['comparison']['result']['artists']['@attr']['matches']
        jsonartists = match['comparison']['result']['artists']['artist']
        artists = []
        for artist in jsonartists:
            artists.append(artist['name'])
        print(artists)
        artists = ", ".join(artists)

        e.output = "Matching %s and %s :: Score: %s - Artists (%s matches): %s" % (user1, user2, score, artistmatches, artists)

    return e
compare.command = "~compare"
