import urllib2, xml.dom.minidom, botmodules.tools as tools
 
def get_woot(nothing, nick):
    #display the current woot.com sale
      try:
          url = "http://www.woot.com/salerss.aspx"
          dom = xml.dom.minidom.parse(urllib2.urlopen(url))
      
          product = dom.getElementsByTagName("woot:product")[0].childNodes[0].data
          product = tools.decode_htmlentities(product)
      
          price = dom.getElementsByTagName("woot:price")[0].childNodes[0].data
      
          return product + " [" + price + "]"
      except:
          pass
get_woot.command = "!woot"
get_woot.helptext = "Usage: !woot\nShows today's deal from woot.com"