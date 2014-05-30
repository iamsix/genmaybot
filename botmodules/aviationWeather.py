import urllib.request
import xml.etree.ElementTree as ET

def metar(self, e):
  station = e.input.split(' ')[0]
  url = 'https://aviationweather.gov/adds/dataserver_current/httpparam?' \
  + 'dataSource=metars&requestType=retrieve&format=xml&stationString=' \
  + station \
  + '&hoursBeforeNow=2&mostRecent=true'
  xml = ET.parse(urllib.request.urlopen(url))
  e.output = xml.getroot().find('raw_text').text
  return e
  
metar.command = '!metar'
