from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sodalabs.accounts.views',
        (r'^signup/$', 'signup'),
        (r'^ajax_signup/$', 'ajax_signup'),
        (r'^ajax_login/$', 'ajax_login'),
        (r'^ajax_login_container/$', direct_to_template, {'template':'top_right_tab.html'}),
        (r'^logout', 'logout'),
        (r'^song_played/(?P<lastfm_track_song_id>.+)/$','song_played'),
        (r'^me/$', 'anonymous'),
        (r'^flush/$','flush'),
        (r'^$', 'profile'),
        (r'^(?P<username>.+)/$', 'profile'),
)
