from sodalabs.jukebox.models import LastFMTrackSong
from sodalabs.lastfm.models import Track
from sodalabs.accounts.models import PlayHistory
from sodalabs.playlist.models import Playlist,PlaylistSong,PlaylistUser
def save_session_playhistory(request,user):
    # @TODO save playlists here 
    playhistory = request.session.get('playhistory',[])
    for song in playhistory:
        try:
            lastfm_track_song = LastFMTrackSong.objects.get(id=song['lastfm_track_song_id'])
        except LastFMTrackSong.DoesNotExist:
            continue

        song_played = PlayHistory(musiphile=user,song=lastfm_track_song)
        song_played.save()


    playlist = request.session.get('playlist', [])
    if playlist:
        pls = Playlist(creator=user)
        pls.save()
        pls_user = PlaylistUser(user=user, playlist=pls)
        pls_user.save()
        for song in playlist:
            try:
                pls_song = PlaylistSong.objects.get(lastfm_track=song.id, playlist=pls)
            except PlaylistSong.DoesNotExist:
                pls_song = PlaylistSong(lastfm_track=song, playlist=pls)
                pls_song.save()
