from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.jukebox.views',
        (r'^open/$', 'open'),
)
