import sqlite3

def set_location(arg, nick):
    conn = sqlite3.connect('userlocations.sqlite')
    c = conn.cursor()
    result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userlocations';").fetchone()
    if not result:
        c.execute('''create table userlocations(user text UNIQUE ON CONFLICT REPLACE, location text)''')
        
    c.execute("""insert into userlocations values (?,?)""", (nick, arg))
    
    conn.commit()
    c.close()

set_location.command = "!setlocation"
    
def get_location(nick):
    conn = sqlite3.connect('userlocations.sqlite')
    c = conn.cursor()
    result = c.execute("SELECT location FROM userlocations WHERE user=?", [nick]).fetchone()
    if result:
        return result[0]
    else:
        return ""

