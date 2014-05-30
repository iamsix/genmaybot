import urllib.request
import xml.etree.ElementTree as ET

def metar(self, e):
  station = e.input.split(' ')[0]
  url = 'http://aviationweather.gov/adds/dataserver_current/httpparam?' \
  + 'dataSource=metars&requestType=retrieve&format=xml&stationString=' \
  + station \
  + '&hoursBeforeNow=2&mostRecent=true'
  response = urllib.request.urlopen(url)
  xml = ET.parse(response)
  print(url)
  print(response)
  print(xml)
  e.output = xml.getroot().find('raw_text').text
  return e
  
metar.command = '!metar'
