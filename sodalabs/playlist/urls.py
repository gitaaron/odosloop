from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.playlist.views',
        (r'^add/$', 'add'),
        (r'^get/(?P<username>.+)/(?P<name>.+)/$', 'get'),
)
