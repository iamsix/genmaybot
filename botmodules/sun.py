import urllib2, urllib, re, botmodules.tools as tools

def google_sunrise(term):
    #returns the next sunrise time and time from now of the place specified it 'term'
    return google_sun(term, "Sunrise")
google_sunrise.command = "!sunrise"
    
def google_sunset(term):
    #returns the next sunset time and time from now of the place specified it 'term'
    return google_sun(term, "Sunset")
google_sunset.command = "!sunset"

def google_sun(term, sun):
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

