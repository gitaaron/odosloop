# Create your views here.
import urllib
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse,Http404
import gdata.youtube
import gdata.youtube.service
import django.utils.simplejson as json


def open(request):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    q = request.GET.get('q',False)
    if not q:
        return HttpResponse(json.dumps({'status':'failed','message':'search term missing'}),content_type="application/json")

    query.vq = _unescape(urllib.unquote(q))
    query.max_results = 25
    try:
        feed = client.YouTubeQuery(query)
    except KeyError:
        return HttpResponse(json.dumps({'status':'failed','message':'a problem occured while searching youtube for the appropriate song'}),content_type="application/json")
    video_id = ''
    embedable_found = False
    for entry in feed.entry:
        if not entry.noembed:
            embedable_found = True
            break

    if not feed.entry:
        return HttpResponse(json.dumps({'status':'failed', 'message':'no results returned'}),content_type="application/json")
    elif not embedable_found:
        return HttpResponse(json.dumps({'status':'failed', 'message':'no embedable songs found'}),content_type="application/json")
    else:
        dict = {'status':'ok', 'video_id':entry.id.text.split('/').pop(), 'video_title':entry.title.text}

    return HttpResponse(json.dumps(dict), content_type="application/json")




##PRAGNOTE Taken from http://effbot.org/zone/re-sub.htm#unescape-html

import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def _unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
