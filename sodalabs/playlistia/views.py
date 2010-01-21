# Create your views here.
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse,Http404
import gdata.youtube
import gdata.youtube.service
import django.utils.simplejson as json
import urllib
from lxml.html import fromstring
from lxml import etree


def _get_lastfm_api_url(method,params):
    url = 'http://ws.audioscrobbler.com/2.0/?method=%s&api_key=575da82dcdf635b030df7efa4386e351' % method
    for key in params:
        url+='&'+key+'='+params[key]
    return url 

def _make_lastfm_request(method,params={}):
    try:
        lastfm_url = _get_lastfm_api_url(method,params)
        content = urllib.urlopen(lastfm_url).read()
        return fromstring(content)

    except IOError:
        return None

error_path = etree.XPath('//error')
track_path = etree.XPath('//track')
user_path = etree.XPath('//user')

def profile(request, username=None):
    if not username:
        username = request.GET.get('username',None)
    if not username:
        return diret_to_template(request,'playlistia/index.html',{'message':'Your request is missing a required paramater.'})
    # compile lastfm list of name,artist 

    doc = _make_lastfm_request('user.getrecenttracks',{'limit':'100','user':username})
    if not doc:
        return direct_to_template(request, 'playlistia/index.html',{'message':'A problem occured accessing the last.fm api.'})
    errors = error_path(doc)
    if errors:
        return direct_to_template(request, 'playlistia/index.html',{'message':errors[0].text_content()})

    lastfm_recents = []
    tracks = track_path(doc)
    for track in tracks:
        artist = track.find('artist').text_content()
        name = track.find('name').text_content()
        lastfm_recents.append({'name':name,'artist':artist})

    lastfm_friends = []
    doc = _make_lastfm_request('user.getfriends',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_friends.append({'name':user.find('name').text_content()})

    lastfm_neighbours = []
    doc = _make_lastfm_request('user.getneighbours',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_neighbours.append({'name':user.find('name').text_content()})

    return direct_to_template(request, 'playlistia/profile.html', {'lastfm_recents': lastfm_recents, 'lastfm_friends':lastfm_friends, 'lastfm_neighbours':lastfm_neighbours, 'username':username})

def open(request):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    q = request.GET.get('q',False)
    if not q:
        return HttpResponse(json.dumps({'status':'failed','message':'search term missing'}),content_type="application/json")

    query.vq = q
    query.max_results = 25
    feed = client.YouTubeQuery(query)
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
