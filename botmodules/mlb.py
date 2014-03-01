import datetime, urllib.request
import xml.etree.ElementTree as ET

def mlb_schedule(self, e):
    url = 'http://wap.mlb.com/gdcross/components/game/mlb/year_' + datetime.date.today().strftime("%Y/month_%m/day_%d") + '/master_scoreboard.xml'
    games = ET.parse(urllib.request.urlopen(url)).getroot().getchildren()
    gameDetails = []

    for game in games:
        gameDetails.append(game.attrib['away_name_abbrev'] + ' at ' + game.attrib['home_name_abbrev'] + ' ' + game.attrib['home_time'] + ' ' + game.attrib['ampm'] + ' ' + game.attrib['home_time_zone'])

    e.output = ' | '.join(gameDetails)

    return e

mlb_schedule.command = '!mlb'