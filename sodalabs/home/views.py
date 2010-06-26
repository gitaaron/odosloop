# Create your views here.
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from sodalabs.lastfm import make_lastfm_request,get_tracks
from sodalabs.accounts.models import PlayHistory
from sodalabs.playlist.helpers import ordered_unique
from lastfm import _encode

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))


def feed(request):
    songs_played = PlayHistory.objects.all().order_by('created_at').reverse()[0:50]
    tracks = []
    for play in songs_played:
        lastfm_track = play.song.lastfm_track
        tracks.append({'name':_encode(lastfm_track.name), 'artist':_encode(lastfm_track.artist),'created_at':play.created_at})

    tracks = ordered_unique(tracks)
    playlist_title = 'recently listened to on odosloop'

    return direct_to_template(request, 'includes/playlist.html', {'playlist_id':'feed','playlist_title':playlist_title, 'lastfm_tracks':tracks})
