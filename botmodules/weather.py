import urllib.request, urllib.parse, urllib, xml.dom.minidom
import json
try:
    import botmodules.userlocation as user
except ImportError:
    user = None
    pass


def set_wwokey(line, nick, self, c):
    self.botconfig["APIkeys"]["wwoAPIkey"] = line[7:]
    with open('genmaybot.cfg', 'w') as configfile:
        self.botconfig.write(configfile)
set_wwokey.admincommand = "wwokey"

def set_fiokey(line, nick, self, c):
    self.botconfig["APIkeys"]["forecastIO_APIkey"] = line[14:]
    with open('genmaybot.cfg', 'w') as configfile:
        self.botconfig.write(configfile)
set_fiokey.admincommand = "forecastiokey"

def google_geocode(address):
    gapikey = self.botconfig["APIkeys"]["shorturlkey"] #This uses the same Google API key as URL shortener
    address = urllib.parse.quote(address)

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    url = url.format(address, gapikey)


    try:
        request = urllib.request.Request(url, None, {'Referer': 'http://irc.00id.net'})
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as err:
        print(err.read())

    try:
        results_json = json.loads(response.read().decode('utf-8'))
        status = results_json['status']

        if status != "OK":
            raise

        formatted_address = results_json['results'][0]['formatted_address']

        # Take only the city and state if in the USA
        if formatted_address.find("USA") != -1:
            formatted_address = formatted_address.split(",")[0]+", "+formatted_address.split(",")[1].split(" ")[1]

        lng = results_json['results'][0]['geometry']['location']['lng']
        lat = results_json['results'][0]['geometry']['location']['lat']

        
    except:
        print("Failed to geocode location using Google API.")
        print("Geocode URL: %s" % url)
        return
    
    return formatted_address, lat, lng

def bearing_to_compass(bearing):
    dirs = {}        
    dirs['N'] = (348.75, 11.25)
    dirs['NNE'] = (11.25, 33.75)
    dirs['NE'] = (33.75, 56.25)
    dirs['ENE'] = (56.25, 78.75)
    dirs['E'] = (78.75, 101.25)
    dirs['ESE'] = (101.25, 122.75)
    dirs['SE'] = (123.75, 146.25)
    dirs['SSE'] = (146.25, 168.75)
    dirs['S'] = (168.75, 191.25)
    dirs['SSW'] = (191.25, 213.75)
    dirs['SW'] = (213.75, 236.25)
    dirs['WSW'] = (236.25, 258.75)
    dirs['W'] = (258.75, 281.25)
    dirs['WNW'] = (281.25, 303.75)
    dirs['NW'] = (303.75, 326.25)
    dirs['NNW'] = (326.25, 348.75)

    for direction in dirs:
        min, max = dirs[direction]
        if bearing >= min and bearing <= max:
            return direction
        elif bearing >= dirs['N'][0] or bearing <= dirs['N'][1]:
            return "N"


def get_weather(self, e):

    
    #This callback handling code should be able to be reused in any other function
    if get_weather.waitfor_callback:
        return

    try:
        location = e.location
    except:
        location = e.input
        
    if location == "" and user:
        location = user.get_location(e.nick)
        if location == "":
            get_weather.waitfor_callback = True
            user.get_geoIP_location(self, e, "", "", "", get_weather)
            
            return
    
    # Try weather functions in order
    e.output = forecast_io(self,  e, location)
    
    if not e.output:
        e.output = get_wwo(self, location, e)
    if not e.output:
        return get_weather2(self, e)
        
    return e
    
def forecast_io(self,e, location=""):
    apikey = self.botconfig["APIkeys"]["forecastIO_APIkey"]
    print ("Entered Forecast.IO function. Location %s or %s" % (location, e.input))
    if location == "":
        location = e.input
        
    #try:
    address, lat, lng = google_geocode(location, gapikey)
    print (address, lat, lng)
    #except: #Google geocode failed
    #    return False

    
    url = "https://api.forecast.io/forecast/{}/{},{}"
    url = url.format(apikey, lat, lng)

    try:
        request = urllib.request.Request(url, None, {'Referer': 'http://irc.00id.net'})
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as err:
        print(err.read())

    #try:
    results_json = json.loads(response.read().decode('utf-8'))
    current_conditions = results_json['currently']

    temp = current_conditions['temperature']
    humidity = int(100*current_conditions['humidity'])
    precip_probability = current_conditions['precipProbability']
    current_summary = current_conditions['summary']
    
    wind_speed = current_conditions['windSpeed']
    wind_speed_kmh = round(wind_speed * 1.609, 1)

    wind_direction = current_conditions['windBearing']
    wind_direction = bearing_to_compass(wind_direction)

    cloud_cover = int(100*current_conditions['cloudCover'])
    
    feels_like = current_conditions['apparentTemperature']

        
        
    if feels_like != temp:
        feels_like = " / Feels like: %s°F %s°C" % (int(round(feels_like,0)), int(round((feels_like- 32)*5/9,0)))
    
    else:
        feels_like = ""
    temp_c = int(round((temp - 32)*5/9,0))
    temp = int(round(temp,0))

    # If the minute by minute outlook isn't available, grab the hourly
    try:
        outlook = results_json['minutely']['summary']
    except:
        outlook = results_json['hourly']['summary']
            
        
        #print(temp,humidity,precip_probability,current_summary,wind_speed,wind_direction,cloud_cover,feels_like)



    #except:
    #    return
    
    output = "{} / {} / {}°F {}°C{} / Humidity: {}% / Wind: {} at {} mph ({} km/h) / Cloud Cover: {}% / Outlook: {}"
    output = output.format(address, current_summary, temp, temp_c, feels_like, humidity, wind_direction, wind_speed, wind_speed_kmh, cloud_cover, outlook)
    return output

