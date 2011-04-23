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

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import time, asyncore, imp
import sys, os, socket, datetime, ConfigParser, threading

socket.setdefaulttimeout(5)

class TestBot(SingleServerIRCBot):
  
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.doingcommand = False

        self.commandaccesslist = {}    
        self.commandcooldownlast = {}

        self.spam ={}
        
        config = ConfigParser.ConfigParser()
        try: 
            cfgfile = open('genmaybot.cfg')
        except IOError:
            print "You need to create a .cfg file using the example"
            sys.exit(1)
            
        config.readfp(cfgfile)
        self.identpassword = config.get("irc","identpassword")
        self.botadmins = config.get("irc","botadmins").split(",")

        print self.loadmodules()
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_kick(self, c, e):
        #attempt to rejoin any channel we're kicked from
        if e.arguments()[0][0:6] == c.get_nickname():
           c.join(e.target()) 

    def on_disconnect(self, c, e):
        print "DISCONNECT: " + str(e.arguments())
        
    def on_welcome(self, c, e):
        c.privmsg("NickServ", "identify " + self.identpassword)
        c.join(self.channel)       
        self.alerts(c)  
            
    def on_invite(self, c, e):
        c.join(e.arguments()[0])
        
    def on_pubmsg(self, c, e):
        line = e.arguments()[0]
        from_nick = e.source().split("!")[0]
        self.process_line(c, line, from_nick, e.target())

    def on_privmsg(self, c, e):
        from_nick = e.source().split("!")[0]
        line = e.arguments()[0].strip()
        command = line.split(" ")[0]
        
        if command in self.admincommands and self.isbotadmin(from_nick):
            self.admincommand = line
            c.who(from_nick) 
                
        self.process_line(c, line, from_nick, from_nick)
    
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
          print "admin exception: " + line + " : " + str(inst)

    def process_line(self, c, line, from_nick, linesource):
        if self.doingcommand:
            return
        self.doingcommand = True
        command = line.split(" ")[0]
        args = line[len(command)+1:].strip()
        
        try:
          say = []  
          saytmp = []
          
          #commands names are defined by the module as function.command = "!commandname"
          if command in self.bangcommands:
            if linesource in self.channels and hasattr(self.bangcommands[command], 'privateonly'):
              self.doingcommand = False
              return
            if command=="!help":  ##the help command needs access to the main bot object
              saytmp.append(self.bangcommands[command](args, self))              
            else:
              saytmp.append(self.bangcommands[command](args, from_nick))
          else:        
            #lineparsers take the whole line and nick for EVERY line
            #ensure the lineparser function is short and simple. Try to not to add too many of them
            #Multiple lineparsers can output data, leading to multiple 'say' lines
            for command in self.lineparsers:
                if linesource in self.channels and hasattr(command, 'privateonly'): continue
                saytmp.append(command(line, from_nick))
        
          for sayline in saytmp:
            if sayline:
               if type(sayline) != tuple:
                    say.append(sayline)
               else:
                 if sayline[1] in self.channels:
                    linesource = sayline[1]
                    say.append(sayline[0])
                 else:
                    say.append("bot not in targeted channel")
   
          if say:
              if linesource == from_nick or self.isbotadmin(from_nick) or (self.commandaccess(command) and not self.isspam(from_nick)):
                  for sayline in say:
                      sayline = sayline.replace("join", "join")
                      sayline = sayline.replace("come", "come") 
                      
                      if command=="!help":
                          for line in sayline.split("\n"):
                            c.privmsg(linesource, line)
                      else:
                            c.privmsg(linesource, sayline[0:600])       
                      
        except Exception as inst: 
          print line + " : " + str(inst)
          pass

        self.doingcommand = False
        return

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
                print "Error loading module " + name + " : " + str(inst)
            else:
                for name, func in vars(module).iteritems():
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
                        
        if self.bangcommands:
            commands = 'Loaded command modules: %s' % self.bangcommands.keys()
        else:
            commands = "No command modules loaded!"
        if self.botalerts:
            botalerts = 'Loaded alerts: %s' % ', '.join((command.__name__ for command in self.botalerts))
        if self.lineparsers:
            lineparsers = 'Loaded line parsers: %s' % ', '.join((command.__name__ for command in self.lineparsers))
        if self.admincommands:
            admincommands = 'Loaded admin commands: %s' % self.admincommands.keys()
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
                
    def isspam(self, user):

      if not (self.spam.has_key(user)):
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
          print "%s : %s band %s seconds" % (time.strftime("%d %b %Y %H:%M:%S", time.localtime()), user, bantime)
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
          print "alerts: " + str(inst)
          pass
      
      t=threading.Timer(60,self.alerts, [context])
      t.start()
  
  
def main():
    #print sys.argv
    if len(sys.argv) != 4:
        print "Usage: testbot <server[:port]> <channel> <nickname>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
    
    
