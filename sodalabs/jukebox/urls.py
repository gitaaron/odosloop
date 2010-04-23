from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.jukebox.views',
        (r'^get_closest_video/$', 'get_closest_video'),
        (r'^get_lastfm_track/$', 'get_lastfm_track'),
)
