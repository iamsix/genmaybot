import urllib.request
import xml.dom.minidom

def metar(self, e):
  station = e.input.split(' ')[0]
  url = 'http://aviationweather.gov/adds/dataserver_current/httpparam?' \
  + 'dataSource=metars&requestType=retrieve&format=xml&stationString=' \
  + station \
  + '&hoursBeforeNow=2&mostRecent=true'
  dom =  xml.dom.minidom.parse(urllib.request.urlopen(url))
  e.output = dom.getElementsByTagName('raw_text')[0].childNodes[0].data
  return e
  
metar.command = '!metar'
