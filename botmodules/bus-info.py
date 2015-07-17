import urllib.request, urllib.parse, xml.dom.minidom

def get_bus_times(self, e):
    query = urllib.parse.urlencode({"token":"c1426e9c-b9d7-4dc5-a561-84a78e1f0b86", "stopcode":"60383"})
    url = "http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx"

    #Load XML response and parse DOM in one shot
    dom = xml.dom.minidom.parse(urllib.request.urlopen("%s?%s" % (url,query)))

    routes = dom.getElementsByTagName("Route")

    output = ""

    for route in routes:
        
        depart_times = []
        route_code = route.getAttribute('Code')

        for depart_time in route.getElementsByTagName('DepartureTime'):
            depart_times.append(depart_time.childNodes[0].nodeValue)

        output+=("Route %s: %s min\n" % (route_code, ", ".join(depart_times)))
    e.output = output    
    return e

get_bus_times.command="!bus"
