import urllib.request
import json
import random


class Leafly:
    class LeaflyException(Exception):
        pass

    class Strain:
        def __init__(self, name, tags, negatives, review_count, rating_count, rating, flavors, category, permalink):
            self.name = name
            

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

            # Try to shuffle the tags to get some more interesting ones out
            self.tags = random.shuffle(tags)

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

    def get_strain_scraper(self, name=None):

        if name is None: 
            raise self.LeaflyException("get_strain_scraper: name not provided")


        url = "https://www.leafly.com/search?%s" % (urllib.parse.urlencode({"q":name}))
        req = urllib.request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")        

        search_results = urllib.request.urlopen(req).read()
        search_page = BeautifulSoup(search_results, "html.parser")
        search_section = search_page.findAll("section", attrs={"class":"search"})[0]
        first_result = search_section.findNext("li", attrs={"class":"search__item info-block divider bottom padding-listItem"})
        link = first_result.findAll("a")[0].attrs['href']

        permalink = "https://www.leafly.com"+link
        req = urllib.request.Request(permalink)
        req.add_header("User-Agent","Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
        strain_page = urllib.request.urlopen(req).read()
        strain_page = BeautifulSoup(strain_page, "html.parser")

        name = strain_page.findAll("h1",attrs={"itemprop":"name"})[0].text
        rating = strain_page.findAll("span", attrs={"itemprop":"ratingValue"})[0].text
        rating = int(round(float(rating)/5*100,0))

        review_count = strain_page.findAll("span", attrs={"itemprop":"reviewCount"})[0].text

        effects_tab = strain_page.findAll("div", attrs={"ng-show":"currentAttributeTab==='Effects'"})[0]
        effects_tags = effects_tab.findAll("div", attrs={"class":"m-attr-label copy--sm"})
        
        effects = []
        for effect_tag in effects_tags:
            effects.append(effect_tag.text)


        negatives_tab = strain_page.findAll("div", attrs={"ng-show":"currentAttributeTab==='Negatives'"})[0]
        negatives_tags = negatives_tab.findAll("div", attrs={"class":"m-attr-label copy--sm"})

        negatives = []
        for negatives_tag in negatives_tags:
            negatives.append(negatives_tag.text)       
        
        flavors_section = strain_page.findAll("section",attrs={"class":"strain__flavors padding-listItem divider bottom"})[0]
        flavors = []
        for flavor_tag in flavors_section.findAll("li"): 
            flavors.append(flavor_tag.attrs['title'])

        category = strain_page.findAll("div", attrs={"data-ng-bind":re.compile("category")})[0].text
        
        return self.Strain( name=name,  
                            negatives=negatives, 
                            rating_count=review_count,
                            rating=rating,
                            category=category,
                            flavors=flavors,
                            effects=effects,
                            permalink=permalink)


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
        strain = Leafly(app_id, app_key).get_strain_scraper(e.input)
    else:
        e.output = "Please enter a strain name to search for"
        return e

    strain_line = "Strain: %s (%s) - Grade: %s [%s, %s ratings]" % (strain.name, strain.category, strain.rating, strain.rating_word, strain.rating_count)

    if type(strain.flavors) is list:
        strain_line += " Flavors: [%s]" % (", ".join(strain.flavors[0:5]))

    if type(strain.effects) is list:
        strain_line += " Flavors: [%s]" % (", ".join(strain.effects[0:5]))
    
    if type(strain.negatives) is list:
        strain_line += " Negatives: [%s]" % (", ".join(strain.negatives[0:5]))

    if type(strain.tags) is list:
        strain_line += " Tags: [%s]" % (", ".join(strain.tags[0:5]))

    strain_line +=  " [ %s ]" % self.tools['shorten_url'](strain.url)

    e.output = strain_line
    return e

leafly_search.command = "!weed"
leafly_search.helptext = """\
Usage: !weed <strain name>
Example: !weed og kush
Finds a given strain on Leafly and returns some useful info"""


