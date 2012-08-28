import re, random
def decider(self, e):
    regex = "bot" + "[^\s]? (.*) or ([^?]*)"
    result = re.search(regex, e.input)
    if result:
        if (random.randint(0,1) == 0):
            e.output = e.nick + ": " + result.group(1)
        else:
            e.output = e.nick + ": " + result.group(2)
    return e
decider.lineparser = True