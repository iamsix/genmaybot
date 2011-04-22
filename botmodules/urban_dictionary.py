from BeautifulSoup import BeautifulSoup
import urllib2, botmodules.tools as tools



def get_urbandictionary(searchterm, nick):
    url = "http://www.urbandictionary.com/define.php?term=%s" % urllib2.quote(searchterm)
    
    if searchterm=="wotd":
      return get_urbandictionary_wotd()
    
    try:
      opener = urllib2.build_opener()
      opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
      pagetmp = opener.open(url)
      page = pagetmp.read()
      opener.close()

      page = BeautifulSoup(page)
      
      first_definition = page.findAll('div',attrs={"class" : "definition"})[0].contents[0]
      first_definition = tools.decode_htmlentities(first_definition.decode("utf-8", 'ignore')).encode("utf-8", 'ignore')
      first_definition = first_definition.replace("\n", " ")
      first_definition = first_definition[0:420]
      
      first_definition = (searchterm + ": " + first_definition.decode('utf-8') + " [ %s ]" % tools.shorten_url(url)).encode('utf-8', 'ignore')
      
      return first_definition
      
    except:
      print "!ud %s went wrong" % searchterm
      return

get_urbandictionary.command = "!ud" 


def get_urbandictionary_wotd():

  url = "http://www.urbandictionary.com"
  try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
    pagetmp = opener.open(url)
    page = pagetmp.read()
    opener.close()

    page = BeautifulSoup(page)
    first_word = page.findAll('div',attrs={"class" : "word"})[0].contents[1].contents[0]
    first_definition = page.findAll('div',attrs={"class" : "definition"})[0].contents[0]
    first_definition = tools.decode_htmlentities(first_definition.decode("utf-8", 'ignore')).encode("utf-8", 'ignore')
    first_definition = first_definition.replace("\n", " ")

    wotd = (first_word.decode('utf-8') + ": " + first_definition.decode('utf-8') + " [ %s ]" % tools.shorten_url(url)).encode('utf-8', 'ignore')

    return wotd
  except:
    print "!ud wotd went wrong"
    return