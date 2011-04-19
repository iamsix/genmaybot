from BeautifulSoup import BeautifulSoup
import re, urllib2, botmodules.tools as tools

def get_imdb(searchterm, nick, urlposted=False):  
    #reads title, rating, and movie description of movie titles 
     if urlposted:
         url = searchterm
     else:
         url = tools.google_url("site:imdb.com/title " + searchterm,"imdb.com/title/tt\\d{7}/")
         
     title = "" 
     if not url:
       pass
     elif url.find("imdb.com/title/tt") != -1:
       try:
         movietitle = ""
         rating = ""
         summary = ""
         imdbid = re.search("tt\\d{7}", url)
         imdburl = ('http://www.imdb.com/title/' + imdbid.group(0) + '/')
         opener = urllib2.build_opener()
         opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),
                              ('Range', "bytes=0-40960")]
         pagetmp = opener.open(imdburl)
         page = BeautifulSoup(pagetmp.read(40960))
         opener.close()
         
         movietitle = tools.decode_htmlentities(tools.remove_html_tags(str(page.find('title'))).replace(" - IMDb", ""))
         movietitle = "Title: " + movietitle

         
         if page.find(id="overview-top") != None:
             page = page.find(id="overview-top").extract()
             
             if page.find(id="star-bar-user-rate") != None:
                 rating = tools.remove_html_tags(str(page.find(id="star-bar-user-rate").b))
                 rating = " - Rating: " + rating
             
             if len(page.findAll('p')) == 2:

                 summary = str(page.findAll('p')[1])
         
                 removelink = re.compile(r'\<a.*\/a\>')
                 summary = removelink.sub('',summary)
                 summary = tools.remove_html_tags(summary)
                 summary = summary.replace('&raquo;', "")
                 summary = tools.decode_htmlentities(summary.decode("utf-8", 'ignore'))
                 summary = re.sub("\&.*?\;", " ", summary)
                 summary = summary.replace("\n", " ")
                 summary = " - " + summary
                 
         title = movietitle + rating + summary       
         if not urlposted:
             title = title + " [ %s ]" % url
       except Exception as inst: 
         print "!imdb " + searchterm + ": " + str(inst)
         
#        IMDBAPI CODE
#        -not in use because it's unreliable
#           try:
#              imdbid = re.search("tt\\d{7}", url)
#              imdburl = ('http://www.imdbapi.com/?i=&t=' + imdbid.group(0))
#              request = urllib2.Request(imdburl, None, {'Referer': ''})
#              response = urllib2.urlopen(request)
#              results = json.load(response)
#              title = "Title: " + results['Title'] + " (" + results['Year'] + ") - Rating: " + results['Rating'] + " - " + results['Plot']
#              response.close()
#              title = title.encode('utf-8')
#
#           except:
#              pass
      
     return title.encode('utf-8', 'ignore')
get_imdb.command = "!imdb"
