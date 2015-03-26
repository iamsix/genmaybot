import urllib.request, urllib.parse, xml.dom.minidom

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
    
    
    # %s gets substituted with variables in % (foo, bar)
    output = "%s by %s (%s) | Avg rating: %s (%s ratings)" % (firsttitle, name, pubyear, avgrating, ratingscount)    
    e.output = output

    return e
        


get_goodreads_book_rating.command = "!gr"
get_goodreads_book_rating.helptext = "Usage: !gr <book title> Retrieves book ratings from Goodreads."
