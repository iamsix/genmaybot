import urllib, urllib2, xml.dom.minidom, botmodules.tools as tools
from BeautifulSoup import BeautifulSoup

def google_news (self, e):
    query = urllib.quote(e.input)
    url = ""
    if not query:
        url = "http://news.google.com/news?ned=us&topic=h&output=rss"
    else:
        url = "http://news.google.com/news?q=%s&output=rss" % query
    
           
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))
    newest_news = dom.getElementsByTagName('item')[0]
    title = newest_news.getElementsByTagName('title')[0].childNodes[0].data
    description = BeautifulSoup(newest_news.getElementsByTagName('description')[0].childNodes[0].data)
    
    links = description.findAll('a')
    for link in links:
        link.extract()          
    links = description.findAll(color='#6f6f6f')
    for link in links:
        link.extract()
    
    description = str(description).strip().decode("utf-8", 'ignore')
    description = tools.remove_html_tags(description)
    description = tools.decode_htmlentities(description)
    description = description[0:len(description) - 9]
    if description.rfind(".")!=-1:
        description = description[0:description.rfind(".")+1]
    link = tools.shorten_url(newest_news.getElementsByTagName('link')[0].childNodes[0].data)
    
    e.output = "%s - %s [ %s ]" % (title.encode("utf-8", 'ignore'), description.encode("utf-8", 'ignore'), link.encode("utf-8", 'ignore'))
    
    return e
    
google_news.command = "!news"
google_news.helptext = "Usage: !news"