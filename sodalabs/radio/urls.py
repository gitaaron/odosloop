from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('sodalabs.radio.views',
        (r'^$', 'get_similar'),
        (r'^ajax_get_similar$', 'ajax_get_similar'),

)
