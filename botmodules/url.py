# coding=utf-8

import re, urllib.request, urllib.error, urllib.parse, hashlib, datetime, botmodules.tools as tools
import traceback, encodings.idna

import sqlite3
#except ImportError: pass

try: import botmodules.wiki
except ImportError: pass

def url_parser(self, e):
    url = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>])*\))+(?:\(([^\s()<>])*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", e.input)
    #http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    if url:
        url = url.group(0)
        if url[0:4].lower() != "http":
            url = "http://" + url
        e.input = url
        return url_posted(self, e)
    else:
        return None
url_parser.lineparser = True

def url_posted(self, e):
    url = e.input
    #checks if the URL is a dupe (if mysql is enabled)
    #detects if a wikipedia or imdb url is posted and does the appropriate command for it

    repost=""
    days = ""

    if tools.config.sqlmode > 0:
        urlhash = hashlib.sha224(url.encode()).hexdigest()
        conn = sqlite3.connect ("links.sqlite")
        cursor = conn.cursor()
        query = "SELECT reposted, timestamp FROM links WHERE hash='%s'" % urlhash
        result = cursor.execute(query)
        result = cursor.fetchone()
        if result:
            repost="LOL REPOST %s " % (result[0] + 1)

            orig = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.utcnow()
            delta = now - orig

            plural = ""
            if delta.days > 0:
              if delta.days > 1:
                plural = "s"
              days = " (posted %s day%s ago)" % (str(delta.days), plural)
            else:
              hrs = int(round(delta.seconds/3600.0,0))
              if hrs == 0:
                mins = round(delta.seconds/60)
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
    except: 
      print(traceback.print_exc())
      pass
    try: imdb = self.bangcommands["!imdb"](self, e, True)
    except: 
      print(traceback.print_exc())
      pass
    if wiki and wiki.output:
        title = wiki.output
    elif imdb and imdb.output:
        title = imdb.output
    else:
        if url.find("imgur.com") != -1 and url.find("/a/") == -1:
          imgurid =  url[url.rfind('/')+1:url.rfind('/')+6]
          url = "http://imgur.com/" + imgurid
        title = get_title(self, url)
        if title.find("imgur: the simple") != -1:
          title = ""

    title = title.replace("\n", " ")
    title = re.sub('\s+', ' ', title)
    pattern = re.compile('whatsisname', re.IGNORECASE)
    title = pattern.sub('', title)
    title = tools.decode_htmlentities(title)

    titler = "%s%s%s" % (repost, title, days)

    if tools.config.sqlmode == 2:
        cursor.execute("""UPDATE OR IGNORE links SET reposted=reposted+1 WHERE hash = ?""", [urlhash])
        cursor.execute("""INSERT OR IGNORE INTO links(url, hash) VALUES (?,?)""", (url, urlhash))
        conn.commit()

    if tools.config.sqlmode > 0:
        conn.close()

    e.output = titler
    return e

def get_title(self, url):
    #extracts the title tag from a page
    title = ""
    try:
        url = fixurl(url)

        opener = urllib.request.build_opener()
        readlength = 10240
        if url.find("amazon.") != -1:
            readlength = 100096 #because amazon is coded like shit

        opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),
                             ('Range',"bytes=0-" + str(readlength))]


        pagetmp = opener.open(url)
        if pagetmp.headers['content-type'].find("text") != -1:
            page = pagetmp.read(readlength).decode('utf-8')
            opener.close()
            if page.find('meta name="generator" content="MediaWiki') != -1:
                title = botmodules.wiki.read_wiki_page(url)
            else:
                titletmp = tools.remove_html_tags(re.search('(?is)\<title\>.*?<\/title\>',page).group(0))
                title = "Title: " + titletmp.strip()[0:180]
    except Exception as err:
        print(traceback.print_exc())
        print("urlerr: " + url + " " + str(err))
        pass

    return title

def fixurl(url):
    # turn string into unicode
    if not isinstance(url,str):
        url = url.decode('utf8')

    # parse it
    parsed = urllib.parse.urlsplit(url)

    # divide the netloc further
    hostport = parsed.netloc
    host,colon2,port = hostport.partition(':')

    hostnames = host.split(".")
    tmplist = []

    for tmp in hostnames:
        tmp = encodings.idna.ToASCII(tmp).decode()
        tmplist.append(tmp)
	
    host = ".".join(tmplist)

    scheme = parsed.scheme

    path = '/'.join(  # could be encoded slashes!
        urllib.parse.quote(urllib.parse.unquote(pce),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.parse.quote(urllib.parse.unquote(parsed.query),'=&?/')
    fragment = urllib.parse.quote(urllib.parse.unquote(parsed.fragment))

    # put it back together
    netloc = ''.join((host,colon2,port))
    return urllib.parse.urlunsplit((scheme,netloc,path,query,fragment))



def last_link(self, e):
    #displays last link posted (requires mysql)
    if tools.config.sqlmode > 0:
      conn = sqlite3.connect ("links.sqlite")
      cursor = conn.cursor()
      if (cursor.execute("SELECT url FROM links ORDER BY rowid DESC LIMIT 1")):
        result = cursor.fetchone()
        url = result[0]

      conn.close()
      e.output = "[ " + url + " ] " + get_title(self, url)
      return e
    else:
      return None
last_link.command = "!lastlink"
last_link.helptext = "Usage: !lastlink\nShows the last URL that was posted in the channel"

