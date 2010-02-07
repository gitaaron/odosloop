from sodalabs.jukebox.models import LastFMTrackSong
from sodalabs.accounts.models import PlayHistory
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

