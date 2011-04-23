def commands_help(command,bot):

  if command == "":
    help="The following bot commands are available:\n"
    for command in bot.bangcommands:
      help+=command + "   "
    help+="\nUse !help <command> to get more detailed info on each command"

    return help
  elif command in bot.bangcommands and hasattr(bot.bangcommands[command],"helptext"):
    help = bot.bangcommands[command].helptext

    if hasattr(bot.bangcommands[command],"privateonly"):
      help+="\nNote: This command works only in a private message to the bot"

    return help

  else:
    return "Incorrect command or no help available."
    
    
    
    
#    if hasattr(bot.bangcommands[command],"helptext"):        
#      help += "%s:\t\t" % command
#      help += bot.bangcommands[command].helptext

#      
#      help+="\n"  
  

  
commands_help.command = "!help" 
commands_help.privateonly = True
commands_help.helptext="Usage: !help <command> or !help\n!help: Shows a list of available bot commands\n!help <command>: get more detailed info on each command"