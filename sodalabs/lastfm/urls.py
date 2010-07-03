from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.lastfm.views',
        (r'^$', 'profile'),
        (r'^search$', 'search'),
        (r'^(?P<username>.+)/$', 'profile'),
        (r'^get/(?P<lastfm_id>\d+)$', 'get')
)
