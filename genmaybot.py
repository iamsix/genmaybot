#! /usr/bin/env python
#
#To run this bot use the following command:
#
#  python genmaybot.py irc.0id.net "#chan" Nickname
#

### look in to !seen functionality 
# |- on_join, on_part, on_kick, on_nick, on_quit
# |---use on_whoreply to confirm the users are who their nick is?
# |---check who is in the channel when the bot joins?
# | db: users_table: user UNQ | hostmask | last action | <user_aliases> | <user_knownhostmasks>
# | db: user_aliases: user UNQ | alternick
# | db: user_knownhostmasks: user UNQ | hostmask
# (hostmask might be username | hostmask where username@hostmask 
# 
### random descision maker?
# test comment please ignore 


from ircbot import SingleServerIRCBot
import time, imp
import sys, os, socket, configparser, threading, traceback

socket.setdefaulttimeout(5)

class TestBot(SingleServerIRCBot):
    

    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, 30)
        self.channel = channel
        self.doingcommand = False
        self.botnick = nickname
        
        
          
        self.commandaccesslist = {}    
        self.commandcooldownlast = {}

        self.spam ={}
        
        config = configparser.ConfigParser()
        try: 
            cfgfile = open('genmaybot.cfg')
        except IOError:
            print("You need to create a .cfg file using the example")
            sys.exit(1)
            
        config.readfp(cfgfile)
        self.identpassword = config.get("irc","identpassword")
        self.botadmins = config.get("irc","botadmins").split(",")

        print(self.loadmodules())
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
        self.botnick = c.get_nickname() + "_"

    def on_kick(self, c, e):
        #attempt to rejoin any channel we're kicked from
        if e.arguments()[0][0:6] == c.get_nickname():
            c.join(e.target()) 

    def on_disconnect(self, c, e):
        print("DISCONNECT: " + str(e.arguments()))

    def on_welcome(self, c, e):
        c.privmsg("NickServ", "identify " + self.identpassword)
        c.join(self.channel)       
        self.alerts(c)  
        self.irccontext = c
            
    #def on_invite(self, c, e):
        #c.join(e.arguments()[0])
        
    def on_pubmsg(self, c, e):
        self.process_line(c, e)

    def on_privmsg(self, c, e):
        from_nick = e.source().split("!")[0]
        line = e.arguments()[0].strip()
        command = line.split(" ")[0]
        
        if command in self.admincommands and self.isbotadmin(from_nick):
            self.admincommand = line
            c.who(from_nick) 
                
        self.process_line(c, e, True)
    
    def on_whoreply(self, c,e):
        nick = e.arguments()[4]
        line = self.admincommand
        command = line.split(" ")[0]
        self.admincommand = ""
        try:
            if e.arguments()[5].find("r") != -1 and line != "":
                say = self.admincommands[command](line, nick, self, c)
                say = say.split("\n")
                for line in say:
                    c.privmsg(nick, line)

        except Exception as inst:
            print("admin exception: " + line + " : " + str(inst))

    def process_line(self, c, ircevent, private = False):
        if self.doingcommand:
            return
        self.doingcommand = True
        
        line = ircevent.arguments()[0]
        from_nick = ircevent.source().split("!")[0]
        hostmask = ircevent.source()[ircevent.source().find("!")+1:]
        command = line.split(" ")[0].lower()
        args = line[len(command)+1:].strip()
        if private:
            linesource = from_nick
        else:
            linesource = ircevent.target()
        
        e = None
        etmp = []

                
        try:
            #commands names are defined by the module as function.command = "!commandname"
            if command in self.bangcommands and (self.commandaccess(command) or from_nick in self.botadmins):
                e = self.botEvent(linesource, from_nick, hostmask, args)
                e.botnick = self.botnick #store the bot's nick in the event in case we need it.

                if linesource in self.channels and hasattr(self.bangcommands[command], 'privateonly'):
                    self.doingcommand = False
                    return
                etmp.append(self.bangcommands[command](self, e))
          
            else:
                #lineparsers take the whole line and nick for EVERY line
                e = self.botEvent(linesource, from_nick, hostmask, line)
                e.botnick = self.botnick #store the bot's nick in the event in case we need it.
                #ensure the lineparser function is short and simple. Try to not to add too many of them
                #Multiple lineparsers can output data, leading to multiple 'say' lines
                for command in self.lineparsers:
                    if linesource in self.channels and hasattr(command, 'privateonly'): continue
                    etmp.append(command(self, e))
          
            firstpass = True
            for e in etmp:      
                if e and e.output:
                    if firstpass and not e.source == e.nick and not e.nick in self.botadmins:
                        if self.isspam(e.hostmask, e.nick): break
                        firstpass = False
                    self.botSay(e)
                                            
        except Exception as inst: 
            traceback.print_exc()
            print(line + " : " + str(inst))
            pass

        self.doingcommand = False
        return
    
    def botSay(self, botevent):
        try:
            if botevent.output:
                for line in botevent.output.split("\n"):
                    line = line.replace("join", "join")
                    line = line.replace("come", "come") 
                    if botevent.notice:
                        self.irccontext.notice(botevent.source, line)
                    else:              
                        self.irccontext.privmsg(botevent.source, line)
        except Exception as inst:
            print("bot failed trying to say " + str(botevent.output) + "\n" + str(inst)) 
            traceback.print_exc()

    def loadmodules(self):
        filenames = []
        for fn in os.listdir('./botmodules'):
            if fn.endswith('.py') and not fn.startswith('_'):
                filenames.append(os.path.join('./botmodules', fn))
               
        self.bangcommands = {}
        self.admincommands = {}
        self.botalerts = []
        self.lineparsers = []
               
        for filename in filenames:
            name = os.path.basename(filename)[:-3]
            try:
                module = imp.load_source(name, filename)
            except Exception as inst: 
                print("Error loading module " + name + " : " + str(inst))
            else:
                for name, func in vars(module).items():
                    if hasattr(func, 'command'):
                        command = str(func.command)
                        self.bangcommands[command] = func
                    elif hasattr(func, 'admincommand'):
                        command = str(func.admincommand)
                        self.admincommands[command] = func                      
                    elif hasattr(func, 'alert'):
                        self.botalerts.append(func)
                    elif hasattr(func, 'lineparser'):
                        self.lineparsers.append(func) 
        
        commands, botalerts, lineparsers, admincommands = "","","",""
                        
        if self.bangcommands:
            commands = 'Loaded command modules: %s' % list(self.bangcommands.keys())
        else:
            commands = "No command modules loaded!"
        if self.botalerts:
            botalerts = 'Loaded alerts: %s' % ', '.join((command.__name__ for command in self.botalerts))
        if self.lineparsers:
            lineparsers = 'Loaded line parsers: %s' % ', '.join((command.__name__ for command in self.lineparsers))
        if self.admincommands:
            admincommands = 'Loaded admin commands: %s' % list(self.admincommands.keys())
        return commands + "\n" + botalerts + "\n" + lineparsers + "\n" + admincommands   
    
    def isbotadmin(self, nick):
        return nick in self.botadmins
   
    def commandaccess(self, command):
        if "all" in self.commandaccesslist:
            command = "all"
        if command in self.commandaccesslist:
            if type(self.commandaccesslist[command]) == int:
                if time.time() - self.commandcooldownlast[command] < self.commandaccesslist[command]:
                    return False
                else:
                    self.commandcooldownlast[command] = time.time()
                    return True
            elif self.commandaccesslist[command] == "Disabled":
                return False
        else: #if there's no entry it's assumed to be enabled
            return True
                
    def isspam(self, user, nick):

        if not (user in self.spam):
            self.spam[user] = {}
            self.spam[user]['count'] = 0
            self.spam[user]['last'] = 0
            self.spam[user]['first'] = 0
            self.spam[user]['limit'] = 15
      
        self.spam[user]['count'] +=1
        self.spam[user]['last'] = time.time()
      
        if self.spam[user]['count'] == 1:
            self.spam[user]['first'] = time.time()
      
        if self.spam[user]['count'] > 1:
            self.spam[user]['limit'] = (self.spam[user]['count'] - 1) * 15

            if not ((self.spam[user]['last'] - self.spam[user]['first']) > self.spam[user]['limit']):
                bantime = self.spam[user]['limit'] + 15
                print("%s : %s band %s seconds" % (time.strftime("%d %b %Y %H:%M:%S", time.localtime()), nick, bantime))
                return True
            else:
                self.spam[user]['first'] = 0
                self.spam[user]['count'] = 0
                self.spam[user]['limit'] = 15
                return False
  
    def alerts(self, context):
        try: 
            for command in self.botalerts:
                say = command()
                if say:
                    for channel in self.channels:  
                        context.privmsg(channel, say)
        except Exception as inst: 
            print("alerts: " + str(inst))
            pass
      
        t=threading.Timer(60,self.alerts, [context])
        t.start()
      
    class botEvent:
        def __init__(self, source, nick, hostmask, input, output="", notice = False):
            self._source = source
            self._nick = nick
            self._input = input
            self._output = output
            self._notice = notice
            self._hostmask = hostmask
            
        @property
        def source(self):
            return self._source
        @source.setter
        def source(self, value):
            self._source = value
        
        @property
        def nick(self):
            return self._nick
        @nick.setter
        def nick(self, value):
            self._nick = value
        
        @property
        def hostmask(self):
            return self._hostmask
        @hostmask.setter
        def hostmask(self, value):
            self._hostmask = value
        
        @property
        def input(self):
            return self._input
        @input.setter
        def input(self, value):
            self._input = value
        
        @property
        def output(self):
            return self._output
        @output.setter
        def output(self, value):
            self._output = value
            
        @property
        def notice(self):
            return self._notice
        @notice.setter
        def notice(self, value):
            self._notice = value
  
  
def main():
    #print sys.argv
    if len(sys.argv) != 4:
        print("Usage: testbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
    

