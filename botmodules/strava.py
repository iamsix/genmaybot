import re
import sqlite3
import urllib.request
import json
import datetime
import time
from urllib.parse import urlparse


def __init__(self):
    """ On init, do a system check which runs upgrades and creates tables. """
    strava_check_system()  # Check the system for tables and/or upgrades


def strava_software_version():
    """ Returns the current version of the strava module, used upgrade """
    return 1


def strava_check_system():
    """ Run upgrades and check on initial table creation/installation """
    strava_check_upgrades()
    strava_check_create_tables()


def strava_check_upgrades():
    """ Check the version in the database and upgrade the system recursively until we're at the current version """
    software_version = strava_get_version('software')
    latest_version = strava_software_version()
    if(software_version == False):
        # This must be a new revision
        # we need to set it to the current version that is being installed.
        strava_set_version('software', latest_version)
        strava_check_upgrades()
    elif(software_version < strava_software_version()):
        # Then we need to perform an upgrade for this version.
        func = 'strava_upgrade_%s' % (software_version + 1)
        globals()[func]()
        strava_check_upgrades()


def strava_set_version(version_field, version_number):
    """ Sets a version number for any component """
    conn = sqlite3.connect('strava.sqlite')
    c = conn.cursor()
    query = "INSERT INTO version VALUES (:version_field, :version_number)"
    c.execute(query,
        {'version_field': version_field,
        'version_number': version_number})
    conn.commit()
    c.close()


def strava_get_version(version_field):
    """ Get the version for a component of code """
    strava_check_create_tables()
    conn = sqlite3.connect('strava.sqlite')
    c = conn.cursor()
    query = "SELECT version_number FROM version WHERE version_field = :version_field"
    result = c.execute(query, {'version_field': version_field}).fetchone()
    if (result):
        c.close()
        return result[0]
    else:
        c.close()
        return False


def strava_check_create_tables():
    """ Create tables for the database, these should always be up to date """
    conn = sqlite3.connect('strava.sqlite')
    c = conn.cursor()
    tables = {
        'version': "CREATE TABLE version (version_field TEXT, version_number INTEGER)",
        'athletes': "CREATE TABLE athletes (user TEXT UNIQUE ON CONFLICT REPLACE, strava_id TEXT)"
    }
    # Go through each table and check if it exists, if it doesn't, run the SQL statement to create it.
    for (table_name, sql_statement) in tables.items():
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"
        if not c.execute(query, {'table_name': table_name}).fetchone():
            # Run the command.
            c.execute(sql_statement)
            conn.commit()
            c.close()


def strava_insert_athlete(nick, athlete_id):
    """ Insert a user's strava id into the athletes table """
    conn = sqlite3.connect('strava.sqlite')
    c = conn.cursor()
    query = "INSERT INTO athletes VALUES (:user, :strava_id)"
    c.execute(query, {'user': nick, 'strava_id': athlete_id})
    conn.commit()
    c.close()


def strava_get_athlete(nick):
    """ Get an athlete ID by user """
    conn = sqlite3.connect('strava.sqlite')
    c = conn.cursor()
    query = "SELECT strava_id FROM athletes WHERE UPPER(user) = UPPER(?)"
    result = c.execute(query, [nick]).fetchone()
    if (result):
        c.close()
        return result[0]
    else:
        c.close()
        return False


