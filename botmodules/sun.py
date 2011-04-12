import urllib2, urllib, re, botmodules.tools as tools

def google_sunrise(term):
    return google_sun(term, "Sunrise")
google_sunrise.command = "!sunrise"
    
def google_sunset(term):
    return google_sun(term, "Sunset")
google_sunset.command = "!sunset"

def google_sun(term, sun):
    url = "http://www.google.com/search?hl=en&client=opera&hs=6At&rls=en&q=%s+in+%s&aq=f&aqi=g1&aql=&oq=&gs_rfai=" % (sun, term)
    request = urllib2.Request(url, None, {})
    request.add_header('User-Agent', "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.2.15 Version/10.10")
    request.add_header('Range', "bytes=0-40960")
    response = urllib2.urlopen(request).read()

    if sun == "Sunset":
        m = re.search('(sunset-40.gif.*?\<b\>)(.*?)(\<\/b\> )(.*?)( - \<b\>)(.*?)(\<\/b\> in\s*)(.*?)(\s*?\<tr\>.*?top\"\>)(.*?)(\<\/table\>)', response)
    else:
        m = re.search('(sunrise-40.gif.*?\<b\>)(.*?)(\<\/b\> )(.*?)( -\s*\<b\>)(.*?)(\<\/b\> in\s*)(.*?)(\s*?\<tr\>.*?top\"\>)(.*?)(\<\/table\>)', response)
    #print self.remove_html_tags(m.group(2))
    
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
    result = result.replace("<sup>","^")
    result = result.replace("&#215;","x")
    return tools.remove_html_tags(result)

