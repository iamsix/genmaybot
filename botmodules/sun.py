import urllib2, urllib, re, botmodules.tools as tools
try: import botmodules.userlocation as user
except: pass

def google_sunrise(self, e):
    #returns the next sunrise time and time from now of the place specified
    e.output = google_sun(e.input, "Sunrise", e.nick)
    return e
google_sunrise.command = "!sunrise"
google_sunrise.helptext = "Usage: !sunrise <location>\nExample: !sunrise las vegas, nv\nShows the time of sunrise at a given location\nUse !setlocation <location> to save your location\nThen, using !sunrise without arguments will always show sunrise at your location"
    
def google_sunset(self, e):
    #returns the next sunset time and time from now of the place specified
    e.output = google_sun(e.input, "Sunset", e.nick)
    return e
google_sunset.command = "!sunset"
google_sunset.helptext = "Usage: !sunset <location>\nExample: !sunrise las vegas, nv\nShows the time of sunrise at a given location\nUse !setlocation <location> to save your location\nThen, using !sunrise without arguments will always show sunset at your location"

def google_sun(term, sun, nick):
    if term == "" and user:
       term = user.get_location(nick)
    term = urllib.quote(term)
    url = "http://www.google.com/search?hl=en&client=opera&hs=6At&rls=en&q=%s+in+%s&aq=f&aqi=g1&aql=&oq=&gs_rfai=" % (sun, term)
    request = urllib2.Request(url, None, {})
    request.add_header('User-Agent', "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.2.15 Version/10.10")
    request.add_header('Range', "bytes=0-40960")
    response = urllib2.urlopen(request).read()

    m = re.search('(-40.gif.*?\<b\>)(.*?)(\<\/b\> )(.*?)( -\s*\<b\>)(.*?)(\<\/b\> in\s*)(.*?)(\s*?\<tr\>.*?top\"\>)(.*?)(\<\/table\>)', response)
    
    try:
      settime = m.group(2)
      setday = m.group(4)
      setday = re.sub("\s+"," ",setday)
      setword = m.group(6)
      setcity = m.group(8)
      settimeword = m.group(10)
      
      result = "%s in %s: %s %s (%s)" % (sun, setcity,settime,setday,settimeword)
   
      #print result
    except:
      pass
      return

    return tools.remove_html_tags(result)

