import re
import random


def decider(self, e):
    regex = "^bot[^\s]? (.*)$"
    result = re.search(regex, e.input)
    if result:
        if (result.group(1)):
            items = result.group(1).split(" or ")
            item_picked = items[random.randint(0, items.__len__() - 1)]
            e.output = e.nick + ": " + item_picked
            return e

decider.lineparser = True
