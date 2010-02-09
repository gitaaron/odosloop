# Create your views here.
from django.http import Http404
from django.views.generic.simple import direct_to_template
from sodalabs.lastfm import make_lastfm_request,get_similar_tracks
from sodalabs.lastfm.models import Track

def get_similar(request):
    lastfm_track_id = request.GET.get('lastfm_track',False)
    if not lastfm_track_id:
        raise Http404()

    try:
        lastfm_track = Track.objects.get(id=lastfm_track_id)
    except Track.DoesNotExist:
        raise Http404()

    doc = make_lastfm_request('track.getsimilar',{'track':lastfm_track.name,'artist':lastfm_track.artist})
    tracks = get_similar_tracks(doc)
    return direct_to_template(request, 'index.html', {'playlist_title':'radio','lastfm_tracks':tracks,'q':lastfm_track.artist + ' - ' + lastfm_track.name})
