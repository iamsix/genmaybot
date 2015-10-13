import urllib.request
import json


class Leafly:
    class LeaflyException(Exception):
        pass

    class Strain:
        def __init__(self, name, tags, negatives, review_count, rating_count, rating, flavors, category, permalink):
            self.name = name
            self.tags = tags

            self.review_count = review_count
            self.rating_count = rating_count
            self.rating = int(round(rating/10*100,0))
            self.category = category
            self.url = permalink

            # Process some of the more annoyingly presented info
            self.negatives = []
            for negative in negatives:
                if negative['Active'] == True:
                    self.negatives.append(negative['Name'])

            self.flavors = []
            for flavor in flavors:
                if flavor['Active'] == True:
                    self.flavors.append(flavor['Name'])

            if self.rating >=95:
                self.rating_word = "world-class"
            elif self.rating >= 90 and self.rating <= 94:
                self.rating_word = "outstanding"
            elif self.rating >=85 and self.rating <= 89:
                self.rating_word = "very good"
            elif self.rating >=80 and self.rating <= 84:
                self.rating_word = "good"
            elif self.rating >=70 and self.rating <=79:
                self.rating_word = "okay"
            elif self.rating >=60 and self.rating <=69:
                self.rating_word = "poor"
            elif self.rating < 60:
                self.rating_word = "awful"



    def __init__(self, app_id=None, app_key=None):
        if app_id is None or app_key is None:
            raise LeaflyException("API info missing or invalid")
        else:
            self.app_id = app_id
            self.app_key = app_key

    def get_strain(self, name=None, params={"page":0, "take":1}):
        if name is None:
            raise LeaflyException("get_strain: name not provided")
        opts = {}
        opts.update({"search":name})
        opts.update(params)
        
        auth_headers = {"app_id":self.app_id, "app_key":self.app_key}

        opts = json.dumps(opts).encode()
        url = "http://data.leafly.com/strains"

        strain = self.request_json(url, opts, auth_headers)['Strains'][0]
        
        return self.Strain( name=strain['Name'], 
                            tags=strain['LogTags'], 
                            negatives=strain['NegativeEffects'], 
                            review_count=strain['ReviewCount'],
                            rating_count=strain['RatingCount'],
                            rating=strain['Rating'],
                            category=strain['Category'],
                            flavors=strain['Flavors'],
                            permalink=strain['permalink'])


    def request_json(self, url, data=None, headers={}):
        # Request and parse JSON and return the object
        req = urllib.request.Request(url)

        for header in headers:
            req.add_header(header, headers[header])

        response = urllib.request.urlopen(req, data)
        response = json.loads(response.read().decode('utf-8'))

        return response


def leafly_search(self, e):
    app_id = self.botconfig["APIkeys"]["leafly_app_id"]
    app_key = self.botconfig["APIkeys"]["leafly_app_key"]

    if e.input:
        strain = Leafly(app_id, app_key).get_strain(e.input)
    else:
        e.output = "Please enter a strain name to search for"
        return e

    rating = strain.rating
    try:
        tags = ", ".join(strain.tags[0:5])
    except:
        tags = False
    try:    
        negatives = ", ".join(strain.negatives[0:5])
    except:
        negatives = False

    try:
        flavors = ", ".join(strain.flavors[0:5])
    except:
        flavors = False



    strain_line = "Strain: %s - Grade: %s [%s, %s ratings] Category: %s" % (strain.name, strain.rating, strain.rating_word, strain.rating_count, strain.category)

    if flavors:
        strain_line += " Flavors: [%s]" % flavors

    if negatives:
        strain_line += " Negatives: [%s]" % negatives

    if tags:
        strain_line += " Tags: [%s]" % tags

    strain_line +=  "[ %s ]" % self.tools['shorten_url'](strain.url)

    e.output = strain_line
    return e

leafly_search.command = "!weed"
leafly_search.helptext = """\
Usage: !weed <strain name>
Example: !weed og kush
Finds a given strain on Leafly and returns some useful info"""


