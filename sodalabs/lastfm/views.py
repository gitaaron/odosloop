# Create your views here.
from django.http import Http404
from django.views.generic.simple import direct_to_template
from sodalabs.lastfm import make_lastfm_request,get_tracks,error_path,user_path

def search(request):
    q = request.GET.get('q', False)
    if q:
        doc = make_lastfm_request('track.search',{'track':q})
        tracks = get_tracks(doc)
        playlist_title = 'search results for : ' + q
        return direct_to_template(request, 'includes/playlist.html', {'playlist_id':'search', 'playlist_title':playlist_title, 'lastfm_tracks':tracks})
    else:
        raise Http404()

def profile(request, username=None):
    """
    For now just look the user up in last.fm and display their info.
    """
    #@TODO error templates do not exist anymore
    if not username:
        username = request.GET.get('username',None)
    if not username:
        return direct_to_template(request,'playlist/index.html',{'message':'Your request is missing a required paramater.'})
    # compile lastfm list of name,artist 

    doc = make_lastfm_request('user.getrecenttracks',{'limit':'100','user':username})
    if not doc:
        return direct_to_template(request, 'playlist/index.html',{'message':'A problem occured accessing the last.fm api.'})
    errors = error_path(doc)
    if errors:
        return direct_to_template(request, 'playlist/index.html',{'message':errors[0].text_content()})

    lastfm_recents = []
    lastfm_recents = get_tracks(doc) 

    lastfm_friends = []
    doc = make_lastfm_request('user.getfriends',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_friends.append({'name':user.find('name').text_content()})

    lastfm_neighbours = []
    doc = make_lastfm_request('user.getneighbours',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_neighbours.append({'name':user.find('name').text_content()})

    return direct_to_template(request, 'lastfm/profile.html', {'playlist_id':'feed', 'playlist_title':'recently scrobbled', 'lastfm_tracks': lastfm_recents, 'lastfm_friends':lastfm_friends, 'lastfm_neighbours':lastfm_neighbours, 'username':username})



