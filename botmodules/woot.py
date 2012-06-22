import urllib.request, urllib.error, urllib.parse, xml.dom.minidom, botmodules.tools as tools
 
def get_woot(self, e):
    #display the current woot.com sale
      try:
          url = "http://www.woot.com/salerss.aspx"
          dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
      
          product = dom.getElementsByTagName("woot:product")[0].childNodes[0].data
          product = tools.decode_htmlentities(product)
      
          price = dom.getElementsByTagName("woot:price")[0].childNodes[0].data
      
          e.output = product + " [" + price + "]"
          return e
      except:
          pass
get_woot.command = "!woot"
get_woot.helptext = "Usage: !woot\nShows today's deal from woot.com"

