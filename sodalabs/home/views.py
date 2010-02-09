# Create your views here.
from django.views.generic.simple import direct_to_template
from sodalabs.lastfm import make_lastfm_request,get_tracks
from sodalabs.accounts.models import PlayHistory
from sodalabs.playlist.helpers import ordered_unique

def index(request):
    q = request.GET.get('q', '')
    if q:        
        doc = make_lastfm_request('track.search', {'track':q})
        tracks = get_tracks(doc) 
        playlist_title = 'search results for : ' + q
    else:
        songs_played = PlayHistory.objects.all().order_by('created_at').reverse()[0:15]
        tracks = []
        for play in songs_played:
            lastfm_track = play.song.lastfm_track
            tracks.append({'name':lastfm_track.name, 'artist':lastfm_track.artist,'created_at':play.created_at})

        tracks = ordered_unique(tracks)
        playlist_title = 'recently listened to'

    return direct_to_template(request, 'index.html', {'playlist_title':playlist_title, 'lastfm_tracks':tracks, 'q':q}) 
