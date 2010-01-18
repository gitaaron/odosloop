from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.playlistia.views',
        (r'^$', 'index'),
        (r'^open/$', 'open'),
)
