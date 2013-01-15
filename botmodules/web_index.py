import cherrypy
import threading
from botmodules.web_auth import AuthController, require, member_of, name_is

class RestrictedArea:

    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group

    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""

#generic object to handle the return values from bot functions
class emptyObject:
    def __init__(self):
        return

class Root:


    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    def __init__(self,bot): #make a reference to the main bot object
        self.bot = bot
        self.auth = AuthController(self.bot)
        

    

    restricted = RestrictedArea()

    @cherrypy.expose
    @require()
    def index(self):
        return """

        <center>
        <a href="/commands" target="output">Commands</a>&nbsp;&nbsp;&nbsp;
        <a href="/botconfig" target="output">Bot Config</a>&nbsp;&nbsp;&nbsp;
        <a href="/event_log" target="output">Event log</a>&nbsp;&nbsp;&nbsp;
        <a href="/error_log" target="output">Error log</a>&nbsp;&nbsp;&nbsp;
       <br><br>
       <iframe name="output" width="1024px" height="768px"></iframe>

        """


    @cherrypy.expose
    @require()
    def event_log(self):
        return "<pre>"+open(self.bot.botconfig['misc']['event_log'],"r").read()+"</pre>"

    @cherrypy.expose
    @require()
    def error_log(self):
        return "<pre>"+open(self.bot.botconfig['misc']['error_log'],"r").read()+"</pre>"


    @cherrypy.expose
    @require()
    def commands(self):
        commandlist = ""

        for command in self.bot.bangcommands:
            try: helptext=self.bot.bangcommands[command].helptext.replace("\n","<br>")
            except: helptext=""

            commandlist+= "<p>%s - %s</p>" % (command,helptext)

        return commandlist

    @cherrypy.expose
    @require()
    def botconfig(self):
        output=""

        for section in self.bot.botconfig:
                output+="[%s]<br>" % section
                for item in self.bot.botconfig[section]:
                    output+="%s=%s<br>" % (item,self.bot.botconfig[section][item])

        return output



    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("joe"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


def __init__(bot):
    ##Disable cherrypy logging to stdout, bind to all IPs, start in a separate thread
    cherrypy.config.update({'engine.autoreload_on': False})
    cherrypy.log.screen=False
    cherrypy.server.socket_host = "0.0.0.0"

    cherrypy.server.socket_port = int(bot.botconfig['webui']['port'])
    
    thread = threading.Thread(target=cherrypy.quickstart, args=(Root(bot),))
    thread.start()
