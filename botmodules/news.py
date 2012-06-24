import urllib, urllib.request, urllib.error, urllib.parse, xml.dom.minidom, botmodules.tools as tools
from bs4 import BeautifulSoup

def google_news (self, e):
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
    description = description.replace("\n","")

    description = tools.remove_html_tags(description)
#    description = tools.decode_htmlentities(description)
    description = description[0:len(description) - 9]
    description = description.strip()
    if description.rfind(".")!=-1:
        description = description[0:description.rfind(".")+1]
    
    link = tools.shorten_url(newest_news.getElementsByTagName('link')[0].childNodes[0].data)
    
    e.output = "%s - %s [ %s ]" % (title, description, link)
    
    return e
    
google_news.command = "!news"
google_news.helptext = "Usage: !news - reports the top story. !news <query> reports news containing the specified words"
