import json
import urllib.request


def ytinfo(self, e, urlposted=False):
    if urlposted:
        yt = e.input
        if "youtu" not in yt and "watch" not in yt:
            return
        yt = yt[yt.find("v=") + 2:]
        if "&" in yt:
            yt = yt[:yt.find("&")]
    else:
        yt = self.tools['google_url']('site:youtube.com {}'.format(e.input), 'watch%3Fv%3D')
        yt = yt[yt.find("%3Fv%3D") + 7:]

    print(yt)
    url = "http://gdata.youtube.com/feeds/api/videos/{}?v=2&alt=jsonc".format(yt)
    print(url)
    request = urllib.request.urlopen(url)
    ytinfo = json.loads(request.read().decode())
    ytinfo = ytinfo['data']
    mins = round(ytinfo['duration'] /60)
    if mins:
        mins = "{}m ".format(str(mins))
    secs = ytinfo['duration']  % 60
    if secs:
        secs = "{}s ".format(str(secs))
    duration = "{}{}".format(mins, secs)
    rating = "{0:.1f}/10".format((int(ytinfo['likeCount']) / ytinfo['ratingCount']) * 10)
    ytlink = ""
    if not urlposted:
        ytlink = " - http://youtu.be/" + yt
    print("whatttt")
    e.output = "{} - length {}- rated {} - {} views - {} on {}{}".format(ytinfo['title'],
                                                                        duration,
                                                                        rating,
                                                                        ytinfo['viewCount'],
                                                                        ytinfo['uploader'],
                                                                        ytinfo['uploaded'][:10],
                                                                        ytlink)
    return e
ytinfo.command = "!yt"
