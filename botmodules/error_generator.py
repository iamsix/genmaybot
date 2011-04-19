import random

def error_generator(nothing, nick):
    firstword = firstwords[random.randint(0, len(firstwords) - 1)]
    secondword = secondwords[random.randint(0, len(secondwords) - 1)]
    thirdword = secondwords[random.randint(0, len(thirdwords) - 1)]
    rand5 = random.randint(0,4)
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
    return "%s%s %s %s %s" % (heading, firstword, secondword, thirdword, fourthword)
    
error_generator.command = "!error"

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