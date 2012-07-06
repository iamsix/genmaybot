import random
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timedelta

def error_generator(self, e):
    firstword = firstwords[random.randint(0, len(firstwords) - 1)]
    secondword = secondwords[random.randint(0, len(secondwords) - 1)]
    thirdword = secondwords[random.randint(0, len(thirdwords) - 1)]
    rand5 = random.randint(0, 4)
    fourthword = fourthwords[rand5]
    heading = ""
    if rand5 == 0:
        heading = "Error: "
    if rand5 == 1:
        heading = "Problem: "
    if rand5 == 2:
        heading = "Warning: "
    if rand5 == 3:
        heading = "Signal: "
    e.output = "%s%s %s %s %s" % (heading, firstword, secondword, thirdword, fourthword)
    return e

error_generator.command = "!error"
error_generator.helptext = "Usage: !error\nGenerates a random scary-sounding error message"

firstwords = ["Temporary", "Intermittant", "Partial", "Redundant", "Total",
                "Multiplexed", "Inherent", "Duplicated", "Dual-Homed", "Synchronous",
                "Bidirectional", "Serial", "Asynchronous", "Multiple", "Replicated",
                "Non-Replicated", "Unregistered", "Non-Specific", "Generic", "Migrated",
                "Localised", "Resignalled", "Dereferenced", "Nullified", "Aborted",
                "Serious", "Minor", "Major", "Extraneous", "Illegal", "Insufficient",
                "Viral", "Unsupported", "Outmoded", "Legacy", "Permanent", "Invalid",
                "Deprecated", "Virtual", "Unreportable", "Undetermined", "Undiagnosable",
                "Unfiltered", "Static", "Dynamic", "Delayed", "Immediate", "Nonfatal",
                "Fatal", "Non-Valid", "Unvalidated", "Non-Static", "Unreplicatable",
                "Non-Serious"]

secondwords = ["Array", "Systems", "Hardware", "Software", "Firmware",
                "Backplane", "Logic-Subsystem", "Integrity", "Subsystem", "Memory",
                "Comms", "Integrity", "Checksum", "Protocol", "Parity", "Bus", "Timing",
                "Synchronisation", "Topology", "Transmission", "Reception", "Stack",
                "Framing", "Code", "Programming", "Peripheral", "Environmental",
                "Loading", "Operation", "Parameter", "Syntax", "Initialisation",
                "Execution", "Resource", "Encryption", "Decryption", "File",
                "Precondition", "Authentication", "Paging", "Swapfile", "Service",
                "Gateway", "Request", "Proxy", "Media", "Registry", "Configuration",
                "Metadata", "Streaming", "Retrieval", "Installation", "Library", "Handler"]

thirdwords = ["Interruption", "Destabilisation", "Destruction",
                "Desynchronisation", "Failure", "Dereferencing", "Overflow", "Underflow",
                "NMI", "Interrupt", "Corruption", "Anomoly", "Seizure", "Override",
                "Reclock", "Rejection", "Invalidation", "Halt", "Exhaustion", "Infection",
                "Incompatibility", "Timeout", "Expiry", "Unavailability", "Bug",
                "Condition", "Crash", "Dump", "Crashdump", "Stackdump", "Problem",
                "Lockout"]

fourthwords = ["Error", "Problem", "Warning", "Signal", "Flag"]


def mba_generator(self, e):
    verb = verbs[random.randint(0, len(verbs) - 1)]
    adjective = adjectives[random.randint(0, len(adjectives) - 1)]
    noun = nouns[random.randint(0, len(nouns) - 1)]

    e.output = "%s %s %s" % (verb, adjective, noun)
    return e

mba_generator.command = "!mba"
mba_generator.helptext = "Usage: !mba\nGenerates random corporate jargon"


def bbnet(self, e):
    if (e.nick.lower().startswith('bbnet')):
        e.output = "<%s> !bbnet\n^\n" % e.nick

    rand = random.randint(2, 10)
    for n in range(0, rand):
        e.output = "%s%s" % (e.output, "l")
        e.output = "%s%s" % (e.output, "oo" if random.randint(0, 5) == 0 else "o")

    return e

bbnet.command = "!bbnet"

def football(self, e):
    e.output = "%s days until opening day" % ("1") # (datetime.now() - datetime(year=2012,month=9,day=5,hour=17,minute=15)).days
    return e
football.command = "!football"


def fortune(self, e):
    e.output = urllib.request.urlopen("http://www.fortunefortoday.com/getfortuneonly.php").read().decode('utf-8').replace('\n', ' ').replace('\r', '').strip()
    return e

fortune.command = "!fortune"
fortune.helptext = "Usage: just fucking type !fortune"


verbs = ["aggregate", "architect", "benchmark", "brand", "cultivate", "deliver", "deploy", "disintermediate", "drive",
"e-enable", "embrace", "empower", "enable", "engage", "engineer", "enhance", "envisioneer", "evolve", "expedite",
"exploit", "extend", "facilitate", "generate", "grow", "harness", "implement", "incentivize", "incubate",
"innovate", "integrate", "iterate", "leverage", "matrix", "maximize", "mesh", "monetize", "morph", "optimize",
"orchestrate", "productize", "recontextualize", "redefine", "reintermediate", "reinvent", "repurpose",
"revolutionize", "scale", "seize", "strategize", "streamline", "syndicate", "synergize", "synthesize",
"target", "transform", "transition", "unleash", "utilize", "visualize", "whiteboard"]

adjectives = ["24/365", "24/7", "B2B", "B2C", "back-end", "best-of-breed", "bleeding-edge", "bricks-and-clicks",
"clicks-and-mortar", "collaborative", "compelling", "cross-platform", "cross-media", "customized", "cutting-edge",
"distributed", "dot-com", "dynamic", "e-business", "efficient", "end-to-end", "enterprise", "extensible", "frictionless",
"front-end", "global", "granular", "holistic", "impactful", "innovative", "integrated", "interactive", "intuitive", "killer",
"leading-edge", "magnetic", "mission-critical", "next-generation", "one-to-one", "open-source", "out-of-the-box",
"plug-and-play", "proactive", "real-time", "revolutionary", "rich", "robust", "scalable", "seamless", "sexy", "sticky",
"strategic", "synergistic", "transparent", "turn-key", "ubiquitous", "user-centric", "value-added", "vertical", "viral",
"virtual", "visionary", "web-enabled", "wireless", "world-class", "software-as-a-service"]

nouns = ["action-items", "applications", "architectures", "bandwidth", "channels", "communities", "content", "convergence",
"deliverables", "e-business", "e-commerce", "e-markets", "e-services", "e-tailers", "experiences", "eyeballs",
"functionalities", "infomediaries", "infrastructures", "initiatives", "interfaces", "markets", "methodologies",
"metrics", "mindshare", "models", "networks", "niches", "paradigms", "partnerships", "platforms", "portals", "relationships",
"ROI", "synergies", "web-readiness", "schemas", "solutions", "supply-chains", "systems", "technologies", "users", "vortals",
"web services"]

