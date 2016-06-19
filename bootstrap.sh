#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y python-cherrypy3
apt-get install -y sqlite3
cd /vagrant/support/python-irclib-0.4.8
python3 setup.py install
cd /vagrant/support
wget http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.1.0.tar.gz
tar -xzvf beautifulsoup4-4.1.0.tar.gz
cd beautifulsoup4-4.1.0
2to3 -w bs4
python3 setup.py install
cd /vagrant
python3 genmaybot.py &
