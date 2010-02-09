from django.conf.urls.defaults import *
from sodalabs import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Example:
    # (r'^sodalabs/', include('sodalabs.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^$', include('sodalabs.home.urls')),
    (r'^radio/', include('sodalabs.radio.urls')),
    (r'^jukebox/', include('sodalabs.jukebox.urls')),
    (r'^lastfm/', include('sodalabs.lastfm.urls')),
    (r'^playlist/', include('sodalabs.playlist.urls')),

    # user account 
    (r'^accounts/', include('sodalabs.accounts.urls')),
    (r'^logout', 'django.contrib.auth.views.logout'),

    (r'^password/reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^password/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),

)


if settings.DEBUG:
    urlpatterns += patterns('', 
            (r'site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}), 
            (r'files/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.UPLOAD_ROOT}),
    )
