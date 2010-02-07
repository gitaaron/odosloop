from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.accounts.views',
        (r'signup/$', 'signup'),
        (r'^logout', 'logout'),
        (r'^song_played/(?P<lastfm_track_song_id>.+)/$','song_played'),
        (r'^me/$', 'anonymous'),
        (r'^flush/$','flush'),
        (r'^$', 'profile'),
        (r'^(?P<username>.+)/$', 'profile'),
)
