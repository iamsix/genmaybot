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
    url = "http://free.worldweatheronline.com/feed/weather.ashx?q={}&format=json&num_of_days=1&includeLocation=yes&key={}".format(location, self.botconfig["APIkeys"]["wwoAPIkey"])

    response = urllib.request.urlopen(url).read().decode('utf-8')
    weather = json.loads(response)
    weatherdata = weather["data"]

    if 'error' not in weatherdata:
    
        country = weatherdata['nearest_area'][0]['country'][0]['value']
        
        if country=="United States of America" or country=="Canada" or country=="USA":
            country = ""
        elif country=="United Kingdom":
            country = ", UK"
        else: 
            country = ", " + country
        
    
        city = "%s, %s%s" % (weatherdata['nearest_area'][0]['areaName'][0]['value'], weatherdata['nearest_area'][0]['region'][0]['value'], country)
        desc = weatherdata['current_condition'][0]['weatherDesc'][0]['value']
        temp = "{}°F {}°C".format(weatherdata['current_condition'][0]['temp_F'], weatherdata['current_condition'][0]['temp_C'])
        humidity = "%s%%" % (weatherdata['current_condition'][0]['humidity'])
        wind = "%s at %s mph (%s km/h)" % (weatherdata['current_condition'][0]['winddir16Point'], weatherdata['current_condition'][0]['windspeedMiles'], weatherdata['current_condition'][0]['windspeedKmph'])
        high = "{}°F {}°C".format(weatherdata['weather'][0]['tempMaxF'], weatherdata['weather'][0]['tempMaxC'])
        low = "{}°F {}°C".format(weatherdata['weather'][0]['tempMinF'], weatherdata['weather'][0]['tempMinC'])
        outlook = weatherdata['weather'][0]['weatherDesc'][0]['value']

        if  int(weatherdata['current_condition'][0]['cloudcover']) > 5:
            cloudcover = "Cloud Cover: %s%% / " % (weatherdata['current_condition'][0]['cloudcover'])
        else:
            cloudcover = ""

        if float(weatherdata['current_condition'][0]['precipMM']) > 0:
            precip = "Precipitation: %s mm / " % (weatherdata['current_condition'][0]['precipMM'])
        else:
            precip = ""

        if int(weatherdata['current_condition'][0]['visibility']) < 10:
            visibility = "Visibility: %skm / " % (weatherdata['current_condition'][0]['visibility'])
        else: 
            visibility = ""
        
        

        message = "{} / {} / {} / Humidity: {} / {}Wind: {} / {}{}High: {} - Low: {} - Outlook: {}".format(city, desc, temp, humidity, visibility, wind, cloudcover, precip, high, low, outlook)
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

