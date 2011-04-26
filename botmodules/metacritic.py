from BeautifulSoup import BeautifulSoup
import urllib2, botmodules.tools as tools

def get_metacritic(self, e):
    url = tools.google_url("site:metacritic.com " + e.input, "metacritic.com/")
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
    pagetmp = opener.open(url)
    page = pagetmp.read()
    opener.close()

    page = BeautifulSoup(page)
    title = page.findAll('div',attrs={"class" : "product_title"})[0].a.string.encode("utf-8", 'ignore')
    score = page.findAll('span',attrs={"class" : "score_value"})[0].contents[0].string.encode("utf-8", 'ignore')
    
    e.output = "%s: %s out of 100" % (title, score)
    return e

get_metacritic.command = "!mc"
    
    