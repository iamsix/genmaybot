# -*- coding: utf-8 *-*
import re
import time
import threading


def wotd_trigger(self, e):
    #reset the wotd if it hasn't beeen found in over 24 hours
    if (time.time() - wotd_trigger.wotd_found_timestamp) > (3600 * 24):
        wotd_trigger.wotd = "a"
        wotd_trigger.wotd_setter = ""
        wotd_trigger.wotd_finder = ""
    if re.search(wotd_trigger.wotd, e.input, re.I) and re.search(" ", e.input) and e.source != e.nick and e.nick != "Whatsisname":
        do_wotd(self, e)
    else:
        return
wotd_trigger.lineparser = True
wotd_trigger.wotd = "a"
wotd_trigger.wotd_found_timestamp = time.time()
wotd_trigger.wotd_setter = ""
wotd_trigger.wotd_finder = ""
wotd_trigger.banneds = {}


def new_wotd(self, e):
    if e.nick == wotd_trigger.wotd_finder:
        newwotd = e.input.strip()
        if len(newwotd.split()) != 1:
            e.output = "The command usage is: !newwotd <word>"
        elif len(newwotd) < 3:
            e.output = "The word must be at least 3 letters long."
        elif newwotd in common_words:
            e.output = "Please use a different, less common word."
        else:  # Word is successfully set
            wotd_trigger.wotd = newwotd
            wotd_trigger.wotd_setter = e.nick
            e.output = "The word has been set to: {}\nYou can set it again with !newwotd <word> until someone finds it\nIf the word is not found in 24 hours it will be reset".format(newwotd)
    else:
        if wotd_trigger.wotd_finder:
            e.output = "Someone else already found the word, sorry."
        else:
            e.output = "You have to find the word of the day if you want to change it."

    return e
new_wotd.command = "!newwotd"
new_wotd.privateonly = True


common_words = ["the", "people", "would", "really", "think", "right", "there", "about", "were", "when", "your", "can",
                "which", "each", "other", "them", "then", "into", "him", "write", "more", "their", "make", "word", "some",
                "many", "time", "look", "see", "who", "may", "down", "get", "day", "come", "part", "like", "now", "these",
                "other", "said", "could", "she"]


def do_wotd(self, e):
    #If the word was found over 10 minutes ago but a new one wasn't set, allow the new person who got it to set it.
    if time.time() - wotd_trigger.wotd_found_timestamp > 600 and wotd_trigger.wotd_finder:
        wotd_trigger.wotd_finder = ""
    ban_user(self, e)
    if not wotd_trigger.wotd_finder:
        wotd_trigger.wotd_finder = e.nick
        wotd_trigger.wotd_found_timestamp = time.time()
        self.irccontext.privmsg(e.nick, "You can set a new word of the day with the command !newwotd <word>  You have 10 minutes to change the word")


def ban_user(self, e):
    self.irccontext.privmsg("Angstserv", "deprotect {} {}".format(e.source, e.nick))
    self.irccontext.privmsg("Angstserv", "NOP {} add {}".format(e.source, e.nick))
    time.sleep(1)
    self.irccontext.mode(e.source, '+b {}'.format(e.hostmask))
    self.irccontext.kick(e.source, e.nick, "Congratulations! You found the word of the day, courtesy of {}!".format(wotd_trigger.wotd_setter or self.irccontext.get_nickname()))
    wotd_trigger.banneds[e.nick] = [e.source, e.hostmask]
    threading.Timer(60, unban_user, [self, e.nick, e.hostmask, e.source]).start()


def unban_user(self, nick, hostmask, channel):
    self.irccontext.mode(channel, '-b {}'.format(hostmask))
    self.irccontext.privmsg("Angstserv", "AOP {} add {}".format(channel, nick))
    self.irccontext.invite(nick, channel)
    del(wotd_trigger.banneds[nick])
