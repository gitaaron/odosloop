# Create your views here.
from sodalabs.rest_ws.helpers import ResponseNotAllowed,ResponseBadRequest,HttpResponse
from django.http import Http404,HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.generic.simple import direct_to_template
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from sodalabs.lastfm.models import Track
from sodalabs.accounts.models import Musiphile
from sodalabs.playlist.models import PlaylistUser,Playlist,PlaylistSong
from sodalabs.playlist.helpers import ordered_unique

def get(request, slug_name):
    if slug_name=='anonymous':
        playlist = Playlist()
        playlist.name = 'untitled playlist'
        tracks = request.session.get('playlist',[])
    else:
        try:
            playlist = Playlist.objects.get(slug_name=slug_name)
        except Playlist.DoesNotExist:
            raise Http404()

        tracks = playlist.lastfm_track.all()

    
    
    return direct_to_template(request, 'includes/playlist.html', {'playlist_id':'playlist_%s' % slug_name, 'playlist_title':playlist.name, 'lastfm_tracks':tracks})

def menu_list(request, username=None):
    show_create = False
    playlists = None
    if username:
        if username=='me':
            playlists = [];
            playlists.append({'id':-1, 'name':'untitled playlist', 'slug_name':'anonymous'})
        else:
            try:
                user = Musiphile.objects.get(username=username)
            except Musiphile.DoesNotExist:
                raise Http404()

            playlists = Playlist.objects.filter(users=user)


            if request.user.is_authenticated():
                if request.user == user:
                    show_create = True


    return direct_to_template(request, 'includes/menu.html', {'playlists':playlists, 'show_create_button':show_create})

@login_required
def json_list(request):
    musiphile = Musiphile.objects.from_request(request)
    if not musiphile:
        return HttpResponse(json.dumps({'status':'failed','message':'User is not a musiphile'}), content_type="application/json")
   
    playlists = Playlist.objects.filter(users=musiphile)

    l = [{'id':p.id,'name':p.name} for p in playlists]
    return HttpResponse(json.dumps({'status':'ok', 'playlists':l}), content_type="application/json")

def add(request):
    if request.method!="POST":
        return ResponseNotAllowed(['POST'])

    lastfm_track_id = request.POST.get('lastfm_track',None)
    if not lastfm_track_id:
        return ResponseBadRequest('Required lastfm_track_song_id was not specified.')

    try:
        lastfm_track = Track.objects.get(id=lastfm_track_id)
    except Track.DoesNotExist:
        return ResponseBadRequest('Could not find track with id : %s' % lastfm_track_id)

    playlist = None
    playlist_id = request.POST.get('playlist', None)
    if playlist_id:
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return ResponseBadRequest('Could not find playlist with id : %s' % playlist_id) 


    if request.user.is_authenticated():
        musiphile = Musiphile.objects.get(id=request.user.id)
        # if no playlist was specified, use the first one found
        if not playlist: # create a new one for this user and add the song to that playlist
            playlist = Playlist(creator=musiphile)
            playlist.save()
            playlist_user = PlaylistUser(playlist=playlist,user=musiphile)
            playlist_user.save()

        # ensure the song has not already been added to the playlist
        try:
            playlist_song = PlaylistSong.objects.get(lastfm_track=lastfm_track,playlist=playlist)
        except PlaylistSong.DoesNotExist:
            # add song to playlist
            playlist_song = PlaylistSong(lastfm_track=lastfm_track,playlist=playlist)
            playlist_song.save()

    else:
        playlist = request.session.get('playlist',[])
        was_added=False
        for item in playlist:
            if item==lastfm_track.id:
                was_added=True
                break
        if not was_added:
            playlist.append(lastfm_track)

        request.session['playlist'] = playlist
        
    return HttpResponse(json.dumps({'status':'ok'}), content_type="application/json")

@login_required
def create(request):
    musiphile = Musiphile.objects.from_request(request)
    if not musiphile:
        return HttpResponse(json.dumps({'status':'failed','message':'User is not a musiphile'}), content_type="application/json")

    pls = Playlist(creator=musiphile)
    pls.save()
    pls_user = PlaylistUser(user=musiphile,playlist=pls)
    pls_user.save()

    return HttpResponse(json.dumps({'status':'ok','playlist_id':pls.id}), content_type="application/json")

@login_required
def save(request):
    musiphile = Musiphile.objects.from_request(request)
    if not musiphile:
        raise Http404()

    if request.method!='POST':
        return HttpResponseNotAllowed(['POST'])

    playlist_id = request.POST.get('playlist_id')
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404()

    if playlist.creator == musiphile: 
        playlist.name = request.POST.get('name')
        playlist.save()
        return HttpResponse(json.dumps({'status':'ok'}), content_type="application/json")
    else:
        return HttpResponseForbidden()

