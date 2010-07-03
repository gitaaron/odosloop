from django.db import models
from sodalabs.model_utils import slugify
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Playlist(models.Model):
    name = models.CharField(max_length=300, default="untitled playlist")
    slug_name = models.SlugField(_('Slug Name'), max_length=255)
    lastfm_track = models.ManyToManyField("lastfm.Track", through="PlaylistSong")
    users = models.ManyToManyField("accounts.Musiphile", through="PlaylistUser")
    creator = models.ForeignKey("accounts.Musiphile", related_name="creator")

    def save(self, **kwargs):
        name = self.name
        if name=='anonymous':
            name = name+'_';
        self.slug_name = slugify(name, instance=self, slug_field='slug_name')
        super(Playlist, self).save(**kwargs)

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist)
    lastfm_track = models.ForeignKey("lastfm.Track")
    last_updated = models.DateTimeField(auto_now=True)

class PlaylistUser(models.Model):
    playlist = models.ForeignKey(Playlist)
    user = models.ForeignKey("accounts.Musiphile")
