import urllib2, xml.dom.minidom, datetime


def get_quake(nothing):
    #returns the latest earthquake on USGS
      try:       
        request = urllib2.urlopen("http://earthquake.usgs.gov/earthquakes/catalogs/1day-M2.5.xml")
        dom = xml.dom.minidom.parse(request)

        latest_quakenode = dom.getElementsByTagName('entry')[0]
        qtitle = latest_quakenode.getElementsByTagName('title')[0].childNodes[0].data
        request.close()
        
        return "Latest Earthquake: " + qtitle  
      except:
        pass
get_quake.command = "!q"


def quake_alert():
    #returns a new quake only if it hasn't returned it before - for use in alerts
      try:       
        request = urllib2.urlopen("http://earthquake.usgs.gov/earthquakes/catalogs/1day-M2.5.xml")
        dom = xml.dom.minidom.parse(request)
        latest_quakenode = dom.getElementsByTagName('entry')[0]
        updated = latest_quakenode.getElementsByTagName('updated')[0].childNodes[0].data
        qtitle = latest_quakenode.getElementsByTagName('title')[0].childNodes[0].data
        updated = datetime.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")
        request.close()
        if not quake_alert.lastquakecheck:
            quake_alert.lastquakecheck = updated
        if updated > quake_alert.lastquakecheck :
            quake_alert.lastquakecheck = updated     
            return "Latest Earthquake: " + qtitle
      except Exception as inst: 
          print "quakealert: " + str(inst)
          pass

quake_alert.lastquakecheck = ""
quake_alert.alert = True