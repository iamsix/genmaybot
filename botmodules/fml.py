import urllib.request, urllib.error, urllib.parse

def get_fml(self, e):
    #queries a random fmylife.com passage
	fmlxml = urllib.request.urlopen("http://api.betacie.com/view/random?key=%s&language=en" % self.botconfig["APIkeys"]["fmlAPIkey"]).read().decode('utf-8')
	start = fmlxml.find("<text>") + 6
	end = fmlxml.find("</text>")

	fml = fmlxml[start:end]

	start = fmlxml.find("<agree>") + 7
	end = fmlxml.find("</agree>")

	fml = fml + " [FYL: " + str(fmlxml[start:end])

	start = fmlxml.find("<deserved>") + 10
	end = fmlxml.find("</deserved>")

	fml = fml + " Deserved it: " + str(fmlxml[start:end]) + "]"


	fml = fml.replace('&quot;', '"')
	fml = fml.replace('&amp;quot;', '"')
	fml = fml.replace('&amp;', "&")
	e.output = self.tools['decode_htmlentities'](fml)

	return e

get_fml.command = "!fml"
get_fml.helptext = "Usage: !fml\nShows a random entry from fmylife.com"

