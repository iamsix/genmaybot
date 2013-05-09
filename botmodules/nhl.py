import xml.dom.minidom, datetime, urllib.request

def get_nhl_live_games(self, e):
    url = "http://feeds.cdnak.neulion.com/fs/nhl/mobile/feeds/data/%s.xml" % (datetime.date.today().strftime("%Y%m%d"))
    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    games = dom.getElementsByTagName("game")
    
    gamestext = "" 
    
    for game in games:
        gametext = ""
        try:
            progress = game.getElementsByTagName('progress-time')[0].childNodes[0].data
            awayteam = game.getElementsByTagName('away-team')[0].getElementsByTagName('name')[0].childNodes[0].data
            hometeam = game.getElementsByTagName('home-team')[0].getElementsByTagName('name')[0].childNodes[0].data
                    
            scoreaway = game.getElementsByTagName('away-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
            scorehome = game.getElementsByTagName('away-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
            gametext = "%s - %s %s:%s (%s)" % (awayteam, hometeam, scoreaway, scorehome, progress)
            if gametext != "":
                gamestext += gametext + " | " 
        except:
            pass


    gamestext = gamestext[0:-3]
    e.output = gamestext
    return e

get_nhl_live_games.command = "!nhl"
get_nhl_live_games.helptext = "Usage: !nhl Shows today's hockey games and current scores"