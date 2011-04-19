import sys, time

def kill_bot(line, nick, self):
    print "got die command from " + nick 
    sys.exit(0)
kill_bot.admincommand = "die"    

def clear_bans(line, nick, self):
    print nick + " cleared bans"
    self.spam ={}
    return "All bans cleared"
clear_bans.admincommand = "clearbans"

def reload_modules(line, nick, self):
    self.loadmodules()

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
reload_modules.admincommand = "reload"        

def enable_command(line, nick, self):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        if command in self.commandaccesslist:
            del self.commandaccesslist[command]
            return command + " Enabled"
        else:
            return command + " not disabled"
enable_command.admincommand = "enable"

def disable_command(line, nick, self):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        self.commandaccesslist[command] = "Disabled"
        return command + " Disabled"
disable_command.admincommand = "disable"

def cooldown_command(line, nick, self):
    if len(line.split(" ")) == 3:
        command = line.split(" ")[1]
        cooldown = line.split(" ")[2]
        if cooldown.isdigit():
            cooldown = int(cooldown)
            if cooldown == 0:
                if command in self.commandaccesslist:
                    del self.commandaccesslist[command]
                return command + " cooldown disabled"
            else:
                self.commandaccesslist[command] = cooldown
                self.commandcooldownlast[command] = time.time() - cooldown   
                return command + " cooldown set to " + str(cooldown) + " seconds (set to 0 to disable)"
        else:
            return "bad format: 'cooldown !wiki 30' (30 second cooldown on !wiki)"
    else:
        return "not enough perameters: cooldown !command ##"
cooldown_command.admincommand = "cooldown"

def command_status(line, nick, self):
    if len(line.split(" ")) == 2:
        command = line.split(" ")[1]
        if command in self.commandaccesslist:
            return command + " " + str(self.commandaccesslist[command]) + " (Seconds cooldown if it's a number)"
        else:
            return command + " Enabled"
command_status.admincommand = "status"

