import urllib2, urllib, xml.dom.minidom
try: import botmodules.userlocation as user
except: pass

def get_weather(self, e):
    #google weather of place specified in 'zip'
   zip = e.input
   
   if zip == "" and user:
       zip = user.get_location(e.nick)

   url = "http://www.google.com/ig/api?weather=" + urllib.quote(zip)
   dom = xml.dom.minidom.parse(urllib2.urlopen(url))
   
   if not dom.getElementsByTagName('problem_cause'):
       degree_symbol = unichr(176)
       city = dom.getElementsByTagName('city')[0].getAttribute('data')
       temp_f = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_f')[0].getAttribute('data')
       temp_c = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_c')[0].getAttribute('data')
       try:
        humidity = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('humidity')[0].getAttribute('data')
       except:
        humidity = ""
       
       try: 
        wind = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('wind_condition')[0].getAttribute('data')
       except:
        wind = "" 
        
       try:
        condition = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('condition')[0].getAttribute('data')
       except:
        condition = "" 
        
       try:
        high_f = dom.getElementsByTagName('forecast_conditions')[0].getElementsByTagName('high')[0].getAttribute('data')
        high_c = str(int((5.0/9.0) * float(int(high_f) -32)))+ degree_symbol + "C"
        high_f = "High: " + high_f + degree_symbol + "F"
        low_f = dom.getElementsByTagName('forecast_conditions')[0].getElementsByTagName('low')[0].getAttribute('data')
        low_c = str(int((5.0/9.0) * float(int(low_f) -32))) + degree_symbol + "C"
        low_f = "Low: " + low_f + degree_symbol + "F"
       except:
           high_f = ""
           low_f = ""
           high_c = ""
           low_c = ""

       
       chanmsg = "%s / %s / %s%sF %s%sC / %s / %s / %s %s - %s %s" % (city, condition, temp_f,degree_symbol, temp_c, degree_symbol, humidity, wind, high_f, high_c,low_f,low_c)
       e.output = chanmsg.encode('utf-8')
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
       
    url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=" + urllib.quote(zip)
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))
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
        
        degree_symbol = unichr(176)
        chanmsg = "%s / %s / %s%sF %s%sC / %s / %s" % (city, condition, temp_f,degree_symbol, temp_c, degree_symbol, humidity, wind)
        e.output = chanmsg.encode('utf-8')
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

