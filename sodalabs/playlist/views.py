# Create your views here.
from sodalabs.rest_ws.helpers import ResponseNotAllowed,ResponseBadRequest,HttpResponse
from django.http import Http404,HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from sodalabs.jukebox.models import LastFMTrackSong
from sodalabs.accounts.models import Musiphile
from sodalabs.playlist.models import PlaylistUser,Playlist,PlaylistSong
from sodalabs.playlist.helpers import ordered_unique

def get(request, username, name):
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

    tracks = ordered_unique(tracks)

    return direct_to_template(request, 'accounts/playlist.html', {'playlist_title':playlist_user.playlist.name, 'lastfm_tracks':tracks})

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
