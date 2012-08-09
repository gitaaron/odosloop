# Create your views here.
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from sodalabs.lastfm import make_lastfm_request,get_tracks,error_path,user_path


def search(request):
    q = request.GET.get('q', False)
    if q:
        doc = make_lastfm_request('track.search',{'track':q})
        tracks = get_tracks(doc)
        return HttpResponse(json.dumps(tracks))
    else:
        raise Http404()
