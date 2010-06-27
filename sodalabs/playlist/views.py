# Create your views here.
from sodalabs.rest_ws.helpers import ResponseNotAllowed,ResponseBadRequest,HttpResponse
from django.http import Http404,HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.generic.simple import direct_to_template
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from sodalabs.jukebox.models import LastFMTrackSong
from sodalabs.accounts.models import Musiphile
from sodalabs.playlist.models import PlaylistUser,Playlist,PlaylistSong
from sodalabs.playlist.helpers import ordered_unique

def get(request, slug_name):
    '''
    if username=='me':
        lastfm_track_songs = request.session.get('playlist',[])
        tracks = []
        for song in lastfm_track_songs:
            lastfm_track = song.lastfm_track
            tracks.append({'name':lastfm_track.name,'artist':lastfm_track.artist})

        playlist_title = 'Favorites'
    else:
        try:
            musiphile = Musiphile.objects.get(username=username)
        except Musiphile.DoesNotExist:
            raise Http404()

        try:
            playlist_user = PlaylistUser.objects.get(playlist__name=name, user=musiphile)
        except PlaylistUser.DoesNotExist:
            raise Http404()

        tracks = []
        playlist_songs = playlist_user.playlist.playlistsong_set.all()
        for playlist_song in playlist_songs:
            lastfm_track = playlist_song.lastfm_track_song.lastfm_track
            tracks.append({'name':lastfm_track.name, 'artist':lastfm_track.artist})

        playlist_title = playlist_user.playlist.name

    tracks = ordered_unique(tracks)

    return direct_to_template(request, 'accounts/playlist.html', {'playlist_id':playlist_title.slugify(), 'playlist_title':playlist_title, 'lastfm_tracks':tracks})
    '''
    return HttpResponse('ok')

def menu_list(request, username):
    try:
        user = Musiphile.objects.get(username=username)
    except Musiphile.DoesNotExist:
        raise Http404()

    playlists = Playlist.objects.filter(users=user)

    show_create = False
    if request.user.is_authenticated():
        if request.user == user:
            show_create = True

    return direct_to_template(request, 'includes/menu.html', {'playlists':playlists, 'show_create_button':show_create})
    

def add(request):
    if request.method!="POST":
        return ResponseNotAllowed(['POST'])

    lastfm_track_song_id = request.POST.get('lastfm_track_song',None)
    if not lastfm_track_song_id:
        return ResponseBadRequest('Required lastfm_track_song_id was not specified.')

    try:
        lastfm_track_song = LastFMTrackSong.objects.get(id=lastfm_track_song_id)
    except LastFMTrackSong.DoesNotExist:
        raise Http404


    if request.user.is_authenticated():
        musiphile = Musiphile.objects.get(id=request.user.id)
        # if no playlist was specified, use the first one found
        playlist_users = PlaylistUser.objects.filter(user=musiphile) 
        if playlist_users:
            playlist_user = playlist_users[0]
        else:
            playlist = Playlist()
            playlist.save()
            playlist_user = PlaylistUser(playlist=playlist,user=musiphile)
            playlist_user.save()

        # ensure the song has not already been added to the playlist
        try:
            playlist_song = PlaylistSong.objects.get(lastfm_track_song=lastfm_track_song,playlist=playlist_user.playlist)
        except PlaylistSong.DoesNotExist:
            # add song to playlist
            playlist_song = PlaylistSong(lastfm_track_song=lastfm_track_song,playlist=playlist_user.playlist)
            playlist_song.save()
        return HttpResponseRedirect('/playlist/get/'+request.user.username+'/'+playlist_user.playlist.name)
    else:
        playlist = request.session.get('playlist',[])
        was_added=False
        for item in playlist:
            if item==lastfm_track_song.id:
                was_added=True
                break
        if not was_added:
            playlist.append(lastfm_track_song)

        request.session['playlist'] = playlist
        
        return HttpResponseRedirect('/playlist/get/me/Favorites')

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

