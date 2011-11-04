import urllib2, xml.dom.minidom, datetime


def get_quake(self, e):
    #returns the latest earthquake on USGS
      try:       
        qtitle,updated,ago,elevation = get_quake_data()   
        e.output = "Latest Earthquake: %s - Depth: %s (%s minutes ago) " % (qtitle, elevation, ago)     
        return e
      except:
        return None
get_quake.command = "!q"
get_quake.helptext = "Usage: !q\nShows the latest earthquake larger than M2.5 and how long ago it occured"

def quake_alert():
    #returns a new get_quake_data only if it hasn't returned it before - for use in alerts
      try:
        qtitle,updated,ago, elevation = get_quake_data()
        if not quake_alert.lastquakecheck:
            quake_alert.lastquakecheck = updated
        if updated > quake_alert.lastquakecheck :
            quake_alert.lastquakecheck = updated     
            return "Latest Earthquake: %s: Depth - %s (%s minutes ago) " % (qtitle, elevation, ago)
      except Exception as inst: 
          print "quakealert: " + str(inst)
          pass
quake_alert.lastquakecheck = ""
quake_alert.alert = True


def get_quake_data():
    request = urllib2.urlopen("http://earthquake.usgs.gov/earthquakes/catalogs/1day-M2.5.xml")
    dom = xml.dom.minidom.parse(request)
    latest_quakenode = dom.getElementsByTagName('entry')[0]
    updated = latest_quakenode.getElementsByTagName('updated')[0].childNodes[0].data
    qtitle = latest_quakenode.getElementsByTagName('title')[0].childNodes[0].data
    updated = datetime.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")
    ago = (datetime.datetime.utcnow() - updated).seconds/60
    elevation = int(latest_quakenode.getElementsByTagName('georss:elev')[0].childNodes[0].data)
    depth = float(elevation) / -1000
    depthmi = '{0:.3}'.format(depth / 1.61)
    depthstring = "%s km (%s mi)" % (depth, depthmi)
    request.close()
    return qtitle, updated, ago, depthstring

