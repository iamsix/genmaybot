import urllib2, re, botmodules.tools as tools
 
def get_woot(nothing):
      try:
          url = "http://www.woot.com/salerss.aspx"
          req = urllib2.Request(url)
          resp = urllib2.urlopen(req).read()
      
          product = re.search('\<woot:product quantity=\"[0-9]*?\"\>(.*?)\<\/woot:product\>',resp).group(1)
          product = tools.decode_htmlentities(product)
      
          price = re.search("<woot:price>(.*?)<\/woot:price>", resp).group(1)
      
          return product + " [" + price + "]"
      except:
          pass
get_woot.command = "!woot"