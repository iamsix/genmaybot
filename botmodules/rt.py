import json, urllib2, botmodules.tools as tools

def get_rt(self, e):
    url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=%s&q=%s&page_limit=1" % (tools.config.rtAPIkey, urllib2.quote(e.input) )
    response = urllib2.urlopen(url).read() 
    movie = json.loads(response)
    movie = movie['movies'][0]
    e.output = "%s (%s) - Critics: %s - Users: %s - %s" % (movie['title'], str(movie['year']), str(movie['ratings']['critics_score']), str(movie['ratings']['audience_score']), movie['critics_consensus'] )
    return e
    
get_rt.command = "!rt"