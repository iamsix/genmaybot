import datetime, urllib.request
import xml.etree.ElementTree as ET

def mlb_schedule(self, e):
    url = 'http://wap.mlb.com/gdcross/components/game/mlb/year_' + datetime.date.today().strftime("%Y/month_%m/day_%d") + '/master_scoreboard.xml'
    # url = 'http://wap.mlb.com/gdcross/components/game/mlb/year_2014/month_03/day_01/master_scoreboard.xml'
    games = ET.parse(urllib.request.urlopen(url)).getroot().getchildren()
    game_details = []

    def isCareAbout(team):
        truth = False

        items = [
            'ATL',
            'NYY',
            'NYM',
            'BOS',
            'BAL',
            'OAK',
            'SF',
            'LAD'
        ]

        for (i, item) in enumerate(items):
            if team == item:
                truth = True
                break

        return truth

    for game in games:
        if game[00].attrib['status'] == 'Final' or game[00].attrib['status'] == 'In Progress'  and (isCareAbout(game.attrib['home_name_abbrev']) or isCareAbout(game.attrib['away_name_abbrev'])):
            game_details.append('{} at {} {}-{} {}/{}'.format(
                game.attrib['away_name_abbrev'],
                game.attrib['home_name_abbrev'],
                game[1][9].attrib['away'],
                game[1][9].attrib['home'],
                game[00].attrib['ind'],
                game[00].attrib['inning']
            ))
        elif (isCareAbout(game.attrib['home_name_abbrev']) or isCareAbout(game.attrib['away_name_abbrev'])):
            game_details.append(game.attrib['away_name_abbrev'] + ' at ' + game.attrib['home_name_abbrev'] + ' ' + game.attrib['home_time'] + ' ' + game.attrib['ampm'] + ' ' + game.attrib['home_time_zone'])

    # print(game_details)
    e.output = ' | '.join(game_details)

    return e

mlb_schedule.command = '!mlb'
# mlb_schedule({}, {})