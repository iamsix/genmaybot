import urllib2, time
from BeautifulSoup import BeautifulSoup

def get_unalaska_blotter(self, e):
	url = "http://kucb.org/community/blotter/"
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
	pagetmp = opener.open(url)
	page = pagetmp.read()
	opener.close()

	page = BeautifulSoup(page)
	try:
		blots = page.findAll('div',attrs={'id' : 'blots'})[0]
		firstBlot = blots.findAll('div',attrs={'class' : 'blot'})[0]

		headline = firstBlot.findAll('span',attrs={'class' : 'headline small'})[0].string
		blotdate = firstBlot.findAll('span',attrs={'class' : 'date'})[0].string
		details = firstBlot.findAll('span',attrs={'class' : 'details'})[0].string
	except:
		print "\nSomething went wrong with processing the blotter page in unalaska_blotter.py\n"
		pass
	
	#Convert date to a bit shorter format
	blotdate = blotdate.replace(".","")
	blotdate = time.strftime("%H:%M %a %m/%d/%y",time.strptime(s, "%A %d %B %Y, %I:%M %p"))
	
	e.output = "%s [%s] %s" % (headline,blotdate,details)
	return e

get_unalaska_blotter.command="!blot"
get_unalaska_blotter.helptext = "Usage: !blot\n Retrieve the latest witty police blotter entry from the city of Unalaska, Alaska"
