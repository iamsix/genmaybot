from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse, botmodules.tools as tools



def get_urbandictionary(self, e):
     searchterm = e.input
     url = "http://www.urbandictionary.com/define.php?term=%s" % urllib.parse.quote(searchterm)
     
     if searchterm=="wotd":
          e.output = get_urbandictionary_wotd()
          return e

     if searchterm== "":
          url = "http://www.urbandictionary.com/random.php"
    
     opener = urllib.request.build_opener()
     opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
     pagetmp = opener.open(url)
     page = pagetmp.read().decode('utf-8')
     
     url = pagetmp.geturl()
     opener.close()

     page = BeautifulSoup(page)
     first_definition= ""

     if page.find(id='not_defined_yet') != None:
          return None

	## depending on the search results the first word may be contained directly under the <td class='word'> tag
	## or it may be the text contents of a <a href> tag
	## we first try to get it from inside a <td><a href>[word]</a></td> type structure
	## if that fails, get the word under the initial <td> tag

     try:
          first_word = page.findAll('td',attrs={"class" : "word"})[0].contents[1].string
     except:
          first_word = page.findAll('td',attrs={"class" : "word"})[0].contents[0].string     
      
     first_word = first_word.replace("\n","")


     for content in page.findAll('div',attrs={"class" : "definition"})[0].contents:
          if content.string != None:
               first_definition += content.string

     #first_definition = first_definition.encode("utf-8", 'ignore')
     first_definition = tools.decode_htmlentities(first_definition)
     first_word = tools.decode_htmlentities(first_word)

     first_definition = first_definition.replace("\n", " ")
     first_definition = first_definition.replace("\r", " ")
     first_definition = first_definition[0:392]

     first_definition = ((first_word + ": " + first_definition) + " [ %s ]" % tools.shorten_url(url))
     #print first_definition
     e.output = first_definition
     return e
      


get_urbandictionary.command = "!ud"
get_urbandictionary.helptext = "Usage: !ud <word or phrase>\nExample: !ud hella\nShows urbandictionary definition of a word or phrase.\n!ud alone returns a random entry\n!ud wotd returns the current word of the day"


def get_urbandictionary_wotd():

  url = "http://www.urbandictionary.com"
  try:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
    pagetmp = opener.open(url)
    page = pagetmp.read()
    opener.close()

    page = BeautifulSoup(page)
    
    first_definition = ""
    
    first_word = page.findAll('div',attrs={"class" : "word"})[0].contents[1].contents[0].string
    first_word = first_word.encode("utf-8", 'ignore')
    
    
    for content in page.findAll('div',attrs={"class" : "definition"})[0].contents:
      if content.string != None:
        first_definition += content.string


    first_definition = tools.decode_htmlentities(first_definition)
    first_definition = first_definition.replace("\n", " ")

    wotd = (first_word.decode('utf-8') + ": " + first_definition + " [ %s ]" % tools.shorten_url(url))

    return wotd
  except:
    print("!ud wotd went wrong")
    return