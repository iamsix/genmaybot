import sqlite3
from dateutil.parser import parse


def __init__(self):
    """ On init, do a system check which runs upgrades and creates tables. """
    age_check_system()  # Check the system for tables and/or upgrades


def age_software_version():
    """ Returns the current version of the module, used upgrade """
    return 1


def age_check_system():
    """ Run upgrades and check on initial table creation/installation """
    age_check_upgrades()
    age_check_create_tables()


def age_check_upgrades():
    """ Check the version in the database and upgrade the system recursively until we're at the current version """
    software_version = age_get_version('software')
    latest_version = age_software_version()
    if(software_version == False):
        # This must be a new revision
        # we need to set it to the current version that is being installed.
        age_set_version('software', latest_version)
        age_check_upgrades()
    elif(software_version < age_software_version()):
        # Then we need to perform an upgrade for this version.
        func = 'age_upgrade_%s' % (software_version + 1)
        globals()[func]()
        age_check_upgrades()


def age_set_version(version_field, version_number):
    """ Sets a version number for any component """
    conn = sqlite3.connect('age.sqlite')
    c = conn.cursor()
    query = "INSERT INTO version VALUES (:version_field, :version_number)"
    c.execute(query,
        {'version_field': version_field,
        'version_number': version_number})
    conn.commit()
    c.close()


def age_get_version(version_field):
    """ Get the version for a component of code """
    age_check_create_tables()
    conn = sqlite3.connect('age.sqlite')
    c = conn.cursor()
    query = "SELECT version_number FROM version WHERE version_field = :version_field"
    result = c.execute(query, {'version_field': version_field}).fetchone()
    if (result):
        c.close()
        return result[0]
    else:
        c.close()
        return False


def age_check_create_tables():
    """ Create tables for the database, these should always be up to date """
    conn = sqlite3.connect('age.sqlite')
    c = conn.cursor()
    tables = {
        'version': "CREATE TABLE version (version_field TEXT, version_number INTEGER)",
        'users': "CREATE TABLE users (user TEXT UNIQUE ON CONFLICT REPLACE, birth_year INTEGER, birth_month INTEGER, birth_day INTEGER)"
    }
    # Go through each table and check if it exists, if it doesn't, run the SQL statement to create it.
    for (table_name, sql_statement) in tables.items():
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
        if not c.execute(query, {'table_name': table_name}).fetchone():
            # Run the command.
            c.execute(sql_statement)
            conn.commit()
    c.close()


def age_insert_birthday(nick, birthday):
    """ Insert a user's birthday """
    birthday_parsed = parse(birthday)
    if birthday_parsed:
        conn = sqlite3.connect('age.sqlite')
        c = conn.cursor()
        query = "INSERT INTO users VALUES (:user, :birth_year, :birth_month, :birth_day)"
        c.execute(query, {'user': nick, 'birth_year': birthday_parsed.year, 'birth_month': birthday_parsed.month, 'birth_day': birthday_parsed.day})
        conn.commit()
        c.close()
        return True
    return False


def age_delete_birthday(nick):
    """ Delete a user's birthday """
    conn = sqlite3.connect('age.sqlite')
    c = conn.cursor()
    query = "DELETE FROM users WHERE user = :user"
    c.execute(query, {'user': nick})
    conn.commit()
    c.close()


def age_get_birthday(nick):
    """ Get an user's birthday """
    conn = sqlite3.connect('age.sqlite')
    c = conn.cursor()
    query = "SELECT * FROM users WHERE UPPER(user) = UPPER(?)"
    result = c.execute(query, [nick]).fetchone()
    if (result):
        c.close()
        return result
    else:
        c.close()
        return False


def age_set_birthday(self, e):
    """ Set a user's birthday. """
    if e.input:
        # Insert the user age, we should probably validate the user though right?
        if age_insert_birthday(e.nick, e.input):
            self.irccontext.privmsg(e.nick, "Your age has been set to %s." % (e.input))
        else:
            self.irccontext.privmsg(e.nick, "I didn't understand what you meant by %s, please try a real date?" % (e.input))

age_set_birthday.command = "!age-set"
age_set_birthday.helptext = """
                        Usage: !age-set <birthday>
                        Example: !age-set September 10th, 1982
                        Saves your birthday to the bot.
                        Once your birthday is saved you can use age commands without an argument."""


def age_reset_birthday(self, e):
    """ Resets a user's age. """
    age = age_get_birthday(e.nick)
    if age:
        age_delete_birthday(e.nick)
        self.irccontext.privmsg(e.nick, "Your birthday has been reset.")
    else:
        self.irccontext.privmsg(e.nick, "You don't even have a birthday set, why would you want to reset it?")


age_reset_birthday.command = "!age-reset"
age_reset_birthday.helptext = """
                        Usage: !age-reset
                        Removes your birthday from the bot."""


def age(self, e):
    self_birthday = age_get_birthday(e.nick)
    if e.input:
        input_birthday = age_get_birthday(e.input)
        if input_birthday:
            input_nick, input_year, input_month, input_day = input_birthday
            e.output = "Do something with %s" % (input_year)
        else:
            e.output = "Sorry, %s doesn't have an age set." % (e.input)
    elif self_birthday:
        self_nick, self_year, self_month, self_day = self_birthday
        e.output = "Do something with user's own birthday: %s" % (self_year)
    else:
        e.output = "Sorry %s, you don't have a birthday setup yet, please enter one with the !age-set command." % (e.nick)
    return e


age.command = "!age"
age.helptext = """
                Usage: !age [user]"
                Example: !age, !age jeffers
                Gets the age of the user specified or saved via !age-set.
                If you have an birthday set with !age-set you can use this command without an arguement.
                """
