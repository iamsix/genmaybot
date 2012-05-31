import urllib, urllib2, xml.dom.minidom, socket, botmodules.tools as tools
try: import botmodules.userlocation as user
except: pass

def get_wolfram(self, e):
    
    #query 'input' on wolframalpha and get the plaintext result back
    if user:
        location = urllib.quote(user.get_location(e.nick))
    socket.setdefaulttimeout(30)
    url = "http://api.wolframalpha.com/v2/query?appid=%s&format=plaintext&input=%s&location=%s" % (tools.config.wolframAPIkey, urllib.quote(e.input), location)
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))
    socket.setdefaulttimeout(10)

    if (dom.getElementsByTagName("queryresult")[0].getAttribute("success") == "false"):
        try:
            related = dom.getElementsByTagName("relatedexample")[0].getAttribute("input")
            e.input = related
            return get_wolfram(self, e)
        except Exception as inst:
            print "!wolframrelated " + e.input + " : " + str(inst)
            result = "poop!"
            e.output = result.encode("utf-8")
            return e
    else:
        try:
            query = dom.getElementsByTagName("plaintext")[0].childNodes[0].data
            try:
                result = dom.getElementsByTagName("plaintext")[1].childNodes[0].data
            except:
                result = "poop!"
            output = query.replace("\n", " || ") + " :: " + result.replace("\n", " || ")
            
            e.output = output.encode("utf-8")
            return e
        except Exception as inst:
            print "!wolfram " + e.input + " : " + str(inst)
            result = "poop!"
            e.output = result.encode("utf-8")
            return e
            
get_wolfram.command = "!wolfram"
get_wolfram.helptext = "Usage: !wolfram <query>\nExample: !wolfram population of New York City\nPerforms a query through Wolfram|Alpha and returns the first result"

