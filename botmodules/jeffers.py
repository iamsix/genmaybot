def page_effigy(self, e):
    if e.nick.find("jeff") != -1 and e.input.find("page effigy") != -1:
        e.output = "http://is.gd/jeffers"
        return e
    else:
        return None

page_effigy.lineparser = True

def ban_jeffers(self, e):
    if e.input == "ban jeffers":
      if "#genmay" in self.channels:
        print e.nick + " ban jeffers"
        e.output = "!ban jeffers"
        e.source = "#genmay"
      else:
        e.output = "bot isn't in #genmay"
    else:
        e = None

    return e
ban_jeffers.lineparser = True
ban_jeffers.pivateonly = True
