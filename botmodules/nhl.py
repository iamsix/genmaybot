import xml.dom.minidom, datetime, urllib.request

def get_nhl_live_games(self, e):
    url = "http://feeds.cdnak.neulion.com/fs/nhl/mobile/feeds/data/%s.xml" % (datetime.date.today().strftime("%Y%m%d"))
    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    games = dom.getElementsByTagName("game")
    
    gamestext = "" 
    
    for game in games:
        gametext = ""
        try:
            state = game.getElementsByTagName('game-state')[0].childNodes[0].data
            
            if state == "LIVE":       
                progress = game.getElementsByTagName('progress-time')[0].childNodes[0].data
            else:
                progress = state
            
            awayteam = game.getElementsByTagName('away-team')[0].getElementsByTagName('name')[0].childNodes[0].data
            hometeam = game.getElementsByTagName('home-team')[0].getElementsByTagName('name')[0].childNodes[0].data
                    
            scoreaway = game.getElementsByTagName('away-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
            scorehome = game.getElementsByTagName('home-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
            gametext = "%s %s - %s %s (%s)" % (awayteam, scoreaway, scorehome, hometeam, progress)
            if gametext != "":
                gamestext += gametext + " | " 
        except:
            pass


    gamestext = gamestext[0:-3]
    e.output = gamestext
    return e

get_nhl_live_games.command = "!nhl"
get_nhl_live_games.helptext = "Usage: !nhl Shows today's hockey games and current scores"

def get_nhl_live_streams(self, e):
    url = "http://feeds.cdnak.neulion.com/fs/nhl/mobile/feeds/data/%s.xml" % (datetime.date.today().strftime("%Y%m%d"))
    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    games = dom.getElementsByTagName("game")

    streamstext = "" 
        
    for game in games:
        streamtext = ""
    #    try:
        state = game.getElementsByTagName('game-state')[0].childNodes[0].data
        if state == "LIVE":       
            progress = game.getElementsByTagName('progress-time')[0].childNodes[0].data
        else:
            continue

        awayteam = game.getElementsByTagName('away-team')[0].getElementsByTagName('name')[0].childNodes[0].data
        hometeam = game.getElementsByTagName('home-team')[0].getElementsByTagName('name')[0].childNodes[0].data
        scoreaway = game.getElementsByTagName('away-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
        scorehome = game.getElementsByTagName('home-team')[0].getElementsByTagName('goals')[0].childNodes[0].data
        gametext = "%s %s - %s %s (%s)" % (awayteam, scoreaway, scorehome, hometeam, progress)
        awaystream = game.getElementsByTagName('streams')[0].getElementsByTagName("sony_ced")[0].getElementsByTagName("away")[0].getElementsByTagName("live")[0].childNodes[0].data.replace("ced","4500")
        homestream = game.getElementsByTagName('streams')[0].getElementsByTagName("sony_ced")[0].getElementsByTagName("home")[0].getElementsByTagName("live")[0].childNodes[0].data.replace("ced","4500")

        awayradio = game.getElementsByTagName('streams')[0].getElementsByTagName("iphone")[0].getElementsByTagName("away")[0].getElementsByTagName('radio')[0].childNodes[0].data
        homeradio = game.getElementsByTagName('streams')[0].getElementsByTagName("iphone")[0].getElementsByTagName("home")[0].getElementsByTagName('radio')[0].childNodes[0].data
        streamtext = "%s stream: %s\n%s stream: %s\n%s radio: %s\n%s radio: %s" % (awayteam, awaystream, hometeam, homestream, awayteam, awayradio, hometeam, homeradio)
    #    except:
    #        pass

        streamstext += "%s\n%s\n---------\n" % (gametext, streamtext)    

    streamstext = streamstext[0:-10]
    e.notice = True
    e.output = streamstext
    return e    
        
get_nhl_live_streams.command = "!nhl-vid"
get_nhl_live_streams.helptext = "Usage: !nhl-vid Shows today's hockey game live video and audio stream URLs"            
            
            