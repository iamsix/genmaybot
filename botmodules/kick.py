def do_kick(self, e):
    self.irccontext.kick("#auzland", e.nick, "thank you for participating in this test (by mixomatosys)")
do_kick.command = "!kick"
