import urllib2, socket
import botmodules.tools as tools

def advocate_beer(query):
    url = tools.google_url("site:beeradvocate.com " + query, "/beer/profile/[0-9]*/")
    #url = "http://beeradvocate.com/beer/profile/306/1212/"
    socket.setdefaulttimeout(30)
    try:
      beerpage = urllib2.urlopen(url).read()#.decode("ISO-8859-1")
    except:
      return
    socket.setdefaulttimeout(10)
    
    titlestart = beerpage.find("<title>") + 7
    titleend = beerpage.find(" - ", titlestart)
    beertitle = beerpage[titlestart:titleend]

    score_start_tag = '<span class="BAscore_big">'
    score_end_tag = 'Reviews</td>'

    start = beerpage.find(score_start_tag) + len(score_start_tag)
    score_line = beerpage[start:start+50]

    find_start_tag = "</span>\n<br>"
    find_end_tag = "<br>"

    #print score_line

    grade = score_line[0:score_line.find(find_start_tag)]

    #print "\n" + grade
    grade_wording = score_line[score_line.find(find_start_tag)+len(find_start_tag):score_line.rfind(find_end_tag)]
    #print grade_wording


    find_start_tag = find_end_tag
    find_end_tag = "</td>"

    num_reviews = score_line[score_line.rfind(find_start_tag)+len(find_start_tag):score_line.find(find_end_tag)]

    #print num_reviews

    find_start_tag = "Style | ABV"
    style_line = beerpage[beerpage.find(find_start_tag):beerpage.find(find_start_tag)+120]

    find_start_tag = "><b>"
    find_end_tag = "</b></a> | &nbsp;"

    style = style_line[style_line.find(find_start_tag)+len(find_start_tag):style_line.find(find_end_tag)]

    find_start_tag = find_end_tag
    find_end_tag = "% <a href"

    abv = style_line[style_line.find(find_start_tag)+len(find_start_tag):style_line.find(find_end_tag)+1]
    response_string = "Beer: %s - Grade: %s [%s, %s] Style: %s ABV: %s [ %s ]" % (beertitle, grade, grade_wording, num_reviews, style, abv, tools.shorten_url(url))
    
    return response_string
advocate_beer.command = "!beer"