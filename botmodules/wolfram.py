import urllib, urllib.request, urllib.error, urllib.parse, xml.dom.minidom, socket, botmodules.tools as tools, botmodules.error_generator as error_generator, traceback
try: import botmodules.userlocation as user
except: pass

def get_wolfram(self, e):
    
    #query 'input' on wolframalpha and get the plaintext result back
    if user:
        location = urllib.parse.quote(user.get_location(e.nick))
    socket.setdefaulttimeout(30)
    url = "http://api.wolframalpha.com/v2/query?appid=%s&format=plaintext&input=%s&location=%s" % (tools.config.wolframAPIkey, urllib.parse.quote(e.input), location)
    dom = xml.dom.minidom.parse(urllib.request.urlopen(url))
    socket.setdefaulttimeout(10)

    if (dom.getElementsByTagName("queryresult")[0].getAttribute("success") == "false"):
        try:
            related = dom.getElementsByTagName("relatedexample")[0].getAttribute("input")
            e.input = related
            return get_wolfram(self, e)
        except Exception as inst:
            traceback.print_exc()
            print("!wolframrelated " + e.input + " : " + str(inst))
            result = error_generator.error_generator(self,e).output
            e.output = result
            return e
    else:
        try:
            query = dom.getElementsByTagName("plaintext")[0].childNodes[0].data
            try:
                result = dom.getElementsByTagName("plaintext")[1].childNodes[0].data
            except:
                result = error_generator.error_generator(self,e).output
            
            output = query.replace("\n", " || ") + " :: " + result.replace("\n", " || ")
            e.output = output
            return e
        except Exception as inst:
            traceback.print_exc()
            print("!wolfram " + e.input + " : " + str(inst))
            result = error_generator.error_generator(self,e).output
            e.output = result
            return e
            
get_wolfram.command = "!wolfram"
get_wolfram.helptext = "Usage: !wolfram <query>\nExample: !wolfram population of New York City\nPerforms a query through Wolfram|Alpha and returns the first result"

