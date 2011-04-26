import re, urllib2, hashlib, datetime, botmodules.tools as tools

try: import MySQLdb
except ImportError: pass

def url_parser(self, e):
    url = re.search("(?P<url>https?://[^\s]+)", e.input)
    if url:
        e.input = url.group(1)
        return url_posted(self, e)
    else:
        return None
url_parser.lineparser = True

def url_posted(self, e):
  url = e.input
    #checks if the URL is a dupe (if mysql is enabled)
    #detects if a wikipedia or imdb url is posted and does the appropriate command for it

  try:

    repost=""
    days = ""
    
    if tools.config.sqlmode > 0:
        urlhash = hashlib.sha224(url).hexdigest()

        conn = MySQLdb.connect (host = "localhost",
                                  user = tools.config.sqlusername,
                                  passwd = tools.config.sqlpassword,
                                  db = "irc_links")   
        cursor = conn.cursor()
        query = "SELECT reposted, timestamp FROM links WHERE hash='%s'" % urlhash
        result = cursor.execute(query)
        
        if result !=0:
            result = cursor.fetchone()
            
            repost="LOL REPOST %s " % (result[0] + 1)
        
            orig = result[1]
            now = datetime.datetime.now()
            delta = now - orig
                     
            plural = ""
            if delta.days > 0:
              if delta.days > 1:
                plural = "s"
              days = " (posted %s day%s ago)" % (str(delta.days), plural)
            else:
              hrs = int(round(delta.seconds/3600.0,0))
              if hrs == 0:
                mins = delta.seconds/60
                if mins > 1:
                  plural = "s"
                days = " (posted %s minute%s ago)" % (str(mins), plural)
                if mins == 0:
                    repost=""
                    days=""
              else:
                if hrs > 1:
                  plural = "s"
                days = " (posted %s hour%s ago)" % (str(hrs), plural)
            
    title = "" 
    
    try: wiki = self.bangcommands["!wiki"](self, e, True)
    except: pass
    try: imdb = self.bangcommands["!imdb"](self, e, True)
    except: pass
    if wiki and wiki.output:
        title = wiki.output
    elif imdb and imdb.output:
        title = imdb.output
    else:
        if url.find("imgur.com") != -1:
          imgurid =  url[url.rfind('/')+1:url.rfind('/')+6]
          url = "http://imgur.com/" + imgurid
        title = get_title(url)
        if title.find("imgur: the simple") != -1:
          title = ""

    title = title.replace("\n", " ")
    pattern = re.compile('whatsisname', re.IGNORECASE)
    title = pattern.sub('', title)      
    title = tools.decode_htmlentities(title.decode("utf-8", 'ignore')).encode("utf-8", 'ignore')

    titler = "%s%s%s" % (repost, title, days)
    
    if tools.config.sqlmode == 2:
        title = MySQLdb.escape_string(title)
        url = MySQLdb.escape_string(url)
        query = "INSERT INTO links (url, title, hash) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE reposted=reposted+1,title='%s'" % (url, title, urlhash, title)       
        cursor.execute(query)
    if tools.config.sqlmode > 0:
        conn.close()
        
    e.output = titler
    return e

  
  except Exception as inst: 
    print url + ": " + str(inst)
    pass
  return

def get_title(url):
    #extracts the title tag from a page
    title = ""
    try:
        opener = urllib2.build_opener()
        readlength = 10240
        if url.find("amazon.") != -1: 
            readlength = 100096 #because amazon is coded like shit
            
        opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),    
                             ('Range',"bytes=0-" + str(readlength))]

        pagetmp = opener.open(url)
        page = pagetmp.read(readlength)
        opener.close()
        
        titletmp = tools.remove_html_tags(re.search('(?is)\<title\>.*\<\/title\>',page).group(0))
        title = "Title: " + titletmp.strip()[0:180]
    except:
        pass
        
    return title

def last_link(self, e):
    #displays last link posted (requires mysql)
    if tools.config.sqlmode > 0:
      conn = MySQLdb.connect (host = "localhost",
                                user = tools.config.sqlusername,
                                passwd = tools.config.sqlpassword,
                                db = "irc_links")
                                
      cursor = conn.cursor()
      if (cursor.execute("SELECT url FROM links ORDER BY id DESC LIMIT 1")):
        result = cursor.fetchone()
        url = result[0]

      conn.close()
      e.output = "[ " + url + " ] " + get_title(url)
      return e
    else:
      return None
last_link.command = "!lastlink"
last_link.helptext = "Usage: !lastlink\nShows the last URL that was posted in the channel"

