from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.lastfm.views',
        (r'^$', 'profile'),
        (r'^(?P<username>.+)/$', 'profile'),
)
