# No longer maintaned

I maintan a discord version at [Palbot](https://github.com/iamsix/palbot)  

The fork at [KpaBap/genmaybot](https://github.com/KpaBap/genmaybot/tree/cycling) is maintaned

# Vagrant Easy Setup

1. Install Vagrant (http://www.vagrantup.com/)
2. Copy genmaybot.cfg.example to genmaybot.cfg and change the config.
3. cd into the repo's working directory.
4. vagrant up
5. Profit, or develop or something?

This is the Python 3.x branch - it works, for Brak's pleasure.

The following non-standard Python modules need to be installed:

Python IRC Library
http://python-irclib.sourceforge.net/
Note: A Python3 compatible port has been included in this repo

BeautifulSoup 4.1.0
http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.1.0.tar.gz
Note: run "2to3 -w bs4" before installing

CherryPy is required
http://download.cherrypy.org/cherrypy/3.2.2/CherryPy-3.2.2.tar.gz

sqlite3 is required

Remember to set your API keys and ident password in the .cfg

This bot is created as a learning project, and may not be suitable for production environments.
No warranties or guarantees are given. The creators take no responsibilty for damage/attacks/etc.
