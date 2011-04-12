import urllib2, urllib, json, re

def google_convert(term):
        term = term.replace("ANS", google_convert.lastresult)
        url = "http://www.google.com/ig/calculator?q=%s" % urllib.quote(term)
        result = ""
        try:
            response = urllib2.urlopen(url).read() 
            response = response.replace("\xa0"," ").decode('unicode-escape')
            response = re.sub("([a-z]+):", '"\\1" :', response)
            response = response.replace("<sup>","^(")
            response = response.replace("</sup>",")")
            response = response.replace("&#215;","x")
            response = json.loads(response)
            if not response['error']:
                result = "%s = %s" % (response['lhs'],response['rhs'])
                google_convert.lastresult = response['rhs']
        except Exception as inst: 
            print "!c " + term + " : " + str(inst)
            pass
        
        return result
google_convert.command = "!c"
google_convert.lastresult = ""