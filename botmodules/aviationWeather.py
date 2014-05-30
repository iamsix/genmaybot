import urllib.request
import xml.etree.ElementTree as ET

def metar(self, e):
  station = e.input.split(' ')[0]
  url = 'http://aviationweather.gov/adds/dataserver_current/httpparam?' \
  + 'dataSource=metars&requestType=retrieve&format=xml&stationString=' \
  + station \
  + '&hoursBeforeNow=2&mostRecent=true'
  xml =  xml.dom.minidom.parse(urllib.request.urlopen(url))
  e.output = xml.getElementsByTagName('raw_text')[0].data
  return e
  
metar.command = '!metar'
