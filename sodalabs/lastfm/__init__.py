import urllib, traceback
from lxml.html import fromstring
from lxml import etree

error_path = etree.XPath('//error')
track_path = etree.XPath('//track')
user_path = etree.XPath('//user')

def get_tracks(doc):
    tracks = track_path(doc)

    lastfm_tracks = []
    for track in tracks:
        artist = track.find('artist').text_content()
        name = track.find('name').text_content()
        lastfm_tracks.append((name,artist))

    lastfm_tracks = set(lastfm_tracks)
    tracks = []
    for track in lastfm_tracks:
        tracks.append({'name':track[0],'artist':track[1]})

    return tracks

def get_similar_tracks(doc):
    tracks = track_path(doc)

    lastfm_tracks = []
    for track in tracks:
        artist_obj = track.find('artist')
        artist_name = artist_obj.find('name').text_content()
        name = track.find('name').text_content()
        lastfm_tracks.append((name,artist_name))

    lastfm_tracks = set(lastfm_tracks)
    tracks = []
    for track in lastfm_tracks:
        tracks.append({'name':track[0],'artist':track[1]})

    return tracks





def _get_lastfm_api_url(method,params):
    url = 'http://ws.audioscrobbler.com/2.0/?method=%s&api_key=575da82dcdf635b030df7efa4386e351' % method
    for key in params:
        url+='&'+key+'='+urllib.quote(params[key])
    return url 

def make_lastfm_request(method,params={}):
    lastfm_url = _get_lastfm_api_url(method,params)
    content = urllib.urlopen(lastfm_url).read()
    return fromstring(content)


