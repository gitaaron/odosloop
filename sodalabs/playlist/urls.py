from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.playlist.views',
        (r'^add/$', 'add'),
        (r'^get/(?P<slug_name>[-\w]+)$', 'get'),
        (r'^menu/(?P<username>.+)$', 'menu_list'),
        (r'^menu/$', 'menu_list'),
        (r'^create/', 'create'),
        (r'^save/', 'save')
)
