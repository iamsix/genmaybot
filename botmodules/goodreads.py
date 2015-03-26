import urllib.request, urllib.parse, xml.dom.minidom, re

def get_goodreads_book_rating(self, e):
    
    # Read the API key from the main bot object. It loads the config for us.
    goodreadskey = self.botconfig["APIkeys"]["goodreadskey"]
    
    query = urllib.parse.urlencode({"key":goodreadskey, "q":e.input}) #Pass the command input directly into the URL query
    url = "https://www.goodreads.com/search.xml"

    #Load XML response and parse DOM in one shot
    dom = xml.dom.minidom.parse(urllib.request.urlopen("%s?%s" % (url,query)))

    firsttitle = dom.getElementsByTagName("title")[0].firstChild.nodeValue

    # At this point `firsttitle` contains the title of the first book found by Goodreads
    
    name = dom.getElementsByTagName("name")[0].firstChild.nodeValue
    avgrating = dom.getElementsByTagName("average_rating")[0].firstChild.nodeValue
    ratingscount = dom.getElementsByTagName("ratings_count")[0].firstChild.nodeValue
    pubyear = dom.getElementsByTagName("original_publication_year")[0].firstChild.nodeValue
    
    #No idea wtf is going on here v
    bookid = dom.getElementsByTagName("best_book")[0].getElementsByTagName("id")[0].firstChild.nodeValue
    #No idea wtf is going on here ^
    
    
    bookurl = "https://www.goodreads.com/book/show/%s" % bookid
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', "Opera/9.10 (YourMom 8.0)")]
    
    
    bookpage = opener.open(bookurl).read
    bookdesc = re.search('''<meta property="og:description" content="(.*)"/>''', bookpage).group(1)
    
    
    bookurl = self.tools['shorten_url'](bookurl)
    
    # %s gets substituted with variables in % (foo, bar)
    output = "%s by %s (%s) | %s | Avg rating: %s (%s ratings) - [ %s ]" % (firsttitle, name, pubyear, bookdesc, avgrating, ratingscount, bookurl)    
    e.output = output

    return e
        


get_goodreads_book_rating.command = "!gr"
get_goodreads_book_rating.helptext = "Usage: !gr <book title> Retrieves book ratings from Goodreads."
