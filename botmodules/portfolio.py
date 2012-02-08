import sqlite3

def portfolio(self, e):
	
	args = e.input.upper().split()
	nick = e.nick.upper()
	
		
	if len(args) == 4:		# arguments for adding stock
		command,stock,numshares,pricepaid = args
		if command != "ADD":
			return
		
		e.source = e.nick
		e.notice = True
		e.output = add_stock(nick, stock, numshares, pricepaid)
		return e
			
		
	elif len(args) == 2:	# arguments for deleting stock
		command,stock_rowid = args
		if command != "DEL":
			return
			
		e.source = e.nick		
		e.notice = True
		e.output = del_stock(nick, stock_rowid)
		return e
		
	elif len(args) == 1:	# argument for listing portfolio
		command = args[0]
		if command != "LIST":
			return
		e.source = e.nick
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
	
	if type(stock) is not str or type(numshares) is not int or type(pricepaid) is not float or type(pricepaid) is not int
	
	c.execute("INSERT INTO portfolios VALUES (?,?,?,?)", (nick,stock,numshares,pricepaid))
	conn.commit()
	conn.close()
	
	return "Added %s shares of %s at $%s." % (numshares, stock, pricepaid)

def del_stock(nick, stock_rowid):
	

	return "Deleted portfolio entry #%s" % (stock_rowid)

def list_stock(nick):
	conn = sqlite3.connect('portfolios.sqlite')
	c = conn.cursor()
	try:
		result = c.execute("SELECT rowid, stock, numshares, pricepaid FROM portfolios WHERE user='?'", (nick)).fetchall()
	except:
		return "You're too poor to own stock."
		
	
	conn.close()
	
	return_line="ID%s%s%s\n" % ("Symbol".center(10),"# of Shares".center(15),"Price Paid".center(12))
	
	if result:
		for stock in result:
			return_line += "%s\t%s\t%s\t%s\n" % (stock[0],stock[1].center(10),str(stock[2]).center(15),str(stock[3]).center(12))
		return return_line
	else: 
		return "You're too poor to own stock."
	
		
	

portfolio.command = "!portfolio"
portfolio.helptext = "!portfolio help text"
