def get_trope(self, e, urlposted=False):

    if urlposted:
        url = e.input
    else:
        searchterm = "site:tvtropes.org " + e.input
        url = self.tools['google_url'](searchterm, "tvtropes.org/pmwiki/pmwiki.php")
    print(url)
    trope = ""

    page = self.tools["load_html_from_URL"](url)
    page = page.select('#wikitext')[0].extract()
    for div in page.findAll('div'):
        div.extract()

    print(page)
    trope = self.tools['remove_html_tags'](str(page))
    
    trope = trope.replace("\n", " ").strip()
    
    trope = trope[0:392]
    if trope.rfind(".") != -1:
        trope = trope[0:trope.rfind(".") + 1]
        
    trope = (trope + " [ %s ]" % self.tools['shorten_url'](url))

    e.output = trope
    return e

get_trope.command = "!trope"
