import json, urllib2, re, botmodules.tools as tools

def gwiki(bot, e):
      url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site:wikipedia.org+' + urllib2.quote(e.input))
      request = urllib2.Request(url, None, {'Referer': 'http://irc.00id.net'})
      response = urllib2.urlopen(request)

      results_json = json.load(response)
      results = results_json['responseData']['results']
      regexstring = "wikipedia.org/wiki/"
      result = results[0]
      m = re.search(regexstring,result['url'])   
      if (m):
         url = result['url']
         url = tools.shorten_url(url.replace('%25','%'))
         #content = result['content'].encode('utf-8')
         
         content = tools.decode_htmlentities(tools.remove_html_tags(result['content'].encode('utf-8', 'ignore')))
         content = re.sub('\s+', ' ', content)
         content = content.replace("...", "")
         #print content
         #content = content.decode('unicode-escape')
         #e.output = content
         e.output = "%s [ %s ]" % (content, url.encode('utf-8', 'ignore'))
      return e
    
gwiki.command = "!gwiki"
get_imdb.helptext = "!gwiki <query> - attempts to look up what you want to know on wikipedia using google's synopsis context"