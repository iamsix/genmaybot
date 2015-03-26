import urllib.request, urllib.parse, xml.dom.minidom, re

def get_goodreads_book_rating(self, e):
    
    # Read the API key from the main bot object. It loads the config for us.
    goodreadskey = self.botconfig["APIkeys"]["goodreadskey"]
    
    query = urllib.parse.urlencode({"key":goodreadskey, "q":e.input}) #Pass the command input directly into the URL query
    url = "https://www.goodreads.com/search.xml"

    #Load XML response and parse DOM in one shot
    dom = xml.dom.minidom.parse(urllib.request.urlopen("%s?%s" % (url,query)))


    # This finds the first `title` tag and gets its text value
    firsttitle = dom.getElementsByTagName("title")[0].firstChild.nodeValue

    # At this point `firsttitle` contains the title of the first book found by Goodreads
    
    # These all do the same as above, first name, first rating, etc
    name = dom.getElementsByTagName("name")[0].firstChild.nodeValue
    avgrating = dom.getElementsByTagName("average_rating")[0].firstChild.nodeValue
    ratingscount = dom.getElementsByTagName("ratings_count")[0].firstChild.nodeValue
    pubyear = dom.getElementsByTagName("original_publication_year")[0].firstChild.nodeValue
    
    #Find the first `best_book` tag and then inside of that get the first `id` tag's value
    bookid = dom.getElementsByTagName("best_book")[0].getElementsByTagName("id")[0].firstChild.nodeValue
 
    
    # Set the URL to the user friendly URL you would load in your web browser
    bookurl = "https://www.goodreads.com/book/show/%s" % bookid
    
    # This lets us add custom headers to HTTP requests and other more complicated things
    opener = urllib.request.build_opener()
    
    # Add the 'User-Agent' header to trick the site that we're using an actual web browser (rekt)
    opener.addheaders = [('User-Agent', "Opera/9.10 (YourMom 8.0)")]
    
    # This downloads the actual HTML page, in binary form, encoded in UTF-8, so we read it and decode it
    bookpage = opener.open(bookurl).read().decode('utf-8')
    
    # Regular expression to find the description META tag
    # This matches first: <meta property="og:description" content="
    # Then we look for zero or more characters in (.*) -> later refered to by .group(1) - parenthesis in regular expressions form 'groups'
    # Then we end the matching line with: "/>
    #
    # Example line: <meta property="og:description" content="The irresistible, ever-curious, and always best-selling Mary Roach returns with a new adventure to the invisible realm we carry around in..."/>
    bookdesc = re.search('<meta property="og:description" content="(.*)"/>', bookpage).group(1)
    try:
        bookdesc = re.search('^(.*[\.|\?])\s.*?\.\.\.', bookdesc).group(1)
    except:
        pass
    
    
    # Use the bot function to Google shorten the URL
    bookurl = self.tools['shorten_url'](bookurl)
    
    # %s gets substituted with variables in % (foo, bar)
    output = "%s by %s (%s) | Avg rating: %s (%s ratings) | %s [ %s ]" % (firsttitle, name, pubyear, avgrating, ratingscount, bookdesc, bookurl)    
    e.output = output

    return e
        


get_goodreads_book_rating.command = "!gr"
get_goodreads_book_rating.helptext = "Usage: !gr <book title> Retrieves book ratings from Goodreads."

# HOLD
