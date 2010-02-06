from django.db import models

# Create your models here.
class Song(models.Model):
    lastfm_tracks = models.ManyToManyField("lastfm.Track", through='LastFMTrackSong') 
    media_id = models.CharField(max_length=255, unique=True)
    media_title = models.CharField(max_length=300)


class LastFMTrackSong(models.Model):
    song = models.ForeignKey(Song)
    lastfm_track = models.ForeignKey('lastfm.Track')
    created_at = models.DateTimeField(auto_now_add=True)
