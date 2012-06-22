from botmodules.chatterbotapi import ChatterBotFactory, ChatterBotType

import re, botmodules.tools as tools


def chatter(self, e):
	botnick = e.botnick.lower()
	
	if e.input.lower().find(botnick) != -1:
		if e.input[0:5].lower() == botnick:
			e.input = e.input[5:].strip()
		e.input = re.sub("(?i)%s" % botnick, "cleverbot", e.input)
		factory = ChatterBotFactory()
	
		bot1 = factory.create(ChatterBotType.CLEVERBOT)
		bot1session = bot1.create_session()
	
		e.output = bot1session.think(e.input)
		e.output = tools.decode_htmlentities(re.sub("(?i)cleverbot", botnick, e.output))
		return e
	else:
		return None

chatter.lineparser = True


