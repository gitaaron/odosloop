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

    (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^playlist/', include('sodalabs.playlistia.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('', 
            (r'site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}), 
            (r'files/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.UPLOAD_ROOT}),
    )
