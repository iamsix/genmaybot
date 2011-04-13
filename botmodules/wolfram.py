import urllib, urllib2, xml.dom.minidom, socket, botmodules.tools as tools

def get_wolfram(input):
    #query 'input' on wolframalpha and get the plaintext result back
    socket.setdefaulttimeout(30)
    url = "http://api.wolframalpha.com/v2/query?appid=%s&format=plaintext&input=%s" % (tools.config.wolframAPIkey, urllib.quote(input))
    dom = xml.dom.minidom.parse(urllib2.urlopen(url))
    socket.setdefaulttimeout(10)

    if (dom.getElementsByTagName("queryresult")[0].getAttribute("success") == "false"):
        try:
            related = dom.getElementsByTagName("relatedexample")[0].getAttribute("input")
            get_wolfram(related)
        except Exception as inst:
            print "!wolframrelated " + input + " : " + inst
    else:
        try:
            query = dom.getElementsByTagName("plaintext")[0].childNodes[0].data
            result = dom.getElementsByTagName("plaintext")[1].childNodes[0].data
            output = query.replace("\n", " || ") + ": " + result.replace("\n", " || ")
            
            return output.encode("utf-8")
        except Exception as inst:
            print "!wolfram " + input + " : " + inst
get_wolfram.command = "!wolfram"