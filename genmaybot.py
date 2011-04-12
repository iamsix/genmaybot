#! /usr/bin/env python
#
#To run this bot use the following command:
#
#  python genmaybot.py irc.0id.net "#chan" Nickname
#

#? look in to !seen functionality 
###? Investigate flight tracker info
#random descision maker?

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import time, urllib2, asyncore, imp
import xml.dom.minidom
import sys, os, socket, re, datetime, ConfigParser, threading

socket.setdefaulttimeout(5)



class TestBot(SingleServerIRCBot):
    
  
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.doingcommand = False
      
        self.lastquakecheck = ""
        self.commandaccesslist = {}
        self.commandcooldownlast = {}

        self.spam ={}

        self.loadmodules()
        
        if self.bangcommands:
            print 'Loaded command modules: %s' % self.bangcommands.keys()
        
        config = ConfigParser.ConfigParser()
        config.readfp(open('genmaybot.cfg'))
        self.identpassword = config.get("irc","identpassword")
        self.botadmins = config.get("irc","botadmins").split(",")
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")
    
    def on_kick(self, c, e):
        if e.arguments()[0][0:6] == c.get_nickname():
           c.join(self.channel)

    def on_welcome(self, c, e):
        c.privmsg("NickServ", "identify " + self.identpassword)
        c.join(self.channel)       
        self.alerts(c)  
            
    def on_invite(self, c, e):
        c.join(e.arguments()[0])

    def on_privmsg(self, c, e):
        #print "PRIVMSG: " + e.arguments()[0]
        #print "Target: " + e.target()
        #print "Source: " + e.source()
        
        from_nick = e.source().split("!")[0]
        line = e.arguments()[0].strip()
        
        if line == "die" or \
           line == "clearbans" or\
           line == "reload" or\
           line[0:6] == "enable" or\
           line[0:7] == "disable" or\
           line[0:8] == "cooldown" or\
           line[0:6] == "status":
                self.admincommand = line
                c.who(from_nick) 
        
        say = ""
        if line[0:1] == "!":
            command = line.split(" ")[0]
            args = line[len(command)+1:].strip()
            try:
                say = self.bangcommands[command](args)
            except:
                pass
        if say:
            c.privmsg(from_nick, say[0:600]) 
        
        if line == "ban jeffers":
          print from_nick
          c.privmsg(from_nick, "NO U! " + from_nick)
          c.privmsg(self.channel, "!ban jeffers")
    
    def on_whoreply(self, c,e):
        nick = e.arguments()[4]
        line = self.admincommand
        self.admincommand = ""
        if e.arguments()[5].find("r") != -1 and line != "" and self.isbotadmin(nick):       
            if line == "die":
                print "got die command from " + nick 
                sys.exit(0)
            elif line == "clearbans":
                print nick + "cleared bans"
                self.spam ={}
                c.privmsg(nick, "All bans cleared")
            elif line == "reload":
                self.loadmodules()
                c.privmsg(nick, "Modules reloaded: %s" % self.bangcommands.keys())
            elif line[0:6] == "enable":
                if len(line.split(" ")) == 2:
                    command = line.split(" ")[1]
                    if command in self.commandaccesslist:
                        del self.commandaccesslist[command]
                        c.privmsg(nick, command + " enabled")
                    else:
                        c.privmsg(nick, command + " not disabled")
            elif line[0:7] == "disable":
                if len(line.split(" ")) == 2:
                    command = line.split(" ")[1]
                    self.commandaccesslist[command] = "Disable"
                    c.privmsg(nick, command + " disabled")
            elif line[0:8] == "cooldown":
                if len(line.split(" ")) == 3:
                    command = line.split(" ")[1]
                    cooldown = line.split(" ")[2]
                    if cooldown.isdigit():
                        cooldown = int(cooldown)
                        if cooldown == 0:
                            del self.commandaccesslist[command]
                            c.privmsg(nick, command + " cooldown disabled")
                        else:
                            self.commandaccesslist[command] = cooldown
                            self.commandcooldownlast[command] = time.time() - cooldown   
                            c.privmsg(nick, command + " cooldown set to " + str(cooldown) + " seconds (set to 0 to disable)")
                    else:
                        c.privmsg(nick, "bad format: 'cooldown !wiki 30' (30 second cooldown on !wiki)")
                else:
                    c.privmsg(nick, "not enough args")
            elif line[0:6] == "status":
                if len(line.split(" ")) == 2:
                    command = line.split(" ")[1]
                    if command in self.commandaccesslist:
                        c.privmsg(nick, command + " " + str(self.commandaccesslist[command]) + " (Seconds cooldown if it's a number)")
                    else:
                        c.privmsg(nick, command + " Enabled")
                
        else:
            print "attempted admin command: " + line + " from " + nick
                      
    def on_pubmsg(self, c, e):
        if self.doingcommand:
            return
        self.doingcommand = True
        line = e.arguments()[0]

        from_nick = e.source().split("!")[0]
        command = line.split(" ")[0]
        args = line[len(command)+1:].strip()
        
        try:
          say = ""  
                      
          url = re.search("(?P<url>https?://[^\s]+)", e.arguments()[0])
          if url:
            args = url.group(1)
            command = "url_titler"
        
          if command in self.bangcommands:
            if hasattr(self.bangcommands[command], 'requiresnick'):
                say = self.bangcommands[command](args, from_nick)
            else:
                say = self.bangcommands[command](args)
                
          if say:
              if (not self.isspam(from_nick) and self.commandaccess(command)) or self.isbotadmin(from_nick):
                  say = say.replace("join", "join")
                  say = say.replace("come", "come") 
                  c.privmsg(e.target(), say[0:600])     
        except Exception as inst: 
          print e.arguments()[0] + " : " + str(inst)
          pass

        self.doingcommand = False
        return

    def loadmodules(self):
        filenames = []
        for fn in os.listdir('./botmodules'):
            if fn.endswith('.py') and not fn.startswith('_'):
               filenames.append(os.path.join('./botmodules', fn))
               
        self.bangcommands = {}
        self.botalerts = []
               
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
                    elif hasattr(func, 'alert'):
                        self.botalerts.append(func)    
                 
    def isbotadmin(self, nick):
        return nick in self.botadmins
   
    def commandaccess(self, command):
        if command in self.commandaccesslist:
            if type(self.commandaccesslist[command]) == int:
                if time.time() - self.commandcooldownlast[command] < self.commandaccesslist[command]:
                    return False
                else:
                    self.commandcooldownlast[command] = time.time()
                    return True
            elif self.commandaccesslist[command] == "Disable":
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
                context.privmsg(channel, "Latest Earthquake: " + qtitle)
      except Exception as inst: 
          print "quakealert: " + str(inst)
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
    
    
