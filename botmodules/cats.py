import json, urllib2, random
def get_cat(self, e):
    url = "http://www.reddit.com/r/catpictures/.json"
    response = urllib2.urlopen(url).read() 
    cats = json.loads(response)
    catlist = []
    for cat in cats['data']['children']:
        if 'jpg' in cat['data']['url'] or 'imgur.com' in cat['data']['url']:
            catlist.append(cat['data']['url'] + " - " + cat['data']['title'])
    
    #cat = random.randint(0, len(catlist) - 1)
    e.output = catlist[random.randint(0, len(catlist) - 1)] + " :: " + catlist[random.randint(0, len(catlist) - 1)] 
    return e
    
    
get_cat.command = "!cats"