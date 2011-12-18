import urllib2, xml.dom.minidom, datetime


def get_bbc(self, e):
    #returns the latest earthquake on USGS
      try:       
        description,updated,ago = get_bbc_data()   
        e.output = "%s (%s minutes ago) " % (description, ago)     
        return e
      except:
        return None
get_bbc.command = "!bbc"
get_bbc.helptext = "Usage: !bbc\nShows the latest BBC breaking news alert"

def bbc_alert():
    #returns a new get_quake_data only if it hasn't returned it before - for use in alerts
      try:
        description,updated,ago = get_bbc_data()
        if not bbc_alert.lastcheck:
            bbc_alert.lastcheck = updated
        if updated > bbc_alert.lastcheck :
            bbc_alert.lastcheck = updated     
            return "%s" % (description)
      except Exception as inst: 
          print "bbclert: " + str(inst)
          pass
bbc_alert.lastcheck = ""
bbc_alert.alert = True


def get_bbc_data():
    request = urllib2.urlopen("https://twitter.com/statuses/user_timeline/5402612.rss")
    dom = xml.dom.minidom.parse(request)
    latest_update = dom.getElementsByTagName('item')[0]
    updated = latest_update.getElementsByTagName('pubDate')[0].childNodes[0].data
    description = latest_update.getElementsByTagName('description')[0].childNodes[0].data
    #print description
    updated = datetime.datetime.strptime(updated, "%a, %d %b %Y %H:%M:%S +0000")
    #print updated
    ago = (datetime.datetime.utcnow() - updated).seconds/60
    request.close()
    return description, updated, ago

