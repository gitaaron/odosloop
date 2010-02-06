from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Musiphile(User):
    '''
    Extends built-in django user to ensure email is supplied and is unique
    '''
    musiphile_email = models.EmailField('e-mail address', max_length=255, blank=False,null=False, unique=True)
    songs_played = models.ManyToManyField("jukebox.LastFMTrackSong", through="PlayHistory")

class PlayHistory(models.Model):
    musiphile = models.ForeignKey(Musiphile)
    song = models.ForeignKey("jukebox.LastFMTrackSong")
    created_at = models.DateTimeField(auto_now_add=True)

admin.site.register(Musiphile)
