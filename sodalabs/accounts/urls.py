from django.conf.urls.defaults import *

urlpatterns = patterns('sodalabs.accounts.views',
        (r'signup/$', 'signup'),
        (r'^logout', 'logout'),
        (r'^$', 'profile'),
        (r'^(?P<username>.+)/$', 'profile'),
)
