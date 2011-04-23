from BeautifulSoup import BeautifulSoup
import re, urllib2, botmodules.tools as tools

def get_wiki(searchterm, nick, urlposted=False):
    #read the first paragraph of a wikipedia article
  if urlposted:
      url = searchterm
  else:
      url = tools.google_url("site:wikipedia.org " + searchterm,"wikipedia.org/wiki")
  
  title = ""    
  if not url:
      pass
  elif url.find("wikipedia/wiki/File:") != -1:
    return get_wiki_file_description(url)
    
  elif url.find("wikipedia.org/wiki/") != -1:

    try:
      opener = urllib2.build_opener()
      opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
      pagetmp = opener.open(url)
      page = pagetmp.read()
      opener.close()

      if url.find('#') != -1:
        anchor = url.split('#')[1]
        page = page[page.find('id="' + anchor):]

      page = BeautifulSoup(page)
      tables = page.findAll('table')
      for table in tables:
        table.extract()
        
      page = page.findAll('p')
      if str(page[0])[0:9] == '<p><span ':
          page = unicode(page[1].extract())
      else:
          page = unicode(page[0].extract())

      title = tools.remove_html_tags(re.search('(?s)\<p\>(.*?)\<\/p\>',page).group(1))
      title = title.encode("utf-8", 'ignore')
      title = title.replace("<","");
      rembracket = re.compile(r'\[.*?\]')
      title = rembracket.sub('',title)
      #title = re.sub("\&.*?\;", " ", title)
      title = title.replace("\n", " ")
      
      title = tools.decode_htmlentities(title.decode("utf-8", 'ignore')).encode("utf-8", 'ignore')

      title = title[0:420]
      if title.rfind(".")!=-1:
        title = title[0:title.rfind(".")+1]
        
      if not urlposted:
        title = (title.decode('utf-8') + " [ %s ]" % tools.shorten_url(url)).encode('utf-8', 'ignore')
    except Exception as inst: 
      print "!wiki " + searchterm + " : " + str(inst)
      title = tools.remove_html_tags(re.search('\<p\>(.*?\.) ',str(page)).group(1))

  return title
get_wiki.command = "!wiki"
get_wiki.helptext = "Usage: !wiki <search term>\nExample: !wiki carl sagan\nShows the first couple of sentences of a wikipedia entry for the given search term"


def get_wiki_file_description(url):
  try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
    pagetmp = opener.open(url)
    page = pagetmp.read()
    opener.close()

    page = BeautifulSoup(page)
    
    desc = page.findAll("div",attrs={"class":"description en"})[0].contents[1].string
    title = title.encode("utf-8", 'ignore')
    title = tools.decode_htmlentities(title.decode("utf-8", 'ignore')).encode("utf-8", 'ignore')
    title = title[0:420]
    if title.rfind(".")!=-1:
      title = title[0:title.rfind(".")+1]
      
    return desc.decode('utf-8')
    
  except:
      return