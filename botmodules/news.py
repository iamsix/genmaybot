import urllib, urllib.request, urllib.error, urllib.parse, xml.dom.minidom, datetime
from bs4 import BeautifulSoup


def google_news(self, e):
    query = urllib.parse.quote(e.input)
    url = ""
    if not query:
        url = "http://news.google.com/news?ned=us&topic=h&output=rss"
    else:
        url = "http://news.google.com/news?q=%s&output=rss" % query

    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    newest_news = dom.getElementsByTagName('item')[0]
    title = newest_news.getElementsByTagName('title')[0].childNodes[0].data
    description = BeautifulSoup(newest_news.getElementsByTagName('description')[0].childNodes[0].data)

    links = description.findAll('a')
    for link in links:
        link.extract()
    links = description.findAll(color='#6f6f6f')
    for link in links:
        link.extract()

    title = title.strip()

    description = str(description)
    description = description.replace("\n", "")

    description = self.tools['remove_html_tags'](description)
#    description = tools.decode_htmlentities(description)
    description = description[0:len(description) - 9]
    description = description.strip()
    if description.rfind(".") != -1:
        description = description[0:description.rfind(".") + 1]

    link = self.tools['shorten_url'](newest_news.getElementsByTagName('link')[0].childNodes[0].data)

    e.output = "%s - %s [ %s ]" % (title, description, link)

    return e

google_news.command = "!news"
google_news.helptext = "Usage: !news - reports the top story. !news <query> reports news containing the specified words"

def get_breaking(self, e):
    #returns the latest earthquake on USGS
      try:       
        description,updated,ago = get_breaking_data()   
        e.output = "%s (%s minutes ago) " % (description, ago)     
        return e
      except:
        return None
get_breaking.command = "!breaking"
get_breaking.helptext = "Usage: !breaking\nShows the latest breaking news alert"

def breaking_alert():
    #returns a new get_quake_data only if it hasn't returned it before - for use in alerts
      try:
        description,updated,ago = get_breaking_data()
        if not breaking_alert.lastcheck:
            breaking_alert.lastcheck = updated
        if updated > breaking_alert.lastcheck :
            breaking_alert.lastcheck = updated     
            return "%s" % (description)
      except Exception as inst: 
          print("breakinglert: " + str(inst))
          pass
breaking_alert.lastcheck = ""
breaking_alert.alert = True


def get_breaking_data():
    request = urllib.request.urlopen("https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=BreakingNews&count=1")
    dom = xml.dom.minidom.parse(request)
    latest_update = dom.getElementsByTagName('item')[0]
    updated = latest_update.getElementsByTagName('pubDate')[0].childNodes[0].data
    description = latest_update.getElementsByTagName('description')[0].childNodes[0].data
    #print description
    updated = datetime.datetime.strptime(updated, "%a, %d %b %Y %H:%M:%S +0000")
    #print updated
    ago = round((datetime.datetime.utcnow() - updated).seconds/60)
    request.close()
    return description, updated, ago

def npr_science(self, e):
    ## Grab the latest entry from the NPR Health and Science RSS feed
    
    url = "http://www.npr.org/rss/rss.php?id=1007"
    
    
    e.output = "%s - %s [ %s ]" % (get_newest_rss(url))

    return e

npr_science.command="!npr-sci"
npr_science.helptext="Usage: !npr-sci\nShows the latest entry from the NPR Health and Science RSS feed"


def get_newest_rss(url):
## Retreive an RSS feed and get the newest item
## Then, nicely format the title and description, and add a shortened URL

    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    newest_news = dom.getElementsByTagName('item')[0]
    title = newest_news.getElementsByTagName('title')[0].childNodes[0].data
    description = BeautifulSoup(newest_news.getElementsByTagName('description')[0].childNodes[0].data)

    links = description.findAll('a')
    for link in links:
        link.extract()
    links = description.findAll(color='#6f6f6f')
    for link in links:
        link.extract()

    title = title.strip()

    description = str(description)
    description = description.replace("\n", "")

    description = self.tools['remove_html_tags'](description)
    description = description[0:len(description) - 9]
    description = description.strip()
    if description.rfind(".") != -1:
        description = description[0:description.rfind(".") + 1]

    link = self.tools['shorten_url'](newest_news.getElementsByTagName('link')[0].childNodes[0].data)
    
    return title, description, link

