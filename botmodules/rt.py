import json
import urllib.request
import urllib.parse
import re
import gzip


def get_rt(self, e):
    url = "http://api.flixster.com/android/api/v14/movies.json?cbr=1&filter={}"
    url = url.format(urllib.parse.quote(e.input))
    movie = loadjson(url)
    flxurl = "http://api.flixster.com/android/api/v1/movies/{}.json".format(movie[0]['id'])
    movie = loadjson(flxurl)

    url = self.tools['shorten_url'](movie['urls'][2]['url'])

    concensus = movie['reviews']['rottenTomatoes']['consensus']
    concensus = "- " + self.tools['remove_html_tags'](concensus)

    e.output = "%s (%s) - Critics: %s - Users: %s %s [ %s ]" % (movie['title'],
                                                                str(movie['theaterReleaseDate']['year']),
                                                                str(movie['reviews']['rottenTomatoes']['rating']),
                                                                str(movie['reviews']['flixster']['popcornScore']),
                                                                concensus,
                                                                url)

    return e
get_rt.command = "!rt"

def loadjson(url):
    response = urllib.request.urlopen(url).read()
    try:
        #RT likes to randomly give us gzipped data even though we never requested it
        response = gzip.decompress(response)
    except:
        pass
    response = response.decode("utf-8", "replace")
    return json.loads(response)
