import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta


def set_wunderkey(line, nick, self, c):
    self.botconfig["APIkeys"]["wunderAPIkey"] = line[10:]
    with open('genmaybot.cfg', 'w') as configfile:
        self.botconfig.write(configfile)
set_wunderkey.admincommand = "wunderkey"


def get_sun(self, e):
    apikey = self.botconfig["APIkeys"]["wunderAPIkey"]
    loc = urllib.parse.quote(e.input)
    url = "http://api.wunderground.com/api/{}/astronomy/q/{}.json"
    url = url.format(apikey, loc)

    response = urllib.request.urlopen(url).read().decode("utf-8", "replace")
    data = json.loads(response)['moon_phase']
    time = "{}:{}".format(data['current_time']['hour'], data['current_time']['minute'])

    sunrise = "{}:{}".format(data['sunrise']['hour'], data['sunrise']['minute'])
    sunset = "{}:{}".format(data['sunset']['hour'], data['sunset']['minute'])

    now = datetime.strptime(time, "%H:%M")
    sunriseobj = datetime.strptime(sunrise, "%H:%M")
    sunsetobj = datetime.strptime(sunset, "%H:%M")

    sunlength = sunsetobj - sunriseobj
    if sunriseobj > now:
       ago = "from now"
       td = sunriseobj - now
    else:
       td = now - sunriseobj
       ago = "ago"
    til = self.tools['prettytimedelta'](td)
    #til = td
    sunrise = "{} ({} {})".format(sunrise, til, ago)
    if sunsetobj > now:
       ago = "from now"
       td = sunsetobj - now
    else:
       ago = "ago"
       td = now - sunsetobj
    #til = td
    til = self.tools['prettytimedelta'](td)
    sunset = "{} ({} {})".format(sunset, til, ago)

    out = "Sunrise: {} / Sunset: {} / Day Length: {}".format(sunrise, sunset, sunlength)
    e.output = out
    return e
get_sun.command = "!sun"
