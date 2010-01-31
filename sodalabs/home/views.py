# Create your views here.
from django.views.generic.simple import direct_to_template
from sodalabs.lastfm import make_lastfm_request,get_tracks

def index(request):
    q = request.GET.get('q', False)
    if not q:
        return direct_to_template(request, 'index.html')
        
    doc = make_lastfm_request('track.search', {'track':q})
    tracks = get_tracks(doc) 

    return direct_to_template(request, 'index.html', {'lastfm_tracks':tracks, 'q':q}) 
