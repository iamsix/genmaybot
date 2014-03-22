import datetime, urllib.request
import xml.etree.ElementTree as ET

def mlb_schedule(self, e):
    team = e.input
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

        if team in items:
                truth = True

        return truth

    for game in games:
        # get results for final game specified
        if team and (team == game.attrib['home_name_abbrev'] or team == game.attrib['away_name_abbrev']) and game[00].attrib['status'] == 'Final':
            game_details.append('{} vs {} {}-{} {}/{} | WP: {} ({}-{}) {} ERA | LP: {} ({}-{}) {} ERA | SV: {} ({}-{}) {}'.format(
                game.attrib['away_name_abbrev'],
                game.attrib['home_name_abbrev'],
                game[1][9].attrib['away'],
                game[1][9].attrib['home'],
                game[00].attrib['ind'],
                game[00].attrib['inning'],
                game[3].attrib['last'],
                game[3].attrib['wins'],
                game[3].attrib['losses'],
                game[3].attrib['era'],
                game[4].attrib['last'],
                game[4].attrib['wins'],
                game[4].attrib['losses'],
                game[4].attrib['era'],
                game[5].attrib['last'],
                game[5].attrib['saves'],
                game[5].attrib['svo'],
                game[5].attrib['era']
            ))
        elif not team:
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
#mlb_schedule({}, {})