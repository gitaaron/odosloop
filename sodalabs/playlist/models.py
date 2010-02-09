from django.db import models

# Create your models here.
class Playlist(models.Model):
    name = models.CharField(max_length=300, default="untitled playlist")
    lastfm_track_songs = models.ManyToManyField("jukebox.LastFMTrackSong", through="PlaylistSong")
    users = models.ManyToManyField("accounts.Musiphile", through="PlaylistUser")

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist)
    lastfm_track_song = models.ForeignKey("jukebox.LastFMTrackSong")
    last_updated = models.DateTimeField(auto_now=True)

class PlaylistUser(models.Model):
    playlist = models.ForeignKey(Playlist)
    user = models.ForeignKey("accounts.Musiphile")
