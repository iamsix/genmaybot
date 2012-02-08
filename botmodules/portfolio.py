import sqlite3

#def add_stock(self, e):
	
	#conn = sqlite3.connect('portfolios.sqlite')
	#c = conn.cursor()
	#result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolios';").fetchone()
	#if not result:
	#	c.execute('''create table portfolios(user text, stock text UNIQUE ON CONFLICT REPLACE, numshares integer, pricepaid real)''')
	
#	pass	
	#c.execute("INSERT INTO portfolios 

def portfolio(self, e):
	e.output = "what the fuck"
	return e

portfolio.command = "!portfolio"
portfolio.helptext = "!portfolio help text"
