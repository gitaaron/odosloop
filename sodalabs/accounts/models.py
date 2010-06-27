from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class MusiphileManager(models.Manager):
    def from_request(self, request):
        if request.user.is_authenticated():
            try:
                m = request.user.musiphile
                return m
            except Musiphile.DoesNotExist:
                pass

        return None

# Create your models here.
class Musiphile(User):
    '''
    Extends built-in django user to ensure email is supplied and is unique
    '''
    musiphile_email = models.EmailField('e-mail address', max_length=255, blank=False,null=False, unique=True)
    songs_played = models.ManyToManyField("jukebox.LastFMTrackSong", through="PlayHistory")
    
    objects = MusiphileManager()

class PlayHistory(models.Model):
    musiphile = models.ForeignKey(Musiphile)
    song = models.ForeignKey("jukebox.LastFMTrackSong")
    created_at = models.DateTimeField(auto_now_add=True)

admin.site.register(Musiphile)
