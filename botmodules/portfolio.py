import sqlite3

def portfolio(self, e):
	
	args = e.input.upper().split()
	nick = e.nick.upper()
	
	if len(args) == 4:		# arguments for adding stock
		command,stock,numshares,pricepaid = args
		if command != "ADD":
			return
		
		e.notice = True
		e.output = add_stock(nick, stock, numshares, pricepaid)
		return e
			
		
	elif len(args) == 2:	# arguments for deleting stock
		command,stock_rowid = args
		if command != "DEL":
			return
		
		e.notice = True
		e.output = del_stock(nick, stock_rowid)
		return e
		
	elif len(args) == 1:	# argument for listing portfolio
		command = args[0]
		if command != "LIST":
			return
		
		e.notice = True
		e.output = list_stock(nick)
		
	elif len(args) == 0:
		#e.output = get_user_portfolio(user)
		#return e
		pass #not done yet
		
	
	return e

def add_stock(nick,stock,numshares,pricepaid):
	conn = sqlite3.connect('portfolios.sqlite')
	c = conn.cursor()
	result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolios';").fetchone()
	if not result:
		c.execute('''create table portfolios(user text, stock text, numshares integer, pricepaid real)''')
	

	c.execute("INSERT INTO portfolios VALUES (%s, %s, %s, %s)" % (nick,stock,numshares,pricepaid))
	return "Added %s shares of %s at $%s." % (numshares, stock, pricepaid)

def del_stock(nick, stock_rowid):
	return "Deleted portfolio entry #%s" % (stock_rowid)

def list_stock(nicK):
	#conn = sqlite3.connect('portfolios.sqlite')
	#c = conn.cursor()
	#result = c.execute("SELECT stock, numshares, pricepaid FROM portfolios WHERE user=%s" % (nick)).fetchall()
	#if result:
				
	
	return "You so poor\nnyah nyah nyah\nNYAH"
		
	

portfolio.command = "!portfolio"
portfolio.helptext = "!portfolio help text"
