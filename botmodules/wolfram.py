import urllib, urllib2, xml.dom.minidom, socket, botmodules.tools as tools
try: import botmodules.userlocation as user
except: pass

def get_wolfram(input, nick):
    #query 'input' on wolframalpha and get the plaintext result back
    if user:
       location = urllib.quote(user.get_location(nick))
    socket.setdefaulttimeout(30)
    url = "http://api.wolframalpha.com/v2/query?appid=%s&format=plaintext&input=%s&location=%s" % (tools.config.wolframAPIkey, urllib.quote(input), location)
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))
    socket.setdefaulttimeout(10)

    if (dom.getElementsByTagName("queryresult")[0].getAttribute("success") == "false"):
        try:
            related = dom.getElementsByTagName("relatedexample")[0].getAttribute("input")
            return get_wolfram(related, nick)
        except Exception as inst:
            print "!wolframrelated " + input + " : " + str(inst)
    else:
        try:
            query = dom.getElementsByTagName("plaintext")[0].childNodes[0].data
            result = dom.getElementsByTagName("plaintext")[1].childNodes[0].data
            output = query.replace("\n", " || ") + ": " + result.replace("\n", " || ")
            
            return output.encode("utf-8")
        except Exception as inst:
            print "!wolfram " + input + " : " + str(inst)
get_wolfram.command = "!wolfram"
