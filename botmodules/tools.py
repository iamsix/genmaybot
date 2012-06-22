import re, urllib.request, urllib.error, urllib.parse, urllib, json, configparser, traceback
from html.entities import name2codepoint as n2cp

def decode_htmlentities(string):
    #decodes things like &amp
    entity_re = re.compile("&(#?)(x?)(\w+);")
    return entity_re.subn(substitute_entity, string)[0]

def substitute_entity(match):
  try:
    ent = match.group(3)
    
    if match.group(1) == "#":
        if match.group(2) == '':
            return chr(int(ent))
        elif match.group(2) == 'x':
            return chr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return chr(cp)
        else:
            return match.group()
  except:
      return ""
  
def remove_html_tags(data):
    #removes all html tags from a given string
      p = re.compile(r'<.*?>')
      return p.sub('', data)
  
def google_url(searchterm, regexstring):
    url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + urllib.parse.quote(searchterm))
    request = urllib.request.Request(url, None, {'Referer': 'http://irc.00id.net'})
    response = urllib.request.urlopen(request)

    results_json = json.loads(response.read().decode('utf-8'))
    results = results_json['responseData']['results']
  
    for result in results:
        m = re.search(regexstring,result['url'])   
        if (m):
           url = result['url']
           url = url.replace('%25','%')
           return url
    return
  
def shorten_url(url):
    #goo.gl url shortening service, not used directly but used by some commands
  try:
    values =  json.dumps({'longUrl' : url})
    headers = {'Content-Type' : 'application/json'}
    requestUrl = "https://www.googleapis.com/urlshortener/v1/url"
    req = urllib.request.Request (requestUrl, values, headers)
    response = urllib.request.urlopen (req)
    results = json.loads(response.read().decode('utf-8'))
    shorturl = results['id']
    return shorturl
  except:
    traceback.print_exc()
    return ""

def config():
    #placeholder used to hold configs used by various modules
    pass
cfg = configparser.ConfigParser()
cfg.readfp(open('genmaybot.cfg'))
config.fmlAPIkey = cfg.get("APIkeys","fmlAPIkey")
config.wolframAPIkey = cfg.get("APIkeys","wolframAPIkey")
config.rtAPIkey = cfg.get("APIkeys","rtAPIkey")
config.sqlpassword = cfg.get("mysql","sqlpassword")
config.sqlusername = cfg.get("mysql","sqlusername")
config.sqlmode = cfg.getint("mysql","mysqlmode")
