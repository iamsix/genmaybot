import json, urllib2, random
def get_cat(self, e):
    url = "http://www.reddit.com/r/catpictures/.json"
    e.output = get_redditpics(url)
    return e     
get_cat.command = "!cats"

def get_dog(self, e):
    url = "http://www.reddit.com/r/dogpictures/.json"
    e.output = get_redditpics(url)
    return e
get_dog.command = "!dogs"

def get_bird(self, e):
    url = "http://www.reddit.com/r/birdpics/.json"
    e.output = get_redditpics(url)
    return e
get_bird.command = "!birds"

def get_cacti(self, e):
    url = "http://www.reddit.com/r/cacti/.json"
    e.output = get_redditpics(url)
    return e
get_cacti.command = "!cacti"

def get_sloth(self, e):
    url = "http://www.reddit.com/r/sloths/.json"
    e.output = get_redditpics(url)
    return e
get_sloth.command = "!sloths"

def get_redditpics(url):
    response = urllib2.urlopen(url).read()
    cats = json.loads(response)
    catlist = []
    for cat in cats['data']['children']:
        if 'jpg' in cat['data']['url'] or 'imgur.com' in cat['data']['url']:
            catlist.append(cat['data']['url'] + " - " + cat['data']['title'])

    cats = catlist[random.randint(0, len(catlist) - 1)] + " :: " + catlist[random.randint(0, len(catlist) - 1)]
    return cats

