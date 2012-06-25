import re


def get_wiki(self, e, urlposted=False, forcemediawiki=False):
    #read the first paragraph of a wikipedia article
    searchterm = e.input

    if urlposted:
        url = searchterm
    else:
        if searchterm == "":
            url = "http://en.wikipedia.org/wiki/Special:Random"
        else:
            searchterm = "site:wikipedia.org " + searchterm
            url = self.tools['google_url'](searchterm, "wikipedia.org/wiki")

    title = ""

    if url and url.find("wikipedia.org/wiki/") != -1 or forcemediawiki:
        if url.find("File:") != -1:
            title = get_wiki_file_description(self, url)
        else:
            title = read_wiki_page(self, url)

    if not urlposted:
        url = self.tools['shorten_url'](url)
        title = (title + " [ %s ]" % url)

    e.output = title
    return e
get_wiki.command = "!wiki"
get_wiki.helptext = "Usage: !wiki <search term>\nExample: !wiki carl sagan\nShows the first couple of sentences of a wikipedia entry for the given search term"


def read_wiki_page(self, url):
    page = self.tools["load_html_from_URL"](url)

    tables = page.findAll('table')
    for table in tables:
        table.extract()

    if url.find('#') != -1:
        anchor = url.split('#')[1]
        page = str(page.find(id=anchor).findNext('p'))
    else:
        page = page.findAll('p')

        if str(page[0])[0:9] == '<p><span ':
            page = str(page[1].extract())
        else:
            page = str(page[0].extract())

    title = self.tools['remove_html_tags'](page)
    title = re.sub(r'\[.*?\]', '', title)
    title = title.replace("\n", " ")

    title = title[0:420]
    if title.rfind(".") != -1:
        title = title[0:title.rfind(".") + 1]

    return title


def get_wiki_file_description(self, url):
    page = self.tools["load_html_from_URL"](url)

    try:
      desc = page.findAll("div",attrs={"class":"description en"})[0].getText(separator=" ")
      #print "hit 1st case"
    except:
      try:
        desc = page.find("th",attrs={"id" : "fileinfotpl_desc"}).findNextSibling("td").find("p").getText(separator=" ")
       #print "hit 2nd case"
      except:
        try:
          desc = page.find("th",attrs={"id" : "fileinfotpl_desc"}).findNextSibling("td").find("div").getText(separator=" ")
          #print "hit 3rd case"
        except:
          try:
            desc = page.find("div",attrs={"id":"shared-image-desc"}).next.getText(separator=" ")
            #print "hit 4th case"
          except:
            print("Couldn't find description for file %s" % url)
            return

    desc = desc.replace("English:", "")
    desc = desc[0:420]
    if desc.rfind(".") != -1:
        desc = desc[0:desc.rfind(".") + 1]

    return desc.strip()

