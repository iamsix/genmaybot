import urllib.request, urllib.error, urllib.parse, urllib, xml.dom.minidom
import json
try:
    import botmodules.userlocation as user
except:
    pass


def get_weather(self, e):
    # WWO weather of place specified in 'zip'
    # http://www.worldweatheronline.com/free-weather-feed.aspx

    location = e.input
    if location == "" and user:
        location = user.get_location(e.nick)
    location = urllib.parse.quote(location)
    url = "http://free.worldweatheronline.com/feed/weather.ashx?q={}&format=json&num_of_days=1&key={}".format(location, self.botconfig["APIkeys"]["wwoAPIkey"])

    response = urllib.request.urlopen(url).read().decode('utf-8')
    weather = json.loads(response)
    weather = weather["data"]

    if 'error' not in weather:
        city = weather['request'][0]['query']
        desc = weather['current_condition'][0]['weatherDesc'][0]['value']
        temp = "{}°F {}°C".format(weather['current_condition'][0]['temp_F'], weather['current_condition'][0]['temp_C'])
        humidity = weather['current_condition'][0]['humidity']
        wind = "{} at {} mph".format(weather['current_condition'][0]['winddir16Point'], weather['current_condition'][0]['windspeedMiles'])
        high = "{}°F {}°C".format(weather['weather'][0]['tempMaxF'], weather['weather'][0]['tempMaxC'])
        low = "{}°F {}°C".format(weather['weather'][0]['tempMinF'], weather['weather'][0]['tempMinC'])
        outlook = weather['weather'][0]['weatherDesc'][0]['value']
        message = "{} / {} / {} / Humidity: {} / Wind: {} / High: {} - Low: {} - Outlook: {}".format(city, desc, temp, humidity, wind, high, low, outlook)
        e.output = message
        return e
    else:
        return get_weather2(self, e)


get_weather.command = "!w"
get_weather.helptext = "Usage: !w <location>\nExample: !w hell, mi\nShows weather info from google.com.\nUse !setlocation <location> to save your location"

def get_weather2(self, e):
    #wunderground weather of place specified in 'zip'
    zip = e.input
    if zip == "" and user:
        zip = user.get_location(e.nick)

    url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=" + urllib.parse.quote(zip)
    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    city = dom.getElementsByTagName('display_location')[0].getElementsByTagName('full')[0].childNodes[0].data
    if city != ", ":
        temp_f = dom.getElementsByTagName('temp_f')[0].childNodes[0].data
        temp_c = dom.getElementsByTagName('temp_c')[0].childNodes[0].data
        try:
            condition = dom.getElementsByTagName('weather')[0].childNodes[0].data
        except:
            condition = ""
        try:
            humidity = "Humidity: " + str(dom.getElementsByTagName('relative_humidity')[0].childNodes[0].data)
        except:
            humidity = ""
        try:
            wind = "Wind: " + str(dom.getElementsByTagName('wind_string')[0].childNodes[0].data)
        except:
            humidity = ""

        degree_symbol = chr(176)
        chanmsg = "%s / %s / %s%sF %s%sC / %s / %s" % (city, condition, temp_f,degree_symbol, temp_c, degree_symbol, humidity, wind)
        e.output = chanmsg
        return e
    else:
        if user:
            ziptry = user.get_location(e.input)
            if ziptry:
                e.nick = e.input
                e.input = ""
                return get_weather(self, e)
            else:
                return None

get_weather2.command = "!wu"
get_weather2.helptext = "Usage: !wu <location>\nExample: !wu hell, mi\nShows weather info from wunderground.com.\nUse !setlocation <location> to save your location"

