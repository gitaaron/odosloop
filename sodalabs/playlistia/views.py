# Create your views here.
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse,Http404
import gdata.youtube
import gdata.youtube.service
import django.utils.simplejson as json
import urllib
from lxml.html import fromstring
from lxml import etree

lastfm_api_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&api_key=575da82dcdf635b030df7efa4386e351&limit=100&user='


def profile(request):
    username = request.GET.get('username',False)
    if not username:
        username = 'surtyaar'
    # compile lastfm list of name,artist 
    lastfm_recents = []
    try:
        content = urllib.urlopen(lastfm_api_url+username).read()
    except IOError:
        raise Http404()
    doc = fromstring(content)
    track_path = etree.XPath('//track')
    tracks = track_path(doc)
    for track in tracks:
        artist = track.find('artist').text_content()
        name = track.find('name').text_content()
        lastfm_recents.append({'name':name,'artist':artist})

    
    return direct_to_template(request, 'playlistia/profile.html', {'lastfm_recents': lastfm_recents})

def open(request):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    q = request.GET.get('q',False)
    if not q:
        raise Http404()

    query.vq = q
    query.max_results = 25
    feed = client.YouTubeQuery(query)
    video_id = ''
    for entry in feed.entry:
        if not entry.noembed:
            break

    if entry: 
        dict = {'video_id':entry.id.text.split('/').pop(), 'video_title':entry.title.text}
    else:
        raise Http404()

    return HttpResponse(json.dumps(dict), content_type="application/json")
