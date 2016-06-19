import re
import botmodules.cleverbot as cleverbot

def chatter(self, e):
    botnick = e.botnick.lower()

    if e.input.lower().find(botnick) != -1:
        if e.input[0:len(botnick)].lower() == botnick:
            e.input = e.input[len(botnick):].strip()
        e.input = re.sub("(?i)%s" % botnick, "cleverbot", e.input)
        cleverbot_client = cleverbot.Cleverbot()
        e.output = cleverbot_client.ask(e.input)

        e.output = self.tools['decode_htmlentities'](re.sub("(?i)cleverbot", botnick, e.output))
        return e
    else:
        return None

chatter.lineparser = True


