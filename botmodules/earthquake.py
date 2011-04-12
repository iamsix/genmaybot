import urllib2, xml.dom.minidom


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


def quake_alert(context, channels):
    #alerts (in near-realtime) all joined channels about new quakes
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
            self.lastquakecheck = updated     
            for channel in channels:  
                context.privmsg(channel, "Latest Earthquake: " + qtitle)
      except Exception as inst: 
          print inst
          pass
      
      t=threading.Timer(60,quake_alert, [context])
      t.start()
quake_alert.lastquakecheck = ""
quake_alert.alert = True