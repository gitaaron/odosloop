import urllib, traceback
from lxml.html import fromstring
from lxml import etree
from sodalabs.playlist.helpers import ordered_unique

error_path = etree.XPath('//error')
track_path = etree.XPath('//track')
user_path = etree.XPath('//user')

def get_tracks(doc):
    tracks = track_path(doc)

    lastfm_tracks = []
    for track in tracks:
        artist = track.find('artist').text_content()
        name = track.find('name').text_content()
        lastfm_tracks.append({'name':_encode(name),'artist':_encode(artist)})

    lastfm_tracks = ordered_unique(lastfm_tracks)

    return lastfm_tracks

def get_similar_tracks(doc):
    tracks = track_path(doc)

    lastfm_tracks = []
    for track in tracks:
        artist_obj = track.find('artist')
        artist_name = artist_obj.find('name').text_content()
        name = track.find('name').text_content()
        lastfm_tracks.append({'name':_encode(name),'artist':_encode(artist_name)})

    lastfm_tracks = ordered_unique(lastfm_tracks)

    return lastfm_tracks


def _encode(str):
    return str.encode('iso-8859-15','replace')


def _get_lastfm_api_url(method,params):
    url = 'http://ws.audioscrobbler.com/2.0/?method=%s&api_key=575da82dcdf635b030df7efa4386e351' % method
    for key in params:
        url+='&'+key+'='+urllib.quote(params[key])
    return url 

def make_lastfm_request(method,params={}):
    lastfm_url = _get_lastfm_api_url(method,params)
    content = urllib.urlopen(lastfm_url).read()
    return fromstring(content)