forecast_io.command = "!fio"

def get_wwo(self, location, e):
    # WWO weather of place specified in 'zip'
    # http://www.worldweatheronline.com/free-weather-feed.aspx
    
    location = urllib.parse.quote(location)
    
    #End callback handling code
    url = "http://api.worldweatheronline.com/free/v1/weather.ashx?" \
          "q={}&format=json&num_of_days=1&includeLocation=yes&key={}".format(location,
                                                                             self.botconfig["APIkeys"]["wwoAPIkey"])

    response = urllib.request.urlopen(url).read().decode('utf-8')
    weather = json.loads(response)
    weatherdata = weather["data"]

    if 'error' not in weatherdata:
    
        country = weatherdata['nearest_area'][0]['country'][0]['value']
        
        if country == "United States Of America" or country == "Canada" or country == "USA":
            country = ""
        elif country == "United Kingdom":
            country = ", UK"
        else: 
            country = ", " + country

        try:
            region = ", " + weatherdata['nearest_area'][0]['region'][0]['value']
        except:
            region = ""
        
        city = "%s%s%s" % (weatherdata['nearest_area'][0]['areaName'][0]['value'], region, country)
        desc = weatherdata['current_condition'][0]['weatherDesc'][0]['value']
        temp = "{}°F {}°C".format(weatherdata['current_condition'][0]['temp_F'],
                                  weatherdata['current_condition'][0]['temp_C'])
        humidity = "%s%%" % (weatherdata['current_condition'][0]['humidity'])
        high = "{}°F {}°C".format(weatherdata['weather'][0]['tempMaxF'], weatherdata['weather'][0]['tempMaxC'])
        low = "{}°F {}°C".format(weatherdata['weather'][0]['tempMinF'], weatherdata['weather'][0]['tempMinC'])
        outlook = weatherdata['weather'][0]['weatherDesc'][0]['value']

        if int(weatherdata['current_condition'][0]['cloudcover']) > 5:
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
            
        if int(weatherdata['current_condition'][0]['windspeedMiles']) > 0:
            wind = "Wind: %s at %s mph (%s km/h) / " % (weatherdata['current_condition'][0]['winddir16Point'],
                                                        weatherdata['current_condition'][0]['windspeedMiles'],
                                                        weatherdata['current_condition'][0]['windspeedKmph'])
        else:
            wind = ""

        message = "{} / {} / {} / Humidity: {} / {}{}{}{}High: {} - Low: {} Outlook: {}".format(city,
                                                                                                desc,
                                                                                                temp,
                                                                                                humidity,
                                                                                                visibility,
                                                                                                wind,
                                                                                                cloudcover,
                                                                                                precip,
                                                                                                high,
                                                                                                low,
                                                                                                outlook)
        e.output = message
        return e
    else:
        return False

get_weather.waitfor_callback = False
get_weather.command = "!w"
get_weather.helptext = """Usage: \002!w <location>\002
Example: !w hell, mi
Shows weather info from google.com.
Use \002!setlocation <location>\002 to save your location"""


def get_weather2(self, e):
    #wunderground weather of place specified in 'zipcode'
    zipcode = e.input
    if zipcode == "" and user:
        zipcode = user.get_location(e.nick)

    url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=" + urllib.parse.quote(zipcode)
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
            wind = ""

        degree_symbol = chr(176)
        chanmsg = "%s / %s / %s%sF %s%sC / %s / %s" % (city,
                                                       condition,
                                                       temp_f,
                                                       degree_symbol,
                                                       temp_c,
                                                       degree_symbol,
                                                       humidity,
                                                       wind)
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
get_weather2.helptext = """Usage: \002!wu <location>\002
Example: !wu hell, mi
Shows weather info from wunderground.com.
Use \002!setlocation <location>\002 to save your location"""
