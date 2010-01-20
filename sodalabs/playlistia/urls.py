from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sodalabs.playlistia.views',
        (r'^$', direct_to_template, {'template':'playlistia/index.html'}),
        (r'^user/$', 'profile'),
        (r'^open/$', 'open'),
)
