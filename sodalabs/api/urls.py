from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.api.views',
    (r'^search$', 'search')
)