def strava_line_parser(self, e):
    """ Watch every line for a valid strava line """
    url = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>])*\))+(?:\(([^\s()<>])*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", e.input)
    if url:
        url = url.group(0)
        url_parts = urlparse(url)
        if url_parts[1] == 'www.strava.com' or url_parts[1] == 'app.strava.com':
            ride = re.match(r"^/rides/(\d+)", url_parts[2])
            if ride and ride.group(1):
                recent_ride = strava_get_ride_extended_info(ride.group(1))
                if recent_ride:
                    e.output = strava_ride_to_string(recent_ride)
                else:
                    e.output = "Sorry %s, an error has occured attempting to retrieve ride details for %s." % (e.nick, url)
                return e
    else:
        return
strava_line_parser.lineparser = True


def strava_set_athlete(self, e):
    """ Set an athlete's user ID. """
    if e.input.isdigit():
        # Insert the user strava id, we should probably validate the user though right?
        if (strava_is_valid_user(e.input)):
            strava_insert_athlete(e.nick, e.input)
        else:
            # Inform the user that the strava id isn't valid.
            self.irccontext.privmsg(e.nick, "Sorry that is not a valid Strava user.")
    else:
        # Bark at stupid users.
        self.irccontext.privmsg(e.nick, "Usage: !strava-set <strava id>")


strava_set_athlete.command = "!strava-set"
strava_set_athlete.helptext = """
                        Usage: !strava-set <strava id>
                        Example: !strava-set 12345
                        Saves your strava id to the bot.
                        Once your strava id is saved you can use those commands without an argument."""


def strava(self, e):
    strava_id = strava_get_athlete(e.nick)
    if e.input:
        # Process a last ride request for a specific strava id.
        response = urllib.request.urlopen('http://app.strava.com/api/v1/rides?athleteId=%s' % e.input)
        rides_response = json.loads(response.read().decode('utf-8'))
        e.output = strava_extract_latest_ride(rides_response, e)
    elif strava_id:
        # Process the last ride for the current strava id.
        response = urllib.request.urlopen('http://app.strava.com/api/v1/rides?athleteId=%s' % strava_id)
        rides_response = json.loads(response.read().decode('utf-8'))
        e.output = strava_extract_latest_ride(rides_response, e)
    else:
        e.output = "Sorry %s, you don't have a Strava ID setup yet, please enter one with the !strava-set command." % e.nick
    return e


strava.command = "!strava"
strava.helptext = """
                        Usage: !strava [strava id]"
                        Example: !strava-last, !strava-last 12345
                        Gets the information about the last ride for the strava user.
                        If you have a strava id set with !strava-set you can use this command without an arguement.
                        """


def strava_extract_latest_ride(response, e):
    """ Grab the latest ride from a list of rides and gather some statistics about it """
    if 'rides' in response:
        recent_ride = response['rides'][0]
        recent_ride = strava_get_ride_extended_info(recent_ride['id'])
        if recent_ride:
            return strava_ride_to_string(recent_ride)
        else:
            return "Sorry %s, an error has occured attempting to retrieve the most recent ride's details." % e.nick
    else:
        return "Sorry %s, no rides have been recorded yet." % e.nick


def strava_ride_to_string(recent_ride):
    # Convert a lot of stuff we need to display the message
    mph = strava_convert_meters_per_second_to_miles_per_hour(recent_ride['averageSpeed'])
    miles = strava_convert_meters_to_miles(recent_ride['distance'])
    moving_time = str(datetime.timedelta(seconds=recent_ride['movingTime']))
    max_mph = strava_convert_meters_per_hour_to_miles_per_hour(recent_ride['maximumSpeed'])
    feet_climbed = strava_convert_meters_to_feet(recent_ride['elevationGain'])
    ride_datetime = time.strptime(recent_ride['startDateLocal'], "%Y-%m-%dT%H:%M:%SZ")
    time_start = time.strftime("%B %d, %Y at %I:%M %p", ride_datetime)
    # Output string
    return_string = "%s rode %s near %s on %s (http://app.strava.com/rides/%s)\n" % (recent_ride['athlete']['name'], recent_ride['name'], recent_ride['location'], time_start, recent_ride['id'])
    return_string += "Ride Stats: %s mi in %s | %s mph average / %s mph max | %s feet climbed" % (miles, moving_time, mph, max_mph, int(feet_climbed))
    # Figure out if we need to add average watts to the string.
    # Users who don't have a weight won't have average watts.
    if 'averageWatts' in recent_ride:
        return_string += " | %s watts average power" % (int(recent_ride['averageWatts']))
    return return_string


def strava_get_ride_extended_info(ride_id):
    """ Get all the details about a ride. """
    response = urllib.request.urlopen("http://app.strava.com/api/v1/rides/%s" % ride_id)
    ride_details = json.loads(response.read().decode('utf-8'))
    if 'ride' in ride_details:
        return ride_details['ride']
    else:
        return False


def strava_get_ride_efforts(ride_id):
    """ Get all the efforts (segments and their respective performance) from a ride. """
    response = urllib.request.urlopen("http://www.strava.com/api/v1/rides/%s/efforts" % ride_id)
    ride_efforts = json.loads(response.read().decode('utf-8'))
    if 'efforts' in ride_efforts:
        return ride_efforts['efforts']
    else:
        return False


def strava_get_ride_distance_since_date(athlete_id, begin_date, offset_count=0):
    """ Recursively aggregate all of the ride mileage since the begin_date by using strava's pagination """
    ride_distance_sum = 0
    response = urllib.request.urlopen("http://app.strava.com/api/v1/rides?date=%s&athleteId=%s&offset=%s" % (begin_date, athlete_id, offset_count))
    rides_details = json.loads(response.read().decode('utf-8'))
    if 'rides' in rides_details:
        for ride in rides_details['rides']:
            ride_details = strava_get_ride_extended_info(ride['id'])
            if 'distance' in ride_details:
                ride_distance_sum = ride_distance_sum + strava_convert_meters_to_miles(ride_details['distance'])
        ride_distance_sum = ride_distance_sum + strava_get_ride_distance_since_date(athlete_id, begin_date, offset_count + 50)
    else:
        return ride_distance_sum


def strava_is_valid_user(strava_id):
    try:
        response = urllib.request.urlopen("http://app.strava.com/athletes/%s" % strava_id)
        return True
    except urllib.error.URLError as e:
        return False


def strava_convert_meters_per_second_to_miles_per_hour(mps):
    mph = 2.23694 * float(mps)
    return round(mph, 1)


def strava_convert_meters_per_hour_to_miles_per_hour(meph):
    mph = 0.000621371192 * float(meph)
    return round(mph, 1)


def strava_convert_meters_to_miles(meters):
    miles = 0.000621371 * float(meters)
    return round(miles, 1)


def strava_convert_meters_to_feet(meters):
    feet = 3.28084 * float(meters)
    return round(feet, 1)
