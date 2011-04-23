def commands_help(bot):
  help="The following bot commands are available:\n"

  for command in bot.bangcommands:
    if hasattr(bot.bangcommands[command],"helptext"):
      help += "%s: " % command
      help += bot.bangcommands[command].helptext
      if hasattr(bot.bangcommands[command],"privateonly"):
        help+=" (works only in PM)"
      
      help+="\n"  
  
  return help
  
commands_help.command = "!help" 
commands_help.privateonly = True
commands_help.helptext="Shows this help listing"