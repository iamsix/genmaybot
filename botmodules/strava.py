import json
import urllib, urllib.request, urllib.parse

#this is only needed if we ever have to change the strava token
def set_stravatoken(line, nick, self, c):
     self.botconfig["APIkeys"]["stravaToken"] = line[12:]
     with open('genmaybot.cfg', 'w') as configfile:
         self.botconfig.write(configfile)
set_stravatoken.admincommand = "stravatoken"

def request_json(url, self):
    headers = {'Authorization': 'access_token ' + self.botconfig["APIkeys"]["stravaToken"]}
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    response = json.loads(response.read().decode('utf-8'))
    return response

def latest_ride(self, e):
    data = request_json("https://www.strava.com/api/v3/activities", self)
    name = data[0]['name']
    distance = int(data[0]['distance']) / 1000
    time = int(data[0]['moving_time']) / 60
    elevation = data[0]['total_elevation_gain']
    watts = data[0]['average_watts']
    kj = data[0]['kilojoules']
    string = "%s rode %s: %skm with %sm elevation in %s minutes. Produced %s watts and spent %s Kilojoules" % (e.nick, name, distance, elevation, time, watts, kj)
    e.output = string
    return e
     
latest_ride.command = "!strava"

